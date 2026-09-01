# ValarMorghulis

**项目与 Grok Bot 管理中枢** —— 管理个人项目、服务器上的 Grok/OpenClaw Bot，以及全局基础设施（Mac mini / 阿里云 VPS）运维手册。

> 本仓库由「个人试验场」升级而来。旧的试验代码（notebooks / CSV）已归档到 `archive/playground/`，
> 并打标签 / 分支 `backup/playground-2026-09-01` 备份，可随时找回。

## Remote

- `https://github.com/zzz562/ValarMorghulis.git`

## 仓库定位

- 存放 **索引 / 运维手册 / 脚本 / 归档**；各项目的实际代码住在各自独立仓库，本仓库只登记引用。
- 适合「非公司业务线」的探索、配置、运维类任务。公司 DA 请改去 `~/gitlab_bzl/<biz-repo>`。

## 目录

| 路径 | 作用 |
|------|------|
| `projects/` | 项目索引（WhaleTrail Lab / ValarmClub …） |
| `runbooks/` | 设备运维手册（`macmini/`、`aliyun-openclaw/`） |
| `grok-bots/` | 服务器上的 Grok / OpenClaw Bot 清单 |
| `scripts/` | 通用脚本 |
| `archive/playground/` | 改造前试验代码归档 |

## 项目 / 设备索引

| 对象 | 类型 | 位置 / 手册 |
|------|------|-------------|
| WhaleTrail Lab（主项目 · 量化交易「store」） | 独立仓库 `gwht` | `~/github_code/whaletrail-lab` · 索引 `projects/whaletrail/` |
| Mac mini | 设备 | `runbooks/macmini/README.md` |
| 阿里云 VPS | 设备 | `runbooks/aliyun-openclaw/README.md` |
| Grok / OpenClaw Bot | 服务 | `grok-bots/README.md` |

## Rules

- **各项目代码住在各自独立仓库**，本仓库不 vendor 其它仓库代码，只做索引/引用。
- 保持小步提交；**勿提交密钥与大二进制**，脚本密钥一律走环境变量。
- 归档只增不删；`backup/*` 标签/分支保留改造前状态。

```bash
cd ~/github_code/ValarMorghulis && grok
```
