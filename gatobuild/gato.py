import sys
import os
import parser
import compiler

def main(args: list):
	# load the yaml file

	projects: list

	if len(args) == 2:
		projects = parser.createProject(os.path.abspath(args[1]))
	else:
		projects = parser.createProject(os.path.abspath("gato.yaml"))

	for project in projects:
		project.build(compiler.GCC())

if __name__ == "__main__":
	main(sys.argv)