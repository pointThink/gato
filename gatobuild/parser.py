import yaml
import project
import os
import compiler

import utils

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
		newProject.includeDirs = yamlContent[projectName]["include_dirs"]

		# recurse through the source folders and find files
		for sourceFolder in yamlContent[projectName]["sources"]:
			newProject.sourceFiles += utils.findFilesEndingWith(os.path.dirname(filePath) + "/" + sourceFolder, ".cpp")
			newProject.sourceFiles += utils.findFilesEndingWith(os.path.dirname(filePath) + "/" + sourceFolder, ".c")

		projects.append(newProject)

	return projects