from color import *

class Error:
	severity: int

	line: int
	column: int
	file: str

	description: str

def printError(error: Error):
	if error.severity == 1:
		printColored("[ WARNING ] ", Color.YELLOW)
	elif error.severity == 2:
		printColored("[ ERROR ] ", Color.RED)

	print(f"{error.line}:{error.column} {error.file} - {error.description}")
