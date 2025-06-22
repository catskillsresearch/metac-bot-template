def format_multiple_choices(choices, multiplier=1, pct = '', prefix = ''):
    return "### Forecast\n\n"+'\n'.join([f'{prefix}{key}: {multiplier*choices[key]}{pct}' for key in choices.keys()])