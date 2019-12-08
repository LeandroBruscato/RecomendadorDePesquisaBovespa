import csv
import os
import pandas as pd

path = "Stocks/"
extention = ".csv"
def Write(dataFrame,name):
    print(name)
    dataFrame.to_csv(path + name + extention, header=True)  # Don't forget to add '.csv' at the end of the path

def Read(name):
    #print(pd.read_csv(path + name + extention, index_col=['Date'], parse_dates=['Date']))
    return pd.read_csv(path + name + extention)
    #with open("Stocks/"+name + ".csv") as csv_file:
    #    return csv.reader(csv_file, delimiter=',')

def CheckIfFileExist(name):
    return os.path.exists(path + name + extention)