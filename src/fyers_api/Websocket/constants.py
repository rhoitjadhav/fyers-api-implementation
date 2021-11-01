
from struct import Struct

# constants for API usage
WS_ORDERS_URL = "wss://api.fyers.in/socket/v2/orderSock?type=orderUpdate&access_token={access_token}&user-agent=fyers-api"
WS_DATA_URL = "wss://api.fyers.in/socket/v2/dataSock?access_token={access_token}"
QUOTES_URL = "https://api.fyers.in/data-rest/v2/quotes/"
CONTENT_TYPE = "application/json"

# constants for message conversions
FY_P_ENDIAN	= '> '
FY_P_HEADER_FORMAT = Struct(FY_P_ENDIAN + "Q L H H H 6x")
FY_P_COMMON_7208 = Struct(FY_P_ENDIAN + "10I Q")
FY_P_EXTRA_7208 = Struct(FY_P_ENDIAN + "4I 2Q")
FY_P_MARKET_PIC = Struct(FY_P_ENDIAN + "3I")
FY_P_LENGTH = Struct(FY_P_ENDIAN + "H")

# constants for packet length definitions
FY_P_LEN_NUM_PACKET = 2
FY_P_LEN_HEADER = 24
FY_P_LEN_COMN_PAYLOAD = 48 
FY_P_LEN_EXTRA_7208	= 32 
FY_P_LEN_BID_ASK = 12 
FY_P_BID_ASK_CNT = 10
FY_P_LEN_RES = 6 

# constants for keywords
KEY_ORDER_UPDATE = "orderUpdate"
KEY_DATA_UPDATE = "symbolData"
        
    

