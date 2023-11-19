import yaml
import project

import os

def findSourcesInFolder(folder: str):
	contents = os.listdir(folder)

	sourceFiles = []

	for path in contents:
		if os.path.isdir(os.path.join(folder, path)):
			sourceFiles += findSourcesInFolder(folder + "/" + path)
		elif path.endswith(".cpp"):
			sourceFiles.append(folder + "/" + path)

	return sourceFiles

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
			newProject.projectType = project.ProjectType.EXECUTABLE
		elif projectType == "lib_static":
			newProject.projectType = project.ProjectType.LIB_STATIC
		elif projectType == "lib_shared":
			newProject.projectType = project.ProjectType.LIB_SHARED

		newProject.sourceFiles = []

		# recurse through the source folders and find files
		for sourceFolder in yamlContent[projectName]["sources"]:
			newProject.sourceFiles += findSourcesInFolder(os.path.dirname(filePath) + "/" + sourceFolder)

		projects.append(newProject)

	return projects