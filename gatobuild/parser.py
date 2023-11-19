import yaml
import project
import os
import compiler
import utils
from color import *

def resolveDeps(project: project.Project, projects: list):
		for dep in project.deps:
			# find the project with the dep name in the projects list
			for project2 in projects:
				if project2.name == dep:
					if project2.projectType == compiler.ProjectType.EXECUTABLE:
						print_colored(f"Project \"{dep}\" is not a library!\n", Color.RED)
						exit(1)

					project.libraries.append("bin/" + project2.targetName)
					project.includeDirs += project2.includeDirs

def createProject(filePath: str):
	gatoFile = open(filePath, "r")
	yamlContent = yaml.safe_load(gatoFile)

	projects = []

	# go through all the projects
	for projectName in yamlContent:
		newProject = project.Project()

		newProject.name = projectName
		newProject.targetName = yamlContent[projectName]["target_name"]
		projectType = yamlContent[projectName]["type"]

		if projectType == "executable":
			newProject.projectType = compiler.ProjectType.EXECUTABLE
		elif projectType == "lib_static":
			newProject.projectType = compiler.ProjectType.LIB_STATIC
		elif projectType == "lib_shared":
			newProject.projectType = compiler.ProjectType.LIB_SHARED

		newProject.sourceFiles = []
		newProject.defines = {}
		newProject.includeDirs = []
		newProject.libraries = []

		if "include_dirs" in yamlContent[projectName]:
			newProject.includeDirs = yamlContent[projectName]["include_dirs"]

		if "libraries" in yamlContent[projectName]:
			newProject.libraries = yamlContent[projectName]["libraries"]

		# recurse through the source folders and find files
		for sourceFolder in yamlContent[projectName]["sources"]:
			newProject.sourceFiles += utils.findFilesEndingWith(os.path.dirname(filePath) + "/" + sourceFolder, ".cpp")
			newProject.sourceFiles += utils.findFilesEndingWith(os.path.dirname(filePath) + "/" + sourceFolder, ".c")

		# add preprocessor defines
		if "defines" in yamlContent[projectName]:
			for define in yamlContent[projectName]["defines"]:
				defineSplit = define.split("=")

				if len(defineSplit) >= 2:
					newProject.defines[defineSplit[0]] = defineSplit[1]
				else:
					newProject.defines[defineSplit[0]] = None

		# add dependencies
		newProject.deps = []

		if "deps" in yamlContent[projectName]:
			newProject.deps = yamlContent[projectName]["deps"]

		resolveDeps(newProject, projects)

		projects.append(newProject)

	return projects