# box bot 角色规划（全局角色控制）

> 给 **box 上运行期 bot** 看的角色/职责定义。六个助手跑在共享 Grok Bot 机上，不在 Mac mini。
> 人设源是 valar `origin/main` 本目录；**生效靠把 `roles/<bot>.md` 贴进该 bot 档案栏**，push 完侧边栏不会自动变。
>
> 文档分工:`runbooks/`(含 WhaleTrail 手册)是给**开发期 agent**(如 Grok Build 做开发/运维时)看的,**不是** box bot 的运行期角色。两者不混用。

## 部署铁律（重要）

**每个 bot 的档案栏只贴它自己那一段（`roles/<bot>.md`）**,不要六段都塞进同一个 bot——上下文会互相污染,分轨就废了。**`roles/project-ops.md`(群说明)单独贴到群**,不进任何单个 bot。

## 模型

```
valar 远端 (origin/main)  ──读取──▶  box(bot 群)
   ├─ grok-bots/roles/*.md      每个 bot 的角色（单独分发）
   ├─ grok-bots/roles/project-ops.md  群协作说明（单独贴群）
   ├─ journal/                  跨项目决策与工作日志
   └─ projects/whaletrail/      当前重点项目索引
```

- valar = box bot 群的**全局指导 + 角色控制**单一来源。
- 当前业务:**WhaleTrail Lab**,两本薄账——**黄金日线对照** + **A 股跟庄观察/15:30 paper**(见 [`projects/whaletrail/`](../projects/whaletrail/README.md))。
- 各角色 `对照` 里引用的 `SCOPE.md` / `DASHBOARD.md` / `DEPLOY.md` 住在 **whaletrail-lab 仓库**(`projects/whaletrail/docs/…`),不在 valar 里。

## bot 名册

| # | 角色 | 一句话定位 | 档案 |
|---|------|-----------|------|
| 1 | **Axiom**（组织者 / owner） | WhaleTrail 运行时 owner:收敛已拍/不做/未决,盯现网,过审文案 | [`roles/axiom.md`](roles/axiom.md) |
| 2 | **RD**（技术开发） | 工程位:在 whaletrail-lab 改读取/展示/扫描脚本与 docs,改前报文件与风险 | [`roles/rd.md`](roles/rd.md) |
| 3 | **Big-A**（A 股研究） | A 股跟庄日线:阴线锚点 + 观察/接近/触发三分类,不荐股 | [`roles/big-a-mast.md`](roles/big-a-mast.md) |
| 4 | **Gold Mast**（黄金研究） | 黄金一轨:现网 paper(GLD)/对照(GC=F 等)/纸黄金三线不混 | [`roles/gold-mast.md`](roles/gold-mast.md) |
| 5 | **Data Mast**（DE & DA） | 数据合同:无源不出 OHLC,声明来源/日历/缺口 | [`roles/data-mast.md`](roles/data-mast.md) |
| 6 | **Challenger**（审视者） | 按合同打回:查买卖词/标的混淆/无源出数/越权改现网 | [`roles/challenger.md`](roles/challenger.md) |
| — | **project-ops**（群说明） | 群协作规则与发言顺序(单独贴群,非 bot) | [`roles/project-ops.md`](roles/project-ops.md) |
| 7 | _第 7 个助手_ | _待定_（admin 提供名称与职责后按同格式补） | _TBD_ |

## 边界与规则

- 产品形状以 `whaletrail-lab/SCOPE.md` 为准。Mini runbook 已按「黄金 + A 股两本账」对齐；开发期仍不要把 Mini 写成六个 Grok Bot 的宿主。
- 角色/职责变更走工作日志 [`journal/`](../journal/README.md) 留痕。
- 不在本目录写任何密钥 / token。
