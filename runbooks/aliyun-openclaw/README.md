# 阿里云 OpenClaw 服务器 Runbook

> 最后更新：2026-08-10 | 维护人：zeph  
> 镜像：Alibaba Cloud Linux 4 **Agentic Edition**（云端 OpenClaw /「云龙虾」）  
> 角色：**OpenClaw 网关主机** + **Mac mini SSH 反向隧道跳板**

---

## 概览

| 项目 | 值 |
|------|-----|
| **公网 IP** | `139.224.244.214` |
| **内网 IP** | `172.24.46.82` |
| **地域** | `cn-shanghai`（上海） |
| **主机名** | `iZuf6al73khytvbzycbq6vZ` |
| **系统** | Alibaba Cloud Linux 4.0.3 (Agentic Edition) |
| **规格** | 2 vCPU · 1.8 GiB RAM · 40 GB 系统盘 · 6 GB Swap |
| **工作区盘** | `/mnt/btrfs-workspace` 16 GB btrfs（loop） |
| **登录用户** | `admin`（uid 1000，在 docker 组）· 可用 `root` |
| **SSH（MacBook）** | `ssh aliyun-vps` |
| **主要用途** | 1) OpenClaw Gateway 公网可达  2) Mac mini 反向隧道跳板（`:2222`） |

### 与 Mac mini 的关系

```
MacBook ──ssh aliyun-vps──> 本机 (VPS)
                              ├─ OpenClaw Gateway :13749
                              ├─ SearXNG :8080 (仅本机)
                              └─ reverse tunnel :2222 ──> Mac mini:22

MacBook ──ssh macmini-remote──> VPS:22 ──ProxyJump──> localhost:2222 ──> Mac mini
```

Mac mini 侧 runbook：`../macmini/README.md`。

---

## 如何连接

```bash
# 从 MacBook（~/.ssh/config 已配 Host aliyun-vps）
ssh aliyun-vps

# 等价
ssh admin@139.224.244.214
```

| Host alias | 说明 |
|------------|------|
| `aliyun-vps` | 本机 |
| `macmini-remote` | 经本机跳板连 Mac mini（需 reverse tunnel 存活） |

---

## OpenClaw

| 项目 | 值 |
|------|-----|
| **版本** | OpenClaw `2026.6.10` |
| **Node** | v22.22.0 |
| **安装路径** | `/usr/local/lib/node_modules/openclaw` · CLI `/usr/local/bin/openclaw` |
| **配置** | `~/.openclaw/openclaw.json` |
| **Workspace** | `~/.openclaw/workspace` → `/mnt/btrfs-workspace/ws-398ab6` |
| **Gateway 端口** | `13749`（`bind=lan`，公网可达） |
| **Dashboard basePath** | `/0ba25f50/` |
| **公网 Dashboard** | `http://139.224.244.214:13749/0ba25f50/` |
| **Health** | `http://127.0.0.1:13749/health` → `{"ok":true,"status":"live"}` |
| **认证** | gateway auth token（见配置，勿写入仓库） |
| **默认模型** | `qwenprovider/qwen3.7-plus`（~195k ctx） |
| **Channels** | 当前 **未配置** 聊天通道（钉钉/飞书/微信等插件在 allowlist，待接入） |
| **Heartbeat** | 30m（main） |

### 服务管理

```bash
# 状态
openclaw gateway status
openclaw status
systemctl --user status openclaw-gateway

# 重启
systemctl --user restart openclaw-gateway
# 或
openclaw gateway restart

# 日志
openclaw logs --follow
# 文件日志
tail -f /tmp/openclaw/openclaw-*.log

# 配置
openclaw config get gateway
openclaw doctor
```

systemd user unit：`~/.config/systemd/user/openclaw-gateway.service`  
依赖：`app-init.service` 完成后才启动（`ExecStartPre` 等 `/tmp/app-init.done`）。

### 插件（enabled / allow）

