def extract_python(txt):
    return txt.split('```python')[1].split('```')[0]