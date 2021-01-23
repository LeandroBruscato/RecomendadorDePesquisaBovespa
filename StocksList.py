from Stock import *
from Email import *
from prettytable import PrettyTable
import xml.etree.ElementTree as ET
import operator
from datetime import date



StocksMyName = ['ABEV3','BBAS3','CYRE3','BBDC4','GGBR4','PETR4','VALE3','LIGT3','VVAR3','WEGE3','IRBR3']
StocksIBOV = ['EMBR3','CRFB3','RAIL3','CYRE3','NTCO3','YDUQ3','ABEV3','ENEV3','BPAC11','BEEF3','GOLL4','BTOW3','EZTC3','FLRY3','MRVE3','AZUL4','WEGE3','HGTX3','MGLU3','CVCB3','B3SA3','TAEE11','LCAM3','CIEL3','TOTS3','PCAR3','CSAN3','HYPE3','JHSF3','IRBR3','RENT3','ELET3','ENBR3','MRFG3','RADL3','JBSS3','ELET6','CCRO3','IGTA3','LAME4','BRML3','KLBN11','LREN3','MULT3','SANB11','BBAS3','BRDT3','ITSA4','BBSE3','COGN3','CPFE3','EGIE3','CSNA3','SBSP3','VVAR3','ENGI11','ITUB4','SULA11','ECOR3','QUAL3','BBDC3','BRKM5','EQTL3']
StocksDani = ['ITSA4','JBSS3','CCRO3','LREN3','MYPK3','UNIP6','ALPA4','BBSE3','RAPT4','POMO4','TIET11','TAEE11','B3SA3','CASH3','SAPR11']
StocksISE ={'ABCB4','ALSO3','BRSR6','BBRK3','BRML3','BRPR3','BBDC4','BRAP4','BRKM5','CMIG4','CESP6','HGTX3','CIEL3','COCE5','CGAS5','CSMG3','CPLE6','CSAN3','CPFE3','CARD3','CYRE3','DTEX3','ECOR3','ELET6','EMBR3','ENBR3','EQTL3','YDUQ3','ETER3','EUCA4','EVEN3','EZTC3','FHER3','FESA4','FLRY3','GFSA3','GGBR4','GOAU4','GOLL4','GRND3','GUAR3','HYPE3','PDTC3','IGTA3','ROMI3','MYPK3','ITSA4','ITUB4','JBSS3','JHSF3','KEPL3','KLBN11','COGN3','LIGT3','RENT3','LOGN3','LAME4','LREN3','LPSB3','MDIA3','POMO4','MRFG3','BEEF3','MRVE3','MULT3','NTCO3','ODPV3','PCAR3','PMAM3','PETR4','PSSA3','RAPT4','RSID3','SBSP3','SANB11','STBP3','SMTO3','SLED4','CSNA3','SLCE3','SULA11','SUZB3','TCSA3','TGMA3','TIMS3','TOTS3','TRPL4','UGPA3','USIM5','VALE3','WEGE3'}#,'ELPL3','MAGG3','FIBR3','MPLU3'
StockDVI = {'CYRE3','BBSE3','BRDT3','CSNA3','ITSA4','QUAL3','MRVE3','VIVT4','SMLS3','ITUB4','TAEE11','BRML3','SANB11','CCRO3','CMIG4','BBDC4','BRAP4','CIEL3','KLBN11','FLRY3','BBAS3','BPAC11','EGIE3','ELET6','B3SA3','HYPE3','PETR4','IRBR3'}#,'TIP3'

AllStocks = StockDVI.intersection(StocksISE)

AllStocks = AllStocks.union(StocksMyName)
AllStocks = AllStocks.union(StocksDani)
AllStocks = AllStocks.union(StocksIBOV)
AllStocks = list(AllStocks)
AllStocks.sort()
print(AllStocks)

