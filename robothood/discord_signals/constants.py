# pylint:disable=unused-variable
PAIR_KEYWORDS = ["pair"]
BUY_KEYWORDS = ["buy", "price"]
SELL_KEYWORDS = ["selling", "targets"]
STOP_KEYWORDS = ["stop", "price"]
SIGNAL_KEYWORDS = BUY_KEYWORDS + SELL_KEYWORDS + STOP_KEYWORDS
TARGET_REACH_KEYWORDS = ["target", "hit", "reached"]
REGEX_PATTERNS = {
    "quote_currency": {
        "pattern": r"PAIR: ([^/]+)(?:/BTC|/USDT|USDT|BTC)",
        "keywords": PAIR_KEYWORDS,
    },
    "buy_around": {"pattern": r"(\d+(?:\.\d+)?)", "keywords": BUY_KEYWORDS},
    "targets": {"pattern": r"(\d+(?:\.\d+)?)", "keywords": SELL_KEYWORDS},
    "stop_loss": {"pattern": r"(\d+(?:\.\d+)?)", "keywords": STOP_KEYWORDS},
}
