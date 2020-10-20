#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import requests
import codecs
import json
# git clone git@github.com:quadratic-be/gsconfig-py3.git
# cd gsconfig-py3
# python setup.py install
from geoserver.catalog import Catalog
if __name__ == "__main__":
    source_path = ""  # 新创建的txt文件的存放路径 C:\\Users\\zhaoyun\\PycharmProjects\\untitled1\\python\\Scripts\\source\\
    geoserverurl=""#http://192.168.1.73:2024
    user=""
    pw=""
    targeworkspace=""
    configfile = open("config.txt", 'r', encoding='UTF-8')
    #图层顺序表
    layersorder = open("layers.txt", 'r', encoding='UTF-8')
    layersconfig=[]
    for layer in layersorder.readlines():
        if layer.startswith("#"):
            continue
        layer=layer.replace("\n","")
        layersconfig.append(layer)
    int=0
    layernames=[]
    for congfigline in configfile.readlines():
        if congfigline.startswith("#"):
            continue
        if int==0:
            source_path=congfigline.replace("\n","")
        if int==1:
            geoserverurl=congfigline.replace("\n","")
        if int==2:
            user=congfigline.replace("\n","")
        if int==3:
            pw=congfigline.replace("\n","")
        if int==4:
            targeworkspace=congfigline.replace("\n","")
        int = int + 1

    files = os.listdir(source_path)
    print("Start upload Style")
    for singerfile in files:
        endindex = len(singerfile) - 4
        if singerfile[endindex:] != ".sld":
            continue
        # 新样式名称
        layername = singerfile[:endindex]
        layernames.append(layername)
        # 样式地址
        mysld_address = source_path + singerfile
        # k=open(mysld_address,'r',encoding='UTF-8')
        # payload = k.read().encode()
        # if payload[:3]==codecs.BOM_UTF8:
        #     payload=payload[3:]
        # # 上传样式
        # os.system(
        #     'curl -u admin:geoserver1 -X POST -H "Content-type: application/zip" --data-binary @' + mysld_address + ' http://192.168.2.34:2006/geoserver/rest/styles')
        # 创建样式
        myUrl = '%s/geoserver/rest/styles?name=%s&raw=true' % (geoserverurl, layername)
        file = open(mysld_address, 'r', encoding='UTF-8')
        # print(layername)
        payload = file.read().encode()
        if payload[:3] == codecs.BOM_UTF8:
            payload = payload[3:]

        headers = {'Content-type': 'application/vnd.ogc.sld+xml'}

        resp = requests.post(myUrl, auth=('admin', 'geoserver1'), data=payload, headers=headers)

        layerurl = '%s/geoserver/rest/layers/%s' % (geoserverurl, layername)
        layerheaders = {'Content-type': 'application/json'}
        jsonstr = {'layer': {'defaultStyle': {'name': layername}}}
        layerpayload = json.dumps(jsonstr)
        layerresp = requests.put(layerurl, auth=(user, pw), data=layerpayload,
                                 headers=layerheaders)
        # pubilsh grouplayers
    geourl = "%s/geoserver/rest/" % (geoserverurl)  # the url of geoserver
    geocat = Catalog(geourl,user,pw)  # create a Catalog object
    workspace = geocat.get_workspace(targeworkspace)  # workspace name
    layers = geocat.get_layers()
    lys = []
    for layer in layersconfig:
        size= len(targeworkspace)+1
        isingeoserver=False
        if(layernames.__contains__(layer)):
            for geoserverlyr in layers:
                if geoserverlyr.name[size:]==layer:
                    isingeoserver=True
                    lys.append(targeworkspace +":"+layer)
                    break
        else:
            print(layer+" not in slds!!")
        if not isingeoserver:
            print(layer + " not in geoserver!!")
    layersgroup = geocat.create_layergroup(targeworkspace, lys, lys, None, workspace.name)
    geocat.save(layersgroup, content_type="application/xml")

print("finished all!!")