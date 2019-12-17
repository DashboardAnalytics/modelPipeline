import os
import AlterCSV
import DBConnection
from datetime import datetime
import subprocess
#import DownloadBlobs

def createSubFolders(shoppingCenter, shop):
    shoppingCenterDir = "Results/"+shoppingCenter+"/"
    shopDir = shoppingCenterDir+shop+"/"
    if not (os.path.isdir(shoppingCenterDir)):
        os.mkdir(shoppingCenterDir)
    if not (os.path.isdir(shopDir)):
        os.mkdir(shopDir)
    return shopDir

def callModel(videoName):
    bashCommand = "pipenv run computer_vision video-label --nth_frame 1 "+videoName
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, cwd="../computer_vision/")
    output, error = process.communicate()
def parseVideoName():
   
    for file in os.listdir("Videos/"):
        if file.endswith(".avi"):
            videoName = os.path.join("../modelPipeline/Videos/", file)
            videoProperties = videoName.split("_")
            # OJOOO
            videoNFrames = 5
            shoppingCenter = videoProperties[2]
            store = videoProperties[3]
            videoDate = videoProperties[4]
            videoStart = videoProperties[5]
            videoStart = datetime.strptime(videoStart, '%H-%M-%S').time()
            videoStart = datetime.combine(datetime.today(), videoStart)
            # Creacion del nombre del directorio a guardar el csv
            storeDir = createSubFolders(shoppingCenter, store)
            # Modificacion de la ruta
            storeDir = "../modelPipeline/"+storeDir
            # Llamar modelo
            #callModel(videoName)
    
            # mover resultados a carpeta
            
            # Se obtienen las ids del shopping center y de la tienda
            shoppingID, shopID = DBConnection.GetIDS(shoppingCenter, store)

            for file in os.listdir("../computer_vision/"):
                if file.endswith(".csv"):
                    csvName = file
                    csvName = "../computer_vision/"+csvName
                    csvDir = AlterCSV.mainAlterCSV(csvName, shopID, shoppingID, storeDir, videoStart, videoNFrames, videoDate)
                    DBConnection.SendToDB(csvDir)
#DownloadBlobs.download()

parseVideoName()
