# https://github.com/rafa-acioly/animal_case
import re

def _unpack(data):
    if isinstance(data, dict):
        return data.items()
    return data

def to_snake_case(value, preserve_regex=None):
    """
    Convert camel case string to snake case
    :param value: string
    :return: string
    """
    if preserve_regex and re.search(preserve_regex, value):
        return value
    first_underscore = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', first_underscore).lower()


def keys_to_snake_case(content, preserve_regex=None):
    """
    Convert all keys for given dict to snake case
    :param content: dict
    :return: dict
    """
    return {
        to_snake_case(key, preserve_regex=preserve_regex): value for key, value in _unpack(content)
    }


def to_camel_case(value, preserve_regex=None):
    """
    Convert the given string to camel case
    :param value: string
    :return: string
    """
    if preserve_regex and re.search(preserve_regex, value):
        return value
    content = value.split('_')
    return content[0] + ''.join(word.title() for word in content[1:] if not word.isspace())


def keys_to_camel_case(content, preserve_regex=None):
    """
    Convert all keys for given dict to camel case
    :param content: dict
    :return: dict
    """
    return {
        to_camel_case(key, preserve_regex=preserve_regex): value for key, value in _unpack(dict(content))
    }


def animalify(*args, **kwargs):
    """
    Convert all keys for given dict/list to snake case recursively
    the main type are 'snake' and 'camel'
    :return: dict/list

    """
    types = 'camel'
    preserve_regex = None

    if len(args) > 3:
        raise ValueError("Invalid number of arguments")

    if len(args) >= 2:
        types = args[1]
    
    if len(args) == 3:
        preserve_regex = args[2]
        

    if kwargs.get('types'):
        types = kwargs.get('types')
        del kwargs['types']

    if kwargs.get('preserve_regex'):
        preserve_regex = kwargs.get('preserve_regex')
        del kwargs['preserve_regex']

    if types not in ('snake', 'camel'):
        raise ValueError("Invalid parse type, use snake or camel")

    if args and kwargs:
        raise TypeError('animalify() behavior undefined when passed both args and kwargs')

    if args:
        data = args[0]
    else:
        data = kwargs

    if type(data) == list:
        formatted = []
    elif type(data) == dict:
        formatted = {}
    else:
        return data

    formatter = keys_to_snake_case if types == 'snake' else keys_to_camel_case

    if type(data) == dict:
        for key, value in _unpack(formatter(data, preserve_regex=preserve_regex)):
            if isinstance(value, dict):
                formatted[key] = animalify(value, types, preserve_regex)
            elif isinstance(value, list) and len(value) > 0:
                formatted[key] = []
                for _, val in enumerate(value):
                    formatted[key].append(animalify(val, types, preserve_regex))
            else:
                formatted[key] = value
        return formatted

    else:
        for i, each in enumerate(data):
            if isinstance(each, dict):
                formatted.append(animalify(each, types, preserve_regex))
            elif isinstance(each, list) and len(each) > 0:
                formatted.append([])
                for _, val in enumerate(each):
                    formatted[i].append(animalify(val, types, preserve_regex))
            else:
                formatted.append(each)
        return formatted
