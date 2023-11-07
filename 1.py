import yaml
import json


def json_to_yaml(json_str: str) -> str:
    return yaml.dump(json.loads(json_str), allow_unicode=True)


json_str = open("schedule0.json").read()
print(json_to_yaml(json_str))
