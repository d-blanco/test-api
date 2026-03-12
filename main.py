"""FastAPI application for real-time stock quotes."""

import re
from pathlib import Path

import yfinance as yf
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Stock Quote API", version="1.0.0")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

SYMBOL_RE = re.compile(r"^[A-Z]{1,5}$")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the stock quote lookup page."""
    return templates.TemplateResponse(request, "index.html")


@app.get("/api/quote/{symbol}")
async def get_quote(symbol: str):
    """Return a real-time stock quote for the given ticker symbol."""
    symbol = symbol.upper().strip()

    if not SYMBOL_RE.match(symbol):
        raise HTTPException(
            status_code=400,
            detail="Invalid ticker symbol. Use 1-5 uppercase letters.",
        )

    ticker = yf.Ticker(symbol)
    info = ticker.fast_info

    try:
        last_price = info.last_price
    except Exception:
        last_price = None

    if last_price is None:
        raise HTTPException(
            status_code=404,
            detail=f"No quote data found for symbol '{symbol}'.",
        )

    return {
        "symbol": symbol,
        "price": round(last_price, 2),
        "previous_close": round(info.previous_close, 2) if info.previous_close else None,
        "open": round(info.open, 2) if info.open else None,
        "day_low": round(info.day_low, 2) if info.day_low else None,
        "day_high": round(info.day_high, 2) if info.day_high else None,
        "market_cap": info.market_cap if info.market_cap else None,
        "currency": info.currency if info.currency else "USD",
    }
