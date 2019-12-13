import pandas as pd
import os
import shutil
from datetime import datetime, timedelta

def moveCSV(csvName, shopDir):
    shutil.move(csvName, shopDir+csvName.split("/")[2])

def writeCSV(csvName, data):
    data.to_csv(csvName)
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
def mainAlterCSV(csvName, idStore, idShopping, shopDir, videoStart, videoNFrames, videoDate):
    data = open(csvName)
    data = addStoreId(data, idStore, idShopping, videoStart, videoNFrames, videoDate)
    if(writeCSV(csvName, data)):
        print("Csv "+csvName+" altered!")
    moveCSV(csvName, shopDir)
