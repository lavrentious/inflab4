import unittest
import json
from t3 import Parser


class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = Parser()

    def test_valid_1(self):
        data = """
        {
            "string": "Hello, World!",
            "emptyString": "",
            "number": 42,
            "negativeNumber": -17,
            "float": 3.14159,
            "booleanTrue": true,
            "booleanFalse": false,
            "nullValue": null,
            "array": [1, 2, 3, "four", 5.5, true, false, null, [], {}],
            "emptyArray": [],
            "object": {
                "key1": "value1",
                "key2": 42,
                "key3": true,
                "key4": false,
                "key5": null,
                "emptyArray": [],
                "emptyObject": {}
            }
        }
        """
        self.assertDictEqual(self.parser.parse(data), json.loads(data))

    def test_valid_2(self):
        data = """
        {
            "string_example": "This is a string",
            "number_example": 42.5,
            "boolean_example": true,
            "null_example": null,
            "array_example": [1, 2, 3, "four", true, false, null],
            "object_example": {
                "key_with_space": "value with space",
                "nested_object": {
                "empty_object": {},
                "empty_array": []
                },
                "unicode_example": "Unicode characters: \u00A9 \u0041 \u0031"
            }
        }
        """
        self.assertDictEqual(self.parser.parse(data), json.loads(data))
        self.assertDictEqual(self.parser.parse(data), json.loads(data))

    def test_valid_3(self):
        data = """
        {
            "glossary": {
                "title": "example glossary",
                "GlossDiv": {
                    "title": "S",
                    "GlossList": {
                        "GlossEntry": {
                            "ID": "SGML",
                            "SortAs": "SGML",
                            "GlossTerm": "Standard Generalized Markup Language",
                            "Acronym": "SGML",
                            "Abbrev": "ISO 8879:1986",
                            "GlossDef": {
                                "para": "A meta-markup language, used to create markup languages such as DocBook.",
                                "GlossSeeAlso": ["GML", "XML"]
                            },
                            "GlossSee": "markup"
                        }
                    }
                }
            }
        }
        """
        self.assertDictEqual(self.parser.parse(data), json.loads(data))


if __name__ == "__main__":
    unittest.main()
