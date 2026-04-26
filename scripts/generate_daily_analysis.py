from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BRIEF_FILE = PROJECT_ROOT / "memory" / "daily_brief.md"
OUTPUT_FILE = PROJECT_ROOT / "memory" / "daily_analysis.md"


def read_brief():
    if not BRIEF_FILE.exists():
        raise FileNotFoundError("No existe memory/daily_brief.md")
    return BRIEF_FILE.read_text(encoding="utf-8")


def extract_lines_with_prefix(text, prefix="- "):
    return [line.strip() for line in text.splitlines() if line.strip().startswith(prefix)]


def build_analysis(text):
    bullet_lines = extract_lines_with_prefix(text)

    market_open = None
    next_open = None
    next_close = None
    equity = None
    cash = None
    buying_power = None
    has_positions = None

    market_lines = []

    for line in bullet_lines:
        lower = line.lower()

        if "mercado abierto:" in lower:
            market_open = line.split(":", 1)[1].strip()
        elif "próxima apertura:" in lower:
            next_open = line.split(":", 1)[1].strip()
        elif "próximo cierre:" in lower:
            next_close = line.split(":", 1)[1].strip()
        elif "equity:" in lower:
            equity = line.split(":", 1)[1].strip()
        elif "cash:" in lower:
            cash = line.split(":", 1)[1].strip()
        elif "buying power:" in lower:
            buying_power = line.split(":", 1)[1].strip()
        elif "no hay posiciones abiertas" in lower:
            has_positions = False
        elif any(line.startswith(f"- {symbol}:") for symbol in [
            "AAPL", "MSFT", "NVDA", "SPY", "QQQ", "TSLA", "AMZN", "GOOGL", "META"
        ]):
            market_lines.append(line)

    if has_positions is None:
        has_positions = True

    if market_open == "True":
        market_status_text = "El mercado aparece abierto en Alpaca."
    elif market_open == "False":
        market_status_text = "El mercado aparece cerrado en Alpaca."
    else:
        market_status_text = "No se pudo determinar con claridad si el mercado está abierto."

    lines = []
    lines.append("# Daily Analysis")
    lines.append("")
    lines.append("## Resumen automático")
    lines.append(f"- {market_status_text}")

    if next_open:
        lines.append(f"- Próxima apertura detectada: {next_open}")
    if next_close:
        lines.append(f"- Próximo cierre detectado: {next_close}")
    if equity:
        lines.append(f"- Equity actual detectado: {equity}")
    if cash:
        lines.append(f"- Cash actual detectado: {cash}")
    if buying_power:
        lines.append(f"- Buying power detectado: {buying_power}")

    if has_positions:
        lines.append("- El sistema detecta que sí hay posiciones abiertas o no puede confirmarlo con total claridad.")
    else:
        lines.append("- El sistema detecta que no hay posiciones abiertas.")

    lines.append("")
    lines.append("## Lectura de la watchlist")
    if market_lines:
        lines.append(f"- Se han detectado datos recientes para {len(market_lines)} símbolos de la watchlist.")
        lines.append("- Los datos actuales son observacionales y no implican ninguna señal de trading.")
        lines.append("- Si los datos provienen de after-hours o fin de semana, el contexto de volumen puede ser poco representativo.")
    else:
        lines.append("- No se detectaron líneas de mercado utilizables en el daily brief.")

    lines.append("")
    lines.append("## Limitaciones actuales")
    lines.append("- El sistema todavía no genera señales de compra o venta.")
    lines.append("- El sistema no ejecuta órdenes.")
    lines.append("- El sistema no compara precios contra medias, momentum o noticias.")
    lines.append("- El análisis actual sirve como observación estructurada, no como decisión operativa.")

    return "\n".join(lines)


def main():
    text = read_brief()
    analysis = build_analysis(text)
    OUTPUT_FILE.write_text(analysis, encoding="utf-8")
    print(f"Daily analysis guardado en: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
