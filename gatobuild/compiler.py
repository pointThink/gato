import os
import utils
from enum import Enum

class ProjectType(Enum):
	EXECUTABLE = 0
	LIB_SHARED = 1
	LIB_STATIC = 2

class Compiler:
	def compileFile(self, sourcePath: str, objectPath: str, includeDirs: list):
		pass

	def linkFiles(self, objectList: list, outputPath: str, outputType: ProjectType):
		pass

class GCC(Compiler):
	def compileFile(self, sourcePath: str, objectPath: str, includeDirs: list, ):
		includeParams = []

		for includeDir in includeDirs:
			includeParams += "-I\"" + includeDir + "\""

		includeParamsString = utils.joinStringList(includeParams, parenthisies=False)

		objectPath = objectPath.replace("\\", "/");

		if sourcePath.endswith(".c"):
			os.system(f"gcc -c \"{sourcePath}\" {includeParamsString} -o \"{objectPath}.o\"")
		else:
			os.system(f"g++ -c \"{sourcePath}\" {includeParamsString} -o \"{objectPath}.o\"")

	def linkFiles(self, objectList: list, outputPath: str, outputType: ProjectType):
		newObjects = []

		for object in objectList:
			newObjects.append((object + ".o").replace("\\", "/"))

		objectsString = utils.joinStringList(newObjects)

		if outputType == ProjectType.EXECUTABLE:
			os.system(f"g++ {objectsString} -o \"{outputPath}\"")

		elif outputType == ProjectType.LIB_STATIC:
			outputPath = os.path.join(os.path.dirname(outputPath), "lib" + os.path.basename(outputPath))
			os.system(f"ar rvs \"{outputPath}.a\" {objectsString} ")