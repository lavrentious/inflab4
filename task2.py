import re


def get_indent(m: re.Match, json: str, indent: str):
    k = 0
    for i in range(1, m.span()[1]):
        if json[i] in "{[":
            k += 1
        elif json[i] in "}]":
            k -= 1
    return k * indent


def json_to_yaml(json: str, indent="  ") -> str:
    ans: str = re.sub(r'(".*?")|[\n\t\s]', lambda m: m.group(1) or "", json)
    ans = re.sub(
        r'(".*?")|,', lambda m: m.group(1) or "\n" + get_indent(m, ans, indent), ans
    )
    ans = re.sub(
        r'(".*?")|:{', lambda m: m.group(1) or ":\n" + get_indent(m, ans, indent), ans
    )
    ans = re.sub(r'(".*?")|:(?!\n)', lambda m: m.group(1) or ": ", ans)
    ans = re.sub(r'"(\S+)"', lambda m: m.group(1), ans, 0)
    ans = re.sub("[{}]", "", ans)
    ans = re.sub(r'(".*?")|null', "", ans)
    return "---\n" + ans


json = open("schedule2.json").read()
print(json_to_yaml(json))
