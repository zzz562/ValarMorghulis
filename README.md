# ValarMorghulis · 项目与 Grok Bot 管理中枢

> 从「个人试验场」升级为 **管理个人项目 + 服务器上的 Grok Bot** 的中枢仓库。
> 本仓库主要存放 **索引、运维手册、脚本、box bot 角色规划**；各项目的实际代码住在各自独立仓库。

Remote: `https://github.com/zzz562/ValarMorghulis.git`

---

## 目录结构

| 路径 | 作用 |
|------|------|
| `projects/` | 各项目的索引与说明（代码在各自独立仓库，这里只做登记/引用） |
| `runbooks/` | 设备与服务运维手册（Mac mini / 阿里云 VPS）——给**开发期 agent**看 |
| `grok-bots/` | box 上运行的 bot 清单 + `ROLES.md` + `roles/*.md`（每 bot 一份角色） |
| `journal/` | 共享工作日志（box bot 与我的 agent 都可写；规则见 `journal/README.md`） |
| `scripts/` | 通用小脚本（如模型连通性测试） |

> **box bot 交付模型**：box(grok bot 主机)上的 6 个 bot **读本仓库的远端分支**获取全局指导与角色定义，
> 所以面向 bot 的改动**必须推到 `origin/main`** 才生效。角色规划见 [`grok-bots/ROLES.md`](grok-bots/ROLES.md)。

---

## 我管理的东西

### 设备 / 基础设施

| 设备 | 角色 | 运维手册 |
|------|------|----------|
| **Mac mini** (M4, `Zephyrs-Mac-mini.local`) | 主开发 / 本地推理 / 回测 / Grok Bot | [`runbooks/macmini/`](runbooks/macmini/README.md) |
| **阿里云 VPS** (`139.224.244.214`, 上海) | 公网 Gateway 入口 + Mac mini 反向隧道跳板 | [`runbooks/aliyun-openclaw/`](runbooks/aliyun-openclaw/README.md) |

### 项目

| 项目 | 状态 | 索引 |
|------|------|------|
| **WhaleTrail Lab**（量化交易 · 主项目 · 黄金 + A 股两本账） | Active · 独立仓库 `gwht` | [`projects/whaletrail/`](projects/whaletrail/README.md) |

### Grok Bot（box 上运行）

见 [`grok-bots/`](grok-bots/README.md) 与 [`grok-bots/ROLES.md`](grok-bots/ROLES.md)：Axiom / RD / Big-A / Gold / Data / Challenger 等 6 个 bot 的角色定义；相关 OpenClaw Gateway / Telegram 服务见清单。

---

## 约定

- **各项目代码住在各自独立仓库**，本仓库只登记引用，不 vendor 别的仓库代码。
- 保持小步提交；**绝不提交密钥 / API Token / 大二进制**。脚本里的密钥一律走环境变量。
- 主分支保持线性精简；改造前的试验代码只保留在标签 / 分支 `backup/playground-2026-09-01`，需要时从那里找回。

```bash
cd ~/github_code/ValarMorghulis && grok
```
