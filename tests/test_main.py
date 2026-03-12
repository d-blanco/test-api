"""Tests for the stock quote API."""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_home_page_returns_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Stock Quote Lookup" in response.text


def test_invalid_symbol_returns_400():
    response = client.get("/api/quote/TOOLONG")
    assert response.status_code == 400
    assert "Invalid ticker symbol" in response.json()["detail"]


def test_invalid_symbol_with_numbers_returns_400():
    response = client.get("/api/quote/AB1")
    assert response.status_code == 400


def _make_mock_fast_info(last_price, prev_close=150.0, open_price=151.0,
                         day_low=149.0, day_high=153.0, market_cap=2_500_000_000_000,
                         currency="USD"):
    info = MagicMock()
    info.last_price = last_price
    info.previous_close = prev_close
    info.open = open_price
    info.day_low = day_low
    info.day_high = day_high
    info.market_cap = market_cap
    info.currency = currency
    return info


@patch("main.yf.Ticker")
def test_valid_symbol_returns_quote(mock_ticker_cls):
    mock_ticker = MagicMock()
    mock_ticker.fast_info = _make_mock_fast_info(last_price=175.50)
    mock_ticker_cls.return_value = mock_ticker

    response = client.get("/api/quote/AAPL")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert data["price"] == 175.50
    assert data["currency"] == "USD"


@patch("main.yf.Ticker")
def test_unknown_symbol_returns_404(mock_ticker_cls):
    mock_ticker = MagicMock()
    mock_ticker.fast_info = _make_mock_fast_info(last_price=None)
    mock_ticker_cls.return_value = mock_ticker

    response = client.get("/api/quote/ZZZZZ")
    assert response.status_code == 404
    assert "No quote data found" in response.json()["detail"]


@patch("main.yf.Ticker")
def test_symbol_is_uppercased(mock_ticker_cls):
    mock_ticker = MagicMock()
    mock_ticker.fast_info = _make_mock_fast_info(last_price=100.0)
    mock_ticker_cls.return_value = mock_ticker

    response = client.get("/api/quote/msft")
    assert response.status_code == 200
    assert response.json()["symbol"] == "MSFT"
