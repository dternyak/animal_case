from __future__ import absolute_import

import pytest

from ..animal_case import to_camel_case, to_snake_case, animalify


class TestAnimalCase:

    @pytest.fixture
    def snake_case_list(self):
        return [{
            "first_key": "first value",
            "second_key": "second value",
            "third_key": [
                {"sub_third_key": 1},
                {"sub_third_key2": 2},
                {"sub_third_key3": [
                    {"super_deep": "wow"}
                ]
                }
            ]
        }]

    @pytest.fixture
    def camel_case_list(self):
        return [{
            "firstKey": "first value",
            "secondKey": "second value",
            "thirdKey": [
                {"subThirdKey": 1},
                {"subThirdKey2": 2},
                {"subThirdKey3": [
                    {"superDeep": "wow"}
                ]
                }
            ]
        }]

    @pytest.fixture
    def snake_case_dict(self):
        return {
            "first_key": "first value",
            "second_key": "second value",
            "third_key": [
                {"sub_third_key": 1},
                {"sub_third_key2": 2},
                {"sub_third_key3": [
                    {"super_deep": "wow"}
                ]
                }
            ]
        }

    @pytest.fixture
    def camel_case_dict(self):
        return {
            "firstKey": "first value",
            "secondKey": "second value",
            "thirdKey": [
                {"subThirdKey": 1},
                {"subThirdKey2": 2},
                {"subThirdKey3": [
                    {"superDeep": "wow"}
                ]
                }
            ]
        }

    def test_convert_string_to_snake_case(self):
        str_camel_case = 'myCamelCaseString'

        assert to_snake_case(str_camel_case) == 'my_camel_case_string'

    def test_convert_string_to_camel_case(self):
        str_snake_case = 'str_in_snake_case'

        assert to_camel_case(str_snake_case) == 'strInSnakeCase'

    def test_convert_dict_keys_to_snake_case(self, camel_case_dict):
        converted = animalify(camel_case_dict, 'snake')

        assert 'first_key' in converted
        assert 'second_key' in converted
        assert 'third_key' in converted

        assert 'sub_third_key' in converted['third_key'][0]
        assert 'sub_third_key2' in converted['third_key'][1]
        assert 'sub_third_key3' in converted['third_key'][2]

        assert 'super_deep' in converted['third_key'][2]['sub_third_key3'][0]

    def test_convert_dict_keys_to_camel_case(self, snake_case_dict):
        converted = animalify(snake_case_dict)

        assert 'firstKey' in converted
        assert 'secondKey' in converted
        assert 'thirdKey' in converted

        assert 'subThirdKey' in converted['thirdKey'][0]
        assert 'subThirdKey2' in converted['thirdKey'][1]
        assert 'subThirdKey3' in converted['thirdKey'][2]

        assert 'superDeep' in converted['thirdKey'][2]['subThirdKey3'][0]

    def test_convert_list_of_dict_keys_to_snake_case(self, camel_case_list):
        converted = animalify(camel_case_list, types='snake')[0]

        assert 'first_key' in converted
        assert 'second_key' in converted
        assert 'third_key' in converted

        assert 'sub_third_key' in converted['third_key'][0]
        assert 'sub_third_key2' in converted['third_key'][1]
        assert 'sub_third_key3' in converted['third_key'][2]

        assert 'super_deep' in converted['third_key'][2]['sub_third_key3'][0]

    def test_convert_list_of_dict_keys_to_camel_case(self, snake_case_list):
        converted = animalify(snake_case_list)[0]

        assert 'firstKey' in converted
        assert 'secondKey' in converted
        assert 'thirdKey' in converted

        assert 'subThirdKey' in converted['thirdKey'][0]
        assert 'subThirdKey2' in converted['thirdKey'][1]
        assert 'subThirdKey3' in converted['thirdKey'][2]

        assert 'superDeep' in converted['thirdKey'][2]['subThirdKey3'][0]

    def test_invalid_option_parse_keys(self):
        with pytest.raises(ValueError):
            animalify({}, types='invalid')

    def test_convert_list_of_dict_keyword_args_to_camel_case(self):
        converted = animalify(my_name="daniel", my_title="Software Developer")

        assert 'myName' in converted
        assert 'myTitle' in converted

    def test_convert_list_of_dict_keyword_args_to_snake_case(self):
        converted = animalify(myName="daniel", myTitle="Software Developer", types='snake')

        assert 'my_name' in converted
        assert 'my_title' in converted

    def test_root_level_array_values_dont_fail(self):
        x = {"trustees": ["0x0123"], "nested_key": {"more_stuff": [1, 2, 3]}}
        converted = animalify(x, types='camel')
        assert 'moreStuff' in str(converted)
        assert converted["trustees"] == ["0x0123"]
        assert converted["nestedKey"]["moreStuff"] == [1, 2, 3]

    def test_root_level_tuple_values_dont_fail(self):
        x = {"trustees": ("0x0123"), "nested_key": {"more_stuff": (1, 2, 3)}}
        converted = animalify(x, types='camel')
        assert 'moreStuff' in str(converted)
        assert converted["trustees"] == "0x0123"
        assert converted["nestedKey"]["moreStuff"] == (1, 2, 3)

    def test_convert_dict_keys_to_snake_case_preserve_constant_case(self, camel_case_dict):
        constant_dict = {**camel_case_dict, **{ 'FOURTH_KEY': 4 }}
        constant_dict['thirdKey'].append({ 'SUB_THIRD_KEY_CONSTANT': 4 })
        converted = animalify(constant_dict, 'snake', "^[A-Z0-9_]+$")

        assert 'FOURTH_KEY' in converted
        assert 'SUB_THIRD_KEY_CONSTANT' in converted['third_key'][3]

    def test_convert_dict_keys_to_camel_case_preserve_constant_case(self, snake_case_dict):
        constant_dict = {**snake_case_dict, **{ 'FOURTH_KEY': 4 }}
        constant_dict['third_key'].append({ 'SUB_THIRD_KEY_CONSTANT': 4 })
        converted = animalify(constant_dict, preserve_regex="^[A-Z0-9_]+$")

        assert 'FOURTH_KEY' in converted
        assert 'SUB_THIRD_KEY_CONSTANT' in converted['thirdKey'][3]
