import json
import unittest
from io import StringIO
from unittest.mock import patch

from tools.market_updown_15min import (
    Market,
    fetch_kalshi_markets,
    fetch_polymarket_markets,
    run,
)


class FakeHeaders:
    def get_content_charset(self):
        return "utf-8"


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload
        self.headers = FakeHeaders()

    def read(self):
        return json.dumps(self.payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class MarketFetchTests(unittest.TestCase):
    def test_fetch_polymarket_markets(self):
        payload = [
            {"id": "1", "question": "BTC up?", "volume": "123.4", "url": "x"},
            {"id": "2", "question": "BTC down?", "volume": "1.0", "url": "y"},
        ]

        with patch("tools.market_updown_15min.urlopen", return_value=FakeResponse(payload)):
            markets = fetch_polymarket_markets("https://example.com", "btc", 10, 10)

        self.assertEqual(len(markets), 1)
        self.assertEqual(markets[0].identifier, "1")
        self.assertEqual(markets[0].title, "BTC up?")

    def test_fetch_kalshi_markets(self):
        payload = {
            "markets": [
                {"ticker": "BTCUP", "title": "BTC up", "volume": 42},
                {"ticker": "BTCDN", "title": "BTC down", "volume": 1},
            ]
        }

        with patch("tools.market_updown_15min.urlopen", return_value=FakeResponse(payload)):
            markets = fetch_kalshi_markets("https://example.com", "btc", 10, 10)

        self.assertEqual(len(markets), 1)
        self.assertEqual(markets[0].identifier, "BTCUP")
        self.assertEqual(markets[0].title, "BTC up")

    def test_run_outputs(self):
        polymarket_payload = [{"id": "1", "question": "BTC up?", "volume": "0"}]
        kalshi_payload = {"markets": []}

        with patch(
            "tools.market_updown_15min.urlopen",
            side_effect=[FakeResponse(polymarket_payload), FakeResponse(kalshi_payload)],
        ):
            with patch("sys.stdout", new_callable=StringIO) as fake_out:
                run(["--search", "btc", "--limit", "1"])
                output = fake_out.getvalue()

        self.assertIn("Polymarket", output)
        self.assertIn("Kalshi", output)


if __name__ == "__main__":
    unittest.main()
