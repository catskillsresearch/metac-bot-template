def standardize_cdf(cdf: list[float], question_data: dict) -> list[float]:
    """
    Takes a cdf and returns a standardized version of it

    - assigns no mass outside of closed bounds (scales accordingly)
    - assigns at least a minimum amount of mass outside of open bounds
    - increasing by at least the minimum amount (0.01 / 200 = 0.0005)

    TODO: add smoothing over cdfs that spike too heavily (exceed a change of 0.59)
    """
    lower_open = question_data["open_lower_bound"]
    upper_open = question_data["open_upper_bound"]

    scale_lower_to = 0 if lower_open else cdf[0]
    scale_upper_to = 1.0 if upper_open else cdf[-1]
    rescaled_inbound_mass = scale_upper_to - scale_lower_to

    def standardize(F: float, location: float) -> float:
        # `F` is the height of the cdf at `location` (in range [0, 1])
        # rescale
        rescaled_F = (F - scale_lower_to) / rescaled_inbound_mass
        # offset
        if lower_open and upper_open:
            return 0.988 * rescaled_F + 0.01 * location + 0.001
        elif lower_open:
            return 0.989 * rescaled_F + 0.01 * location + 0.001
        elif upper_open:
            return 0.989 * rescaled_F + 0.01 * location
        return 0.99 * rescaled_F + 0.01 * location

    standardized_cdf = []
    for i, F in enumerate(cdf):
        standardized_F = standardize(F, i / (len(cdf) - 1))
        # round to avoid floating point errors
        standardized_cdf.append(round(standardized_F, 10))

    return standardized_cdf