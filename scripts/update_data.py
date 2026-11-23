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
    f"Data through {px.index[-1].date()}\n\n" + table.to_markdown(floatfmt=".2f")
)


# ---- Group charts ------------------------------------------------------------
# Macro series are excluded from group charts because a yield or an index
# level is not comparable with a tradable price.
groups = tickers.set_index("ticker")["group"]
tradable = groups[groups != "macro"].index

BLUE, ORANGE, INK, MUTED, AXIS = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#c9c8c2"


def bar_chart(values, title, subtitle, path):
    """Write a horizontal bar chart as inline SVG. Handles negative values."""
    row_h, top, width = 34, 48, 720
    low, high = min(values.min(), 0), max(values.max(), 0)
    # plot area; leave room for value labels left of negative bars
    x0, x1 = (235 if low < 0 else 175), width - 65
    span = (high - low) or 1
    zero = x0 + (0 - low) / span * (x1 - x0)
    height = top + row_h * len(values) + 10
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'style="width:100%;max-width:{width}px;font-family:inherit" role="img" '
        f'aria-label="{title}. {subtitle}">',
        f'<text x="0" y="18" font-size="15" font-weight="600" fill="{INK}">{title}</text>',
        f'<text x="0" y="37" font-size="12" fill="{MUTED}">{subtitle}</text>',
    ]
    for i, (name, value) in enumerate(values.items()):
        y = top + i * row_h + 5
        length = max(abs(value) / span * (x1 - x0), 2)
        x = zero if value >= 0 else zero - length
        color = BLUE if value >= 0 else ORANGE
        sign = "+" if value > 0 and low < 0 else ""
        svg.append(
            f'<text x="160" y="{y + 15}" font-size="13" text-anchor="end" '
            f'fill="{INK}">{name}</text>'
        )
        svg.append(
            f'<rect x="{x:.1f}" y="{y}" width="{length:.1f}" height="20" rx="4" '
            f'fill="{color}"><title>{name}: {sign}{value:.1f}%</title></rect>'
        )
        if value >= 0:
            svg.append(
                f'<text x="{zero + length + 7:.1f}" y="{y + 15}" font-size="13" '
                f'fill="{INK}">{sign}{value:.1f}%</text>'
            )
        else:
            svg.append(
                f'<text x="{zero - length - 7:.1f}" y="{y + 15}" font-size="13" '
                f'text-anchor="end" fill="{INK}">{value:.1f}%</text>'
            )
    svg.append(
        f'<line x1="{zero:.1f}" y1="{top}" x2="{zero:.1f}" y2="{height - 6}" '
        f'stroke="{AXIS}" stroke-width="1"/>'
    )
    svg.append("</svg>")
    Path(path).write_text("```{=html}\n" + "\n".join(svg) + "\n```\n")


# 1) Five-day return by group: average close-to-close return of the members
ticker_ret = (last / px.iloc[-6] - 1) * 100
group_ret = (
    ticker_ret[tradable].groupby(groups).mean().dropna()
    .sort_values(ascending=False).round(1)
)
bar_chart(
    group_ret,
    "Five-day return by group",
    "Average close-to-close return of the tickers in each group (%)",
    "data/_group_returns.md",
)

# 2) Volatility by group: annualized, from daily returns over 20 trading days
ticker_vol = px.pct_change().tail(20).std() * (252 ** 0.5) * 100
group_vol = (
    ticker_vol[tradable].groupby(groups).mean().dropna()
    .sort_values(ascending=False).round(1)
)
bar_chart(
    group_vol,
    "Volatility by group",
    "Average annualized volatility of daily returns, last 20 trading days (%)",
    "data/_group_volatility.md",
)

pd.DataFrame({
    "5d return %": group_ret,
    "annualized volatility %": group_vol,
}).to_csv("data/group_summary.csv")
