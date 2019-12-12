import os
import AlterCSV
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
            shop = videoProperties[3]
            videoDate = videoProperties[4]
            videoStart = videoProperties[5]
            videoStart = datetime.strptime(videoStart, '%H-%M-%S').time()
            videoStart = datetime.combine(datetime.today(), videoStart)
            shopDir = createSubFolders(shoppingCenter, shop)
            # Llamar modelo
            callModel(videoName)
            # mover resultados a carpeta
            for file in os.listdir("../modelPipeline"):
                if file.endswith(".csv"):
                    csvName = file
                    AlterCSV.mainAlterCSV(csvName, 1, 1, shopDir, videoStart, videoNFrames, videoDate)

#DownloadBlobs.download()
parseVideoName()
