import requests
import json
import base64
import datetime
from datetime import datetime
import time
import pytz
import os


class TrashtechApi:
    api_base = 'http://trashtech.herokuapp.com/api'

    def create_status(self, device_reference, complete_file_path, image_created_at):
        with open(complete_file_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read())

        request_json = {
            "device_status": {
                "image_created_at": image_created_at,
                "image_base": "data:image/jpg;base64,%s" % encoded_image.decode('utf-8'),
                "device_reference": device_reference,
                "container_identifier_number": device_reference,
            }
        }

        # logging.info("[INFO] request json: %s", request_json)
        url = "%s/device_statuses/" % (self.api_base)

        response = requests.post(url, json=request_json)
        json = response.json()
        print(json)
        return json


trashtechApi = TrashtechApi()


while True:

    dirName = './Resources/P3Tworzywo/'
    for filename in os.listdir(dirName):

        trashtechApi.create_status("000006", dirName + filename, datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        time.sleep(3600)
