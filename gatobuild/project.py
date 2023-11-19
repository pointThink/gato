import os
import time
from enum import Enum
import yaml

import utils
import compiler
from color import *


class Project:
	name: str
	targetName: str
	projectType: compiler.ProjectType

	sourceFiles: list
	includeDirs: list
	libraries: list
	defines: dict

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

			utils.createDirsForFile(objPath.replace("\\", "/"))

			# Check if should rebuild the file
			dateFile = None
			relPath = ".gato/" + os.path.relpath(file)
			utils.createDirsForFile(relPath)

			if os.path.isfile(relPath):
				dateFile = open(relPath, "r+")
			else:
				dateFile = open(relPath, "w+")

			if dateFile.read() != time.ctime(os.path.getmtime(file)):
				print_colored(f"Compiling file {os.path.basename(file)}\n", Color.CYAN)
				succeded, error = compiler.compileFile(file, objPath, self.includeDirs, self.defines)

				if succeded:
					dateFile = open(relPath, "w+") # todo find a better way to do this
					dateFile.write(time.ctime(os.path.getmtime(file)))
				else:
					print_colored(f"Failed to build file{os.path.basename(file)}\n", Color.RED)
					print_colored(error, Color.RED)



		if objects != []:
			print_colored(f"Linking project \"{self.name}\"\n", Color.BLUE)
			succeded, error = compiler.linkFiles(objects, "bin/" + self.targetName, self.projectType, self.libraries)

			if succeded:
				print_colored(f"Linked project \"{self.name}\"\n", Color.GREEN)
			else:
				print_colored(f"Failed to link project \"{self.name}\"\n", Color.RED)
				print_colored(error, Color.RED)
		else:
			print("No files to link!")
