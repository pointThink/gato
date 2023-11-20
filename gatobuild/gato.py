"""
TODO: Cleanup this entire fucking codebase
"""

import ctypes
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(sys.argv[0])))

import projectLoader
import color
import utils
import gcc

# Enable colors in ConHost aka default terminal emulator
if sys.platform == "win32": # Why is it called win32 if it's 64 bit most of the time
	kernel32 = ctypes.windll.kernel32
	kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

def main(args: list):
	print()
	print("===================================")
	print("  Gato build system - Version 0.1")
	print("  Copyright (C) PointThink (2023)")
	print("===================================")
	print()

	# load the yaml file
	if len(args) == 2:
		if args[1] == "build":
			projects = []
			fileChanged = utils.fileWasChanged("gato.yaml")
			solution = projectLoader.createSolution(os.path.abspath("gato.yaml"))

			solution.build(gcc.GCC(), fileChanged)

			if fileChanged:
				utils.updateFileTimeStamp("gato.yaml")

		elif args[1] == "clean":
			print("Cleaning...")
			print()

			print ("Removing directory \"build\"")
			utils.deleteItem("build")
			print("Removing gato cache")
			utils.deleteItem(".gato")
		else:
			color.printColored(f"Unknown command: {args[1]}", color.Color.RED)
			exit(1)

	else:
		color.printColored(f"Expected 1 argument", color.Color.RED)

if __name__ == "__main__":
	main(sys.argv)