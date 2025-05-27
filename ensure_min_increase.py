def ensure_min_increase(lst, min_step=5e-05):
    """
    Ensure each element in the list is at least `min_step` greater than the previous.
    If not, set it to previous + min_step.
    
    Args:
        lst (list of float): Input list of floats.
        min_step (float): Minimum required increase between elements.
        
    Returns:
        list of float: Adjusted list with minimum step enforced.
    """
    if not lst:
        return []
    result = [lst[0]]
    for num in lst[1:]:
        prev = result[-1]
        if num < prev + min_step:
            result.append(prev + min_step)
        else:
            result.append(num)
    return result

if __name__=="__main__":
    # Example usage:
    original = [0.0, 0.00001, 0.0001, 0.00011, 0.00015]
    adjusted = ensure_min_increase(original)
    print("Original:", original)
    print("Adjusted:", adjusted)
