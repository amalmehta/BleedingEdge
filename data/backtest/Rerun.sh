set -e
uv run python -m bleedingedge.mining 2024 > data/backtest/Mining2024.log 2>&1
uv run python -m bleedingedge.mining 2024 --ro > data/backtest/Mining2024RO.log 2>&1
uv run python -m bleedingedge.backtest --year 2024 > data/backtest/Run2024.log 2>&1
uv run python -m bleedingedge.backtest --year 2024 --holdout > data/backtest/Run2024Holdout.log 2>&1
uv run python -m bleedingedge.backtest --year 2024 --ro > data/backtest/Run2024RO.log 2>&1
uv run python -m bleedingedge.backtest --year 2024 --ro --holdout > data/backtest/Run2024ROHoldout.log 2>&1
