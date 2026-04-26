# Rutina End-of-Day Review

## Qué hacer
1. Leer CLAUDE.md para contexto.
2. Verificar Alpaca paper trading.
3. **Ejecutar en orden**:
   - python scripts/get_portfolio_snapshot.py
   - python scripts/get_market_snapshot.py
   - python scripts/fetch_news_headlines.py
   - python scripts/build_daily_brief.py
   - python scripts/generate_daily_analysis.py
   - python scripts/detect_unusual_movements.py
4. Leer todos los archivos memory/ generados.
5. Generar **resumen ejecutivo de 8-12 líneas**:
   - estado final de cuenta vs. inicio del día
   - movimientos más notables de la watchlist
   - noticias clave del día
   - observaciones para pre-market de mañana
6. **NO ejecutar órdenes**.
7. Guardar resumen en memory/eod_summary.md.
8. Confirmar que todos los archivos se actualizaron.
