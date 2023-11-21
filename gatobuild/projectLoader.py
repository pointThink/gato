import yaml
import project
import os
import compiler
import utils
import solution
from color import *

def resolveDeps(project: project.Project, projects: list):
		for dep in project.deps:
			# find the project with the dep name in the projects list
			for project2 in projects:
				if project2.name == dep:
					if project2.projectType == compiler.ProjectType.EXECUTABLE:
						printColored(f"Project \"{dep}\" is not a library!\n", Color.RED)
						exit(1)

					project.libraries.append("build/bin/" + project2.targetName)
					project.includeDirs += project2.includeDirs

def createProjects(filePath: str):
	gatoFile = open(filePath, "r")
	yamlContent = yaml.safe_load(gatoFile)

	projects = []

	if "imports" in yamlContent:
		for importName in yamlContent["imports"]:
			projects += createProjects(f"{importName}/gato.yaml")

	# go through all the projects
	for projectName in yamlContent["projects"]:
		newProject = project.Project()
		yamlProject = yamlContent["projects"][projectName]

		if filePath == os.path.basename(filePath):
			newProject.rootFolder = filePath
		else:
			newProject.rootFolder = os.path.dirname(filePath)

		newProject.name = projectName
		newProject.targetName = yamlProject["target_name"]
		projectType = yamlProject["type"]

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

		if "include_dirs" in yamlProject:
			for includeDir in yamlProject["include_dirs"]:
				newProject.includeDirs.append(newProject.rootFolder + "/" + includeDir)

		if "libraries" in yamlProject:
			for library in yamlProject["libraries"]:
				newProject.libraries.append(os.path.join(newProject.rootFolder, library))

		# recurse through the source folders and find files
		for sourceFolder in yamlProject["sources"]:
			newProject.sourceFiles += utils.findFilesEndingWith(newProject.rootFolder + "/" + sourceFolder, ".cpp")
			newProject.sourceFiles += utils.findFilesEndingWith(newProject.rootFolder + "/" + sourceFolder, ".c")

		# add preprocessor defines
		if "defines" in yamlProject:
			for define in yamlProject["defines"]:
				defineSplit = define.split("=")

				if len(defineSplit) >= 2:
					newProject.defines[defineSplit[0]] = defineSplit[1]
				else:
					newProject.defines[defineSplit[0]] = None

		# add dependencies
		newProject.deps = []

		if "deps" in yamlProject:
			newProject.deps = yamlProject["deps"]

		resolveDeps(newProject, projects)

		# set language versions
		if "cpp_lang" in yamlProject:
			cppDialect = yamlProject["cpp_lang"]

			if cppDialect in project.supportedCppLangs:
				newProject.cppDialect = cppDialect
			else:
				printColored(f"Unsupported C++ dialect: \"{cppDialect}\".\n", Color.RED)
				print("Supported dialects are: ")

				for dialect in project.supportedCppLangs:
					print(f"\t- {dialect}")

				exit(1)
		else:
			newProject.cppDialect = "c++17"

		if "c_lang" in yamlProject:
			cDialect = yamlProject["c_lang"]

			if cDialect in project.supportedCLangs:
				newProject.cDialect = cDialect
			else:
				printColored(f"Unsupported C dialect: \"{cDialect}\".\n", Color.RED)
				print("Supported dialects are: ")

				for dialect in project.supportedCLangs:
					print(f"\t- {dialect}")

				exit(1)

		else:
			newProject.cDialect = "c99"


		projects.append(newProject)

	return projects

def createSolution(filePath: str):
	newSolution = solution.Solution()

	gatoFile = open(filePath, "r")
	yamlContent = yaml.safe_load(gatoFile)

	newSolution.name = yamlContent["solution_name"]
	newSolution.projects = createProjects(filePath)

	return newSolution