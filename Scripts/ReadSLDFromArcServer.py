#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
class layers:
    def __init__(self):
     self.layers=[]
if __name__ == "__main__":
    ArcGisurl="http://192.168.1.66:6080/arcgis/rest/services/YingKou/Lm_YingKou_Gs_GWT/MapServer"
    Tojson="?f=pjson"
    resp=requests.post(ArcGisurl+Tojson)
    print(resp)
    mxd=json.loads(resp.text.encode(),object_hook=layers)
    print(mxd)

