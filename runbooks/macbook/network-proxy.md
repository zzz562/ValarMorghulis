# MacBook 网络 / 代理排障手册

> 最后更新：2026-09-09 ・ 范围：Clash Party / BoostNet / Google Meet
> 本文件只记 MacBook 的代理与网络排障经验，不与其它运维信息混放。

## 结论速览

- Google Meet「网页能开、进不去会议」= **TUN 没开**（WebRTC/UDP 不走系统 HTTP 代理）+ **Google 系域名 DNS 被墙**（订阅把 Google 域名强制走 Cloudflare DoH）。
- 两个代理客户端（Clash Party 与机场专用 BoostNet.app）**只留一个当流量引擎**：系统代理 + TUN 只能有一个主人。
- 最终方案：Clash Party 当唯一引擎（开 TUN），并用 **Override（覆写）** 把 Google 系 DNS 改到腾讯 DoH，持久化、防订阅更新覆盖。

## 环境

| 项 | 值 |
|----|----|
| 设备 | MacBook（macOS，用户 admin） |
| 客户端 | Clash Party（mihomo-party） |
| 机场 | BoostNet（订阅客户端 BoostNet.app 已停用） |
| 端口 | mixed 7890 / socks 7891 / http 7892（三端口都由 mihomo 监听） |
| 系统代理 | 127.0.0.1:7890 |
| TUN | utun1500，auto-route |

## 现象

上网、普通网页正常；但 Google Meet 进不去（卡「正在连接 / 无法加入会议」），Google 页面明显慢。

## 排查证据链

1. **分段计时定位**：`curl -w` 显示慢在「TLS 握手约 5s」，而本地 DNS 0.001s、TCP 到代理 0.002s。
2. **同节点对照**：`www.cloudflare.com` 走同一代理 0.67s，`www.google.com` 3-5s → 说明不是节点/隧道问题。
3. **内核 DNS 查询定位根因**：`GET /dns/query?name=www.google.com` 报 `context deadline exceeded`（在请求 `https://dns.cloudflare.com/dns-query`）；而 `www.cloudflare.com`、`www.baidu.com` 0.006s 秒回。

## 根因

订阅配置里 `dns.nameserver-policy` 把 Google / YouTube / GitHub / OpenAI 等域名强制指定为 Cloudflare DoH：

mihomo 是**直连**该 DoH 的（不走代理），而 Cloudflare DoH 从本机被墙 → 每次解析 Google 域名卡 3-5s 超时，之后才兜底成功。所以「网络没问题、但 Google 系慢、Meet 进不去」。

## 修复

1. 把 `nameserver-policy` 里所有 `https://dns.cloudflare.com/dns-query` 换成腾讯 DoH `https://doh.pub/dns-query`（实测：秒回，且返回真实 Google IP，非污染）。
2. 用 Clash Party 的 **Override（覆写）** 持久化，避免「启动时自动更新订阅」把改动冲掉。

Override 片段（放进已有覆写文件即可；键首带 `+` 必须用 `<>` 包裹）：

```yaml
dns:
  nameserver-policy:
    <+.google.com>: https://doh.pub/dns-query
    <+.googleapis.com>: https://doh.pub/dns-query
    <+.gstatic.com>: https://doh.pub/dns-query
    # 其余 google / youtube / github / openai 等域名同样处理
```

3. Clash Party 里开 **TUN（虚拟网卡）**，并点「重载配置 / 重启内核」。

## 修复前后对比

| 指标 | 修复前 | 修复后 |
|------|--------|--------|
| 内核 DNS 解析 google.com | 3.5s 超时 | 0.004s |
| google 204 | 4.7-5.5s | 0.26-0.40s |
| meet.google.com | 5.5s | 0.40s |

## 规则 / 教训

- **代理引擎只留一个**：Clash Party 与 BoostNet 同时开，会出现「慢的那个占着系统代理 + TUN、快的那个空转」。别两个都开 TUN。
- **Meet / 音视频必须 TUN**：网页/信令走 HTTPS 代理能通，但 WebRTC 音视频是 UDP，不走系统 HTTP 代理；只有 TUN 能接管。
- **TUN 与办公内网直连 agent 冲突**：TUN 抢默认路由 + DNS 劫持（`any:53`），会把内网域名解析劫持到公共 DNS、破坏直连 app 的路由。因此 **TUN 按需开**：平时关（系统代理够用），开 Google Meet 时临时开，开完关。
- **Clash Party 会「启动时自动更新订阅」**：直接改订阅 profile 文件会被下次启动冲掉；持久化要写 **Override**。
- **Grok Build 的公司内网模型不走代理**：`~/.grok/config.toml` 里 Muses 模型 `base_url` 是内网（10.x / weizhipin.com），代理规则必须把这些域名走 DIRECT，否则模型调用失败；不必在 toml 里给模型单独配代理。
- 旧 ClashX 残留（`~/.config/clash` 的 `clash-core-service`、`~/Library/Application Support/clash_win_boomcloud`）建议清理，避免混淆。

## 已知副作用：TUN 会让 git SSH 走节点

开 TUN 后，`git@github.com` 的 SSH（22 端口）被 TUN 接管、经代理节点转发；本机场节点不放行 22 端口，导致 `git pull/push` 报 `Connection closed by 198.18.x.x port 22`。

- **临时绕过（不改配置）**：`GIT_SSH_COMMAND='ssh -o Hostname=ssh.github.com -p 443' git push`
- **永久方案二选一**：
  1. `~/.ssh/config` 给 github.com 指定 `Hostname ssh.github.com` + `Port 443`；
  2. 或 Clash 覆写里加 `DST-PORT,22,DIRECT`（所有 SSH 直连，符合本仓库「SSH 不走隧道」原则）。

## 复现验证命令

```bash
# 代理端口与系统代理
lsof -nP -i :7890 | head
scutil --proxy

# 延迟分段计时（定位慢在 DNS/TCP/TLS/首字节哪一段）
curl -sS -x http://127.0.0.1:7890 -o /dev/null \
  -w 'DNS:%{time_namelookup} TCP:%{time_connect} TLS:%{time_appconnect} 首字节:%{time_starttransfer} 总:%{time_total}\n' \
  https://www.google.com/generate_204

# 内核 DNS 查询（unix socket 路径见 mihomo 进程参数 -ext-ctl-unix）
curl --unix-socket /tmp/mihomo-party-<pid>.sock \
  'http://localhost/dns/query?name=www.google.com&type=A'

# Google 连通性
curl -sS -x http://127.0.0.1:7890 -o /dev/null -w '%{http_code} %{time_total}s\n' \
  https://www.google.com/generate_204
```

## 关键文件

| 文件 | 作用 |
|------|------|
| `~/Library/Application Support/mihomo-party/work/config.yaml` | 运行时配置（每次启动由 profile + override 重新生成） |
| `~/Library/Application Support/mihomo-party/profiles/<id>.yaml` | 订阅原始配置 |
| `~/Library/Application Support/mihomo-party/override/<id>.yaml` | 覆写（持久，优先级高于订阅） |
