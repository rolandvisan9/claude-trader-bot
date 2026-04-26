import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT_FILE = PROJECT_ROOT / "memory" / "market_snapshot.md"
OUTPUT_FILE = PROJECT_ROOT / "memory" / "smart_analysis.md"


def parse_snapshot():
    if not SNAPSHOT_FILE.exists():
        return []

    content = SNAPSHOT_FILE.read_text(encoding="utf-8")
    symbols_data = []

    pattern = re.compile(
        r"- (\w+): open=([\d\.]+), high=([\d\.]+), low=([\d\.]+), close=([\d\.]+), volume=([\d\.]+)"
    )

    for line in content.splitlines():
        match = pattern.search(line)
        if match:
            symbols_data.append({
                "symbol": match.group(1),
                "open": float(match.group(2)),
                "close": float(match.group(5)),
                "volume": float(match.group(6))
            })
    return symbols_data


def build_smart_analysis(symbols_data):
    lines = []
    lines.append("# Smart Market Analysis")
    lines.append("")
    lines.append("## Análisis de Watchlist")

    if not symbols_data:
        lines.append("- No hay datos de mercado procesables.")
        return "\n".join(lines)

    lines.append("| Símbolo | Cierre | Variación % | Volumen | Estado |")
    lines.append("|---|---|---|---|---|")

    for s in symbols_data:
        change = ((s["close"] - s["open"]) / s["open"]) * 100
        vol_desc = "Bajo" if s["volume"] < 1000 else "Normal/Alto"
        lines.append(
            f"| {s['symbol']} | {s['close']:.2f} | {change:+.2f}% | {int(s['volume']):,} | {vol_desc} |"
        )

    lines.append("")
    lines.append("## Contexto operativo")
    lines.append("- Este análisis calcula la variación intra-barra basándose en los datos de la última sesión disponible.")
    lines.append("- Un volumen 'Bajo' puede indicar actividad en after-hours o pre-market; ten cuidado con la liquidez.")
    lines.append("- Este informe es observacional: no hay ninguna lógica de trading aplicada todavía.")

    return "\n".join(lines)


def main():
    data = parse_snapshot()
    analysis = build_smart_analysis(data)
    OUTPUT_FILE.write_text(analysis, encoding="utf-8")
    print(f"Smart analysis guardado en: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
