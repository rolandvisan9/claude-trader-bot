import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ANALYSIS_FILE = PROJECT_ROOT / "memory" / "smart_analysis.md"
OUTPUT_FILE = PROJECT_ROOT / "memory" / "unusual_movements.md"

UMBRAL_PORCENTAJE = 1.0


def parse_analysis():
    if not ANALYSIS_FILE.exists():
        return []

    content = ANALYSIS_FILE.read_text(encoding="utf-8")
    movements = []

    pattern = re.compile(r"\| (\w+) \| ([\d\.]+) \| ([+-][\d\.]+)% \| ([\d,]+) \| (\w+/?\w+) \|")

    for line in content.splitlines():
        match = pattern.search(line)
        if match:
            movements.append({
                "symbol": match.group(1),
                "close": float(match.group(2)),
                "change": float(match.group(3)),
                "volume": int(match.group(4).replace(",", "")),
                "state": match.group(5)
            })
    return movements


def build_unusual_report(movements):
    lines = []
    lines.append("# Unusual Market Movements")
    lines.append("")
    lines.append("## Alertas detectadas")

    alert_count = 0

    for m in movements:
        if abs(m["change"]) > UMBRAL_PORCENTAJE:
            alert_count += 1
            lines.append(f"- [ALERTA] {m['symbol']}: Movimiento de {m['change']:+.2f}%")
            lines.append(f"  - Cierre: {m['close']:.2f}")
            lines.append(f"  - Volumen: {m['volume']:,}")
            lines.append(f"  - Contexto: {m['state']}")

    if alert_count == 0:
        lines.append(f"- No se detectaron movimientos inusuales superiores al {UMBRAL_PORCENTAJE}% durante esta observación.")

    lines.append("")
    lines.append("## Nota de contexto")
    lines.append("- Estas alertas son solo observacionales.")
    lines.append("- Un movimiento inusual en after-hours puede deberse a muy poca liquidez.")
    lines.append("- Verifica siempre noticias corporativas o reportes de resultados antes de dar importancia a estos datos.")

    return "\n".join(lines)


def main():
    data = parse_analysis()
    report = build_unusual_report(data)
    OUTPUT_FILE.write_text(report, encoding="utf-8")
    print(f"Unusual movements report guardado en: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
