import GetStocks
import CSV
import Candle
START = "2019-08-01"
END = "2019-11-01"

class Stock:
    def __init__(self, name):
        self.Name = name
        if CSV.CheckIfFileExist(name):
            self.dataFrame = CSV.Read(name)
        else:
            self.dataFrame = GetStocks.GetStock(name, start = START, end = END)
            CSV.Write(self.dataFrame, name)

    def PlotCandle(self):
        #self.PrintName()
        Candle.Plot(self.dataFrame, self.Name)

    def PrintName(self):
        print("Stock name is " + self.Name)

    def AnalysisLastDay(self):
        last = self.dataFrame.iloc[-1:]
        self.LastDifferenceHigh = float(last['HighMeasure3Days'] - last['High'])
        self.LastDifferenceLow = float(last['LowMeasure3Days'] - last['Low'])
        self.Resistance = max(self.dataFrame.iloc[-5:]['High'])
        self.Support = min(self.dataFrame.iloc[-5:]['Low'])
        self.LastHigh = float(self.dataFrame.iloc[-1:]['High'])
        self.LastLow = float(self.dataFrame.iloc[-1:]['Low'])
