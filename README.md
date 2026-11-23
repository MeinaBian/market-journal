# Market Journal

A daily, timestamped research journal on how macroeconomic, policy, and
company-level shocks transmit into asset prices.

**Live site:** https://meinabian.github.io/market-journal/

## Contents

1. Purpose
2. Organizing principle
3. Factor map
4. Transmission map
5. The policy-maker's view
6. Entry structure
7. Quantitative layer
8. Simulated portfolio
9. Universe
10. Data and methodology
11. Implementation
12. Status

## 1. Purpose

Most market commentary explains a move after it happens. This project does the
opposite: each entry states a mechanism, commits a probabilistic prediction
before the outcome is known, and is scored afterwards. The aim is to build
calibrated, mechanism-level judgment about markets, the kind a research
analyst needs before a model and a portfolio manager needs after one.

It is a self-directed training project, paired with a simulated portfolio
(Section 8) so that each view is tested with a position. It makes no claim of
investment performance.

## 2. Organizing principle

Every price is a discounted claim on future cash flows:

$$P_0 = \sum_{t=1}^{\infty} \frac{\mathbb{E}[CF_t]}{(1 + r_t + \rho_t)^t}$$

where $r_t$ is the risk-free rate and $\rho_t$ is the risk premium. Any event
can move a price through only four channels, and each entry must say which:

| Channel | What changes | Typical drivers |
|---|---|---|
| **Cash flows** | Expected revenue, margins, earnings | Growth, demand, costs, regulation, competition |
| **Risk-free rate** | Real rate, expected inflation, term premium | Central bank policy, inflation data, Treasury supply |
| **Risk premium** | Compensation demanded for uncertainty | Volatility, credit stress, governance, geopolitics |
| **Flows and positioning** | Who must buy or sell, regardless of value | Leverage, hedging, index and systematic flows |

A narrative that cannot be assigned to a channel is not yet an explanation.

## 3. Factor map

The factors monitored, grouped by the block of the economy they belong to.

### 3.1 Monetary policy and the rate complex
- Policy rate and its expected path (futures-implied)
- 2-year yield (policy expectations) and 10-year yield (growth, inflation, term premium)
- Real yields and breakeven inflation, which split a nominal move into its two parts
- Yield curve slope (2s10s)
- Central bank balance sheet and reserve levels

### 3.2 Inflation
- Consumer and producer prices, core and headline
- The Federal Reserve's preferred measure (core PCE)
- Wage growth and inflation expectations

### 3.3 Growth and labor
- Payrolls, unemployment, jobless claims
- Purchasing manager surveys, retail sales, industrial production
- Corporate earnings revisions as the market's own growth signal

### 3.4 Credit and financial conditions
- Investment-grade and high-yield spreads
- Bank lending standards and funding-market spreads
- Broad financial conditions: the combined effect of rates, credit, equities, and the dollar

### 3.5 Fiscal policy and liquidity
- Deficits and Treasury issuance, including auction results
- Government cash balance and money-market liquidity

### 3.6 Dollar and global linkages
- Dollar index and major currency pairs
- Policy divergence among the major central banks
- China's growth and credit cycle

### 3.7 Commodities and geopolitics
- Crude oil, natural gas, copper, gold
- Conflict, sanctions, and shipping disruptions, classified as supply or demand shocks

### 3.8 Policy and regulation
- Export controls and technology restrictions
- Tariffs, antitrust, and tax changes

### 3.9 Equity-market internals
- Earnings, guidance, and margins
- Valuation: forward multiples and the equity risk premium
- Style factors: value, momentum, quality, size, low volatility
- Sector rotation and market breadth

### 3.10 Volatility and positioning
- Implied volatility level, term structure, and skew
- Systematic and leveraged positioning, short interest, buybacks, fund flows

### 3.11 Company-specific risk
- Leadership and governance events
- Legal, regulatory, and accounting matters

## 4. Transmission map

Working hypotheses, each to be tested and revised in the journal.

| Shock | Primary channel | First-order expectation | What would falsify it |
|---|---|---|---|
| Yields rise on **higher real rates** | Risk-free rate | Long-duration growth underperforms; banks relatively better | Growth stocks lead on the day with no offsetting earnings news |
| Yields rise on **stronger growth** | Cash flows and rate, offsetting | Cyclicals and financials outperform; index can rise with yields | Cyclicals lag defensives |
| Yields rise on **inflation surprise** | Rate and risk premium | Stocks and bonds fall together; real assets hold up | Stock-bond correlation stays negative |
| Credit spreads widen | Risk premium | Small caps and leveraged balance sheets underperform | High-yield equity proxies outperform |
| Dollar strengthens | Cash flows | Multinationals and commodities under pressure | Exporters outperform domestic names |
| Oil rises on **supply shock** | Cash flows and inflation | Energy up; transports and consumers down; yields up | Energy fails to outperform |
| Oil rises on **demand** | Cash flows | Broad cyclical strength alongside energy | Cyclicals fall while oil rises |
| Export restriction on a technology | Cash flows and risk premium | Affected names reprice on lost revenue plus policy uncertainty | No reaction beyond the directly exposed revenue share |
| Abrupt leadership change | Risk premium | Governance and key-person discount; higher implied volatility | Volatility and discount fade within days without new information |
| Volatility spike | Flows and positioning | Forced de-risking amplifies the initial move | Selling stops without a volatility decline |

Three rules sit behind the table:

