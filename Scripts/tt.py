#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import requests
import codecs
import json
from geoserver.catalog import Catalog
if __name__ == "__main__":
    source_path = "C:\\Users\\zhaoyun\\PycharmProjects\\untitled1\\python\\Scripts\\source\\"  # 新创建的txt文件的存放路径
    targe_path="C:\\Users\\zhaoyun\\PycharmProjects\\untitled1\\python\\Scripts\\test\\"
    geoserverurl="http://192.168.1.153:2056"
    newfilename=""
    files = os.listdir(source_path)
    dict = {'Lm_Mas_Gs_DXT01.DBO.%行政区_1_9': 'p_administrative',
            'Lm_Mas_Gs_DXT01.DBO.%邮电通讯_8': 'p_communication',
            'Lm_Mas_Gs_DXT01.DBO.%P_Judiciary': 'p_judiciary',
            'Lm_Mas_Gs_DXT01.DBO.%地形图_公园': 'p_park',
            'Lm_Mas_Gs_DXT01.DBO.%地形图_学校': 'p_school',
            'Lm_Mas_Gs_DXT01.DBO.%地形图_医院': 'p_hospital',
            'Lm_Mas_Gs_DXT01.DBO.%地形图_交通枢纽': 'p_traffichinge',
            'Lm_Mas_Gs_DXT01.DBO.%地形图_楼栋名称': 'p_buildingname',
            'Lm_Mas_Gs_DXT01.DBO.%地形图_党政机构': 'p_politicalparty',
            'Lm_Mas_Gs_DXT01.DBO.%地形图_居民小区': 'p_residential',
            'Lm_Mas_Gs_DXT01.DBO.%地形图_铁路_7': 'l_railway',
            'Lm_Mas_Gs_DXT01.DBO.%地形图_省道': 'py_provincialhighway',
            'Lm_Mas_Gs_DXT01.DBO.%地形图_国道': 'py_nationalhighway',
            'Lm_Mas_Gs_DXT01.DBO.%地形图_高速_1': 'py_highway',
            'Lm_Mas_Gs_DXT01.DBO.%地形图_县道_6': 'py_countyhighway',
            'Lm_Mas_Gs_DXT01.DBO.%地形图_房屋_5': 'py_building',
            'Lm_Mas_Gs_DXT01.DBO.%地形图_主干道': 'py_arterialroad',
            'Lm_Mas_Gs_DXT01.DBO.%地形图_次干道_4': 'py_collectorstreets',
            'Lm_Mas_Gs_DXT01.DBO.%地形图_山水_山_2': 'py_mountain',
            'Lm_Mas_Gs_DXT01.DBO.PY_WaterSystem': 'py_watersystem',
            '山水_水系':'py_watersystem',
            }
    for singerfile in files:
        # hasnewname=False
        # indexstart=singerfile.find("_")+1
        # indexend=len(singerfile)-4
        # filecnname=singerfile[indexstart:indexend]
        # for key in dict.keys():
        #     if key.__contains__(filecnname):
        #         hasnewname=True
        #         newfilename=dict[key]+".sld"
        #         file = open(targe_path+singerfile, 'w',encoding='UTF-8')
        #         break
        file = open(targe_path + singerfile, 'w', encoding='UTF-8')
        # if hasnewname:

        with open(source_path + singerfile, 'r', encoding='UTF-8') as f:

            for line in f.readlines():
                newline=line
                # for key in dict.keys():
                #     if line.__contains__(key):
                #         a = False
                #         newline = line.replace(key, dict[key])
                #         file.write(newline)
                #         continue
                if line.__contains__("TEXT_"):
                    newline = line.replace("TEXT_", "text_")
                if line.__contains__("UNAME"):
                    newline = line.replace("UNAME", "uname")
                if line.__contains__("Class"):
                    newline = line.replace("Class", "class")
                if line.__contains__("Label"):
                    newline = line.replace("Label", "label")
                if line.__contains__("微软雅黑"):
                    newline = line.replace("微软雅黑", "Microsoft YaHei")
                if line.__contains__("STName"):
                    newline = line.replace("STName", "stname")
                else:
                    if line.__contains__("NAME"):
                        newline = line.replace("NAME", "name")
                file.write(newline)

        print(singerfile + " finished!!")
        # else:
        #     print(filecnname + "not exist!!!")

    files = os.listdir(targe_path)
    print("Start upload Style")
    for singerfile in files:
        endindex = len(singerfile) - 4
        if singerfile[endindex:] != ".sld":
            continue
        # 新样式名称
        layername = singerfile[:endindex]
        # 样式地址
        mysld_address = targe_path + singerfile
        # k=open(mysld_address,'r',encoding='UTF-8')
        # payload = k.read().encode()
        # if payload[:3]==codecs.BOM_UTF8:
        #     payload=payload[3:]
        # # 上传样式
        # os.system(
        #     'curl -u admin:geoserver1 -X POST -H "Content-type: application/zip" --data-binary @' + mysld_address + ' http://192.168.2.34:2006/geoserver/rest/styles')
        # 创建样式
        myUrl = '%s/geoserver/rest/styles?name=%s&raw=true' % (geoserverurl,layername)
        file = open(mysld_address, 'r', encoding='UTF-8')
        # print(layername)
        payload = file.read().encode()
        if payload[:3] == codecs.BOM_UTF8:
            payload = payload[3:]

        headers = {'Content-type': 'application/vnd.ogc.sld+xml'}

        resp = requests.post(myUrl, auth=('admin', 'geoserver1'), data=payload, headers=headers)

        layerurl = '%s/geoserver/rest/layers/%s' % (geoserverurl,layername)
        layerheaders = {'Content-type': 'application/json'}
        jsonstr = {'layer': {'defaultStyle': {'name': layername}}}
        layerpayload = json.dumps(jsonstr)
        layerresp = requests.put(layerurl, auth=('admin', 'geoserver1'), data=layerpayload,
                                 headers=layerheaders)

print("finished all!!")


