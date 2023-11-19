import os
import utils
from enum import Enum
import subprocess

class ProjectType(Enum):
	EXECUTABLE = 0
	LIB_SHARED = 1
	LIB_STATIC = 2

class Compiler:
	def compileFile(self, sourcePath: str, objectPath: str, includeDirs: list, preprocessorDefines: dict):
		return False, "Blank compiler!"
	def linkFiles(self, objectList: list, outputPath: str, outputType: ProjectType, libraries: list):
		return False, "Blank compiler!"

class GCC(Compiler):
	def compileFile(self, sourcePath: str, objectPath: str, includeDirs: list, preprocessorDefines: dict):
		includeParams = []

		for includeDir in includeDirs:
			includeParams += "-I\"" + includeDir + "\" "

		preprocessorParams = []

		for defineName in preprocessorDefines:
			if preprocessorDefines[defineName] == None:
				preprocessorParams.append(f"-D \"{defineName}\" ")
			else:
				preprocessorParams.append(f"-D \"{defineName}={preprocessorDefines[defineName]}\" ")

		defineString = utils.joinStringList(preprocessorParams, parenthisies=False)
		includeParamsString = utils.joinStringList(includeParams, parenthisies=False)
		objectPath = objectPath.replace("\\", "/")

		output = b''
		errorOut = b''

		if sourcePath.endswith(".c"):
			process = subprocess.Popen(f"gcc -c \"{sourcePath}\" {includeParamsString} {defineString} -o \"{objectPath}.o\"", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, errorOut = process.communicate()
		else:
			process = subprocess.Popen(f"g++ -c \"{sourcePath}\" {includeParamsString} {defineString} -o \"{objectPath}.o\"", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, errorOut = process.communicate()

		if errorOut.decode() == "":
			return True, "No error"
		else:
			return False, errorOut.decode()

	def linkFiles(self, objectList: list, outputPath: str, outputType: ProjectType, libraries: list):
		newObjects = []
		newLibs = []

		for object in objectList:
			newObjects.append((object + ".o").replace("\\", "/"))

		objectsString = utils.joinStringList(newObjects)

		output = b''
		errorOut = b''

		if outputType == ProjectType.EXECUTABLE:
			for lib in libraries:
				folder = os.path.dirname(lib).replace("\\", "/")
				newLibs.append(f"-L\"{folder}\" -l\"{os.path.basename(lib)}\"")

			libsString = utils.joinStringList(newLibs, parenthisies=False)

			process = subprocess.Popen(f"g++ {objectsString} {libsString} -o \"{outputPath}\"", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, errorOut = process.communicate()

		elif outputType == ProjectType.LIB_STATIC:
			outputPath = os.path.join(os.path.dirname(outputPath), "lib" + os.path.basename(outputPath))
			process = subprocess.Popen(f"ar rvs \"{outputPath}.a\" {objectsString} ", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, errorOut = process.communicate()

		if errorOut.decode() == "":
			return True, "No error"
		else:
			return False, errorOut.decode()