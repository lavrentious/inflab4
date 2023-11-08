from utils import dry_json, hydrate_json



def json_to_yaml(json: str):
    json, d, keyword = dry_json(json)
    json = json.replace(",", "\n").replace("{", "").replace("}", "").replace(":", ": ")
    return "---\n" + hydrate_json(json, d, keyword, False)


json = open("schedule0.json").read()
print(json_to_yaml(json))
