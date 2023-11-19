import os
from enum import Enum

import utils

class ProjectType(Enum):
	EXECUTABLE = 0
	LIB_SHARED = 1
	LIB_STATIC = 2

class Project:
	name: str
	targetName: str
	projectType: ProjectType

	sourceFiles: list
	includeDirs: list

	def build(self):
		if not os.path.isdir("obj"):
			os.mkdir("obj")

		if not os.path.isdir("bin"):
			os.mkdir("bin")

		# make inlcude parameters
		includeParams = []

		for includeDir in self.includeDirs:
			absPath = os.path.abspath(includeDir).replace("\\", "/")
			includeParams += f"-I\"{absPath}\""

		# make these into one string
		includeParamsString = utils.joinStringList(includeParams, parenthisies=False)

		for file in self.sourceFiles:
			print("Bleep bloop. Building file " + file)

			objPath = "obj/" + os.path.relpath(file).rstrip(".cpp") + ".o"

			utils.createDirsForFile(objPath)

			print(f"g++ -c \"{file}\" {includeParamsString} -o \"{objPath}\"")
			os.system(f"g++ -c \"{file}\" {includeParamsString} -o \"{objPath}\"")

		# link dat shit
		objects = utils.findFilesEndingWith("obj", ".o")
		objectPathsString = utils.joinStringList(objects)

		print(f"g++ {objectPathsString} -o \"bin/{self.targetName}\"")
		os.system(f"g++ {objectPathsString} -o \"bin/{self.targetName}\"")
