import error

def parseErrors(output: str):
	lines = output.split('\n')
	results = []
	buildFailed = False

	currentFile = ""

	for line in lines:
		line = line.replace("\r", "")
		lineSplit = line.split(": ")

		if len(lineSplit) == 1:
			currentFile = lineSplit[0]

		elif len(lineSplit) == 0:
			continue
		elif len(lineSplit) > 1:
			result = error.Error()

			if lineSplit[1].split(" ")[0] == "error":
				result.severity = 2
				buildFailed = True
			elif lineSplit[1].split(" ")[0] == "warning":
				result.severity = 1

			result.file = currentFile
			result.line = int(lineSplit[0].split("(")[1].split(")")[0])
			result.column = 0

			result.description = ""

			for i in range(2, len(lineSplit)):
				result.description += lineSplit[i] + ": "

			results.append(result)


	return buildFailed, results