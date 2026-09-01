# Mac Mini Runbook

> 最后更新：2026-08-11 | 维护人：zeph
> 
> ⚠️ **当前已知问题：** xAI 认证 token 即将过期（6h），需在 Mac mini 上执行 `openclaw models auth login --provider xai` 刷新。
> 
> ✅ **2026-08-11 日报修复：** Ollama 幻觉已根除（analyze.py 改为直接格式化数据）；daily-report.sh 增加代理 fallback。
> 
> ✅ **2026-08-11 系统升级：** Python venv 从 3.9 → 3.12；OpenClaw 默认模型 deepseek-v4-pro → deepseek-v4-flash（更省更快）；SSH Thunderbolt 自动检测 fallback。
> 
> 🆕 **2026-08-12：** `whaletrail-daily` cron 从 `agentTurn` 切为 `command` 模式——日报不再依赖 DeepSeek LLM，直接跑 `daily-report.sh` 后推送 stdout 到 Telegram。消除 LLM API 瞬时不可用导致的日报漏发。


---

## 概览

| 项目 | 值 |
|------|-----|
| **主机名** | Zephyrs-Mac-mini.local |
| **型号** | Apple M4 |
| **内存** | 16 GB |
| **存储** | 228 GB（已用 11 GB，可用 118 GB） |
| **系统** | macOS 26.1 (25B78) |
| **用户名** | zeph |
| **Home 目录** | `/Users/zeph` |
| **物理位置** | bzl-iot 网段，与 MacBook 同一 AP（隔离） |
| **Thunderbolt IP** | `169.254.230.133`（bridge0，直连 MacBook，<1ms） |
| **VPS 跳板** | `139.224.244.214`（阿里云上海轻量 Agentic/OpenClaw 机；反向隧道端口 2222） |
| **VPS runbook** | 见 `../aliyun-openclaw/README.md`（OpenClaw Gateway + 跳板双角色） |

---

## 如何连接

### 自动检测（推荐）

```bash
ssh macmini        # 自动：Thunderbolt 通 → 直连（<1ms）；不通 → VPS 隧道（~20ms）
```

原理：SSH config 中 `Match exec` 检测 `169.254.230.133` 是否可达，不可达时自动 fallback 到 VPS 跳板。

### Thunderbolt 直连（工位，<1ms）

```bash
ssh macmini-fwd    # 终端 + 仪表盘端口转发（仅 Thunderbolt）
```

| 端点 | bridge0 IP |
|------|-----------|
| MacBook | `169.254.66.46` |
| Mac mini | `169.254.230.133` |

延迟 <1ms，带宽 ~10-20Gbps，物理直连不经过交换机。

### VPS 反向隧道（远程，~20ms）

```bash
ssh macmini-remote  # 强制走 VPS（即使 Thunderbolt 通也走远程）
```

原理：Mac mini 通过 launchd 开机自启维持一条到 VPS 的 SSH 反向隧道（`-R 2222:localhost:22`）。
MacBook 以 VPS 为跳板（`ProxyJump`）通过隧道连入 Mac mini。

**链路：** MacBook → VPS `139.224.244.214:22` → 反向隧道 `localhost:2222` → Mac mini

与 `falaboss_da` 的 `ProxyJump` 架构完全相同，全程仅使用 SSH 端口 22，不依赖任何 VPN/隧道协议。

### 端口转发（访问仪表盘）

```bash
# Thunderbolt（工位）
ssh macmini-fwd

# VPS（远程）— 需先启动隧道再加端口转发
ssh -L 8766:localhost:8766 -L 18789:localhost:18789 -L 11434:localhost:11434 macmini-remote
```

| Mac mini 服务 | MacBook 访问地址 |
|--------------|-----------------|
| WhaleTrail 看板 `:8766` | `http://localhost:8766/` |
| OpenClaw Gateway `:18789` | `http://localhost:18789/health` |
| Ollama API `:11434` | `http://localhost:11434/api/tags` |

---

## 运行中的服务

### launchd 守护进程（开机自启）

