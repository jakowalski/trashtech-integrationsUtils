from ftplib import FTP, all_errors
from Models.ContainerMap import ContainerMap
import json
from collections import namedtuple
from datetime import datetime
from TrashtechApi import TrashtechApi
from io import BytesIO
import base64
import time
import numpy as np
import cv2
from PIL import Image
import sys

class FtpCrawlerWorker:
    configFilePath = "./Resources/ContainerMapConfig.json"

    containerMaps = []
    ftpClient = None
    trashtechApi = None

    def Init(self):
        fileContent = ""
        with open(self.configFilePath, 'rb') as f:
            fileContent = f.read()

        containerMapsRaw = json.loads(fileContent, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

        for containerMapRaw in containerMapsRaw.ContainerMaps:
            self.containerMaps.append(ContainerMap(containerMapRaw.FtpDirectory,
                                                   containerMapRaw.ContainerIdentifierNumber,
                                                   containerMapRaw.ContainerReferenceCode,
                                                   containerMapRaw.ContainerFtpIdentifier))
        if len(self.containerMaps) == 0:
            print(
                "ERROR - ContainerMaps object not defined. Please verify file 'ContainerMapConfig.json' from Resources folder")
            return False

        self.trashtechApi = TrashtechApi()

        try:
            self.ftpClient = FTP('66.220.9.51')
            self.ftpClient.login('trashtechdevice', '!TrashtechDevice1234')
        except all_errors:
            print(
                "ERROR - Ftp client connection failed.")

            print(all_errors)
            return False
        return True

    def Crawl(self):
        print("Crawl started")

        files = self.ftpClient.nlst('/')

        for containerMap in self.containerMaps:
            print("Files from directory %s at time %s" % (containerMap.FtpDirectory, str(datetime.now())))

            sortedFileNamesWithoutArchived = self.GetSortedFileNamesSchemaForContainerMap(files, containerMap)

            for fileDateRaw in sortedFileNamesWithoutArchived:
                currentFileName = self.ComposeFileNameFromDatePart(fileDateRaw, containerMap)

                print(currentFileName)
                try:
                   respone = self.SendFileToApi(currentFileName, containerMap)
                   print('Response from api is %s' % str(respone))
                except:
                   print(sys.exc_info()[0])
                   print('Error send to api')

                self.ArchiveFile(containerMap.FtpDirectory + currentFileName,
                                 containerMap.FtpDirectory + 'ARCHIVED_' + currentFileName)
                print('Photo %s was archived' % str(currentFileName))

                time.sleep(15)

        self.ftpClient.close()

    def ArchiveFile(self, sourceFileName, destFileName):
        self.ftpClient.rename(sourceFileName, destFileName)

    def SendFileToApi(self, currentFileName, containerMap):
        bytesStream = BytesIO()
        self.ftpClient.retrbinary('RETR %s' % containerMap.FtpDirectory + currentFileName, bytesStream.write)

        image = Image.open(bytesStream)

        imageMat = np.asarray(image)
        imageRotated = cv2.rotate(imageMat, cv2.ROTATE_90_COUNTERCLOCKWISE)
        imageRotated = cv2.cvtColor(imageRotated, cv2.COLOR_RGB2BGR)

        retval, buffer = cv2.imencode('.jpg', imageRotated)

        encoded_image = base64.b64encode(buffer)

        response = self.trashtechApi.create_status(containerMap.ContainerReferenceCode,
                                                   encoded_image,
                                                   datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        return response

    def ComposeFileNameFromDatePart(self, fileDateRaw, containerMap):
        dateFromTheFileName = datetime.strptime(fileDateRaw, '%m/%d %H:%M')

        currentFileName = containerMap.ContainerFtpIdentifier + '_' + str(dateFromTheFileName.month).zfill(
            2) + '_' + str(dateFromTheFileName.day).zfill(
            2) + '_' + str(dateFromTheFileName.hour).zfill(
            2) + '_' + str(
            dateFromTheFileName.minute).zfill(
            2) + '.jpg'

        return currentFileName

    def GetSortedFileNamesSchemaForContainerMap(self, files, containerMap):
        containerFileNamesWithoutArchived = [fileName for fileName in files if ('ARCHIVED_' not in fileName and
                                                                                containerMap.ContainerFtpIdentifier in fileName)]

        fileNameDates = map(
            lambda x: x.split('_')[1] + '/' + x.split('_')[2] + ' ' + x.split('_')[3] + ':' + x.split('_')[4][:-4],
            containerFileNamesWithoutArchived)

        sortedFileNamesWithoutArchived = sorted(fileNameDates, key=lambda x: datetime.strptime(x, '%m/%d %H:%M'))

        return sortedFileNamesWithoutArchived


ftpCrawlerWorker = FtpCrawlerWorker()

while True:
    try:
        if ftpCrawlerWorker.Init():
            ftpCrawlerWorker.Crawl()
            time.sleep(600)
        else:
            print("FTP Client initialization failed")
    except all_errors:
        print(all_errors)
        time.sleep(60)
