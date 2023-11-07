from typing import Tuple, List, Dict
import string, random


def yaml_escape(s: str) -> str:
    if any(map(lambda c: c in s, ":-#|>&*!")):
        return '"' + s + '"'
    return s


def minify_json(json: str) -> str:
    json = json.strip("\n").strip(" ").strip("\t")
    assert len(json) and json[0] == "{" and json[-1] == "}"
    ans = "{"
    in_string = False
    for i in range(1, len(json)):
        if json[i] == '"' and json[i - 1] != "\\":
            in_string = not in_string
            ans += '"'
        elif in_string or (not in_string and json[i] not in {" ", "\n", "\t"}):
            ans += json[i]
    assert not in_string
    return ans


# def dry_json(json: str) -> Tuple[str, Dict[str, str]]:
#     def uuid(length=10) -> str:
#         chars = string.ascii_letters + string.digits
#         ans = "".join(random.choice(chars) for _ in range(length))
#         return ans
#     json = minify_json(json)
#     d: Dict[str, str] = {}
#     ans = "{"
#     cur: str = ""
#     in_string = False
#     for i in range(1, len(json)):
#         if json[i] == '"':
#             if in_string:
#                 if json[i - 1] == "\\":
#                     cur += json[i]
#                 else:
#                     k = uuid(10)
#                     assert k not in d
#                     assert "null" not in d
#                     ans += k
#                     d[k] = cur
#                     cur = ""
#                     in_string = False
#             else:
#                 in_string = True
#         elif in_string:
#             cur += json[i]
#         else:
#             ans += json[i]
#     return ans, d


def dry_json(json: str, keyword="owo") -> Tuple[str, Dict[str, str], str]:
    json = minify_json(json)
    d: Dict[str, str] = {}
    ans = "{"
    cur: str = ""
    in_string = False
    k = 0
    for i in range(1, len(json)):
        if json[i] == '"':
            if in_string:
                if json[i - 1] == "\\":
                    cur += json[i]
                else:
                    key = keyword + str(k)
                    ans += key
                    d[key] = cur
                    k += 1
                    cur = ""
                    in_string = False
            else:
                in_string = True
        elif in_string:
            cur += json[i]
        else:
            ans += json[i]
    return ans, d, keyword


def hydrate_json(json: str, d: Dict[str, str], keyword: str, quotes=True) -> str:
    for k, v in d.items():
        v = yaml_escape(v)
        json = json.replace(k, f'"{v}"' if quotes else v, 1)
    return json
