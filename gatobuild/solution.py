from color import *

from compiler import Compiler
class Solution:
	name: str
	projects: list

	def build(self, compiler: Compiler, forceRebuild: bool):
		print(f"--- Building solution \"{self.name}\" ---")
		print()

		failedBuilds = 0

		for project in self.projects:
			print(f"Building project \"{project.name}\"")

			if not project.build(compiler, forceRebuild):
				failedBuilds += 1
			print()

		if failedBuilds == 0:
			printColored("All projects built successfully\n", Color.GREEN)
		elif failedBuilds == 1:
			printColored(f"Failed to build {failedBuilds} project", Color.RED)
		else:
			printColored(f"Failed to build {failedBuilds} projects", Color.RED)