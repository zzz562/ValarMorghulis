# box bot 角色规划(全局角色控制)

> 给 **box 上运行期 bot** 看的角色/职责定义。box bot **读 valar 远端分支**获取本文件,所以改动要推到 `origin/main` 才会生效。
>
> 注意区分:`runbooks/`(含 WhaleTrail 手册)是给**开发期 agent**(如 Grok Build 做开发/运维时)看的,**不是** box bot 的运行期角色。两者不要混用。

## 模型

```
valar 远端 (origin/main)  ──读取──▶  box(6 个 bot)
   ├─ grok-bots/ROLES.md        全局角色 / 职责 / 边界
   ├─ journal/                  跨项目决策与工作日志
   └─ projects/                 各项目索引(当前重点: WhaleTrail Lab)
```

- valar = box bot 的**全局指导 + 角色控制**单一来源。
- 当前主要业务:**WhaleTrail Lab**(量化交易 / paper trading,见 [`projects/whaletrail/`](../projects/whaletrail/README.md))。
- 以后新增其它工程时,同样在 valar 里登记项目 + 定义相关角色。

## bot 名册(6 个 · 待填)

> admin 提供后填入。每个 bot 至少写清:名称、宿主、通道、职责、边界(能做/不能做)、关联项目。

| # | Bot 名称 | 宿主 | 通道 | 职责 | 边界 | 关联项目 |
|---|----------|------|------|------|------|----------|
| 1 | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| 2 | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| 3 | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| 4 | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| 5 | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| 6 | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ |

## 已知的相关 bot / 服务

（来自现有 runbook,可能与上表部分重合,待 admin 核对归并）

| Bot / 服务 | 宿主 | 通道 / 端口 | 现状 |
|------------|------|-------------|------|
| Telegram `@iron_blade_bot` | Mac mini(经 OpenClaw Gateway) | Telegram,白名单 `5102138680` | WhaleTrail 日报 / 情绪扫描 |
| OpenClaw Gateway (Mac mini) | Mac mini | loopback `:18789` | 本地推理 / 触发 |
| OpenClaw Gateway (VPS) | 阿里云 VPS | `:13749`(公网,token) | 公网入口,通道待接入 |

详见 [`../grok-bots/README.md`](README.md) 与 [`../runbooks/`](../runbooks/)。

## 边界与规则

- 规则冲突(box bot 规则 vs 开发期规则)**本阶段不裁决**,等 box bot 正式接管后再定。
- 角色/职责变更走工作日志 [`journal/`](../journal/README.md) 留痕。
- 不在本文件写任何密钥 / token。
