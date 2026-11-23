from pathlib import Path
import pandas as pd
import yfinance as yf

tickers = pd.read_csv("tickers.csv")

# One year of daily closes, adjusted for splits and dividends
px = yf.download(tickers["ticker"].tolist(), period="1y", auto_adjust=True)["Close"]
# keep only days when most tickers traded (drops weekend futures-only rows)
px = px.dropna(thresh=len(px.columns) // 2).ffill()
px.to_csv("data/prices.csv")

last = px.iloc[-1]


def vs_average(days):
    """Percent distance of the latest close from its N-day moving average."""
    average = px.rolling(days).mean().iloc[-1]
    return ((last / average - 1) * 100).round(2)


table = pd.DataFrame({
    "group": tickers.set_index("ticker")["group"],
    "last": last.round(2),
    "1d %": ((last / px.iloc[-2] - 1) * 100).round(2),
    "5d %": ((last / px.iloc[-6] - 1) * 100).round(2),
    "vs 20d avg %": vs_average(20),
    "vs 50d avg %": vs_average(50),
    "vs 200d avg %": vs_average(200),
}).sort_values("1d %")

Path("data/_latest.md").write_text(
    f"Data through {px.index[-1].date()}\n\n" + table.to_markdown()
)