| 插件 | 用途 | 备注 |
|------|------|------|
| `ws-ckpt` | workspace btrfs 快照 | 与 `ws-ckpt` daemon 配套 |
| `tokenless` | token 相关 | 已装 |
| `dingtalk-connector` | 钉钉 | 通道尚未 list 出 |
| `openclaw-lark` | 飞书 | 同上 |
| `openclaw-weixin` | 微信 | 同上 |
| `wecom-openclaw-plugin` | 企业微信 | 同上 |
| `qqbot` | QQ | 同上 |
| `memory-core` | 记忆 | status 显示 enabled |

扩展目录：`~/.openclaw/extensions/`

### Workspace 内容

```
/mnt/btrfs-workspace/ws-398ab6/
├── AGENTS.md / SOUL.md / USER.md / IDENTITY.md / MEMORY.md / TOOLS.md / HEARTBEAT.md
├── avatars/
└── skills/
    ├── searxng/          # 自建搜索，绑 Docker searxng
    ├── agent-browser-fradser-dotclaude
    ├── find-skills
    ├── proactive-agent
    ├── self-improving-agent
    └── skill-vetter
```

`USER.md` / `IDENTITY.md` 仍是模板，首次正式用时建议补全。

### 安全注意（重要）

- Gateway **`bind=lan`**，对公网 `0.0.0.0:13749` 监听；Dashboard 有 basePath 混淆 + token，但仍暴露在互联网。
- 生产建议：仅本机绑定 + SSH 隧道访问，或加安全组只放行自己的 IP。
- 勿把 `gateway.auth.token` 写进 git / 聊天记录。
- root 密码若曾在会话中暴露，应轮换并优先只用密钥登录。

---

## 其它常驻服务

### launch / systemd 一览

| 单元 | 用途 | 端口 / 备注 |
|------|------|-------------|
| `openclaw-gateway.service` (user) | OpenClaw Gateway | `0.0.0.0:13749` |
| `agentsight.service` | eBPF AI Agent 可观测 | CPU 30% 上限 · MemoryMax 350M |
| `ws-ckpt.service` | btrfs workspace 快照 daemon | 配合 OpenClaw ws-ckpt 插件 |
| `docker.service` + 容器 `searxng` | 元搜索 | `127.0.0.1:8080`（host 网络） |
| `sshd` | SSH | `:22` |
| （Mac mini 发起） | reverse tunnel | VPS `127.0.0.1:2222` → mini:22 |
| 阿里云监控 / 安骑士 | cloudmonitor · aegis · loongcollector | 默认装 |

### SearXNG

```bash
docker ps | grep searxng
curl -sS http://127.0.0.1:8080/ | head
# 配置（workspace 内）
ls ~/.openclaw/workspace/skills/searxng/config/
```

- 镜像：`searxng/searxng:latest`
- 网络：`host`，仅本机 8080，**不建议** 直接暴露公网

### AgentSight

```bash
systemctl status agentsight
agentsight discover
agentsight metrics
```

eBPF 追踪 AI 进程 / SSL / LLM API，镜像预装组件。

### ws-ckpt（workspace 快照）

```bash
systemctl status ws-ckpt
ws-ckpt status
ws-ckpt list
# 手动打点（示例）
ws-ckpt checkpoint
```

Workspace 落在 btrfs 子卷，支持 checkpoint / rollback / diff。

---

## Mac mini 反向隧道（本机作为跳板）

| 项目 | 值 |
|------|-----|
| 监听 | `127.0.0.1:2222`（仅本机，安全） |
| 目标 | Mac mini `localhost:22` |
| 发起方 | Mac mini `com.zeph.reverse-tunnel` (launchd) |
| 用户 | VPS 侧登录用户 `admin` |

```bash
# 在 VPS 上确认隧道
ss -tlnp | grep 2222

# 从 MacBook 经跳板进 mini
ssh macmini-remote
```

隧道由 **Mac mini 主动出站** 建立；本机重启后需等 mini 侧 KeepAlive 重连（通常几十秒内）。

