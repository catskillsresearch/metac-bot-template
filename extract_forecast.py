import re

def extract_probability(question):
    text = question.forecast
    # Regex to find 'Probability: XX%' or 'Probability: XX'
    text = text.replace('**', '')
    pattern = r"Probability: (\d+)%?"
    match = re.search(pattern, text)
    if match:
        return int(match.group(1))/100.0
    return 0.5

def extract_percentiles0(question):
    text = question.forecast
    # Regex to find lines like 'Percentile X: number'
    pattern = r"Percentile (\d+): ([\d,]+)"
    matches = re.findall(pattern, text)
    # Convert to dict with integer keys and values (remove commas)
    percentiles = {int(p): int(v.replace(',', '')) for p, v in matches}
    return percentiles

def linear_sample_percentiles(range_min, range_max):
    percentiles = [10, 20, 40, 60, 80, 90]
    fractions = [p / 100 for p in percentiles]
    samples = {int(f*100): range_min + f * (range_max - range_min) for f in fractions}
    return samples

def extract_percentiles1(question):
    text = question.forecast
    return linear_sample_percentiles(question.question_scaling_range_max, question.question_scaling_range_min)

def extract_percentiles2(question):
    text = question.forecast
    # Regex to capture percentage AFTER '+' and before '%', ignoring other numbers
    pattern = r"Percentile\s*(\d+):\s*.*?([+-]\s*)?(\d*\.?\d+)%"
    matches = re.findall(pattern, text)
    # Extract percentile and percentage value (ignore operator like '+')
    percentiles = {int(p): float(percent) for p, _, percent in matches}
    return percentiles

def extract_percentiles3(question):
    text = question.forecast
    # Regex handles commas and variable whitespace
    pattern = r"Percentile\s*(\d+):\s*([\d,]+)"
    matches = re.findall(pattern, text)
    return {int(p): int(v.replace(',', '')) for p, v in matches}

def extract_percentiles4(question):
    text = question.forecast
    # Regex to capture percentile lines with flexible formatting
    pattern = r"Percentile\s*(\d+):\s*([^\n]+)"
    matches = re.findall(pattern, text)

    percentiles = {}
    for p, val_str in matches:
        p = int(p)
        val_str = val_str.strip()

        # Check for percentage format (e.g., "S₀ + 0.5%")
        if '%' in val_str:
            pct_match = re.search(r"(\d+\.?\d+)%", val_str.replace(',', ''))
            if pct_match:
                percentiles[p] = float(pct_match.group(1))
        # Check for absolute numeric format (e.g., "1,600,000")
        else:
            num_match = re.search(r"[\d,]+", val_str)
            if num_match:
                percentiles[p] = int(num_match.group(0).replace(',', ''))

    return percentiles

def extract_percentiles(question):
    tries = [f(question) for f in [extract_percentiles0, extract_percentiles3]]
    lengths = [len(x) for x in tries]
    maxlength = max(lengths)
    if maxlength > 0:
        for x in tries:
            if len(x) == maxlength:
                return x
    return extract_percentiles1(question)

def extract_probabilities(text, question_options, prefix='Option_[A-Z]:'):
    # Regex to capture "Option_X: [label]: [percentage]%"
    pattern = prefix + r"\s*([^:]+?)\s*:\s*\**(\d+)%\**"
    matches = re.findall(pattern, text)

    # Convert to dictionary with percentage values
    prob_map = {}
    for label, pct_str in matches:
        label = label.strip()
        if label in question_options:
            prob_map[label] = int(pct_str) / 100.0

    # Ensure all question options are in the map (0% if missing)
    for option in question_options:
        if option not in prob_map:
            prob_map[option] = 0.0

    return prob_map

def extract_multiple_choice(question):
    text, question_options = question.forecast, eval(question.question_options)
    if 'Option_' in text:
        return extract_probabilities(text, question_options)
    else:
        return extract_probabilities(text, question_options, '')

def extract_forecast(question):
    method = {'binary': extract_probability,
              'numeric': extract_percentiles,
              'multiple_choice': extract_multiple_choice}
    return method[question.question_type](question)
