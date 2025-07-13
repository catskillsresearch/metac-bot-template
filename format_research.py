def format_research(source_summaries):
    """Collect source summaries into block"""
    research = []
    for i, summary in enumerate(source_summaries):
        item = f"""```research_summary_{i}
{summary}
```"""
        research.append(item)
    research = '\n'.join(research)
    return research