| Label | 用途 | 端口 | 状态 |
|-------|------|------|------|
| `ai.openclaw.gateway` | OpenClaw AI Agent 网关 | 18789 (loopback) | ✅ running |
| ~~`ai.gold-dashboard`~~ | ~~黄金策略看板~~ | ~~8765~~ | ❌ 已停用（迁移至 WhaleTrail） |
| ~~`ai.gold-paper`~~ | ~~LEAN paper trading~~ | — | ❌ 已停用（迁移至 WhaleTrail） |
| `homebrew.mxcl.ollama` | 本地 LLM 推理 | 11434 | ✅ running |
| `com.zeph.reverse-tunnel` | SSH 反向隧道 → VPS | 2222 (VPS side) | ✅ running |

### 常驻应用（GUI）

| 应用 | 用途 | 端口 |
|------|------|------|
| Mihomo (Clash) | 代理/VPN | 14122, 38324 (loopback) |
| Docker Desktop | 容器运行时（LEAN 回测用） | — |

### 管理命令

```bash
# OpenClaw Gateway
launchctl list | grep openclaw
tail -f ~/.openclaw/logs/gateway.err.log

# WhaleTrail live
launchctl list | grep whaletrail
launchctl print gui/$(id -u)/ai.whaletrail-live

tail -f ~/Projects/whaletrail-lab/projects/whaletrail/logs/paper-live.log
tail -f ~/Projects/whaletrail-lab/projects/whaletrail/logs/paper-live.err

# Ollama
brew services list | grep ollama
ollama list          # 已安装模型
ollama ps            # 当前运行

# Reverse Tunnel
launchctl list | grep reverse-tunnel
tail -f /tmp/reverse-tunnel.log
```

> `gold-paper` / `gold-dashboard` / LEAN paper trading 已从 `whaletrail-lab` 仓库删除，不再维护；不要再新增旧路径任务。

---

## 项目目录地图

```
/Users/zeph/
├── Projects/whaletrail-lab/          ← 主仓库（Git: zzz562/whaletrail-lab）
│   ├── projects/
│   │   └── whaletrail/             ← 统一回测 / paper trading 平台（唯一 active 项目）
│   │       ├── whaletrail/         # 核心引擎
│   │       ├── scripts/            # 回测、日报、看板、情绪扫描脚本
│   │       ├── config/             # watchlist 等配置
│   │       ├── docs/               # 子系统设计/运维说明
│   │       ├── data_cache/         # Parquet 本地缓存（不入 git）
│   │       ├── results/            # 回测/情绪输出（不入 git）
│   │       └── .venv/              # Python 虚拟环境（不入 git）
│   ├── configs/
│   ├── notes/
│   └── archive/
│
├── .openclaw/                      ← OpenClaw 运行时
│   ├── openclaw.json               # 主配置
│   ├── agents/                     # Agent 会话记录
│   ├── logs/                       # 运行日志
│   └── workspace/                  # Agent 工作区
│
├── archive/                        ← 归档
│   ├── Lean/                       # 旧 LEAN 引擎源码
│   └── OpenClaw-PaperTrading/      # 旧 LEAN workspace
│
├── .grok/                          ← Grok Build 配置
└── .ssh/                           # SSH 密钥
```

---

## 代码同步规则（重要）

| 角色 | 路径 | 规则 |
|------|------|------|
| Mac mini 主开发 | `~/Projects/whaletrail-lab` | **唯一主源**。开发、测试、提交、推送都在这里完成。 |
| GitHub | `zzz562/whaletrail-lab` | 作为两台机器之间的同步中枢。 |
| MacBook 查看副本 | `~/github_code/whaletrail-lab` | 默认只用于查看/轻量验证；不要在这里长期开发。 |

### 标准同步流

```bash
# Mac mini：完成开发后
cd ~/Projects/whaletrail-lab
git status
git add -A
git commit -m "..."
git push origin main

# MacBook：刷新查看副本（先确认没有要保留的本地笔记）
cd ~/github_code/whaletrail-lab
git fetch origin --prune
git reset --hard origin/main
git clean -fd
```

