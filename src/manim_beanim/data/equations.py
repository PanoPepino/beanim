"""Extract labelled equation environments without changing mathematical content."""
import re
from pathlib import Path

def _remove_metadata(text):
    pattern = re.compile('\\\\(?:label|tag)\\s*\\{')
    while (match := pattern.search(text)) is not None:
        depth = 1
        end = match.end()
        while end < len(text) and depth:
            if text[end] in '{}' and (end == 0 or text[end - 1] != '\\'):
                depth += 1 if text[end] == '{' else -1
            end += 1
        if depth:
            raise ValueError('Unclosed label/tag argument')
        text = text[:match.start()] + text[end:]
    return text

def parse_equations(tex_file):
    """Return label-to-LaTeX mapping. Supports equation and equation* environments."""
    source = Path(tex_file).read_text(encoding='utf-8')
    source = re.sub('(?<!\\\\)%[^\\n]*', '', source)
    equations = {}
    for match in re.finditer('\\\\begin\\{(equation\\*?)\\}(.*?)\\\\end\\{\\1\\}', source, re.DOTALL):
        body = match.group(2)
        labels = re.findall('\\\\label\\{([^}]+)\\}', body)
        if not labels or re.search('\\\\begin\\{align\\b', body):
            continue
        label = labels[0]
        if label in equations:
            raise ValueError(f'Duplicate equation label: {label}')
        equations[label] = ' '.join(_remove_metadata(body).strip().split())
    return equations
