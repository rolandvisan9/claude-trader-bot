import os
from pathlib import Path
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta, timezone

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
NEWS_FILE = PROJECT_ROOT / "memory" / "news_headlines.md"


def read_watchlist():
    symbols = []
    for line in WATCHLIST_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        symbols.append(line.upper())
    return symbols


def get_recent_news(symbols):
    now = datetime.now(timezone.utc)
    end_date = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    start_date = (now - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")

    url = "https://data.alpaca.markets/v1beta1/news"
    params = {
        "symbols": ",".join(symbols),
        "start": start_date,
        "end": end_date,
        "limit": 20
    }

    response = requests.get(url, headers=HEADERS, params=params, timeout=30)
    response.raise_for_status()
    return response.json().get("news", [])


def build_news_report(news_items, symbols):
    lines = []
    lines.append("# News Headlines")
    lines.append("")
    lines.append(f"## Últimas noticias de {len(symbols)} símbolos (últimos 7 días)")
    lines.append("")

    if not news_items:
        lines.append("- No hay noticias recientes para la watchlist.")
        return "\n".join(lines)

    for item in news_items[:10]:
        # Alpaca devuelve "symbols" como lista, no "symbol"
        symbol_list = item.get("symbols", [])
        symbol_str = ", ".join(symbol_list) if symbol_list else "N/A"
        headline = item.get("headline", "Sin título")
        created = item.get("created_at", "Sin fecha")
        summary = item.get("summary", "")

        lines.append(f"- **{symbol_str}** ({created}): {headline}")
        if summary:
            lines.append(f"  _{summary[:150]}..._")

    return "\n".join(lines)


def main():
    symbols = read_watchlist()
    news = get_recent_news(symbols)
    report = build_news_report(news, symbols)
    NEWS_FILE.write_text(report, encoding="utf-8")
    print(f"News report guardado en: {NEWS_FILE}")


if __name__ == "__main__":
    main()
