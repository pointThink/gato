import json
import error

# This is bad dumb code but at least it works
def parseError(jsonInput: str):
	results = []

	buildFailed = False

	"""
	file = open("ass.json", "w+")
	file.write(jsonInput)
	"""

	jsonObj = json.loads(jsonInput)

	for jsonError in jsonObj:
		result = error.Error()

		if jsonError["kind"] == "error":
			buildFailed = True
			result.severity = 2

			result.line = jsonError["fixits"][0]["next"]["line"]
			result.column = jsonError["fixits"][0]["next"]["column"]
			result.file = jsonError["fixits"][0]["next"]["file"]
			result.description = jsonError["message"]

		elif jsonError["kind"] == "warning":
			result.line = jsonError["locations"][0]["caret"]["line"]
			result.column = jsonError["locations"][0]["caret"]["column"]
			result.file = jsonError["locations"][0]["caret"]["file"]
			result.description = jsonError["message"]

			result.severity = 1

		elif jsonError["kind"] == "fatal error":
			buildFailed = True
			result.severity = 2
			result.file = jsonError["locations"][0]["finish"]["file"]
			result.line = jsonError["locations"][0]["finish"]["line"]
			result.column = jsonError["locations"][0]["finish"]["column"]
			result.description = jsonError["message"]

		results.append(result)

	return buildFailed, results

