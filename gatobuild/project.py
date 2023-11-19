import os
from enum import Enum

def createDirsForFile(path: str):
	# Create dir for the obj file
	dirsToMake = path.split("/")
	path = ""

	for dir in dirsToMake:
		if dir == dirsToMake[-1]:
			break

		if not os.path.isdir(path + dir):
			os.mkdir(path + dir)

		path = path + dir + "/"

def findObjectFiles(folder: str):
	contents = os.listdir(folder)

	objects = []

	for path in contents:
		if os.path.isdir(os.path.join(folder, path)):
			objects += findObjectFiles(os.path.join(folder, path))
		elif path.endswith(".o"):
			print("aaa")
			objects.append(folder + "/" + path)

	return objects

class ProjectType(Enum):
	EXECUTABLE = 0
	LIB_SHARED = 1
	LIB_STATIC = 2

class Project:
	name: str
	targetName: str
	projectType: ProjectType

	sourceFiles: list

	def build(self):
		if not os.path.isdir("obj"):
			os.mkdir("obj")

		if not os.path.isdir("bin"):
			os.mkdir("bin")

		for file in self.sourceFiles:
			print("Bleep bloop. Building file " + file)

			objPath = "obj/" + file.rstrip(".cpp") + ".o"

			createDirsForFile(objPath)

			os.system(f"g++ -c \"{file}\" -o \"{objPath}\"")

		# link dat shit
		objects = findObjectFiles("obj")
		objectPathsString = ""

		for object in objects:
			objectPathsString += "\"" + object + "\"" + " "

		print(f"g++ {objectPathsString} -o \"bin/{self.targetName}\"")
		os.system(f"g++ {objectPathsString} -o \"bin/{self.targetName}\"")
