import os
import time
from enum import Enum
import yaml

import utils
import compiler
from color import *
from error import printError

class Project:
	name: str
	targetName: str
	projectType: compiler.ProjectType

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

			utils.createDirsForFile(objPath.replace("\\", "/"))

			if utils.fileWasChanged(file) or forceRebuild:
				print_colored(f"Compiling file {os.path.basename(file)}... ", Color.WHITE)
				failed, results = compiler.compileFile(file, objPath, self.includeDirs, self.defines)

				if not failed:
					print_colored("DONE!\n", Color.GREEN)
					utils.updateFileTimeStamp(file)

				else:

					print_colored("FAILED!\n", Color.RED)

				for result in results:
					printError(result)

		print()

		if objects != []:
			print_colored(f"Linking project \"{self.name}\"\n", Color.BLUE)
			failed, error = compiler.linkFiles(objects, "build/bin/" + self.targetName, self.projectType, self.libraries)

			if not failed:
				print_colored(f"Linked project \"{self.name}\"\n", Color.GREEN)
			else:
				print_colored(f"Failed to link project \"{self.name}\"\n", Color.RED)
				print_colored(error, Color.RED)
		else:
			print("No files to link!")

		print()
