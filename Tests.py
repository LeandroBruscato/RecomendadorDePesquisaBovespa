import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta
from stockstats import StockDataFrame as Sdf
from mpl_finance import candlestick2_ochl
import matplotlib.pyplot as plt
# import time

# startTime = time.time()



# start = (datetime.today()+relativedelta(days=-5)).strftime('%Y-%m-%d')
# end = datetime.today().strftime('%Y-%m-%d')

# Raw = yf.download('IRBR3.SA', start=start, end=end,actions = True)
# endTime = time.time()
# print(endTime - startTime)

# startTime = time.time()

start = (datetime.today()+relativedelta(months=-12)).strftime('%Y-%m-%d')
end = datetime.today().strftime('%Y-%m-%d')

Raw = yf.download('IRBR3.SA', start=start, end=end,actions = True)
df = Raw[['Open', 'High', 'Low','Close', 'Adj Close', 'Volume']].copy()
mystock = Sdf.retype(df)
OBV = mystock['boll']

figure = plt.figure()
# Create subgraph
(axPrice, axOBV) = figure.subplots(2, sharex=True)
# Call the method, draw a candlestick chart in the axPrice sub-chart
candlestick2_ochl(ax = axPrice,
                opens=df["Open"].values, closes=df["Close"].values,
                highs=df["High"].values, lows=df["Low"].values,
                width=0.75, colorup='red', colordown='green')

#Draw OBV graphics in the axOBV subgraph
OBV.plot(ax=axOBV,color="blue",label='OBV')
plt.legend(loc='best') # Drawing legend
plt.rcParams['font.sans-serif']=['SimHei']
#Add a negative effect to the OBV subgraph
plt.rcParams['axes.unicode_minus'] = False
axOBV.set_ylabel("Unit: Ten Thousand Hands")
axOBV.set_title("OBV Indicator Chart") # Set the title of the sub-picture
axOBV.grid(linestyle='-.') # With grid lines
#Set the label and rotation angle of the x-axis coordinate
major_index=df.index[df.index%5==0]
major_xtics=df['Date'][df.index%5==0]
plt.xticks(major_index,major_xtics)
plt.setp(plt.gca().get_xticklabels(), rotation=30)
plt.show()


# endTime = time.time()
# print(endTime - startTime)


import yfinance as yf
import yahoo_fin.stock_info as si



# quote = si.get_holders("CVCB3.SA")
# quote = si.get_analysts_info("CVCB3.SA")
quote = si.get_analysts_info("CVCB3.SA")
print (quote)



# import requests
# import re
# import urllib.request
# import urllib.parse
# import http.cookiejar

# from lxml.html import fragment_fromstring
# from collections import OrderedDict


# url = 'http://www.fundamentus.com.br/resultado.php'
# cookie_jar = http.cookiejar.CookieJar()
# opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
# opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'),
#                     ('Accept', 'text/html, text/plain, text/css, text/sgml, */*;q=0.01')]

# # Aqui estão os parâmetros de busca das ações
# # Estão em branco para que retorne todas as disponíveis
# data = {'pl_min': '',
#         'pl_max': '',
#         'pvp_min': '',
#         'pvp_max' : '',
#         'psr_min': '',
#         'psr_max': '',
#         'divy_min': '',
#         'divy_max': '',
#         'pativos_min': '',
#         'pativos_max': '',
#         'pcapgiro_min': '',
#         'pcapgiro_max': '',
#         'pebit_min': '',
#         'pebit_max': '',
#         'fgrah_min': '',
#         'fgrah_max': '',
#         'firma_ebit_min': '',
#         'firma_ebit_max': '',
#         'margemebit_min': '',
#         'margemebit_max': '',
#         'margemliq_min': '',
#         'margemliq_max': '',
#         'liqcorr_min': '',
#         'liqcorr_max': '',
#         'roic_min': '',
#         'roic_max': '',
#         'roe_min': '',
#         'roe_max': '',
#         'liq_min': '',
#         'liq_max': '',
#         'patrim_min': '',
#         'patrim_max': '',
#         'divbruta_min': '',
#         'divbruta_max': '',
#         'tx_cresc_rec_min': '',
#         'tx_cresc_rec_max': '',
#         'setor': '',
#         'negociada': 'ON',
#         'ordem': '1',
#         'x': '28',
#         'y': '16',}

# with opener.open(url, urllib.parse.urlencode(data).encode('UTF-8')) as link:
#     content = link.read().decode('ISO-8859-1')

# pattern = re.compile('<div class="conteudo clearfix".*</div>', re.DOTALL)
# content = re.findall(pattern, content)[0]
# page = fragment_fromstring(content)
# result = OrderedDict()
# print(result)

# # html = requests.get('https://www.fundamentus.com.br/detalhes.php?papel=CTSA8')
# # content = html.text
# # print(content)
# # pattern = re.compile('<div class="conteudo clearfix".*</div>', re.DOTALL)
# # content = re.findall(pattern, content)
# # page = fragment_fromstring(content)
# # result = OrderedDict()
# # class="conteudo clearfix"

import numpy as np

data = [0.32,0.12,0.21,0.47,0.52,0.76,0.87,0.96]
conts = list()
for i in range(0,len(data)): 
    conts.append(i)

x = np.array(conts) # vetor com os valores de x
y = np.array(data) # vetor com os valores de y

p1 = np.polyfit(x,y,1) # fornece os valores do intercepto e a inclinação

yfit = p1[0] * x + p1[1] # calcula os valores preditos
yresid = y - yfit # resíduo = valor real - valor ajustado (valor predito)
SQresid = sum(pow(yresid,2)) # soma dos quadrados dos resíduos 
SQtotal = len(y) * np.var(y) # número de elementos do vetor y vezes a variância de y
R2 = 1 - SQresid/SQtotal # coeficiente de determinação

