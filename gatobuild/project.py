import os
import time
from enum import Enum
import yaml

import utils
import compiler
from color import *
from error import printError

supportedCLangs = [
	"ansi",
	"c89",
	"c99",
	"c11",
	"c17"
]

supportedCppLangs = [
	"c++98",
	"c++03",
	"c++11",
	"c++14",
	"c++17",
	"c++20",
	"c++23"
]

class Project:
	rootFolder: str

	name: str
	targetName: str

	projectType: compiler.ProjectType

	cDialect: str
	cppDialect: str

	sourceFiles: list
	includeDirs: list
	libraries: list
	defines: dict
	deps: list

	def build(self, compiler: compiler.Compiler, forceRebuild: bool):
		if not os.path.isdir("build"):
			os.mkdir("build")

		if not os.path.isdir("build/obj"):
			os.mkdir("build/obj")

		if not os.path.isdir("build/bin"):
			os.mkdir("build/bin")

		objects = []

		if not os.path.isdir(".gato"):
			os.mkdir(".gato")

		for file in self.sourceFiles:
			objPath = "build/obj/" + os.path.relpath(file).rstrip(".cpp")
			objects.append(objPath)

			compileFailed = False

			utils.createDirsForFile(objPath.replace("\\", "/"))

			if utils.fileWasChanged(file) or forceRebuild:
				printColored(f"\tCompiling file \"{os.path.basename(file)}\" ", Color.RESET)

				language = ""

				if file.endswith(".c"):
					language = self.cDialect
				else:
					language = self.cppDialect

				failed, results = compiler.compileFile(file, objPath, self.includeDirs, self.defines, language)

				if not failed:
					printColored("DONE!\n", Color.GREEN)
					utils.updateFileTimeStamp(file)

				else:
					compileFailed = True
					printColored("FAILED!\n", Color.RED)

				for result in results:
					print("\t", end="")
					printError(result)

		if not compileFailed:
			if objects != []:
				print(f"\tLinking project \"{self.name}\" ", end="")
				failed, error = compiler.linkFiles(objects, "build/bin/" + self.targetName, self.projectType, self.libraries)

				if not failed:
					printColored(f"DONE!\n", Color.GREEN)
				else:
					printColored(f"FAILED!\n", Color.RED)
					printColored(error, Color.RED)
			else:
				print("\tNo files to link!")

		return not compileFailed
