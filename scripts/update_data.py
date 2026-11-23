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


def trend_signal():
    """Rule-based trend label from the 50- and 200-day moving averages.

    Up:    close above the 50-day average AND 50-day above the 200-day
    Down:  close below the 50-day average AND 50-day below the 200-day
    Mixed: anything else
    This describes the current trend. It is not a forecast or a recommendation.
    """
    ma50 = px.rolling(50).mean().iloc[-1]
    ma200 = px.rolling(200).mean().iloc[-1]

    def label(ticker):
        if pd.isna(ma50[ticker]) or pd.isna(ma200[ticker]):
            return "n/a"
        if last[ticker] > ma50[ticker] > ma200[ticker]:
            return "Up"
        if last[ticker] < ma50[ticker] < ma200[ticker]:
            return "Down"
        return "Mixed"

    return pd.Series({ticker: label(ticker) for ticker in px.columns})


table = pd.DataFrame({
    "group": tickers.set_index("ticker")["group"],
    "last": last.round(2),
    "1d %": ((last / px.iloc[-2] - 1) * 100).round(2),
    "5d %": ((last / px.iloc[-6] - 1) * 100).round(2),
    "vs 20d avg %": vs_average(20),
    "vs 50d avg %": vs_average(50),
    "vs 200d avg %": vs_average(200),
    "trend": trend_signal(),
}).sort_values("1d %")

Path("data/_latest.md").write_text(
    f"Data through {px.index[-1].date()}\n\n" + table.to_markdown()
)


# ---- Group volatility chart -------------------------------------------------
# Annualized volatility of daily returns over the last 20 trading days,
# averaged across the tickers in each group. Macro series are excluded because
# a yield or an index level is not comparable with a tradable price.
groups = tickers.set_index("ticker")["group"]
returns = px.pct_change().tail(20)
ticker_vol = returns.std() * (252 ** 0.5) * 100
group_vol = (
    ticker_vol[groups[groups != "macro"].index]
    .groupby(groups)
    .mean()
    .dropna()
    .sort_values(ascending=False)
    .round(1)
)
group_vol.rename("annualized volatility %").to_csv("data/group_volatility.csv")

row_h, left, right, top = 34, 170, 70, 44
width = 720
height = top + row_h * len(group_vol) + 12
scale = (width - left - right) / group_vol.max()
svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
    f'style="width:100%;max-width:{width}px;font-family:inherit" role="img" '
    f'aria-label="Average annualized volatility by group, last 20 trading days">',
    f'<text x="0" y="18" font-size="15" font-weight="600" fill="#0b0b0b">'
    f'Volatility by group</text>',
    f'<text x="0" y="36" font-size="12" fill="#52514e">'
    f'Average annualized volatility of daily returns, last 20 trading days (%)</text>',
]
for i, (name, value) in enumerate(group_vol.items()):
    y = top + i * row_h + 6
    bar = max(value * scale, 2)
    svg.append(
        f'<text x="{left - 10}" y="{y + 15}" font-size="13" text-anchor="end" '
        f'fill="#0b0b0b">{name}</text>'
    )
    svg.append(
        f'<rect x="{left}" y="{y}" width="{bar:.1f}" height="20" rx="4" fill="#2a78d6">'
        f'<title>{name}: {value:.1f}%</title></rect>'
    )
    svg.append(
        f'<text x="{left + bar + 8:.1f}" y="{y + 15}" font-size="13" '
        f'fill="#0b0b0b">{value:.1f}%</text>'
    )
svg.append("</svg>")

Path("data/_group_volatility.md").write_text(
    "```{=html}\n" + "\n".join(svg) + "\n```\n"
)