1. **Markets price surprises, not levels.** The relevant quantity is the outcome relative to what was already expected.
2. **Ask why a variable moved before asking what it does.** A yield increase driven by growth and one driven by inflation have opposite implications for equities.
3. **Relationships are regime-dependent.** The stock-bond correlation, for example, changes sign with the inflation regime, so every entry is tagged with the prevailing regime.

## 5. The policy-maker's view

Central bank analysis here follows the reaction function, not the headline:

- Data change the expected policy path; the path moves the front of the curve; the curve and risk appetite together set financial conditions; financial conditions act on the real economy with long and variable lags.
- Rate policy and balance-sheet policy are tracked separately, because they work through different channels.
- Fiscal policy is treated as part of the same system: issuance and deficits influence the term premium and can tighten or loosen conditions independently of the central bank.
- The question asked of each policy event is what it reveals about how the institution will respond to future data, since that is what the market reprices.

## 6. Entry structure

1. **Observation:** what moved, by how much, relative to the benchmark.
2. **Channel and mechanism:** which of the four channels, and the causal chain one link at a time.
3. **Regime tag:** inflation, growth, and volatility conditions at the time.
4. **Prediction:** a falsifiable call with a horizon and a probability.
5. **Scoring:** filled in when the horizon ends, recording which link held or broke.

Every entry is committed to version control, so each prediction carries a
timestamp that precedes its outcome.

## 7. Quantitative layer

| Component | Method | Status |
|---|---|---|
| Daily monitor | 1-day and 5-day moves and distance from 20-, 50- and 200-day moving averages across the watchlist | Live |
| Factor sensitivities | Rolling regressions of each ticker on changes in yields, the dollar, oil, credit spreads, and volatility | Planned |
| Event studies | Abnormal returns against a market model around dated events | Planned |
| Forecast scoring | Hit rate, Brier score, and calibration curve | Planned |
| Simulated portfolio | $10,000 paper portfolio with trade log, risk limits, and performance attribution (Section 8) | Planned |

## 8. Simulated portfolio

The journal is paired with a $10,000 simulated (paper) portfolio, so that every
view carries a position, a size, and a measurable consequence. No real capital
is involved.

**Rules fixed before the first trade**

- Starting notional of $10,000; benchmark is the S&P 500 (SPY).
- Every trade is recorded in `trades.csv` and linked to the journal entry that motivated it.
- Fills are taken at the next session's close after the decision, which rules out look-ahead; a 5 basis point cost is charged per trade.
- Risk limits: no leverage, and no single position above 10% of the portfolio at entry.
- Exits are triggered by the invalidation condition written in the entry, not by price alone.

**Two sleeves, compared against the benchmark**

| Sleeve | Logic |
|---|---|
| Discretionary | Positions that express the journal's predictions, sized by stated conviction |
| Systematic | Rule-based strategies on the watchlist, such as momentum and volatility-targeted trend, each specified in writing before it is run |

**Measurement**

- Net asset value and return against the benchmark
- Annualized volatility, Sharpe ratio, and maximum drawdown
- Beta and alpha from a market-model regression; tracking error and information ratio
- Hit rate, payoff ratio, and turnover
- Attribution by sleeve and by the four channels in Section 2

**Statistical honesty.** Three months of daily returns cannot separate skill
from luck: the standard error of an annualized Sharpe ratio over one quarter is
roughly 2. Results are therefore reported with confidence intervals, and the
project is judged on process: whether rules were followed, risks were sized
sensibly, and mistakes were diagnosed correctly.

## 9. Universe

Tickers are chosen for what they are sensitive to, so each macro shock has a
clean test case: rate-sensitive names, long-duration growth, commodity-linked,
defensives, a market benchmark, and macro series. The watchlist is being built
out to about 30 names; the current list is in `tickers.csv`.

## 10. Data and methodology

**Source.** Dashboard prices come from Yahoo Finance and are downloaded by
script with the open-source `yfinance` package. Nothing is entered by hand.

**Pipeline.** Each run of `scripts/update_data.py`:

1. Reads the watchlist from `tickers.csv`.
2. Downloads the last year of daily closing prices for each ticker.
3. Saves them to `data/prices.csv`.
4. Calculates the return and moving-average columns and writes the Dashboard table.

**Return definition.** Returns are close to close, not open to close, so they
include the overnight move, which is often where news is priced in.

| Column | Calculation |
|---|---|
| 1d % | Latest close compared with the previous trading day's close |
| 5d % | Latest close compared with the close five trading days earlier |
| vs 20d / 50d / 200d avg % | Distance of the latest close from its 20-, 50- and 200-day moving average |

Moving averages are used as trend context in the Observation, not as an
explanation in the Mechanism.

**Adjusted closes.** Prices are adjusted for stock splits and dividends, so
returns stay accurate across those events. Older prices in the file can
therefore differ slightly from what a chart showed on the day.

**Limitations.** Yahoo Finance is a free, unofficial source. Data can
occasionally be delayed, revised, or temporarily unavailable. It is suitable
for a learning project; professional research would use a paid, audited
source such as Bloomberg.

**Figures cited in entries.** Numbers for instruments outside the watchlist,
and macro series such as Treasury yields, are taken from published price
histories and from Federal Reserve and Treasury data, and are identified in
the entry.

## 11. Implementation

- `scripts/update_data.py` downloads prices with Python (yfinance, pandas) and builds the daily table.
- Entries are plain-text files in `entries/`.
- Quarto renders the site, published with GitHub Pages.

## 12. Status

Started November 2026. Intended run: three months of daily entries and
simulated trading, followed by a written review covering forecast accuracy,
portfolio results with confidence intervals, and the mechanisms that were
revised along the way.

## Disclaimer

This is a personal learning project. Nothing here is investment advice.
