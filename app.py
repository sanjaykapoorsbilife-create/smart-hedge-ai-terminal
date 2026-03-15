def fetch_option_chain(symbol):

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br"
    }

    session = requests.Session()
    session.headers.update(headers)

    # first request to set cookies
    session.get("https://www.nseindia.com")

    if symbol == "NIFTY":
        url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    else:
        url = f"https://www.nseindia.com/api/option-chain-equities?symbol={symbol}"

    response = session.get(url)

    return response.json()["records"]["data"]
