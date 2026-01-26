"""Fetch BTC 15-minute up/down markets from Polymarket and Kalshi."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class Market:
    source: str
    identifier: str
    title: str
    volume: Optional[float]
    url: Optional[str]


def _read_json(url: str, headers: Optional[Dict[str, str]] = None) -> Any:
    request = Request(url, headers=headers or {})
    with urlopen(request, timeout=20) as response:  # nosec - trusted endpoints
        charset = response.headers.get_content_charset() or "utf-8"
        payload = response.read().decode(charset)
    return json.loads(payload)


def _coerce_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _extract_polymarket_markets(data: Any) -> Iterable[Dict[str, Any]]:
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("markets", "data", "result", "results"):
            if key in data and isinstance(data[key], list):
                return data[key]
    return []


def _extract_kalshi_markets(data: Any) -> Iterable[Dict[str, Any]]:
    if isinstance(data, dict) and isinstance(data.get("markets"), list):
        return data["markets"]
    if isinstance(data, list):
        return data
    return []


def _build_query(params: Dict[str, Any]) -> str:
    filtered = {key: value for key, value in params.items() if value is not None}
    return urlencode(filtered, doseq=True)


def fetch_polymarket_markets(
    base_url: str,
    search: str,
    limit: int,
    min_volume: Optional[float],
) -> List[Market]:
    query = _build_query(
        {
            "search": search,
            "limit": limit,
        }
    )
    url = f"{base_url}?{query}" if query else base_url
    data = _read_json(url)
    markets = []
    for entry in _extract_polymarket_markets(data):
        volume = _coerce_float(entry.get("volume"))
        if min_volume is not None and (volume is None or volume < min_volume):
            continue
        title = entry.get("question") or entry.get("title") or entry.get("name")
        identifier = str(entry.get("id") or entry.get("slug") or title)
        market_url = entry.get("url")
        markets.append(
            Market(
                source="Polymarket",
                identifier=identifier,
                title=title or "(untitled)",
                volume=volume,
                url=market_url,
            )
        )
    return markets


def fetch_kalshi_markets(
    base_url: str,
    search: str,
    limit: int,
    min_volume: Optional[float],
) -> List[Market]:
    query = _build_query(
        {
            "ticker": None,
            "event_ticker": None,
            "limit": limit,
            "search": search,
        }
    )
    url = f"{base_url}?{query}" if query else base_url
    data = _read_json(url)
    markets = []
    for entry in _extract_kalshi_markets(data):
        volume = _coerce_float(entry.get("volume") or entry.get("volume_24h"))
        if min_volume is not None and (volume is None or volume < min_volume):
            continue
        title = entry.get("title") or entry.get("subtitle") or entry.get("name")
        identifier = str(entry.get("ticker") or entry.get("id") or title)
        market_url = entry.get("url")
        if market_url is None and identifier:
            market_url = urljoin("https://kalshi.com/markets/", identifier)
        markets.append(
            Market(
                source="Kalshi",
                identifier=identifier,
                title=title or "(untitled)",
                volume=volume,
                url=market_url,
            )
        )
    return markets


def _format_market(market: Market) -> str:
    volume = f"{market.volume:.2f}" if market.volume is not None else "n/a"
    url = market.url or ""
    return f"- {market.title} (id: {market.identifier}, volume: {volume}) {url}".rstrip()


def run(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fetch BTC 15-minute up/down markets from Polymarket and Kalshi."
    )
    parser.add_argument(
        "--polymarket-url",
        default="https://gamma-api.polymarket.com/markets",
        help="Polymarket markets endpoint.",
    )
    parser.add_argument(
        "--kalshi-url",
        default="https://trading-api.kalshi.com/trade-api/v2/markets",
        help="Kalshi markets endpoint.",
    )
    parser.add_argument(
        "--search",
        default="BTC 15 minute",
        help="Search string applied to both APIs.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of markets per source.",
    )
    parser.add_argument(
        "--min-volume",
        type=float,
        default=None,
        help="Optional minimum volume filter.",
    )
    args = parser.parse_args(argv)

    polymarket = fetch_polymarket_markets(
        args.polymarket_url,
        args.search,
        args.limit,
        args.min_volume,
    )
    kalshi = fetch_kalshi_markets(
        args.kalshi_url,
        args.search,
        args.limit,
        args.min_volume,
    )

    print("Polymarket")
    if polymarket:
        for market in polymarket:
            print(_format_market(market))
    else:
        print("- No markets found.")

    print("\nKalshi")
    if kalshi:
        for market in kalshi:
            print(_format_market(market))
    else:
        print("- No markets found.")

    return 0


if __name__ == "__main__":
    sys.exit(run())
