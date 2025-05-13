def load_research(row):
    with open(f"research/{row['id_of_question']}.md", 'r') as f:
        return f.read()
