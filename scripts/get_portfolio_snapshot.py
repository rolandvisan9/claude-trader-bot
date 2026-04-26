import os
from pathlib import Path
from dotenv import load_dotenv
import requests

load_dotenv()

BASE_URL = os.getenv("APCA_API_BASE_URL")
API_KEY = os.getenv("APCA_API_KEY_ID")
API_SECRET = os.getenv("APCA_API_SECRET_KEY")

if not BASE_URL or not API_KEY or not API_SECRET:
    raise ValueError("Faltan variables de entorno de Alpaca.")

HEADERS = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": API_SECRET
}

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WATCHLIST_FILE = PROJECT_ROOT / "config" / "symbols_watchlist.md"
OUTPUT_FILE = PROJECT_ROOT / "memory" / "portfolio_snapshot.md"


def read_watchlist():
    symbols = []
    for line in WATCHLIST_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        symbols.append(line.upper())
    return symbols


def get_account():
    response = requests.get(f"{BASE_URL}/account", headers=HEADERS, timeout=20)
    response.raise_for_status()
    return response.json()


def get_positions():
    response = requests.get(f"{BASE_URL}/positions", headers=HEADERS, timeout=20)
    if response.status_code == 404:
        return []
    response.raise_for_status()
    return response.json()


def build_snapshot(account, positions, watchlist):
    lines = []
    lines.append("# Portfolio Snapshot")
    lines.append("")
    lines.append("## Cuenta")
    lines.append(f"- Account status: {account.get('status')}")
    lines.append(f"- Equity: {account.get('equity')}")
    lines.append(f"- Cash: {account.get('cash')}")
    lines.append(f"- Buying power: {account.get('buying_power')}")
    lines.append(f"- Pattern day trader: {account.get('pattern_day_trader')}")
    lines.append("")
    lines.append("## Posiciones abiertas")

    if not positions:
        lines.append("- No hay posiciones abiertas.")
    else:
        for p in positions:
            lines.append(
                f"- {p.get('symbol')}: qty={p.get('qty')}, "
                f"market_value={p.get('market_value')}, "
                f"avg_entry_price={p.get('avg_entry_price')}, "
                f"unrealized_pl={p.get('unrealized_pl')}"
            )

    lines.append("")
    lines.append("## Watchlist")
    for symbol in watchlist:
        lines.append(f"- {symbol}")

    return "\n".join(lines)


def main():
    watchlist = read_watchlist()
    account = get_account()
    positions = get_positions()
    snapshot = build_snapshot(account, positions, watchlist)
    OUTPUT_FILE.write_text(snapshot, encoding="utf-8")
    print(f"Snapshot guardado en: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
