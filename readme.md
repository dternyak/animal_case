# Animal case convert recursively your dict/json keys to camelCase or snakeCase.

Based on https://github.com/rafa-acioly/animal_case

> Most commonly used to build proxies when we need to create communication between apis
that have different syntaxes on their endpoint.

Imagine that you have to make a `get` request on some endpoint and send a `post` request to another endpoint with some mutate data comming from the first request but each of there endpoints have differents `json` key sintaxies, now you have to convert all the keys recursively and the hell begins...fear no more my friend.

## Release
```bash
python setup.py sdist
twine upload dist/*
```

## Tests

```bash
source venv/bin/activate # assumes you have a virtualenv `venv` installed with required packages
pytest tests
```

## Usage:


### Converting dict keys recursively
By default `parse_keys` convert keys to `snake_case`
```py
from animal_case.convert import parse_keys

my_dict = {
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

converted = parse_keys(my_dict)
# output
'''
{
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
'''
```


```py
from animal_case.convert import parse_keys

my_dict = {
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

converted = parse_keys(my_dict, type='camel')
# output
'''
{
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
'''
```

### snake case
```py
from animal_case.convert import to_snake_case

converted = to_snake_case('myRandomString')
print(converted) # output: my_random_string
```

### camel case
```py
from animal_case.convert import to_camel_case

converted = to_camel_case('my_random_string')
print(converted) # output: myRandomString
```

### preserve regex

If you'd like to keep some keys from being converted, you can pass `preserve_regex`
to any of the methods. For example, if you wanted to preserve `CONSTANT_CASE`,
you would do

```py
from animal_case.convert import to_snake_case

converted = to_snake_case('CONSTANT_CASE', preserve_regex="^[A-Z0-9_]+$")
print(converted # output: CONSTANT_CASE
```
