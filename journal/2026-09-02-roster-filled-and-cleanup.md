# bot 名册补全 + 主分支清理

> 日期: 2026-09-02 ・ 作者: Grok Build (admin 的开发 agent) ・ 范围: box 角色规划 / 仓库清理
>
> 关联: [2026-09-02-box-bot-role-planning.md](2026-09-02-box-bot-role-planning.md)

## 背景
admin 提供了 box bot 群的完整角色定义（6 个 bot + 群说明），并要求清理主分支。

## 决定
1. **bot 名册补全**（6 个 bot + project-ops 群说明），每个一份独立档案,放 `grok-bots/roles/<bot>.md`:
   - **Axiom**(组织者/owner)、**RD**(工程)、**Big-A mast**(A 股研究)、**Gold Mast**(黄金研究)、**Data Mast**(DE&DA)、**Challenger**(审视者)。
   - **project-ops**(群说明)单独一份,只贴群,不进任何单个 bot。
   - 部署铁律:**每个 bot 只贴自己那一段**,避免上下文互相污染。第 7 个助手待 admin 提供。
2. **归档不再留在主分支**:删除 `archive/`(playground)。已打 tag/branch `backup/playground-2026-09-01` 并推远端,需要时从那里找回。
3. **不再提公司 GitLab**:AGENTS.md / README 去掉 `~/gitlab_bzl` 相关文案。
4. **ValarmClub 下线**:其选股逻辑已并入 WhaleTrail,作为历史项目不再单列;删除 `projects/valarmclub/`,索引里改为一句历史说明。
5. **WhaleTrail 主方向 = 黄金 + A 股两本账**:更新 `projects/whaletrail/README.md`(黄金日线对照 + A 股跟庄观察/paper)。

## 动作
- ✅ 新建 `grok-bots/roles/`(axiom / rd / big-a-mast / gold-mast / data-mast / challenger / project-ops)。
- ✅ 重写 `grok-bots/ROLES.md` 为名册索引 + 部署铁律 + 模型。
- ✅ `git rm archive/ projects/valarmclub/`。
- ✅ AGENTS.md / README / projects/README / projects/whaletrail/README 同步更新。
- ✅ 清理 `.gitignore` 残留的 archive 行。

## 待办 / 开放问题
- [ ] **第 7 个 bot**:名称 + 实际职责,admin 提供后按同格式补 `roles/` + 名册表。
- [ ] **群名改 `whaletrail-lab`**:仍是聊天端/配置端的手动动作,valar 侧无法代改;沿用前一条记录的待办。
- [ ] **runbook 与新 SCOPE 冲突**:Mac mini runbook 写「不做 A 股」,与现 A 股跟庄轨冲突,以 whaletrail-lab `SCOPE.md` 为准,后续对齐(规则冲突本阶段不裁决)。
- [ ] **主分支保护**:box bot / 其它 agent 写 `main` 需走 PR 或 bypass(见前一条记录)。
