# Grok Bot 与 OpenClaw 清单

> **6 个 Grok Bot 人设见 [`ROLES.md`](ROLES.md)**。本文件分清：Grok Bot 主机上的助手 vs Mini/VPS 上的 OpenClaw 服务。密钥一律不进仓。

## Grok Bot 助手（共用主机）

宿主：Grok Bot Linux（经阿里云 `2223` SSH）。通道：各自 1:1 + 群 `project-ops`。

Axiom · RD · Big-A · Gold Mast · Data Mast · Challenger。细则在 `ROLES.md`。

应用里还有占位 `New Bot`（空壳，不进名册）。

## Mini / VPS 服务（不是上面 6 个人）

| 服务 | 宿主 | 通道 / 端口 | 用途 | 手册 |
|------|------|-------------|------|------|
| OpenClaw Gateway | Mac mini | loopback `:18789` | 本地推理 / Telegram 后端 | [`runbooks/macmini/`](../runbooks/macmini/README.md) |
| Telegram `@iron_blade_bot` | Mac mini（经 Gateway） | Telegram，白名单用户见机器 env | WhaleTrail 日报 / 情绪 | 同上 |
| OpenClaw Gateway | 阿里云 VPS | `:13749`（token） | 公网入口 | [`runbooks/aliyun-openclaw/`](../runbooks/aliyun-openclaw/README.md) |

## 关键操作速查

```bash
# Mac mini — Gateway
launchctl list | grep openclaw
curl -s http://127.0.0.1:18789/health

# VPS — Gateway
systemctl --user status openclaw-gateway
curl -sS http://127.0.0.1:13749/health
```

## 定时任务（Mac mini）

| 任务 | 调度 (Asia/Shanghai) | 说明 |
|------|----------------------|------|
| `whaletrail-daily` | `30 8 * * 1-5` | 工作日 08:30 `daily-report.sh gold_sma GLD` → Telegram |
| `whaletrail-sentiment` | `0 9 * * *` | 每日 09:00 X KOL 情绪扫描 → Telegram |

## 安全约定

- 不把 Gateway token、模型 Key、SSH 密码写进 git 或聊天。
- VPS Gateway 公网暴露见 VPS runbook 待办。
