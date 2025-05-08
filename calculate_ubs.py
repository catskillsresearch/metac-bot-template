def calculate_ubs_binary(instance):
    """
    Calculate Universal Binarized Score (UBS) for a binary question forecast.

    Args:
        instance: Object with:
            - prediction (int/float): Forecast probability for 'yes' (0-100)
            - question_resolution (str): Actual outcome ('yes' or 'no')

    Returns:
        float: UBS score between 0 (worst) and 1 (best)
    """
    # Convert prediction to probability (0.0-1.0 scale)
    p_yes = instance.prediction / 100.0
    p_no = 1.0 - p_yes

    # Convert resolution to binary (1.0 for 'yes', 0.0 for 'no')
    resolution = instance.question_resolution.lower()
    y_yes = 1.0 if resolution == 'yes' else 0.0
    y_no = 1.0 - y_yes

    # Calculate Brier Score (sum of squared errors for both outcomes)
    brier_score = (p_yes - y_yes)**2 + (p_no - y_no)**2

    # Universal Binarized Score (UBS)
    K_max = 2.0  # Maximum possible Brier Score for binary questions
    ubs = 1.0 - (brier_score / K_max)

    return round(ubs, 4)  # Rounded to 4 decimal places for readability

def calculate_ubs_numeric(instance):
    """
    Calculate Universal Binarized Score (UBS) for numeric forecasts using CRPS.

    Args:
        instance: Object with:
            - prediction (dict): Percentile-to-value mapping (e.g., {10: 1600000, ...})
            - question_resolution (float): Actual resolved value

    Returns:
        float: UBS score between 0 (worst) and 1 (best)
    """
    percentiles = sorted(instance.prediction.keys())
    values = [float(instance.prediction[p]) for p in percentiles]
    if instance.question_resolution == "below_lower_bound":
        Q = instance.question_scaling_range_min
    elif instance.question_resolution == "above_upper_bound":
        Q = instance.question_scaling_range_max
    else:
        Q = float(instance.question_resolution)
    min_val, max_val = values[0], values[-1]

    # Linear interpolation for CDF
    def cdf(x):
        if x <= min_val: return 0.0
        if x >= max_val: return 1.0
        for i in range(len(values)-1):
            if values[i] <= x < values[i+1]:
                p_low = percentiles[i]/100
                p_high = percentiles[i+1]/100
                return p_low + (x - values[i]) * (p_high - p_low)/(values[i+1] - values[i])
        return 0.0

    # CRPS calculation
    crps = 0.0
    for i in range(len(values)-1):
        v1, v2 = values[i], values[i+1]
        mid = (v1 + v2)/2
        F_mid = cdf(mid)
        I_mid = 1.0 if mid >= Q else 0.0
        crps += (F_mid - I_mid)**2 * (v2 - v1)

    # Tail contributions
    if Q < min_val:
        crps += (0.0 - 1.0)**2 * (min_val - Q)
    elif Q > max_val:
        crps += (1.0 - 0.0)**2 * (Q - max_val)

    # Normalize using question's intrinsic range
    K_max = max_val - min_val
    ubs = 1.0 - (crps / K_max) if K_max != 0 else 0.0
    return max(0.0, min(1.0, round(ubs, 4)))

def calculate_ubs_multiclass(instance):
    """
    Calculate Universal Binarized Score (UBS) for a multi-category question.

    Args:
        instance: Object with:
            - prediction (dict): {category: percentage forecast (0-100)}
            - question_resolution (str): The correct category

    Returns:
        float: UBS score between 0 (worst) and 1 (best)
    """
    categories = list(instance.prediction.keys())
    n = len(categories)
    # Convert predictions to probabilities (0.0-1.0)
    probs = {k: instance.prediction[k]/100.0 for k in categories}
    # Create outcome vector: 1 for correct, 0 for others
    outcome = {k: 1.0 if k == instance.question_resolution else 0.0 for k in categories}
    # Multi-category Brier score
    brier = sum((probs[k] - outcome[k])**2 for k in categories)
    # Normalize by maximum possible score (which is n)
    ubs = 1.0 - (brier / n)
    return max(0.0, min(1.0, round(ubs, 4)))

def calculate_ubs(question):
    method = {'binary': calculate_ubs_binary,
              'numeric': calculate_ubs_numeric,
              'multiple_choice': calculate_ubs_multiclass}
    return method[question.question_type](question)