---

## 目录地图

```
/home/admin/
├── .openclaw/
│   ├── openclaw.json           # 主配置
│   ├── workspace -> /mnt/btrfs-workspace/ws-398ab6
│   ├── agents/main/
│   ├── extensions/             # 插件
│   ├── state/openclaw.sqlite
│   └── logs/
├── .config/systemd/user/
│   └── openclaw-gateway.service
└── .ssh/authorized_keys

/mnt/btrfs-workspace/
├── ws-398ab6/                  # 活动 workspace
└── snapshots/                  # ws-ckpt 快照

/usr/local/bin/
├── openclaw
├── agentsight / agentsight-start
├── ws-ckpt
└── linux-sandbox
```

---

## 常用运维

```bash
# 资源
free -h; df -h / /mnt/btrfs-workspace; uptime

# 重启 OpenClaw
systemctl --user restart openclaw-gateway

# 重启 SearXNG
docker restart searxng

# 看谁在吃内存（1.8G 很紧，OpenClaw ~350MB）
ps aux --sort=-%mem | head -15

# 安全组 / 端口（控制台核对）
# 建议开放：22（SSH，限源 IP 更佳）
# 13749：仅自己或关掉公网，改 SSH 本地转发访问 Dashboard
```

### 本地安全访问 Dashboard（推荐）

```bash
# MacBook
ssh -L 13749:127.0.0.1:13749 aliyun-vps
# 浏览器
open http://127.0.0.1:13749/0ba25f50/
```

若改成仅 loopback 监听，需在 `openclaw.json` 把 `gateway.bind` 从 `lan` 改为 `loopback`（或等价项）后重启 gateway。

---

## 故障排查

### Gateway 起不来

```bash
systemctl --user status openclaw-gateway
journalctl --user -u openclaw-gateway -n 50 --no-pager
ls -la /tmp/app-init.done    # 启动前置条件
openclaw doctor
node -v   # 期望 22.x
```

### Dashboard 打不开

```bash
curl -sS http://127.0.0.1:13749/health
ss -tlnp | grep 13749
# 公网被墙/安全组：用 SSH -L 转发访问
```

### 模型调用失败

```bash
openclaw models list
# 检查 qwenprovider 凭证是否过期 / 余额
# 配置里 providers 可能在 env 或密钥服务，勿打印到日志
```

### Mac mini 远程连不上

```bash
ss -tlnp | grep 2222          # 无监听 = mini 隧道断了
# 到 mini 上：
# launchctl list | grep reverse-tunnel
# launchctl kickstart -k gui/$(id -u)/com.zeph.reverse-tunnel
```

### 内存吃紧 / OOM

机器只有 1.8G。OpenClaw + Docker + 安骑士已经偏满。  
避免再跑重型服务；必要时升配到 2C4G，或关掉暂时不用的容器。

---

## 备份清单

- [ ] `~/.openclaw/openclaw.json`
- [ ] `~/.openclaw/state/`（sqlite）
- [ ] `/mnt/btrfs-workspace/ws-398ab6/`（workspace + skills）
- [ ] `~/.ssh/authorized_keys`
- [ ] 通道密钥 / 模型 API（若后续配置）

---

## 待办 / 后续可做

- [ ] 补全 `USER.md` / `IDENTITY.md`
- [ ] 接入需要的通道（钉钉/飞书/微信…）
- [ ] Gateway 收紧为 loopback + SSH 转发（或安全组锁 IP）
- [ ] 轮换 root 密码，禁用密码登录
- [ ] 与 Mac mini OpenClaw 分工：本机公网入口 / mini 本地推理与回测

---

## 参考

- OpenClaw 文档：https://docs.openclaw.ai/
- 故障排查：https://docs.openclaw.ai/troubleshooting
- Mac mini runbook：`../macmini/README.md`
- 阿里云控制台轻量应用服务器：实例 `139.224.244.214` · 地域上海
