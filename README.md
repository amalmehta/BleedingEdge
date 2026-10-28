# BleedingEdge

A personal research radar: it looks for AI research topics that are heating up before everyone else notices, and backtests the method on 2021–25 history before trusting it.

**Status:** the backtest **fails**. It flags known topics 20–68 weeks early, but on held-out data almost none of its flags turned into real trends: 1 of 19 for robotics, about what picking at random gives. The bar was half. A 4-week robotics-only trial runs from 27 Oct 2026 as a test of the format (does a firm weekly pick get acted on), not of the detector. See [why](docs/BACKTEST.md).

![Vision-language-action models: papers, new repos, funding rounds and Hacker News stories per 4-week window. The first flag (blue line, Jun 2024) comes 48 weeks before the research crowd arrives (red line, May 2025).](docs/img/backtest-vla.png)

*Vision-language-action models, 2021–25. Blue dashed line: BleedingEdge's first flag (Jun 2024). Red dashed line: the research crowd arrives (May 2025).*

## Links

- **Run it:** [Setup and instructions](docs/INSTRUCTIONS.md) (one `uv run` command; the first run fetches about 2 hours of data, then re-runs are free)
- **Results:** [What the backtest found](docs/BACKTEST.md) · [Every count, query and chart](docs/BacktestResults.md)
- **How it works:** [System design](docs/SYSTEM-DESIGN.md) · [What's where](docs/FILE-STRUCTURE.md)
- **The spec:** [BleedingEdge.md](BleedingEdge.md)
