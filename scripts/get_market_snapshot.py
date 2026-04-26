import os
from pathlib import Path
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("APCA_API_KEY_ID")
API_SECRET = os.getenv("APCA_API_SECRET_KEY")

if not API_KEY or not API_SECRET:
    raise ValueError("Faltan claves de Alpaca en .env")

HEADERS = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": API_SECRET
}

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WATCHLIST_FILE = PROJECT_ROOT / "config" / "symbols_watchlist.md"
OUTPUT_FILE = PROJECT_ROOT / "memory" / "market_snapshot.md"


def read_watchlist():
    symbols = []
    for line in WATCHLIST_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        symbols.append(line.upper())
    return symbols


def get_latest_bar(symbol):
    url = f"https://data.alpaca.markets/v2/stocks/{symbol}/bars/latest"
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()
    return response.json()


def build_snapshot(symbols):
    lines = []
    lines.append("# Market Snapshot")
    lines.append("")
    lines.append("## Watchlist market data")
    lines.append("")

    for symbol in symbols:
        try:
            data = get_latest_bar(symbol)
            bar = data.get("bar")

            if not bar:
                lines.append(f"- {symbol}: sin datos disponibles")
                continue

            lines.append(
                f"- {symbol}: "
                f"open={bar.get('o')}, "
                f"high={bar.get('h')}, "
                f"low={bar.get('l')}, "
                f"close={bar.get('c')}, "
                f"volume={bar.get('v')}, "
                f"timestamp={bar.get('t')}"
            )
        except Exception as e:
            lines.append(f"- {symbol}: error al obtener datos ({e})")

    return "\n".join(lines)


def main():
    symbols = read_watchlist()
    snapshot = build_snapshot(symbols)
    OUTPUT_FILE.write_text(snapshot, encoding="utf-8")
    print(f"Market snapshot guardado en: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
