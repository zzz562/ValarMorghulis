# ValarMorghulis · 项目与 Grok Bot 管理中枢

> 从「个人试验场」升级为 **管理个人项目 + 服务器上的 Grok Bot** 的中枢仓库。
> 本仓库主要存放 **索引、运维手册、脚本、归档**；各项目的实际代码住在各自独立仓库。

Remote: `https://github.com/zzz562/ValarMorghulis.git`

---

## 目录结构

| 路径 | 作用 |
|------|------|
| `projects/` | 各项目的索引与说明（代码在各自独立仓库，这里只做登记/引用） |
| `runbooks/` | 设备与服务运维手册（Mac mini / 阿里云 VPS）——给**开发期 agent**看 |
| `grok-bots/` | box 上运行的 Grok / OpenClaw Bot 清单 + `ROLES.md`（运行期角色规划） |
| `journal/` | 共享工作日志（box bot 与我的 agent 都可写；规则见 `journal/README.md`） |
| `scripts/` | 通用小脚本（如模型连通性测试） |
| `archive/` | 归档：`playground/` 为改造前的试验代码（notebooks / CSV） |

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
| **WhaleTrail Lab**（量化交易平台 / “store”，主项目） | Active · 独立仓库 `gwht` | [`projects/whaletrail/`](projects/whaletrail/README.md) |
| ValarmClub（PyQt A股选股 Lab） | 历史参考 | [`projects/valarmclub/`](projects/valarmclub/SUMMARY.md) |

### Grok Bot（服务器上运行）

见 [`grok-bots/`](grok-bots/README.md)：Mac mini 与 VPS 上的 OpenClaw Gateway、Telegram `@iron_blade_bot` 等。

---

## 约定

- 本仓库只放「非公司业务线」的探索、配置、索引与运维内容。公司 DA 去 `~/gitlab_bzl/<biz-repo>`。
- **各项目代码住在各自独立仓库**，本仓库只登记引用，不 vendor 别的仓库代码。
- 保持小步提交；**绝不提交密钥 / API Token / 大二进制**。脚本里的密钥一律走环境变量。
- 改造前的试验代码已归档到 `archive/playground/`，并打标签 `backup/playground-2026-09-01` 可随时找回。

```bash
cd ~/github_code/ValarMorghulis && grok
```
