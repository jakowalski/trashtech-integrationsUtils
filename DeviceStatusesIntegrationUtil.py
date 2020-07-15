import requests
import json
import base64
import datetime
from datetime import datetime, timezone
import time


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

        return json


trashtechApi = TrashtechApi()

i = 1
imageIndex = 1


while(True):

    trashtechApi.create_status("000006", './Resources/P3Tworzywo/' + str(imageIndex) + '.jpg', str(datetime.now(timezone.utc)))

    time.sleep(3600)

    i = i + 1
    imageIndex = i

    if i > 9:
      imageIndex = 9

    if i > 11:
      i = 1
      imageIndex = 1

