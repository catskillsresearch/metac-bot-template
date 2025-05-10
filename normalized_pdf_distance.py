import bisect

def normalized_pdf_distance(F1, F2):
    # Define percentiles and extract values
    percentiles = [10, 20, 40, 60, 80, 90]
    x1 = [F1[p] for p in percentiles]
    x2 = [F2[p] for p in percentiles]
    
    # Create merged breakpoints
    all_x = sorted(list(set(x1 + x2)))
    total_area = 0.0

    # Process each interval between consecutive x-values
    for i in range(len(all_x)-1):
        a, b = all_x[i], all_x[i+1]
        width = b - a
        
        # Calculate PDF for F1
        if a >= x1[-1] or b <= x1[0]:
            pdf1 = 0.0
        else:
            idx = bisect.bisect_right(x1, a) - 1
            if idx < 0:
                pdf1 = 0.0
            else:
                p_low = percentiles[idx]
                p_high = percentiles[idx+1]
                x_low = x1[idx]
                x_high = x1[idx+1]
                pdf1 = (p_high - p_low) / (100 * (x_high - x_low)) if x_high != x_low else 0

        # Calculate PDF for F2
        if a >= x2[-1] or b <= x2[0]:
            pdf2 = 0.0
        else:
            idx = bisect.bisect_right(x2, a) - 1
            if idx < 0:
                pdf2 = 0.0
            else:
                p_low = percentiles[idx]
                p_high = percentiles[idx+1]
                x_low = x2[idx]
                x_high = x2[idx+1]
                pdf2 = (p_high - p_low) / (100 * (x_high - x_low)) if x_high != x_low else 0

        total_area += abs(pdf1 - pdf2) * width

    # Normalize by maximum possible area (2 for complete divergence)
    return total_area / 2
