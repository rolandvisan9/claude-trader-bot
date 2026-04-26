# claude-trader-bot

Bot de trading asistido por Claude Code. Fase inicial: solo paper trading con Alpaca.

## Requisitos
- Python 3.10+
- Cuenta en Alpaca (paper trading)
- Claude Code instalado

## Setup
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install python-dotenv requests
```

Edita `.env` con tus claves de Alpaca paper.

## Primer test
```powershell
python .\scripts\test_alpaca_connection.py
```

## Estado
Fase 1: conexión y lectura de cuenta. Sin órdenes reales.
