# Stock Quote API

A FastAPI application with a web UI for looking up real-time stock quotes.

## Quick Start

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open <http://localhost:8000> in your browser.

## API

| Method | Endpoint               | Description                        |
|--------|------------------------|------------------------------------|
| GET    | `/`                    | Web UI for stock quote lookup      |
| GET    | `/api/quote/{symbol}`  | Returns JSON quote for a ticker    |

### Example

```
GET /api/quote/AAPL
```

```json
{
  "symbol": "AAPL",
  "price": 175.50,
  "previous_close": 174.00,
  "open": 174.50,
  "day_low": 173.80,
  "day_high": 176.20,
  "market_cap": 2500000000000,
  "currency": "USD"
}
```

## Tests

```bash
pytest tests/ -v
```