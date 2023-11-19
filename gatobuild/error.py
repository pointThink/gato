from color import *

class Error:
	severity: int

	line: int
	column: int
	file: str

	description: str

def printError(error: Error):
	if error.severity == 1:
		print_colored("[ WARNING ] ", Color.YELLOW)
	elif error.severity == 2:
		print_colored("[ ERROR ] ", Color.RED)

	print(f"{error.line}:{error.column} - {error.description}")
