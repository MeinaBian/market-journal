from pathlib import Path
import pandas as pd
import yfinance as yf

tickers = pd.read_csv("tickers.csv")
px = yf.download(tickers["ticker"].tolist(), period="3mo", auto_adjust=True)["Close"]
# keep only days when most tickers traded (drops weekend futures-only rows)
px = px.dropna(thresh=len(px.columns) // 2).ffill()
px.to_csv("data/prices.csv")

table = pd.DataFrame({
    "group": tickers.set_index("ticker")["group"],
    "last": px.iloc[-1].round(2),
    "1d %": ((px.iloc[-1] / px.iloc[-2] - 1) * 100).round(2),
    "5d %": ((px.iloc[-1] / px.iloc[-6] - 1) * 100).round(2),
}).sort_values("1d %")

Path("data/_latest.md").write_text(
    f"Data through {px.index[-1].date()}\n\n" + table.to_markdown()
)
