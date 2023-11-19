import os
import time
from enum import Enum
import yaml

import utils
import compiler

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

	def build(self, compiler: compiler.Compiler):
		if not os.path.isdir("obj"):
			os.mkdir("obj")

		if not os.path.isdir("bin"):
			os.mkdir("bin")

		objects = []

		if not os.path.isdir(".gato"):
			os.mkdir(".gato")

		for file in self.sourceFiles:
			objPath = "obj/" + os.path.relpath(file).rstrip(".cpp")
			objects.append(objPath)

			# Check if should rebuild the file
			dateFile = None
			relPath = ".gato/" + os.path.relpath(file)
			utils.createDirsForFile(relPath)

			if os.path.isfile(relPath):
				dateFile = open(relPath, "r+")
			else:
				dateFile = open(relPath, "w+")

			if dateFile.read() != time.ctime(os.path.getmtime(file)):
				dateFile.truncate()
				dateFile.write(time.ctime(os.path.getmtime(file)))
			else:
				continue

			print("Building file " + file)

			utils.createDirsForFile(objPath)
			compiler.compileFile(file, objPath, self.includeDirs)

		if objects != []:
			print("Linking files")
			compiler.linkFiles(objects, "bin/" + self.targetName)
		else:
			print("No files to link!")