### 约束

- 不提交 `.venv/`、`data_cache/`、`results/`、`logs/`、`*.log`、`*.err`。
- MacBook 如果临时改过，重置前先 `git branch backup/...` 或 `git stash push -u`。
- `projects/gold-paper/` 已删除；不要恢复旧 LEAN/gold-paper 任务。历史资料如需查阅，看 `~/archive/`。

---

## WhaleTrail — 黄金为主 Paper Trading

> **主：黄金 GLD。辅：美股指数 SPY/QQQ 对冲。不做 A股/港股/高频。**  
> 替代旧 LEAN / gold-paper。仓库：`whaletrail-lab/projects/whaletrail/`。

| 项目 | 值 |
|------|-----|
| 路径 | `~/Projects/whaletrail-lab/projects/whaletrail/` |
| 定界文档 | `SCOPE.md` |
| 数据源 | **仅 yfinance** + Parquet 缓存 |
| 看板 | `http://127.0.0.1:8766/` |

### 常用操作

```bash
cd ~/Projects/whaletrail-lab/projects/whaletrail

# daily-report.sh 自带代理检测（7890 不可用时自动直连），无需手动 export

# 黄金主回测
.venv/bin/python scripts/run-backtest.py gold_sma GLD 2018-01-01 2024-12-31 100000

# 美股对冲对照
.venv/bin/python scripts/run-backtest.py ma_cross SPY 2020-01-01 2024-12-31 100000

# 日报（analyze.py 已改为直接格式化，不再使用 Ollama/qwen3:4b）
./scripts/daily-report.sh gold_sma GLD

# 看板
.venv/bin/streamlit run scripts/dashboard.py --server.port 8766
```

### 策略

| 策略 | 说明 |
|------|------|
| gold_sma | **主** 黄金 SMA 20/50 |
| ma_cross / bollinger / turtle / momentum | 对照与实验 |

### 环境

- **Python**：3.12.12（Homebrew），venv 位于 `.venv/`
- **依赖管理**：`requirements.txt`（mplfinance 已移除，未使用）
- **旧 venv 警告**：已从 3.9 升级，urllib3/LibreSSL 警告已消除

### 明确不做

- A股、港股、akshare、Tushare
- 分钟/tick 高频
- LEAN / Docker（已归档 `~/archive/`）

### OpenClaw / Telegram

| 指令 | 效果 |
|------|------|
| 跑黄金回测 | `run-backtest.py gold_sma GLD` |
| 黄金日报 | `daily-report.sh` |
| 跑 SPY 对照 | `run-backtest.py ma_cross SPY` |

---

## AI Agent：OpenClaw / Ironblade

### 模型

| 来源 | 模型 | 角色 |
|------|------|------|
| DeepSeek | deepseek-v4-flash | **主力**（2026-08-11 从 pro 切换，更省更快） |
| xAI | Grok 4.3, Grok 4.20 Beta | 备选推理 |
| Ollama (本地) | qwen3:4b | fallback（仅聊天兜底，不参与数据/分析） |

### 通道

| 通道 | 状态 | 说明 |
|------|------|------|
| Telegram | ✅ 启用 | `@iron_blade_bot`，白名单用户 5102138680 |
| Gateway API | ✅ 启用 | `http://127.0.0.1:18789/`，token 鉴权 |

### 管理

```bash
# 查看 Gateway 状态
openclaw gateway status

# 打开管理 Dashboard
openclaw dashboard

# 获取 Gateway Token
openclaw config get gateway.auth.token

# 重启 Gateway
launchctl bootout gui/$(id -u)/ai.openclaw.gateway
launchctl bootstrap gui/$(id -u)/~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

### Cron 定时任务

| 任务 | 调度 | 类型 | 说明 |
|------|------|------|------|
| `whaletrail-daily` | `30 8 * * 1-5` (Asia/Shanghai) | `command` | 工作日 08:30 直接跑 `daily-report.sh gold_sma GLD` → Telegram |
| `whaletrail-sentiment` | `0 9 * * *` (Asia/Shanghai) | `command` | 每日 09:00 X KOL 情绪扫描 → Telegram |

```bash
# 查看
openclaw cron list
openclaw cron show whaletrail-daily

