import json
import subprocess
import os

from compiler import *
import error
import utils

# This is bad dumb code but at least it works
def parseError(jsonInput: str):
	results = []

	buildFailed = False

	"""
	file = open("ass.json", "w+")
	file.write(jsonInput)
	"""

	jsonObj = json.loads(jsonInput)

	for jsonError in jsonObj:
		result = error.Error()

		if jsonError["kind"] == "error":
			buildFailed = True
			result.severity = 2

			result.line = jsonError["fixits"][0]["next"]["line"]
			result.column = jsonError["fixits"][0]["next"]["column"]
			result.file = jsonError["fixits"][0]["next"]["file"]
			result.description = jsonError["message"]

		elif jsonError["kind"] == "warning":
			result.line = jsonError["locations"][0]["caret"]["line"]
			result.column = jsonError["locations"][0]["caret"]["column"]
			result.file = jsonError["locations"][0]["caret"]["file"]
			result.description = jsonError["message"]

			result.severity = 1

		elif jsonError["kind"] == "fatal error":
			buildFailed = True
			result.severity = 2
			result.file = jsonError["locations"][0]["finish"]["file"]
			result.line = jsonError["locations"][0]["finish"]["line"]
			result.column = jsonError["locations"][0]["finish"]["column"]
			result.description = jsonError["message"]

		results.append(result)

	return buildFailed, results



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
			process = subprocess.Popen(f"gcc -fdiagnostics-format=json -c \"{sourcePath}\" {includeParamsString} {defineString} -o \"{objectPath}.o\"", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, errorOut = process.communicate()
		else:
			process = subprocess.Popen(f"g++ -fdiagnostics-format=json -c \"{sourcePath}\" {includeParamsString} {defineString} -o \"{objectPath}.o\"", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, errorOut = process.communicate()

		return parseError(errorOut.decode().split("\n")[0])

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
			process = subprocess.Popen(f"ar rvs -c \"{outputPath}.a\" {objectsString} ", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, errorOut = process.communicate()

		if errorOut.decode() == "":
			return False, "No error"
		else:
			return True, errorOut.decode()