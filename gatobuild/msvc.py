import gatobuild.error
from gatobuild.compiler import *

def parseErrors(output: str):
	lines = output.split('\n')
	results = []
	buildFailed = False

	currentFile = ""

	for line in lines:
		line = line.replace("\r", "")
		lineSplit = line.split(": ")

		if len(lineSplit) == 1:
			currentFile = lineSplit[0]

		elif len(lineSplit) == 0:
			continue
		elif len(lineSplit) > 1:
			result = gatobuild.error.Error()

			if lineSplit[1].split(" ")[0] == "error":
				result.severity = 2
				buildFailed = True
			elif lineSplit[1].split(" ")[0] == "warning":
				result.severity = 1

			result.file = currentFile
			result.line = int(lineSplit[0].split("(")[1].split(")")[0])
			result.column = 0

			result.description = ""

			for i in range(2, len(lineSplit)):
				result.description += lineSplit[i] + ": "

			results.append(result)


	return buildFailed, results

class MSVC(Compiler):
	def compileFile(self, sourcePath: str, objectPath: str, includeDirs: list, preprocessorDefines: dict):
		includeParams = []
		for includeDir in includeDirs:
			includeParams += "/I\"" + includeDir + "\" "

		defineParams = []
		for define in preprocessorDefines:
			if preprocessorDefines[define] != None:
				defineParams.append("/D" + define +"=\"" + preprocessorDefines[define] + "\" ")
			else:
				defineParams.append("/D" + define + " ")

		definesString = utils.joinStringList(defineParams, parenthisies=False)
		includeString = utils.joinStringList(includeParams, parenthisies=False)

		process = subprocess.Popen(f"cl.exe /c /nologo /EHsc {includeString} {definesString} \"{sourcePath}\" /Fo\"{objectPath}.obj", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = process.communicate()

		return parseErrors(out.decode())

	def linkFiles(self, objectList: list, outputPath: str, outputType: ProjectType, libraries: list):
		objects = []

		for object in objectList:
			objects.append((object + ".obj").replace("\\", "/"))

		newLibs = []
		for library in libraries:
			newLibs.append(library + ".lib")

		libsString = utils.joinStringList(newLibs)

		objectsString = utils.joinStringList(objects)

		process = None

		if outputType == ProjectType.EXECUTABLE:
			process = subprocess.Popen(f"link.exe /NOLOGO /MANIFEST /SUBSYSTEM:CONSOLE /MACHINE:x64 {objectsString} {libsString} /OUT:\"{outputPath}.exe\"", stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		elif outputType == ProjectType.LIB_STATIC:
			process = subprocess.Popen(f"lib.exe /NOLOGO {objectsString} /OUT:{outputPath}.lib", stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		out, err = process.communicate()

		if out.decode() != "":
			return True, out.decode()

		return False, "No error"
