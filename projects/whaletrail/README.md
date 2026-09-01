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

黄金为主的 paper trading / 回测平台：**主 黄金 GLD，辅 美股指数 SPY/QQQ 对冲**；不做 A股/港股/高频。
数据源仅 `yfinance` + Parquet 缓存。看板 `http://127.0.0.1:8766/`。

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
