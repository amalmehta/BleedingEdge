# BleedingEdge

A personal research radar: it looks for AI research topics that are heating up before everyone else notices, and backtests the method on 2021–25 history before trusting it.

**Status:** only the backtest is built, and it **fails**. It flags known topics 16–48 weeks early, but just 6% of its 2024 flags turned into real trends (the bar is 50%). See [why](docs/BACKTEST.md).

![Vision-language-action models: papers, new repos, funding rounds and Hacker News stories per 4-week window. The first flag (blue line, Jun 2024) comes 48 weeks before the research crowd arrives (red line, May 2025).](docs/img/backtest-vla.png)

*Vision-language-action models, 2021–25. Blue dashed line: BleedingEdge's first flag (Jun 2024). Red dashed line: the research crowd arrives (May 2025).*

## Links

- **Run it:** [Reproduce the backtest](docs/BACKTEST.md#reproduce) (one `uv run` command; cached data makes re-runs free)
- **Results:** [What the backtest found](docs/BACKTEST.md) · [Every count, query and chart](docs/BacktestResults.md)
- **How it works:** [System design](docs/SYSTEM-DESIGN.md)
- **The spec:** [BleedingEdge.md](BleedingEdge.md)
