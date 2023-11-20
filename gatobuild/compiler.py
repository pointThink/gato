from enum import Enum

class ProjectType(Enum):
	EXECUTABLE = 0
	LIB_SHARED = 1
	LIB_STATIC = 2

class Compiler:
	def compileFile(self, sourcePath: str, objectPath: str, includeDirs: list, preprocessorDefines: dict):
		return True, []
	def linkFiles(self, objectList: list, outputPath: str, outputType: ProjectType, libraries: list):
		return True, "Blank compiler!"
