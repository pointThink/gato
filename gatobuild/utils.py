import os

def findFilesEndingWith(folder: str, end: str):
	contents = os.listdir(folder)

	sourceFiles = []

	for path in contents:
		if os.path.isdir(os.path.join(folder, path)):
			sourceFiles += findFilesEndingWith(folder + "/" + path, end)
		elif path.endswith(end):
			sourceFiles.append(folder + "/" + path)

	return sourceFiles


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