SaleStocks = []
BuyStocks = []
Stocks = []
for stockName in AllStocks:
    s = Stock(stockName)
    s.GetIndices()
    s.GetProfitPower()
    Stocks.append(s)

    #print(type(s.GetStochasticAnalyze()))
    StochasticAnalyze = s.GetStochasticAnalyze()

    if(StochasticAnalyze == Stock.AnalyzeStatusSale):
         SaleStocks.append(s)
    if(StochasticAnalyze == Stock.AnalyzeStatusBuy):
         BuyStocks.append(s)
Stocks.sort(key=operator.attrgetter('Indicador'))

tabSotocks = PrettyTable()
tabSotocksAnalyze = PrettyTable()
tabSotocks.field_names = ["Name", "Indicador", "Valor", "Graham", "Valor Alvo","Max 1y", "Min 1y","Max 15d", "Min 15d", "PL", "PVP", "EV EBITDA", "Dividend Yield"]
tabSotocksAnalyze.field_names = ["Name", "Stochastic", "RSI", "OBV", "Momentum","MACD"]
for stock in Stocks:

    tabSotocks.add_row([stock.Name, str(format(stock.Indicador,".3f")),str(format(stock.LastClose,".2f")),str(format(stock.ValorIntrínsecoGraham,".3f")),str(format(stock.TargetEst1Y,".2f")),str(format(stock.PV_Max360,".2f")),str(format(stock.PV_Min360,".2f")),str(format(stock.PV_Max15,".2f")),str(format(stock.PV_Min15,".2f")),str(format(stock.PL,"2.3f")),str(format(stock.PVP,".3f")),str(format(stock.EV_EBITDA,".3f")),str(format(stock.DividendYield*100,".1f"))+"%"])
    tabSotocksAnalyze.add_row([stock.Name, str(stock.StochasticAnalyze),str(stock.RSIAnalyze),str(stock.OBVAnalyze),str(stock.MomentumAnalyze),str(stock.MACDAnalyze)])

tableIndicador = tabSotocks.get_html_string(format=True)
tableAnalyze = tabSotocksAnalyze.get_html_string(format=True)
# 
tableAnalyze = tableAnalyze.replace("Compra","<font color=\"Lime\">Saida</font>")
tableAnalyze = tableAnalyze.replace("Venda","<font color=\"Red\">Entrada</font>")

emailBody = open("EmailTemplate.html", "r").read()
emailBody = emailBody.replace("#TABLE_INDICADOR", tableIndicador)
emailBody = emailBody.replace("#TABLE_ANALYZE", tableAnalyze)
# dd/mm/YY
currentDay = date.today().strftime("%d/%m/%Y")
emailBody = emailBody.replace("#DAY",str(currentDay))

SaleText = ""
if(any(SaleStocks)):
    SaleText = SaleText + "<p> Ações pra vender<br>"
    SaleText = SaleText + "<ul>"
    for saleStock in SaleStocks:
        SaleText = SaleText + "<li>"+ str(saleStock.Name)+"</li>"

    SaleText = SaleText + "</ul>"
    SaleText = SaleText + "</p>"

emailBody = emailBody.replace("#SALE", SaleText)

BuyText = ""
if(any(BuyStocks)):
    BuyText = BuyText + "<p> Ações pra comprar <br>"
    BuyText = BuyText + "<ul>"
    for buyStock in BuyStocks:
        BuyText = BuyText + "<li>"+ str(buyStock.Name)+" - "+ buyStock.Sector + "</li>"

    BuyText = BuyText + "</ul>"
    BuyText = BuyText + "</p>"

emailBody = emailBody.replace("#BUY", BuyText)



# with open('Stock.html','w') as file:
#     file.write(emailBody)
# import xml.etree.ElementTree as ET
# tree = ET.parse('Clients.xml')
# root = tree.getroot()
# for client in root.findall('Client'):
#     name = client.find('Name').text.replace("\"","")
#     emailTO = client.find('Email').text
#     py_mail("Indicadores da Bovespa - "+str(currentDay), emailBody.replace("#NAME",name), emailTO)
