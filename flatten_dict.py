def flatten_dict(d, parent_key='', sep='.'):
    """
    Flatten a nested dictionary.

    Args:
        d (dict): The dictionary to flatten.
        parent_key (str): The base key string for recursion (used internally).
        sep (str): Separator between keys.

    Returns:
        dict: A flattened dictionary with dot-separated keys.
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
