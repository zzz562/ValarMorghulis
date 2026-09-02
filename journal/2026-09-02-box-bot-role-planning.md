# box bot 角色规划启动

> 日期: 2026-09-02 ・ 作者: Grok Build (admin 的开发 agent) ・ 范围: box 角色规划

## 背景

- valar 仓库已从「个人试验场」重构为**项目 + Grok bot 管理中枢**,并推送到远端(`origin/main` = 59016e2)。
- box(grok bot 主机)上跑着 **6 个 bot**。它们**读 valar 的远端分支**来获取指导——所以远端 main 必须保持最新。
- valar 对 box bot 的定位:**全局指导 + 全局角色控制**。以后有其它工程时,也用 valar 做统一的角色/协作规划。
- 当前主要工作在 **WhaleTrail Lab**(独立仓库 `gwht`)。

## 决定

1. **valar = box bot 的指导源**,通过 git 远端分支分发;box 侧只读、不需要在 box 上改。
2. **角色规划集中在 `grok-bots/ROLES.md`**;跨项目协作决策记在本 `journal/`。
3. **两类「给 agent 看的文档」分清楚,互不混淆:**
   - `runbooks/`(尤其 whaletrail 相关) = 给**开发期 agent**看的(例如 Grok Build 在做开发/运维时)。
   - `grok-bots/ROLES.md` = 给 **box 上运行期 bot**看的角色/职责。
4. **规则打架的问题本阶段不处理**——等 box bot 正式接管后再谈。本 session 只做 box 的角色规划。
5. 工作日志规则见 [`journal/README.md`](README.md):一条一文件、只追加、写明作者、写前 `pull --rebase`、不落密钥。

## 动作

- ✅ 远端推送:`main`、`backup/playground-2026-09-01` 分支 + 同名 tag。
- ✅ 建立 `journal/` 工作日志与规则。
- ✅ 建立 `grok-bots/ROLES.md` 角色规划骨架(6 个 bot 名额待填)。
- ✅ AGENTS.md / README 增加 journal、roles、「box 读远端」交付模型的索引。

## 待办 / 开放问题

- [ ] **6 个 bot 的身份未知**:名称、职责、宿主(是否都在同一 box、还是分布在 Mac mini / VPS)、通道。需 admin 提供后填入 `grok-bots/ROLES.md` 的名册表。
- [ ] **群名改为 `whaletrail-lab`**:记录此决定(该群主要聊 WhaleTrail 项目)。若指聊天群(Telegram 等),需在聊天端手动改;若指 bot 侧配置,待确认位置后再改。
- [ ] **分支保护**:`main` 有「必须走 PR」保护规则。box bot / 其它 agent 若要往 `main` 写日志,没有 bypass 权限会被挡。待定协作写入方式(独立分支 + PR,或给 bot 账号 bypass)。本阶段先不改。
