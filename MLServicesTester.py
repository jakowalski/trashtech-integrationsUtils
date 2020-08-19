import os
import requests
import base64
import json
import numpy as np
import cv2
from PIL import Image
import io

filePath = "D:\\Projects\\Trashtech\\FTP\\Raw\\"
extractElementsApiUrl = "http://18.191.246.132:5000/api/extractElements"
fillnessPredictionServiceApiUrl = "http://18.222.180.65/api/predictFillness"
newHeaders = {'Content-type': 'application/json', 'Accept': '*/*'}


for f in os.listdir(filePath):
    with open(filePath + 'Results.txt', "a") as result:
        with open(filePath + f, "rb") as fin:
            image = np.fromstring(fin.read(), np.uint8)
            imageDecoded = base64.encodestring(image).decode('utf-8')

            baseImageData = base64.b64decode(imageDecoded)

            imagePil = Image.open(io.BytesIO(baseImageData))
            imageMat = np.asarray(imagePil)
            print(imageMat.shape)

            resized_image = []
            if imageMat.shape == (768, 1024, 3):
                imageRotated = cv2.rotate(imageMat, cv2.ROTATE_90_COUNTERCLOCKWISE)

                resized_image = cv2.resize(imageRotated, (480, 640))
                print(resized_image.shape)
            else:
                resized_image = imageMat
            resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

            cv2.imwrite(filePath + "d1.jpg", resized_image)
            im_pil = Image.fromarray(resized_image)
            imgByteArr = io.BytesIO()
            im_pil.save(imgByteArr, format='jpeg')
            imgByteArr = imgByteArr.getvalue()


            base64_seg_map = base64.b64encode(imgByteArr).decode('utf-8')



            extractElementData = {'image': base64_seg_map}
            extractElementJson = json.dumps(extractElementData)

            extractElementResponse = requests.post(extractElementsApiUrl, data=extractElementJson, headers = newHeaders)

            fillnessPredictionData = {'semantic_segmentation_mask_image': extractElementResponse.content.decode('utf-8')}
            fillnessPredictionJson = json.dumps(fillnessPredictionData)

            fillnessPredictionServiceResponse = requests.post(fillnessPredictionServiceApiUrl, data=fillnessPredictionJson, headers = newHeaders)
            fileLine = "%s %s\n" % (f, fillnessPredictionServiceResponse.content.decode('utf-8'))

            print(fileLine)
            result.write(fileLine)