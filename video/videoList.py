#!/home/chao/anaconda3/envs/test_py2/bin/python
#coding: utf-8
from PIL import Image
import os
import io
import csv
import json
from datetime import datetime
import time
from ImageProcess import Graphics
from pandas import Series,DataFrame
import pandas as pd
import sys



# 定义压缩比，数值越大，压缩越小
SIZE_normal = 1.0
SIZE_small = 1.5
SIZE_more_small = 2.0
SIZE_more_small_small = 3.0
SIZE_more_small_small_small = 4


def make_directory(directory):
    """创建目录"""
    os.makedirs(directory)

def directory_exists(directory):
    """判断目录是否存在"""
    if os.path.exists(directory):
        return True
    else:
        return False

def list_img_file(directory):
    """列出目录下所有文件，并筛选出图片文件列表返回"""
    old_list = os.listdir(directory)
    # print old_list
    new_list = []
    for filename in old_list:
        #print filename
        #name, fileformat = filename.split(".")
        fileformat=os.path.splitext(filename)[1] 
        #name, fileformat = filename.split(".")
        if fileformat.lower() == ".jpg" or fileformat.lower() == ".png" or fileformat.lower() == ".mp4" or fileformat.lower() == ".gif":
            new_list.append(filename)
    #print new_list
    return new_list


def print_help():
    print("""
    This program helps compress many image files
    you can choose which scale you want to compress your img(jpg/png/etc)
    1) normal compress(4M to 1M around)
    2) small compress(4M to 500K around)
    3) smaller compress(4M to 300K around)
    """)

def compress(choose, des_dir, src_dir, file_list):
    """压缩算法，img.thumbnail对图片进行压缩，
    
    参数
    -----------
    choose: str
            选择压缩的比例，有4个选项，越大压缩后的图片越小
    """
    if choose == '1':
        scale = SIZE_normal
    if choose == '2':
        scale = SIZE_small
    if choose == '3':
        scale = SIZE_more_small
    if choose == '4':
        scale = SIZE_more_small_small
    if choose == '5':
        scale = SIZE_more_small_small_small
    for infile in file_list:
        img = Image.open(src_dir+infile)
        # size_of_file = os.path.getsize(infile)
        w, h = img.size
        img.thumbnail((int(w/scale), int(h/scale)))
        print "compress:"+infile
        img.save(des_dir + infile)
def compress_photo():
    '''调用压缩图片的函数
    '''
    src_dir, des_dir = "cuted/", "min_photos/"
    
    if directory_exists(src_dir):
        if not directory_exists(src_dir):
            make_directory(src_dir)
        file_list_src = list_img_file(src_dir)
    if directory_exists(des_dir):
        if not directory_exists(des_dir):
            make_directory(des_dir)
        file_list_des = list_img_file(des_dir)
    '''如果已经压缩了，就不再压缩'''
    for i in range(len(file_list_des)):
        if file_list_des[i] in file_list_src:
            file_list_src.remove(file_list_des[i])
    compress('5', des_dir, src_dir, file_list_src)

def getMyJson():
	src_dir, des_dir = "photos/", "min_photos/"
	file_list = list_img_file(src_dir)
	list_info = []

	for i in range(len(file_list)):
		filename = file_list[i]
		img = Image.open(src_dir+filename)
		w, h = img.size
		new_dict = {"filename": filename, "width":w,"height":h } 
		list_info.append(new_dict)

	with open("init.json","w") as fp:
		json.dump(list_info, fp)
