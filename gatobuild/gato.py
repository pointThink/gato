import sys
import parser

def main(args: list):
	# load the yaml file

	projects: list

	if len(args) == 2:
		projects = parser.createProject(args[1])
	else:
		projects = parser.createProject("gato.yaml")

	for project in projects:
		project.build()

if __name__ == "__main__":
	main(sys.argv)