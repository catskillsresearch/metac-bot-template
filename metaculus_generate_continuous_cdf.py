def metaculus_generate_continuous_cdf(
    percentiles: dict,
    question_data: dict,
    below_lower_bound: float = None,
    above_upper_bound: float = None,
) -> list[float]:
    """
    Takes a set of percentiles and returns a corresponding cdf with 201 values

    Param: percentiles
    dict[str, float | str]
    keys must terminate in a number interpretable as a float in range (0, 100)
      optionally preceded by an underscore "_"
    values must be a nominal value in the scale of the question, either
      interpretable as a float (for "numeric" type questions) or a datetime in
      ISO format (for "date" type questions)
    example percentiles:
    percentiles = {
      "percentile_01": 25,
      "precentile_25.123": 500,
      "50": 650,
      "percentile_75": "700",
      "percentile_99": 990,
    }
    optionally, include `below_lower_bound` and `above_upper_bound`
    to indicate the amount of probability mass assigned to those locations
    percentiles = {
      "percentile_25": 500,
      "percentile_50": 650,
      "percentile_75": 700,
    }
    below_lower_bound = 0.0025,
    above_upper_bound = 0.009,

    If the percentile locations don't encompass
      [scaling["range_min"], scaling["range_max"]]
    and "below_lower_bound"/"above_upper_bound" aren't provided,
    then the prediction can't be interpreted as a cdf properly.
    Note that range_min/range_max for date questions are unix timestamps.
    """

    # This will be the set of (x, y) points that are the set points
    # of the cdf
    percentile_locations = []

    # take the given boundary values
    if below_lower_bound is not None:
        percentile_locations.append((0.0, below_lower_bound))
    if above_upper_bound is not None:
        percentile_locations.append((1.0, 1 - above_upper_bound))

    # generate the remaining set of points
    for percentile, nominal_location in percentiles.items():
        height = float(str(percentile).split("_")[-1]) / 100
        location = nominal_location_to_cdf_location(nominal_location, question_data)
        percentile_locations.append((location, height))

    # sort to ensure lookup works
    percentile_locations.sort()

    # check validity
    first_point, last_point = percentile_locations[0], percentile_locations[-1]
    if (first_point[0] > 0.0) or (last_point[0] < 1.0):
        raise ValueError("Percentiles must encompass bounds of the question")

    def get_cdf_at(location):
        # helper function that takes a location and returns
        # the height of the cdf at that location, linearly
        # interpolating between values
        previous = percentile_locations[0]
        for i in range(1, len(percentile_locations)):
            current = percentile_locations[i]
            if previous[0] <= location <= current[0]:
                return previous[1] + (current[1] - previous[1]) * (
                    location - previous[0]
                ) / (current[0] - previous[0])
            previous = current

    # generate that cdf
    continuous_cdf = [get_cdf_at(i / 200) for i in range(201)]
    return continuous_cdf