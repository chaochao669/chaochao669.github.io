#!/home/chao/anaconda3/bin/python
#coding:utf-8
import os
import csv
import sys
import glob
import shutil
import requests
from requests.adapters import HTTPAdapter
from qcloud_vod.vod_upload_client import VodUploadClient
from qcloud_vod.model import VodUploadRequest

def getUrl(listfile):
	allurls = dict()
	with open(listfile,encoding="gbk") as f:
		readers = csv.reader(f)
		for line in readers:
			if line[0] == '文件ID':
				continue
			print(line[0],line[1],line[9])
			allurls[line[1]]=line[9]
	return allurls 

	#print index,row['文件ID'],row['文件名称']

#workdir="/home/chao/BaiduNetdiskDownload/phone/converted"
#uploadAllMedia(workdir)

listfile="all.csv"
allurls=getUrl(listfile)
print(allurls["VID_20190518_094659_640"])
#downWithList(listfile)
