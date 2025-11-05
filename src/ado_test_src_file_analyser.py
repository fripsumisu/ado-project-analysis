from typing import AnyStr

JAVA_TEST_INDICATOR = "@Test"
PYTHON_TEST_INDICATOR = "self.assert"

PYTHON_FALSE_TRUE_ASSERTION = "assertTrue(True"
PYTHON_FALSE_FALSE_ASSERTION = "assertFalse(False"
PYTHON_FALSE_NULL_ASSERTION = "assertIsNone(None"

JAVA_FALSE_TRUE_ASSERTION = "assertTrue(true"
JAVA_FALSE_FALSE_ASSERTION = "assertFalse(false"
JAVA_FALSE_NULL_ASSERTION = "assertNull(null"
JAVA_DISABLED_TEST_ANNOTATION = "@Disabled"

dud_java_test_tokens = [
    JAVA_DISABLED_TEST_ANNOTATION,
    JAVA_FALSE_TRUE_ASSERTION,
    JAVA_FALSE_FALSE_ASSERTION,
    JAVA_FALSE_NULL_ASSERTION
]
dud_python_test_tokens = [
    PYTHON_FALSE_TRUE_ASSERTION,
    PYTHON_FALSE_FALSE_ASSERTION,
    PYTHON_FALSE_NULL_ASSERTION
]


def parse_possible_test_file(filepath: str):
    if filepath.endswith(".py"):
        return run_test_analysis(file_path=filepath, dud_list=dud_python_test_tokens, language="Python")
    elif filepath.endswith(".java"):
        return run_test_analysis(file_path=filepath, dud_list=dud_java_test_tokens, language="Java")
    else:
        return {
        'filePath': filepath,
        'possibleTests': 0,
        'possibleDudTests': 0
    }

def get_file_contents(filepath: str):
    lines_in_file = []
    with open(filepath) as file:
        for line in file:
            lines_in_file.append(line)

    return lines_in_file

def run_test_analysis(file_path: str, dud_list: list[AnyStr], language: str):
    potential_test_count = 0
    potential_dud_test_count = 0
    file_lines = get_file_contents(filepath=file_path)

    # Parsing file_lines line by line
    for line in file_lines:
        # Determine src language
        if language == "Java":
            if JAVA_TEST_INDICATOR in line:
                potential_test_count+=1
        elif language == "Python":
            if PYTHON_TEST_INDICATOR in line:
                potential_test_count+=1
        # For each dud check provided, check the current line
        for dud in dud_list:
            if dud in line:
                potential_dud_test_count+=1

    return {
        'filePath': file_path,
        'possibleTests': potential_test_count,
        'possibleDudTests': potential_dud_test_count
    }