def handle_photo():
   #根据图片的文件名处理成需要的json格式的数据
   # 最后将data.json文件存到博客的source/photos文件夹下
    
	src_dir, des_dir =  "gif/","out/"
	file_list = list_img_file(src_dir)
	list_info = []
	fileList = []
	dateList = []

	listfile="all.csv"
	allurls=getUrl(listfile)#腾讯云点播的各个视频地址

	for i in range(len(file_list)):
		print  file_list
		filename = file_list[i]
		try:
			date_str = filename[4:19]
			print date_str 
			date = datetime.strptime(date_str, "%Y%m%d_%H%M%S")
			year_month= date.strftime( '%Y_%m' )
			fileList.append(filename)
			dateList.append(date)
		except:
			fileList.append(filename)
			dateList.append(time.strftime("%Y%m%d %H%M%S"))
	d={'file':fileList,'date':dateList}
	df=DataFrame(d)#按年月日排序
	i=0
	for index,row in df.sort_values(axis = 0,ascending = False,by ='date').iterrows():
		print index,row['date'],row['file']
		date =  row['date']
		year_month= date.strftime( '%Y_%m' )
		filename=row['file']

		img = Image.open(src_dir+filename)
		w, h = img.size
		imgsize= str(w)+"x"+str(h)

		portion = os.path.splitext(filename)
		newname = portion[0] + ".mp4"   

		fn = filename.split('.')
		basename = fn[0]#文件名
		postfix = fn[-1]#后缀名

		#new_dict = {"gif": "gif/"+filename, "mp4": allurls[basename] ,"width":str(w),"height":str(h),"time":date.strftime('%Y年%m月%d日 %H点%M分 ')+filename} 
		new_dict = {"gif": "https://tian-1252064124.cos.ap-chengdu.myqcloud.com/"+filename, "mp4": allurls[basename] ,"width":str(w),"height":str(h),"time":date.strftime('%Y年%m月%d日 %H点%M分 ')+filename} #使用腾讯COS加快所有gif图片的加载速度，比github快
		list_info.append(new_dict)
		i+=1	


	with open("data.json","w") as fp:
		json.dump(list_info, fp)

def getUrl(listfile):
	allurls = dict()
	with open(listfile,'r') as f:
		readers = csv.reader(f)
		for line in readers:
			if line[0].decode('GB2312').encode('utf-8') == '文件ID':
				continue
			print line[0],line[1].decode('GB2312').encode('utf-8'),line[9]
			allurls[line[1].decode('GB2312').encode('utf-8')]=line[9]
	return allurls 


def resizePhoto():
    """裁剪算法 将图片缩小 
    """
    src_dir = "/media/chao/影视/cameraLocate/"
    out_dir = "photos/"
    if directory_exists(src_dir):
        if not directory_exists(src_dir):
            make_directory(src_dir)
        # business logic
        file_list = list_img_file(src_dir)
        # print file_list
        if file_list:
            for infile in file_list:
                print "resize :"+infile
                img = Image.open(src_dir+infile)
                Graphics(infile=src_dir+infile, outfile=out_dir + infile).resize_by_times(3)#将原始3M图片尺寸缩小为三分之一大约 100k 
        else:
            pass
    else:
        print("source directory not exist!")     
def cut_photo():
    #调用Graphics类中的裁剪算法，将src_dir目录下的文件进行裁剪（裁剪成正方形）
	src_dir = "photos/"
	out_dir = "cuted/"
	if directory_exists(src_dir):
		if not directory_exists(src_dir):
			make_directory(src_dir)
		file_list = list_img_file(src_dir)
		file_list_cuted = list_img_file(out_dir)
		check_cuted =[]
		print len(file_list)
		if file_list:
			#如果切割过了 就不再切割
			for i in range(len(file_list)):
				if file_list[i] in file_list_cuted:
					check_cuted.append(file_list[i])
			for filename in check_cuted:
				file_list.remove(filename)

			for infile in file_list:
				print "cut:"+infile
				img = Image.open(src_dir+infile)
				Graphics(infile=src_dir+infile, outfile=out_dir + infile).cut_by_ratio()            
		else:
			pass
	else:
		print("source directory not exist!")     
def git_operation():
    '''
    git 命令行函数，将仓库提交
    
    ----------
    需要安装git命令行工具，并且添加到环境变量中
    '''
    os.system('git add --all')
    os.system('git commit -m "add photos"')
    os.system('git push origin master')

if __name__ == "__main__":
    #resizePhoto()        # 缩放照片
    #cut_photo()        # 裁剪图片，裁剪成正方形，去中间部分
    #compress_photo()   # 压缩图片，并保存到mini_photos文件夹下
    #git_operation()    # 提交到github仓库
    handle_photo()     # 将文件处理成json格式，存到博客仓库中
    #getMyJson()     # 将文件处理成json格式，存到博客仓库中