print(p1) # imprime o intercepto e a inclinação
print(R2) # imprime coeficiente de determinação

import matplotlib.pyplot as plt

plt.plot(x,y,'o')
plt.plot(x,np.polyval(p1,x),'g--')
plt.xlabel("x")
plt.ylabel("y")
plt.show()



from Stock import *
import pandas as pd
import matplotlib.pyplot as plt
from stockstats import StockDataFrame as Sdf
# https://github.com/jealous/stockstats/blob/master/stockstats.py

StocksMyName = ['ABEV3.SA','BBAS3.SA','CYRE3.SA','BBDC4.SA','GGBR4.SA','PETR4.SA','VALE3.SA','LIGT3.SA','VVAR3.SA','WEGE3.SA']
StocksDani = ['ITSA4.SA','JBSS3.SA','CCRO3.SA','LREN3.SA','MYPK3.SA','UNIP6.SA','ALPA4.SA','BBSE3.SA','RAPT4.SA','POMO4.SA','TIET11.SA','TAEE11.SA','B3SA3.SA','CASH3.SA','SAPR11.SA']
StocksISE ={'ABCB4.SA','ALSO3.SA','BRSR6.SA','BBRK3.SA','BRML3.SA','BRPR3.SA','BBDC4.SA','BRAP4.SA','BRKM5.SA','CMIG4.SA','CESP6.SA','HGTX3.SA','CIEL3.SA','COCE5.SA','CGAS5.SA','CSMG3.SA','CPLE6.SA','CSAN3.SA','CPFE3.SA','CARD3.SA','CYRE3.SA','DTEX3.SA','ECOR3.SA','ELET6.SA','ELPL3.SA','EMBR3.SA','ENBR3.SA','EQTL3.SA','YDUQ3.SA','ETER3.SA','EUCA4.SA','EVEN3.SA','EZTC3.SA','FHER3.SA','FESA4.SA','FIBR3.SA','FLRY3.SA','GFSA3.SA','GGBR4.SA','GOAU4.SA','GOLL4.SA','GRND3.SA','GUAR3.SA','HYPE3.SA','PDTC3.SA','IGTA3.SA','ROMI3.SA','MYPK3.SA','ITSA4.SA','ITUB4.SA','JBSS3.SA','JHSF3.SA','KEPL3.SA','KLBN11.SA','COGN3.SA','LIGT3.SA','RENT3.SA','LOGN3.SA','LAME4.SA','LREN3.SA','LPSB3.SA','MDIA3.SA','MAGG3.SA','POMO4.SA','MRFG3.SA','BEEF3.SA','MRVE3.SA','MULT3.SA','MPLU3.SA','NTCO3.SA','ODPV3.SA','PCAR3.SA','PMAM3.SA','PETR4.SA','PSSA3.SA','RAPT4.SA','RSID3.SA','SBSP3.SA','SANB11.SA','STBP3.SA','SMTO3.SA','SLED4.SA','CSNA3.SA','SLCE3.SA','SULA11.SA','SUZB3.SA','TCSA3.SA','TGMA3.SA','TIMS3.SA','TOTS3.SA','TRPL4.SA','UGPA3.SA','USIM5.SA','VALE3.SA','WEGE3.SA'}
StockDVI = {'CYRE3.SA','BBSE3.SA','BRDT3.SA','CSNA3.SA','ITSA4.SA','QUAL3.SA','MRVE3.SA','VIVT4.SA','SMLS3.SA','ITUB4.SA','TAEE11.SA','BRML3.SA','SANB11.SA','CCRO3.SA','BBDC3.SA','CMIG4.SA','BBDC4.SA','BRAP4.SA','CIEL3.SA','KLBN11.SA','FLRY3.SA','BBAS3.SA','BPAC11.SA','EGIE3.SA','ELET6.SA','B3SA3.SA','HYPE3.SA','PETR4.SA','TIP3.SA','IRBR3.SA'}

AllStocks = StockDVI.intersection(StocksISE)

AllStocks = AllStocks.union(StocksMyName)
AllStocks = AllStocks.union(StocksDani)

StocksMyName = ['B3SA3']

Stocks = []
for stockName in StocksMyName:
    s = Stock(stockName)
    s.GetIndices()
    s.GetProfitPower()
    Stocks.append(s)

for stock in Stocks:

    # if(stock.GetSaleCheck()):
    #     print("Sale")
    #     plt.figure()
    #     stock.kdjk.plot(color='blue',label='K')
    #     stock.kdjd.plot(color='red',label='D')
    #     plt.legend(loc='best')
    #     plt.setp(plt.gca().get_xticklabels(), rotation=30)

    #     plt.axhline(y=80 )
    #     plt.axhline(y=20 )
    #     plt.title('Sale - '+str(stock.Name))
    #     plt.show()
    
    # if(stock.GetBuyCheck()):
    #     print("Buy")
    #     plt.figure()
    #     stock.kdjk.plot(color='blue',label='K')
    #     stock.kdjd.plot(color='red',label='D')
    #     plt.legend(loc='best')
    #     plt.setp(plt.gca().get_xticklabels(), rotation=30)

    #     plt.axhline(y=80 )
    #     plt.axhline(y=20 )
    #     plt.title('Buy - '+str(stock.Name))
    #     plt.show()
    
    plt.figure()
    stock.RSI.plot()
    plt.legend(loc='best')
    plt.setp(plt.gca().get_xticklabels(), rotation=30)


    plt.show()