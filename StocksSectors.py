import csv
import operator
import xml.etree.ElementTree as gfg  

class StockSectors:
    def __init__(self,Code,CompanyName,Sector,SubSector,segment):
        self.Code = Code
        self.CompanyName = CompanyName
        self.Sector = Sector
        self.Segment = segment
        self.SubSector = SubSector

def RemoveLastNumber(word):
    listOfWord = list(word)
    listOfWord.reverse()
    listOfNumber=[]
    for char in listOfWord:
        if char.isdigit():
            listOfNumber.append(char)
        else:
            break
    for Number in listOfNumber:
        listOfWord.remove(Number)
    listOfWord.reverse()
    return ''.join(listOfWord)

StocksSectors=[]
def ReadSectors():
    with open('Setorial.csv', newline='',encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        # print(spamreader)
        segment =""
        for row in spamreader:
            if(len(row)>3):
                if(row[3]==''):
                    segment=row[2]
                elif(row[2]=='SEGMENTO'):
                    continue
                else:
                    StocksSectors.append(StockSectors(row[3],row[2],row[0],row[1],segment))


def FindStockSector(code):
    for currentStockSectors in StocksSectors :
        if currentStockSectors.Code == code:
            return currentStockSectors


def CreatingXML():
    StocksMyName = ['ABEV3','BBAS3','CYRE3','BBDC4','GGBR4','PETR4','VALE3','LIGT3','VVAR3','WEGE3','IRBR3']
    StocksDani = ['ITSA4','JBSS3','CCRO3','LREN3','MYPK3','UNIP6','ALPA4','BBSE3','RAPT4','POMO4','TIET11','TAEE11','B3SA3','CASH3','SAPR11']
    StocksISE ={'ABCB4','ALSO3','BRSR6','BBRK3','BRML3','BRPR3','BBDC4','BRAP4','BRKM5','CMIG4','CESP6','HGTX3','CIEL3','COCE5','CGAS5','CSMG3','CPLE6','CSAN3','CPFE3','CARD3','CYRE3','DTEX3','ECOR3','ELET6','ELPL3','EMBR3','ENBR3','EQTL3','YDUQ3','ETER3','EUCA4','EVEN3','EZTC3','FHER3','FESA4','FIBR3','FLRY3','GFSA3','GGBR4','GOAU4','GOLL4','GRND3','GUAR3','HYPE3','PDTC3','IGTA3','ROMI3','MYPK3','ITSA4','ITUB4','JBSS3','JHSF3','KEPL3','KLBN11','COGN3','LIGT3','RENT3','LOGN3','LAME4','LREN3','LPSB3','MDIA3','MAGG3','POMO4','MRFG3','BEEF3','MRVE3','MULT3','MPLU3','NTCO3','ODPV3','PCAR3','PMAM3','PETR4','PSSA3','RAPT4','RSID3','SBSP3','SANB11','STBP3','SMTO3','SLED4','CSNA3','SLCE3','SULA11','SUZB3','TCSA3','TGMA3','TIMS3','TOTS3','TRPL4','UGPA3','USIM5','VALE3','WEGE3'}
    StockDVI = {'CYRE3','BBSE3','BRDT3','CSNA3','ITSA4','QUAL3','MRVE3','VIVT4','SMLS3','ITUB4','TAEE11','BRML3','SANB11','CCRO3','CMIG4','BBDC4','BRAP4','CIEL3','KLBN11','FLRY3','BBAS3','BPAC11','EGIE3','ELET6','B3SA3','HYPE3','PETR4','TIP3','IRBR3'}

    AllStocks = StockDVI.union(StocksISE).union(StocksDani).union(StocksMyName)
    AllStocks = list(AllStocks)
    AllStocks.sort() 

    root = gfg.Element("Stocks") 
    for stock in AllStocks:
        result = FindStockSector(RemoveLastNumber(stock))
        if result is None:
            continue
        else:
            m1 = gfg.Element("Stock") 
            root.append (m1) 
            
            b1 = gfg.SubElement(m1, "Code") 
            b1.text = stock.strip()
            b2 = gfg.SubElement(m1, "CompanyName") 
            b2.text = result.CompanyName.strip()
            b3 = gfg.SubElement(m1, "Sector") 
            b3.text = result.Sector.strip()
            b4 = gfg.SubElement(m1, "Sub-sector") 
            b4.text = result.SubSector.strip()
            b5 = gfg.SubElement(m1, "Segment") 
            b5.text = result.Segment.strip()
            b6 = gfg.SubElement(m1, "risk") 
            b6.text = " "

    from xml.dom import minidom

    xmlstr = minidom.parseString(gfg.tostring(root)).toprettyxml(indent="")
    with open("Stocks.xml", "w",encoding='utf-8') as f:
        f.write(xmlstr)
ReadSectors()
CreatingXML()
AllStockSectors = {}
def GetStockSector(Code):
    if not AllStockSectors:
        tree = gfg.parse('Stocks.xml')
        root = tree.getroot()
        for client in root.findall('Stock'):
            code = client.find('Code').text.replace("\"","")
            companyName = client.find('CompanyName').text
            sector = client.find('Sector').text
            subsector = client.find('Sub-sector').text.replace("\"","")
            segment = client.find('Segment').text.replace("\"","")
            AllStockSectors.update({code:StockSectors(code,companyName,sector,subsector,segment)})

    if Code in AllStockSectors:
        return AllStockSectors[Code]
    else:
        result = FindStockSector(''.join([i for i in Code if not i.isdigit()]))
        AllStockSectors.update({Code:result})
        return result
