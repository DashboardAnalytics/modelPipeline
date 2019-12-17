import pandas as pd
import os, csv
import shutil
from datetime import datetime, timedelta

def moveCSV(csvName, storeDir):
    finalDir = storeDir+csvName.split("/")[2]
    shutil.move(csvName, finalDir)
    return finalDir
def writeCSV(csvName, data):
    data.to_csv(csvName, sep=';', index=False, quoting=csv.QUOTE_NONE, quotechar='',escapechar='')
    return True

def open(csvName):
    data = pd.read_csv(csvName)
    return data

def addStoreId(data, idStore, idShopping, videoStart, videoNFrames, videoDate):
    nRow = data.shape[0]
    data['id_shopping'] = [idShopping]*nRow
    data['id_store'] = [idStore]*nRow
    data['frame_date'] = [videoDate]*nRow
    data['frame_time'] = float("NaN")
    seconds = 0
    stringTimeList = []

    for index, row in data.iterrows():
        frameTime = videoStart + timedelta(seconds = seconds)
        stringTime = str(frameTime.hour)+":"+str(frameTime.minute)+":"+str(frameTime.second)+"."+str(frameTime.microsecond)
        stringTimeList.append(stringTime)
        seconds = seconds + 1/videoNFrames
    data['frame_time'] = stringTimeList
    return data
def mainAlterCSV(csvName, idStore, idShopping, storeDir, videoStart, videoNFrames, videoDate):
    data = pd.read_csv(csvName, sep=';'  , engine='python')
    data = addStoreId(data, idStore, idShopping, videoStart, videoNFrames, videoDate)
    if(writeCSV(csvName, data)):
        print("Csv "+csvName+" altered!")
    finalDir = moveCSV(csvName, storeDir)
    return finalDir