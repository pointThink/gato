import sys
import os
import parser
import compiler
import color
import ctypes
import sys

# Enable colors in ConHost aka default terminal emulator
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

def main(args: list):
	# load the yaml file

	projects = []

	if len(args) == 2:
		if args[1] == "build":
			projects = parser.createProject(os.path.abspath("gato.yaml"))
		elif args[1] == "clean":
			pass
		else:
			color.print_colored(f"Unknown command: {args[1]}", color.Color.RED)
			exit(1)

	for project in projects:
		project.build(compiler.GCC())

if __name__ == "__main__":
	main(sys.argv)