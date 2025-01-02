"""Original case templates with independently supplied expected results."""
import copy
import re

TEMPLATES = [('aggregate recorded usage and assertion outcomes by model label', {'runs': [{'id': 'a{n}', 'model': 'local', 'input_tokens': 10, 'output_tokens': 5, 'latency_ms': 100, 'passed': True}, {'id': 'b{n}', 'model': 'local', 'input_tokens': 20, 'output_tokens': 7, 'latency_ms': 200, 'passed': False}]}, {'models': [{'model': 'local', 'runs': 2, 'input_tokens': 30, 'output_tokens': 12, 'latency_ms_total': 300, 'passed': 1, 'average_latency_ms': 150.0, 'pass_rate': 0.5}]}), ('retain a zero-latency recorded model run', {'runs': [{'id': 'a{n}', 'model': 'recorded', 'input_tokens': 0, 'output_tokens': 0, 'latency_ms': 0, 'passed': True}]}, {'models': [{'model': 'recorded', 'runs': 1, 'input_tokens': 0, 'output_tokens': 0, 'latency_ms_total': 0, 'passed': 1, 'average_latency_ms': 0.0, 'pass_rate': 1.0}]}), ('return no model summaries for an empty notebook', {'runs': []}, {'models': []}), ('reject repeated recorded run IDs', {'runs': [{'id': 'a{n}', 'model': 'local', 'input_tokens': 1, 'output_tokens': 1, 'latency_ms': 1, 'passed': True}, {'id': 'a{n}', 'model': 'local', 'input_tokens': 1, 'output_tokens': 1, 'latency_ms': 1, 'passed': True}]}, None), ('require boolean assertion outcomes in recorded runs', {'runs': [{'id': 'a{n}', 'model': 'local', 'input_tokens': 1, 'output_tokens': 1, 'latency_ms': 1, 'passed': 1}]}, None)]


def make_case(index):
    description, source, expected = copy.deepcopy(TEMPLATES[index % len(TEMPLATES)])
    def fill(value):
        if isinstance(value, str):
            if re.fullmatch(r"@i[+]\d+", value):
                return index + int(value[3:])
            return value.replace("{n}", str(index))
        if isinstance(value, list):
            return [fill(item) for item in value]
        if isinstance(value, dict):
            return {fill(key): fill(item) for key, item in value.items()}
        return value
    case = {"id": "runs-{:04d}".format(index), "description": description, "input": fill(source)}
    case.update({"expected_error": True} if expected is None else {"expected": fill(expected)})
    return case
