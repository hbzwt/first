#!/usr/bin/env python
#coding=utf-8
import sys, os, stat

'''
print "Hello World!"

#print current work directory

currentWorkDirectory = os.getcwd();
print currentWorkDirectory;
'''

#print all file absolutely path under particular directory

local_path = "E:\\software\\eclipse-jee-luna-SR2-win32-x86_64\\eclipse\\CTS_workspace\\"

mapFile = "mapFile.txt"	
	
mapFile_replicate = "mapFile_replicate.txt"	

#local_path = "E:\\work\\SVN_test\\test\\"

#local_path = "C:\\temp\\"

print local_path

dictionary = {}
replicate_dict = {}

needfiles = ['.java','.xml']

#
def getJavaFileAddress(path):
	file_object = open(path)
	
	try:
		for line in file_object:
			line = line.strip()
			if line.startswith('package'):
				fileName = os.path.basename(path).replace('.java','')
				address = line.replace('package','').replace(' ','').replace(';','')
				address = address + "." +fileName
				#print "address: " + address
				#print "path: " + path
				relative_path = path.replace(local_path,"")
				if dictionary.has_key(address):
					path = dictionary[address] + " ------------>" +relative_path
					replicate_dict[address] = relative_path

				dictionary[address] = relative_path
				break
	finally:
		file_object.close()		
	
#判断是否是java文件
def isJaveFile(checkFile):
		if checkFile.endswith('.java'):
			return True
		return False

#判断是否为需要的文件	
def isNeedFile(checkFile):
	for suffix in needfiles:
		if checkFile.endswith("java"):
			return True
	return False

#获得目录下所有的文件
def getDirectoryFiles(path, list):
	for file in os.listdir(path):
		subDirectory = os.path.join(path,file)
		if os.path.isdir(subDirectory):
			getDirectoryFiles(subDirectory,list)
		elif os.path.isfile(subDirectory):
			if isNeedFile(subDirectory):
				list.append(subDirectory)
		else:
			print subDirectory
		
#获得需要的所有文件
def getAllNeedFiles(path):
	list = []
	getDirectoryFiles(path,list)
	return list	


#获得所有java文件的字典
def getJavaFileDictionary():
	list = getAllNeedFiles(local_path);
	for item in list:
		#print item
		if isJaveFile(item):
			getJavaFileAddress(item)
		
	print "file count: " + str(len(list))


content = []
def writeDictionaryToFile():
	for key in dictionary:
		javaFilePath = dictionary[key]
		line = key + "=" + javaFilePath + "\n"
		content.append(line)
	
	#文件存在则先删除
	if os.path.exists(mapFile):
		os.remove(mapFile)
	
	#写到文件中	
	mapFile = open(mapFile,"w+")	
	try:
		mapFile.writelines(content)
	finally:
		mapFile.close()
		
replicate = []
def writeReplicateToFile():
	for key in replicate_dict:
		javaFilePath = replicate_dict[key]
		line = key + "=" + javaFilePath + "\n"
		replicate.append(line)
	
	#文件存在则先删除
	if os.path.exists(mapFile_replicate):
		os.remove(mapFile_replicate)
	
	#写到文件中	
	mapFile_replicate = open(mapFile_replicate,"w+")
	try:
		mapFile_replicate.writelines(replicate)
	finally:
		mapFile_replicate.close()
		
	
#run program
getJavaFileDictionary()
writeDictionaryToFile()
writeReplicateToFile()

print "=====End=======";
