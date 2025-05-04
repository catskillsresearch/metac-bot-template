import pandas as pd

def generate_prompt_and_date(row):
    """
    Generates a Perplexity search prompt and date filter from a question row.
    
    Args:
        row (pd.Series): A row from the questions dataframe
        
    Returns:
        tuple: (prompt_text, search_before_date)
    """
    
    # Extract and format dates
    open_time = pd.to_datetime(row['open_time'])
    search_before_date = open_time.strftime('%Y-%m-%d')
    
    # Base prompt structure
    prompt_parts = [
        f"Identify all factual information available as of {open_time.date()} that would help forecast:",
        f"**Question**: {row['title']}",
        f"**Description**: {row['question_description']}",
        f"**Resolution Criteria**: {row['question_resolution_criteria']}"
    ]
    
    # Add fine print if exists
    if row['question_fine_print'] and row['question_fine_print'].strip():
        prompt_parts.append(f"**Fine Print**: {row['question_fine_print']}")
    
    # Add technical specifications
    tech_specs = [
        f"- Question type: {row['question_type']}",
        f"- Measurement unit: {row['question_unit']}",
        f"- Open bounds: [{row['question_scaling_range_min']}, {row['question_scaling_range_max']}]"
    ]
    
    # Add options if present
    if row['question_options'] is not None:
        tech_specs.append(f"- Options: {row['question_options']}")
    
    # Add group variable if specified
    if row['question_group_variable']:
        tech_specs.append(f"- Group variable: {row['question_group_variable']}")
    
    prompt_parts.append("**Technical Specifications**:\n" + "\n".join(tech_specs))
    
    # Final instructions
    prompt_parts.extend([
        "\nProvide:",
        "1. Key historical trends and current status relevant to the metric",
        "2. Recent announcements/policies affecting the metric",
        "3. Authoritative sources for verification",
        "4. Any limitations or uncertainties in measurement"
        "\n**Format your response in markdown, using in-text citations like [1], [2], etc. At the end of your answer, include a section titled 'References' listing each source cited, in markdown list format, matching the in-text citation numbers.**\n"
    ])
    
    return "\n".join(prompt_parts), search_before_date