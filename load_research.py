def load_research(row):
    with open(f"research/{row['id']}.md", 'r') as f:
        return f.read()
