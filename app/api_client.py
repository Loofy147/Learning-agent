import httpx

async def get_btc_price_usd() -> float:
    """Fetches the current price of Bitcoin in USD from the CoinGecko API."""
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            price = data.get("bitcoin", {}).get("usd")
            if price is None:
                # Fallback or error handling if the price is not in the response
                raise ValueError("BTC price not found in CoinGecko API response")
            return float(price)
        except (httpx.RequestError, ValueError) as e:
            # In a real production app, you might have a more robust fallback,
            # like using a cached price or another API.
            # For now, we'll re-raise or handle it as a server error.
            print(f"Error fetching BTC price: {e}")
            # Fallback to a default price if the API fails, to prevent transactions from failing completely.
            # This could also be a configurable value.
            return 50000.0

def get_btc_price_usd_sync() -> float:
    """Fetches the current price of Bitcoin in USD from the CoinGecko API."""
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    with httpx.Client() as client:
        try:
            response = client.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            price = data.get("bitcoin", {}).get("usd")
            if price is None:
                # Fallback or error handling if the price is not in the response
                raise ValueError("BTC price not found in CoinGecko API response")
            return float(price)
        except (httpx.RequestError, ValueError) as e:
            # In a real production app, you might have a more robust fallback,
            # like using a cached price or another API.
            # For now, we'll re-raise or handle it as a server error.
            print(f"Error fetching BTC price: {e}")
            # Fallback to a default price if the API fails, to prevent transactions from failing completely.
            # This could also be a configurable value.
            return 50000.0
