import os
import utils


class Compiler:
	def compileFile(self, sourcePath: str, objectPath: str, includeDirs: list):
		pass

	def linkFiles(self, objectList: list, outputPath: str):
		pass

class GCC(Compiler):
	def compileFile(self, sourcePath: str, objectPath: str, includeDirs: list):
		includeParams = []

		for includeDir in includeDirs:
			includeParams += "-I\"" + includeDir + "\""

		includeParamsString = utils.joinStringList(includeParams, parenthisies=False)

		if sourcePath.endswith(".c"):
			os.system(f"gcc -c \"{sourcePath}\" {includeParamsString} -o \"{objectPath}.o\"")
		else:
			os.system(f"g++ -c \"{sourcePath}\" {includeParamsString} -o \"{objectPath}.o\"")

	def linkFiles(self, objectList: list, outputPath: str):
		newObjects = []

		for object in objectList:
			newObjects.append(object + ".o")

		objectsString = utils.joinStringList(newObjects)

		os.system(f"g++ {objectsString} -o {outputPath}")