# 手动触发（调试）
openclaw cron run whaletrail-daily

# 编辑
openclaw cron edit <id> --message "..." --announce --to 5102138680 --channel telegram
```

⚠️ 日报 cron 已切换为 `command` 类型（`--command "cd ... && ./daily-report.sh"`），不再依赖 LLM。`agentTurn` 仅用于需要 LLM 理解指令的交互式任务。

---

## 网络 & 代理

### Thunderbolt 直连（MacBook ↔ Mac mini）

- 线缆：Thunderbolt 数据线（MacBook ↔ Mac mini 对插）
- 接口：两端均为 `bridge0`（Thunderbolt Bridge）
- IP：MacBook `169.254.66.46`，Mac mini `169.254.230.133`
- 延迟：<1ms，带宽 ~10-20Gbps
- 拓扑：直连，不经过任何交换机/路由器

### VPS 反向隧道（阿里云上海轻量 · 兼 OpenClaw 机）

- IP：`139.224.244.214`，用户 `admin`，SSH：`ssh aliyun-vps`
- 反向隧道端口：VPS `localhost:2222` → Mac mini `localhost:22`
- 守护：`com.zeph.reverse-tunnel`（launchd，KeepAlive 自动重连）
- 架构：`MacBook → VPS:22 → localhost:2222 → Mac mini:22`
- 仅使用 SSH 端口 22，无额外协议
- **同一台 VPS 还跑 OpenClaw Gateway**（`:13749`）与 SearXNG 等，完整说明见  
  **`../aliyun-openclaw/README.md`**

### 代理

- **Mihomo (Clash)** GUI 应用运行中，端口 14122 / 38324
- 系统 HTTP 代理指向 `127.0.0.1:7890`

---

## 环境变量

| 变量 | 用途 | 配置位置 |
|------|------|----------|
| `DEEPSEEK_API_KEY` | DeepSeek API | `~/.openclaw/.env` |
| `PATH` | Homebrew + pipx + .grok | `~/.zshrc` |

---

## 故障排查

### SSH 连不上

`ssh macmini` 已启用自动检测：Thunderbolt 优先，不通时自动走 VPS 隧道。

如需强制指定路径：

```bash
# 强制直连（工位）
ssh -o HostName=169.254.230.133 macmini

# 强制远程（VPS 跳板）
ssh macmini-remote
```

**Thunderbolt 不通时：**

```bash
# 两端检查 IP
ifconfig bridge0 | grep "inet "
# MacBook 应该是 169.254.66.46，Mac mini 应该是 169.254.230.133

# 重新插拔 Thunderbolt 线缆，等待 3-5 秒让 macOS 重建 bridge
```

**远程隧道不通时：**

```bash
# 1. 在 Mac mini 上检查 launchd 守护
ssh macmini 'launchctl list | grep reverse-tunnel'
# 期望 PID > 0

# 2. 看日志
ssh macmini 'tail -20 /tmp/reverse-tunnel.err.log'

# 3. 重启反向隧道
ssh macmini 'launchctl kickstart -k gui/$(id -u)/com.zeph.reverse-tunnel'

# 4. 确认 VPS 侧 2222 在监听
ssh aliyun-vps 'ss -tlnp | grep 2222'

# 5. 手动重连（应急）
ssh macmini 'ssh -o ServerAliveInterval=60 -o ExitOnForwardFailure=yes -R 2222:localhost:22 -N admin@139.224.244.214'
```

### WhaleTrail Live 异常

```bash
# 检查进程
launchctl list | grep whaletrail-live
launchctl print gui/$(id -u)/ai.whaletrail-live

