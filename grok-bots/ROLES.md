# box bot 角色规划（全局角色控制）

> 给 **box 上运行期 bot** 看的角色/职责定义。
> 人设源是 valar `origin/main` 本目录；**生效靠把 `roles/<bot>.md` 贴进该 bot 档案栏**，push 完侧边栏不会自动变。
>
> 文档分工:`runbooks/`(含 WhaleTrail 手册)是给**开发期 agent**(如 Grok Build 做开发/运维时)看的,**不是** box bot 的运行期角色。两者不混用。

## 部署铁律（重要）

**每个 bot 的档案栏只贴它自己那一段（`roles/<bot>.md`）**，不要把多段都塞进同一个 bot——上下文会互相污染，分轨就废了。

## 模型

```
valar 远端 (origin/main)  ──读取──▶  box(bot 群)
   ├─ grok-bots/roles/*.md           每个 bot 的角色（单独分发）
   ├─ journal/                       跨项目决策与工作日志
   └─ projects/whaletrail/           当前重点项目索引
```

- valar = box bot 群的**全局指导 + 角色控制**单一来源。
- 当前业务:**WhaleTrail Lab**（黄金 + A 股两本账）+ 个人生活/NZ 移民规划。
- 各角色引用的 `SCOPE.md` 等住在 **whaletrail-lab 仓库**。

## 新架构（2026-10-15 重构）

采用更轻的 Chief of Staff 模型：你主要只跟 Axiom 说话，其他 Bot 保持窄领域。

| # | 角色 | 一句话定位 | 档案 | 状态 |
|---|------|-----------|------|------|
| 1 | **Axiom**（Chief of Staff / 前门） | 唯一前门：路由、汇总、决策跟踪、早间简报 | [`roles/axiom.md`](roles/axiom.md) | 主 Bot |
| 2 | **Fiona**（私人秘书） | 个人 / 家庭 / NZ 移民 / 英语 / 反思 | [`roles/fiona.md`](roles/fiona.md) | 保留 |
| 3 | **Mast**（市场与量化） | 黄金 + A 股研究、数据合同、日报解读 | [`roles/mast.md`](roles/mast.md) | 新建 |
| 4 | **Forge**（技术执行） | 代码、数据管道、Mac Mini 运维协助 | [`roles/forge.md`](roles/forge.md) | 可选 |

旧的 RD / Big-A / Gold Mast / Data Mast / Challenger 已归档，不再使用。

## 边界与规则

- 产品形状以 `whaletrail-lab/SCOPE.md` 为准。
- 角色/职责变更走工作日志 [`journal/`](../journal/README.md) 留痕。
- 不在本目录写任何密钥 / token。
- 你主要只跟 Axiom 说话；需要深度工作时直接进入对应 Bot 单聊，或让 Axiom 临时建群。
