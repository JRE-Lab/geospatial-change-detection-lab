# BTC 15-minute Up/Down Market Fetcher (Polymarket + Kalshi)

This guide explains how to run the BTC 15-minute up/down market fetcher that queries **Polymarket** and **Kalshi**, then prints results in separate sections so you can compare both sources with the same parameters.

## Prerequisites

- **Python 3.9+**
- Network access to:
  - `https://gamma-api.polymarket.com/markets`
  - `https://trading-api.kalshi.com/trade-api/v2/markets`

## Install

No additional dependencies are required. The tool uses only Python's standard library.

## Run

From the repository root:

```bash
python tools/market_updown_15min.py
```

### Common parameters

- `--search` (default: `"BTC 15 minute"`)
- `--limit` (default: `50`)
- `--min-volume` (optional)
- `--polymarket-url` (optional override)
- `--kalshi-url` (optional override)

Example:

```bash
python tools/market_updown_15min.py \
  --search "BTC 15 minute" \
  --limit 25 \
  --min-volume 100
```

## Output

The tool prints **two separated sections** for easy comparison:

```
Polymarket
- <market line>

Kalshi
- <market line>
```

Each market line includes the title, identifier, volume (if present), and a URL when available.

## Tests

Run the unit tests with:

```bash
python -m unittest discover -v -s tests
```
