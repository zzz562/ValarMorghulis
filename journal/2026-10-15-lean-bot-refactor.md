# 切换到轻量 Chief of Staff Bot 模型

> 日期: 2026-10-15 ・ 作者: Grok (admin agent) ・ 范围: box 角色规划

## 背景
之前 6 个 Bot + 群聊的设置在实际使用中感觉不顺（路由成本高、上下文易污染）。已删除旧 Bot，只保留 Axiom 和 Fiona。

## 决定
采用更轻的架构：
- **Axiom** 作为唯一前门（Chief of Staff / Main Bot）
- **Fiona** 作为私人秘书（个人 / 家庭 / NZ / 英语）
- **Mast** 作为市场与量化研究（合并原 Big-A / Gold / Data 职责）
- **Forge** 作为可选技术执行

你主要只跟 Axiom 说话，需要深度工作时再进入对应单聊。

## 动作
- 更新 `grok-bots/ROLES.md`
- 更新 `roles/axiom.md`
- 新建 `roles/fiona.md`、`roles/mast.md`、`roles/forge.md`

## 待办 / 开放问题
- 把新角色贴进实际 Bot 档案栏
- 把 Axiom 设为 Main Bot
- 跑 1-2 周后评估是否需要 Forge 或其他专家
