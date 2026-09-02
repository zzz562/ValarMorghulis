# WhaleTrail Lab（量化交易平台 · 主项目）

> 本仓库的**核心项目**。用户称其为 “whale tail lab / store”。
> 代码住在独立仓库，本文件只做索引；**不要在本仓库 vendor 它的代码**。

## 位置

| 项 | 值 |
|----|----|
| 主开发源（Mac mini） | `~/Projects/whaletrail-lab`（唯一主源，开发/测试/提交/推送都在这里） |
| MacBook 查看副本 | `~/github_code/whaletrail-lab`（alias `gwht`，只查看/轻量验证，勿长期开发） |
| Git 远端 | `https://github.com/zzz562/whaletrail-lab` |
| 活动子项目 | `projects/whaletrail/`（统一回测 / paper trading 平台，唯一 active） |

## 一句话定位

**黄金 + A 股两本薄账**（后续主方向）：

- **黄金日线一本账**：GLD 策略（`gold_sma`）vs 买入持有 vs SPY 对照，情绪当天气；5m 面板只观察、不跟单。数据源 `yfinance` + Parquet 缓存。
- **A 股跟庄一本账**：现网 `config/watchlist.yaml` 那几只，日线跟庄的观察 / 接近 / 触发三分类，15:30 paper/观察。数据源 tvscreener / baostock。

看板（只读监控）`http://127.0.0.1:8766/`。不做大而全平台；扩名单 / 换主策略 / 纸黄金独立文件都需 Axiom 拍板。

> 产品形状与决策记录以 whaletrail-lab 仓库的 `SCOPE.md` 为准（box bot 角色对照 `grok-bots/ROLES.md`）。
> 注意:Mac mini runbook 旧文案仍写「不做 A 股」,与现方向冲突,以 SCOPE.md 为准,后续对齐(规则冲突本阶段不裁决)。

## 常用入口（在 Mac mini 上）

```bash
cd ~/Projects/whaletrail-lab/projects/whaletrail
.venv/bin/python scripts/run-backtest.py gold_sma GLD 2018-01-01 2024-12-31 100000   # 主回测
./scripts/daily-report.sh gold_sma GLD                                              # 日报 → Telegram
.venv/bin/streamlit run scripts/dashboard.py --server.port 8766                     # 看板
```

## 关联

- 运行/运维：见 [`runbooks/macmini/README.md`](../../runbooks/macmini/README.md) 的 “WhaleTrail” 与 launchd `ai.whaletrail-live` 段落。
- Bot 触发（Telegram / OpenClaw cron）：见 [`grok-bots/README.md`](../../grok-bots/README.md)。

## 同步规则（重要）

- Mac mini `~/Projects/whaletrail-lab` 为唯一主源 → push 到 GitHub → MacBook 查看副本 `git fetch + reset --hard origin/main`。
- 不提交 `.venv/`、`data_cache/`、`results/`、`logs/`、`*.log`、`*.err`。
