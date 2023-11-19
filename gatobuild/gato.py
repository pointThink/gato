import sys
import os
import parser
import compiler
import color
import ctypes
import sys
import utils

# Enable colors in ConHost aka default terminal emulator
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

def main(args: list):
	# load the yaml file

	projects = []

	fileChanged = False

	if len(args) == 2:
		if args[1] == "build":
			fileChanged = utils.fileWasChanged("gato.yaml")

			projects = parser.createProject(os.path.abspath("gato.yaml"))

			if fileChanged:
				utils.updateFileTimeStamp("gato.yaml")

		elif args[1] == "clean":
			pass
		else:
			color.print_colored(f"Unknown command: {args[1]}", color.Color.RED)
			exit(1)

	else:
		color.print_colored(f"Expected 1 argument", color.Color.RED)

	for project in projects:
		project.build(compiler.GCC(), fileChanged)

if __name__ == "__main__":
	main(sys.argv)