# 重启
launchctl bootout gui/$(id -u)/ai.whaletrail-live
launchctl bootstrap gui/$(id -u)/~/Library/LaunchAgents/ai.whaletrail-live.plist

# 看日志
tail -50 ~/Projects/whaletrail-lab/projects/whaletrail/logs/paper-live.log
tail -50 ~/Projects/whaletrail-lab/projects/whaletrail/logs/paper-live.err
```

### Ollama 无响应

```bash
brew services restart ollama
curl http://127.0.0.1:11434/api/tags
```

### WhaleTrail 依赖/路径异常

```bash
# 验证 venv 路径
cd ~/Projects/whaletrail-lab/projects/whaletrail
.venv/bin/python -c "import sys; print(sys.executable)"
# 如果指向旧路径，重建 venv：
rm -rf .venv
/opt/homebrew/bin/python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 编译检查
.venv/bin/python -m compileall whaletrail scripts
```

### OpenClaw Gateway 起不来（PID=-1，HTTP 000）

这是最常见的问题。典型症状：`launchctl list | grep openclaw` 显示 `-1`，端口不监听。

**根因通常是：**
1. Node.js 版本不满足要求（需要 ≥22.22.3 或 ≥24.15.0）
2. 配置文件有语法/校验错误

**修复流程：**

```bash
# 1. 确保使用 nvm 的 Node 24
export NVM_DIR="$HOME/.nvm" && . "$NVM_DIR/nvm.sh" && nvm use 24
export PATH="$(dirname $(which node)):/opt/homebrew/bin:$PATH"

# 2. 修复配置 + 重启 Gateway（一步到位）
openclaw doctor --fix

# 3. 重装 launchd plist（写入正确的 Node 路径）
openclaw gateway install --force

# 4. 验证
launchctl list | grep openclaw    # PID 应该 >0
curl -s http://127.0.0.1:18789/health   # 返回 {"ok":true}
```

**注意：** SSH 远程执行时必须在一个 shell 里完成 nvm 加载 + 命令执行，否则 `nvm use` 不生效。正确写法：

```bash
ssh macmini 'export NVM_DIR="$HOME/.nvm" && . "$NVM_DIR/nvm.sh" && nvm use 24 > /dev/null 2>&1 && export PATH="$(dirname $(which node)):/opt/homebrew/bin:$PATH" && openclaw doctor --fix'
```

### Node.js 版本管理

Mac mini 上同时存在两个 Node：
| 来源 | 路径 | 版本 |
|------|------|------|
| Homebrew (system) | `/opt/homebrew/opt/node@22/bin/node` | v22.22.0 |
| nvm (user) | `~/.nvm/versions/node/v24.19.0/bin/node` | v24.19.0 |

brew 升级有 bug（`bottles.rb` error），暂时改用 nvm 管理 Node。

```bash
# 加载 nvm
export NVM_DIR="$HOME/.nvm" && . "$NVM_DIR/nvm.sh"
nvm use 24

# 安装其他版本
nvm install 22.22.3
nvm alias default 24
```

### xAI 认证过期

```bash
export NVM_DIR="$HOME/.nvm" && . "$NVM_DIR/nvm.sh" && nvm use 24 > /dev/null 2>&1
export PATH="$(dirname $(which node)):/opt/homebrew/bin:$PATH"
openclaw models auth login --provider xai
```

---

## 备份清单

- [ ] `~/.openclaw/openclaw.json` — OpenClaw 主配置
- [ ] `~/.ssh/` — SSH 密钥
- [ ] `~/Projects/whaletrail-lab/` — 主项目仓库（Git 已推远程）
- [ ] `~/Projects/whaletrail-lab/projects/whaletrail/data_cache/` — 回测数据缓存（本地唯一）

---

## 参考链接

- OpenClaw: https://github.com/openclaw/openclaw
- 阿里云 OpenClaw VPS runbook: `../aliyun-openclaw/README.md`
- 主项目仓库: https://github.com/zzz562/whaletrail-lab
- WhaleTrail 代码: `~/Projects/whaletrail-lab/projects/whaletrail/`
