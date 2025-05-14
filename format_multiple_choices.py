def format_multiple_choices(choices, multiplier=1, pct = ''):
    return "### Forecast\n\n"+'\n'.join([f'{key}: {multiplier*choices[key]}{pct}' for key in choices.keys()])