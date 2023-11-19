import os
import utils
from enum import Enum
import subprocess

class ProjectType(Enum):
	EXECUTABLE = 0
	LIB_SHARED = 1
	LIB_STATIC = 2

class Compiler:
	def compileFile(self, sourcePath: str, objectPath: str, includeDirs: list):
		return False, "Blank compiler!"
	def linkFiles(self, objectList: list, outputPath: str, outputType: ProjectType, libraries: list):
		return False, "Blank compiler!"

class GCC(Compiler):
	def compileFile(self, sourcePath: str, objectPath: str, includeDirs: list, ):
		includeParams = []

		for includeDir in includeDirs:
			includeParams += "-I\"" + includeDir + "\""

		includeParamsString = utils.joinStringList(includeParams, parenthisies=False)

		objectPath = objectPath.replace("\\", "/");

		if sourcePath.endswith(".c"):
			process = subprocess.Popen(f"gcc -c \"{sourcePath}\" {includeParamsString} -o \"{objectPath}.o\"", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, errorOut = process.communicate()

			if errorOut.decode() == "":
				return True, "No error"
			else:
				return False, errorOut.decode()
		else:
			process = subprocess.Popen(f"g++ -c \"{sourcePath}\" {includeParamsString} -o \"{objectPath}.o\"", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, errorOut = process.communicate()

			if errorOut.decode() == "":
				return True, "No error"
			else:
				return False, errorOut.decode()

		return False, "Unknown file type"

	def linkFiles(self, objectList: list, outputPath: str, outputType: ProjectType, libraries: list):
		newObjects = []
		newLibs = []

		for object in objectList:
			newObjects.append((object + ".o").replace("\\", "/"))

		objectsString = utils.joinStringList(newObjects)

		for lib in libraries:
			folder = os.path.dirname(lib).replace("\\", "/")
			newLibs.append(f"-L\"{folder}\" -l\"{os.path.basename(lib)}\"")

		libsString = utils.joinStringList(newLibs, parenthisies=False)

		if outputType == ProjectType.EXECUTABLE:
			os.system(f"g++ {objectsString} {libsString} -o \"{outputPath}\"")

		elif outputType == ProjectType.LIB_STATIC:
			outputPath = os.path.join(os.path.dirname(outputPath), "lib" + os.path.basename(outputPath))
			os.system(f"ar rvs \"{outputPath}.a\" {objectsString} ")