from typing import List, Dict
import re


class Parser:
    def __init__(self) -> None:
        self.i = 0
        self.json = ""
        self.c = ""

    def __check_braces(self, s: str) -> bool:
        in_string = False
        brace_pairs = {"{": "}", "[": "]", "(": ")"}
        stack: List[str] = []
        s = "." + s
        for i in range(1, len(s)):
            if s[i] == '"' and s[i - 1] != "\\":
                in_string = not in_string
            if in_string:
                continue
            c = s[i]
            if s[i] in brace_pairs:
                stack.append(brace_pairs[c])
            elif c in brace_pairs.values():
                if len(stack) and c == stack[-1]:
                    stack.pop()
                else:
                    return False
        return len(stack) == 0

    def validate(self, json: str):
        if not self.__check_braces(json):
            raise ValueError("incorrect braces")

    def __minify_json(self, json: str) -> str:
        return re.sub(r'(".*?")|[\n\t\s]', lambda m: m.group(1) or "", json)

    def __next(self):
        self.i += 1
        if self.i == len(self.json):
            return None
        if self.i > len(self.json):
            raise ValueError("parsing error (index out of range)")
        self.c = self.json[self.i]
        return self.c

    def __parse_bool(self) -> None | bool:
        ans = ""
        if self.c not in "ntf":
            raise ValueError()
        for _ in range({"n": 4, "t": 4, "f": 5}[self.c]):
            ans += self.c
            self.__next()
        if ans not in {"null", "true", "false"}:
            raise ValueError()
        return {"null": None, "true": True, "false": False}[ans]

    def __parse_number(self) -> int | float:
        ans = ""

        while self.c.isdigit() or self.c in "+-eE.":
            ans += self.c
            self.__next()

        if not re.match(r"(-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*(.*)", ans):
            raise ValueError("bad number")
        return float(ans) if "e" in ans or "E" in ans or "." in ans else int(ans)

    def __parse_string(self) -> str:
        ans = ""
        escaped = False
        if not self.c == '"':
            raise ValueError('expected a quote (")')
        self.__next()
        while 1:
            if self.c == "\\":
                escaped = True
            if self.c == '"' and not escaped:
                break
            ans += self.c
            self.__next()
            escaped = False
        self.__next()
        return ans

    def __parse_array(self):
        ans = []
        if self.__next() == "]":
            self.__next()
            return []
        while 1:
            ans.append(self.__parse_value())
            if self.c == "]":
                self.__next()
                return ans
            if not (self.c and self.c == "," and self.__next()):
                break
        raise ValueError("incorrect array")

    def __parse_object(self):
        ans = {}
        if self.__next() == "}":
            self.__next()
            return {}
        while 1:
            key = self.__parse_string()
            if self.c != ":":
                raise ValueError("expected a colon (:)")
            self.__next()
            ans[key] = self.__parse_value()
            if self.c == "}":
                self.__next()
                return ans
            if not (self.c and self.c == "," and self.__next()):
                break
        raise ValueError("incorrect object")

    def __parse_value(self):
        if self.c == "{":
            return self.__parse_object()
        elif self.c == "[":
            return self.__parse_array()
        elif self.c == '"':
            return self.__parse_string()
        elif self.c in "ntf":
            return self.__parse_bool()
        elif self.c == "-" or self.c.isdigit():
            return self.__parse_number()
        else:
            raise ValueError("unknown value type")

    def parse(self, json: str) -> Dict:
        json = self.__minify_json(json)
        self.validate(json)
        self.i = 0
        self.json = json
        self.c = self.json[0]
        ans = self.__parse_value()
        if self.i != len(self.json):
            raise ValueError("incorrect json")
        return ans


def yaml_escape(s: str) -> str:
    if any(map(lambda c: c in s, ":-#|>&*!")):
        return '"' + s + '"'
    return s


def obj_to_yaml(
    obj: dict | list | bool | int | float | str | None,
    indent_str="  ",
    level=0,
    skip_indent=False,
) -> str:
    ans = ""
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                ans += (
                    f"{'' if skip_indent else indent_str * level}{yaml_escape(key)}:\n"
                )
                ans += obj_to_yaml(value, level=level + 1)
            else:
                ans += f"{'' if skip_indent else indent_str * level}{yaml_escape(key)}: {obj_to_yaml(value)}"
            skip_indent = False
    elif isinstance(obj, bool):
        ans += str(obj).lower() + "\n"
    elif obj is None:
        ans += f"\n"
    elif isinstance(obj, (int, float)):
        ans += str(obj) + "\n"
    elif isinstance(obj, str):
        ans += yaml_escape(obj) + "\n"
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, (dict, list)):
                ans += f"{'' if skip_indent else indent_str * level}- "
                ans += obj_to_yaml(item, level=level + 1, skip_indent=True)
            else:
                ans += f"{'' if skip_indent else indent_str * level}- {item}\n"
            skip_indent = False

    return ans


if __name__ == "__main__":
    data = open("schedule4.json").read()
    parser = Parser()
    obj = parser.parse(data)
    yaml = obj_to_yaml(obj)
    print(yaml)
