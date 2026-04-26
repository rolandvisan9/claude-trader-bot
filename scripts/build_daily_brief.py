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
PORTFOLIO_FILE = PROJECT_ROOT / "memory" / "portfolio_snapshot.md"
MARKET_FILE = PROJECT_ROOT / "memory" / "market_snapshot.md"
NEWS_FILE = PROJECT_ROOT / "memory" / "news_headlines.md"
OUTPUT_FILE = PROJECT_ROOT / "memory" / "daily_brief.md"


def get_clock():
    response = requests.get(f"{BASE_URL}/clock", headers=HEADERS, timeout=20)
    response.raise_for_status()
    return response.json()


def read_file(path):
    if not path.exists():
        return f"_No existe el archivo: {path.name}_"
    return path.read_text(encoding="utf-8")


def build_brief():
    clock = get_clock()
    portfolio_text = read_file(PORTFOLIO_FILE)
    market_text = read_file(MARKET_FILE)
    news_text = read_file(NEWS_FILE)

    lines = []
    lines.append("# Daily Brief")
    lines.append("")
    lines.append("## Estado del mercado")
    lines.append(f"- Timestamp Alpaca: {clock.get('timestamp')}")
    lines.append(f"- Mercado abierto: {clock.get('is_open')}")
    lines.append(f"- Próxima apertura: {clock.get('next_open')}")
    lines.append(f"- Próximo cierre: {clock.get('next_close')}")
    lines.append("")
    lines.append("## Resumen de cartera")
    lines.append(portfolio_text)
    lines.append("")
    lines.append("## Resumen de mercado")
    lines.append(market_text)
    lines.append("")
    lines.append("## Noticias recientes")
    lines.append(news_text)

    return "\n".join(lines)


def main():
    brief = build_brief()
    OUTPUT_FILE.write_text(brief, encoding="utf-8")
    print(f"Daily brief guardado en: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
