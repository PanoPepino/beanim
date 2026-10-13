"""Safe UTF-8 dictionary IO, resource access and bounded parsed-data cache."""
import ast
from collections.abc import Mapping
from copy import deepcopy
from functools import lru_cache
from importlib.resources import files, as_file
import json
from pathlib import Path
import pprint

def _parse(text, suffix):
    try:
        data = json.loads(text) if suffix == '.json' else ast.literal_eval(text)
    except (ValueError, SyntaxError) as error:
        raise ValueError(f'Invalid dictionary data: {error}') from error
    if not isinstance(data, dict) or not all((isinstance(key, str) for key in data)):
        raise ValueError('Dictionary must map string keys to values')
    return data

@lru_cache(maxsize=128)
def _read_file(filename, size, modified, changed):
    file = Path(filename)
    return _parse(file.read_text(encoding='utf-8'), file.suffix.lower())

@lru_cache(maxsize=3)
def _read_builtin(kind: str) -> dict:
    resource = files('manim_beanim.assets').joinpath('dictionaries', kind + '.json')
    return _parse(resource.read_text(encoding='utf-8'), '.json')

def read_dictionary(source, kind=None):
    if isinstance(source, Mapping):
        data = deepcopy(dict(source))
    elif isinstance(source, str) and source == 'data_base':
        if kind not in {'equations', 'refs', 'tables'}:
            raise ValueError('Unknown built-in dictionary kind')
        data = deepcopy(_read_builtin(kind))
    else:
        file = Path(source).expanduser().resolve()
        stat = file.stat()
        data = deepcopy(_read_file(str(file), stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns))
    if not all((isinstance(key, str) for key in data)):
        raise ValueError('Dictionary keys must be strings')
    return data

def write_dictionary(data, destination):
    file = Path(destination)
    file.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, indent=2) if file.suffix.lower() == '.json' else pprint.pformat(data, sort_dicts=False)
    file.write_text(text + '\n', encoding='utf-8')

def svg_resource(name):
    return as_file(files('manim_beanim.assets').joinpath('svg', name))

def split_dictionary_path(value):
    file = Path(value)
    return ['' if file.parent == Path('.') else str(file.parent), file.name]

def check_file_exists(directory, filename):
    return (Path(directory) / filename).is_file()
