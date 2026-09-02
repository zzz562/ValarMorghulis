# 宿主拆分 + 贴档生效

> 日期: 2026-09-02 ・ 作者: Axiom（box bot） ・ 范围: box 角色规划

## 背景
名册补全后仍有几处对不齐：根 README 把 Mini 写成 Grok Bot 宿主；`grok-bots/README` 只列 OpenClaw/Telegram；「读 origin/main 才生效」容易理解成 push 完人设自动变；Big-A 侧边栏名与仓内「Big-A mast」不一致；跟庄票名写死人设会过期；Mini runbook 仍写「不做 A 股」。

## 决定
- 六个 Grok Bot 住在共享 Grok Bot 机（box）；OpenClaw / Telegram 是 Mini（及阿里云 Gateway）服务。两套分开登记。
- 仓是人设源；**生效靠把 `roles/<bot>.md` 贴进该 bot 档案栏**。push 完侧边栏不会自动变。
- 对外显示名 **Big-A**；档案文件名保持 `big-a-mast.md`。
- 跟庄名单只指向 Mini `config/watchlist.yaml`，人设里不枚举票名。
- Mini runbook 按「黄金 + A 股两本账」改口，仍不做港股/高频/Tushare dump。产品形状以 whaletrail-lab `SCOPE.md` 为准。
- Axiom 仍拍 WhaleTrail 板，同时管跳板 / 现网 / 纪要；不是把连接器当主业。
- A 股收盘叠加层本轮不写入角色和手册，先慢慢建设。

## 动作
docs 对齐：`README.md`、`AGENTS.md`、`grok-bots/README.md`、`grok-bots/ROLES.md`、`roles/axiom.md`、`roles/big-a-mast.md`、`runbooks/macmini/README.md`、`projects/whaletrail/README.md`。

## 待办 / 开放问题
- 第 7 个助手仍 TBD。
- 纸黄金牌价与日切仍未拍，保持无源。
