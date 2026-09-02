# ValarMorghulis

**项目与 Grok Bot 管理中枢** —— 管理个人项目、服务器上的 Grok/OpenClaw Bot，以及全局基础设施（Mac mini / 阿里云 VPS）运维手册。

> 本仓库由「个人试验场」升级而来。旧的试验代码（notebooks / CSV）不再留在主分支，
> 已随标签 / 分支 `backup/playground-2026-09-01` 备份，需要时从那里找回。

## Remote

- `https://github.com/zzz562/ValarMorghulis.git`

## 仓库定位

- 存放 **索引 / 运维手册 / 脚本 / 角色规划**；各项目的实际代码住在各自独立仓库，本仓库只登记引用。
- 面向个人项目与 box 上的 Grok bot 群做全局管理与角色控制。

## 目录

| 路径 | 作用 |
|------|------|
| `projects/` | 项目索引（当前重点 WhaleTrail Lab） |
| `runbooks/` | 设备运维手册（`macmini`、`aliyun-openclaw`）——给**开发期 agent**看 |
| `grok-bots/` | box bot 清单 + `ROLES.md` + `roles/*.md`（运行期角色，每 bot 一份） |
| `journal/` | 共享工作日志（box bot 与我的 agent 都可写；规则见 `journal/README.md`） |
| `scripts/` | 通用脚本 |

## box bot 交付模型

- box(grok bot 主机）上的 **6 个 bot 读本仓库的远端分支**（`origin/main`）获取全局指导与角色定义。
- 因此:**面向 box bot 的改动必须推到远端才生效**。角色规划见 `grok-bots/ROLES.md`（每个 bot 的档案在 `grok-bots/roles/<bot>.md`，只贴各自那一段）。
- 文档分工:`runbooks/`（含 WhaleTrail 手册）给**开发期 agent**（如 Grok Build）；`grok-bots/roles/` 给 **box 运行期 bot**。两者不混用。
- 跨项目的角色/协作决策记入 `journal/`（只追加、写明作者、写前 `git pull --rebase`）。

## 项目 / 设备索引

| 对象 | 类型 | 位置 / 手册 |
|------|------|-------------|
| WhaleTrail Lab（主项目 · 黄金 + A 股两本账） | 独立仓库 `gwht` | `~/github_code/whaletrail-lab` · 索引 `projects/whaletrail/` |
| Mac mini | 设备 | `runbooks/macmini/README.md` |
| 阿里云 VPS | 设备 | `runbooks/aliyun-openclaw/README.md` |
| Grok bot 群（box） | 服务 | `grok-bots/README.md` · `grok-bots/ROLES.md` |

## Rules

- **各项目代码住在各自独立仓库**，本仓库不 vendor 其它仓库代码，只做索引/引用。
- 保持小步提交；**勿提交密钥与大二进制**，脚本密钥一律走环境变量。
- 主分支保持线性精简；改造前的历史内容只保留在 `backup/*` 标签/分支。

```bash
cd ~/github_code/ValarMorghulis && grok
```
