class Config:
    Api = "https://api.fyers.in/api/v2"
    data_Api= "https://api.fyers.in/data-rest/v2"

    get_profile = '/profile'
    tradebook = '/tradebook'
    positions = '/positions'
    holdings = '/holdings'
    convertPosition = '/positions'
    funds = '/funds'
    orders = '/orders'
    minquantity = '/minquantity'
    orderStatus = '/order-status'
    marketStatus = '/market-status'
    auth = '/generate-authcode'
    generateAccessToken = '/validate-authcode'
    exitPositions = '/positions'
    generateDataToken = '/data-token'

    dataVendorTD = "truedata-ws"

    multi_orders = '/orders-multi'
    history = '/history/'
    quotes = '/quotes/'
    market_depth = '/depth/'