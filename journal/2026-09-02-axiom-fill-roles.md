# 落实 6 个 Grok Bot 人设

> 日期: 2026-09-02 ・ 作者: Axiom（Grok Bot） ・ 范围: box角色规划
> 关联: [2026-09-02-box-bot-role-planning.md](2026-09-02-box-bot-role-planning.md)

## 背景

admin 让审 valar 能否当 Grok Bot 主机指导手册，并落实其他人设。当时 `ROLES.md` 名册仍是 TBD。

## 决定

1. **手册骨架可用**，但必须改三处事实：
   - 6 个助手宿主是 **Grok Bot 共用 Linux**，不是 Mac mini。
   - Mini 上的 OpenClaw / Telegram 是服务，不是这 6 个人设。
   - 主机尚未 clone valar；运行期用 GitHub 读 `origin/main`。
2. 名册按已在 Grok Bot 档案里的描述写入：Axiom / RD / Big-A / Gold Mast / Data Mast / Challenger。
3. `New Bot` 仍是空壳，不进名册。
4. 群名仍为 `project-ops`（改 `whaletrail-lab` 未点头）。

## 动作

- 重写 `grok-bots/ROLES.md` 名册与宿主说明。
- `grok-bots/README.md` 把 Grok Bot 助手和 OpenClaw 服务拆开。
- 本条日志。

## 待办 / 开放问题

- [ ] `main` 分支保护：本改动走分支 + PR。
- [ ] 群是否改名 `whaletrail-lab`。
- [ ] 是否在 Grok Bot 主机 clone valar，还是继续 GitHub 只读。
