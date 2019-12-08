import yfinance as yf

def GetStock(name, start, end):
    dataFrame = yf.download(name, start=start, end=end, prepost=True)
    AccumulatedValue(dataFrame)
    return dataFrame

def AccumulatedValue(dataFrame):
    dataFrame['HighMeasure3Days'] = (dataFrame.High.rolling(window=3).mean())
    dataFrame['HighMeasure5Days'] = (dataFrame.High.rolling(window=5).mean())
    dataFrame['HighMeasure10Days'] = dataFrame.High.rolling(window=10).mean()
    dataFrame['HighMeasure15Days'] = dataFrame.High.rolling(window=15).mean()
    dataFrame['LowMeasure3Days'] = (dataFrame.Low.rolling(window=3).mean())
    dataFrame['LowMeasure5Days'] = (dataFrame.Low.rolling(window=5).mean())
    dataFrame['LowMeasure10Days'] = dataFrame.Low.rolling(window=10).mean()
    dataFrame['LowMeasure15Days'] = dataFrame.Low.rolling(window=15).mean()
    dataFrame['Buy'] = [0]*len(dataFrame)
    dataFrame['Sell'] = [0]*len(dataFrame)
    dataFrame['High1'] = dataFrame['High'].shift(1)
    dataFrame['High2'] = dataFrame['High'].shift(2)
    dataFrame['High3'] = dataFrame['High'].shift(3)
    dataFrame['High4'] = dataFrame['High'].shift(4)
    dataFrame['Low1'] = dataFrame['Low'].shift(1)
    dataFrame['Low2'] = dataFrame['Low'].shift(2)
    dataFrame['Low3'] = dataFrame['Low'].shift(3)
    dataFrame['Low4'] = dataFrame['Low'].shift(4)
    return dataFrame
