# Grok Bot 与 OpenClaw 清单

> **角色规划见 [`ROLES.md`](ROLES.md)**。本文件登记两套东西，不要混：
>
> 1. **box 上的 Grok Bot 助手**（人设在 `roles/*.md`）
> 2. **Mini / 阿里云上的 OpenClaw Gateway 与 Telegram**（服务，不是 Bot 本身）
>
> 密钥、Gateway Token **一律不写入本仓库**（见对应 runbook 的“备份清单”，实际值放机器上的 `~/.openclaw/.env` 等）。

## box 上的 Grok Bot 助手

跑在共享 Grok Bot Linux 机上，不在 Mac mini 上。人设源是 valar `origin/main` 的 `roles/<bot>.md`，**生效靠把该段贴进该 bot 档案栏**（push 完侧边栏不会自动变）。

| Bot | 一句话 | 档案 |
|-----|--------|------|
| **Axiom** | Chief of Staff / 前门 | [`roles/axiom.md`](roles/axiom.md) |
| **Fiona** | 私人秘书 | [`roles/fiona.md`](roles/fiona.md) |
| **Mast** | 市场与量化研究 | [`roles/mast.md`](roles/mast.md) |
| **Forge** | 技术执行（可选） | [`roles/forge.md`](roles/forge.md) |

完整名册与边界见 [`ROLES.md`](ROLES.md)。

## Mini / VPS 上的 OpenClaw 服务

| 服务 | 宿主 | 通道 / 端口 | 用途 | 管理手册 |
|------|------|-------------|------|----------|
| **OpenClaw Gateway (Mac mini)** | Mac mini | loopback `:18789` | 本地推理 / 回测触发 / Telegram 后端 | [`runbooks/macmini/`](../runbooks/macmini/README.md) |
| **Telegram `@iron_blade_bot`** | Mac mini（经 Gateway） | Telegram，白名单用户 `5102138680` | WhaleTrail 日报 / 情绪扫描 / 交互 | [`runbooks/macmini/`](../runbooks/macmini/README.md) |
| **OpenClaw Gateway (VPS)** | 阿里云 VPS | `0.0.0.0:13749`（公网，token 鉴权） | 公网可达入口；聊天通道待接入 | [`runbooks/aliyun-openclaw/`](../runbooks/aliyun-openclaw/README.md) |

## 关键操作速查

```bash
# Mac mini — Gateway 状态 / 健康
launchctl list | grep openclaw
curl -s http://127.0.0.1:18789/health        # {"ok":true}

# VPS — Gateway 状态 / 健康
systemctl --user status openclaw-gateway
curl -sS http://127.0.0.1:13749/health

# OpenClaw 定时任务（Mac mini）
openclaw cron list
```

## 定时任务（Mac mini）

| 任务 | 调度 (Asia/Shanghai) | 类型 | 说明 |
|------|----------------------|------|------|
| `whaletrail-daily` | `30 8 * * 1-5` | command | 工作日 08:30 跑 `daily-report.sh gold_sma GLD` → Telegram |
| `whaletrail-sentiment` | `0 9 * * *` | command | 每日 09:00 X KOL 情绪扫描 → Telegram |

## 安全约定

- 不把 `gateway.auth.token`、模型 API Key、root 密码写进 git 或聊天记录。
- VPS Gateway 目前 `bind=lan` 暴露公网，建议收紧为 loopback + SSH 转发或安全组锁 IP（见 VPS runbook 待办）。
