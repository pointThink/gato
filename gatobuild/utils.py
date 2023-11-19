import os
import time

def findFilesEndingWith(folder: str, end: str):
	contents = os.listdir(folder)

	sourceFiles = []

	for path in contents:
		if os.path.isdir(os.path.join(folder, path)):
			sourceFiles += findFilesEndingWith(folder + "/" + path, end)
		elif path.endswith(end):
			sourceFiles.append(folder + "/" + path)

	return sourceFiles

def fileWasChanged(filePath: str):
	dateFile = None
	relPath = ".gato/" + os.path.relpath(filePath)
	createDirsForFile(relPath)

	if os.path.isfile(relPath):
		dateFile = open(relPath, "r+")
	else:
		dateFile = open(relPath, "w+")

	return dateFile.read() != time.ctime(os.path.getmtime(filePath))

def updateFileTimeStamp(filePath: str):
	relPath = ".gato/" + os.path.relpath(filePath)

	dateFile = open(relPath, "w+")  # todo find a better way to do this
	dateFile.write(time.ctime(os.path.getmtime(filePath)))

def createDirsForFile(path: str):
	path = path.replace("\\", "/")

	dirsToMake = path.split("/")
	path = ""

	for dir in dirsToMake:
		if dir is dirsToMake[-1]:
			break

		if not os.path.isdir(path + dir):
			os.mkdir(path + dir)

		path = path + dir + "/"

def joinStringList(list: list, parenthisies=True):
	finalString = ""

	for string in list:
		if parenthisies:
			finalString += "\"" + string + "\" "
		else:
			finalString += string + ""

	return finalString

def deleteItem(item: str):
	# check if the item is a directory
	if os.path.isdir(item):
		for file in os.listdir(item):
			deleteItem(item + '/' + file)

		os.rmdir(item)

	else:
		os.remove(item)
