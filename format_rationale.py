def format_rationale(right, wrong, sources):
    return f"""
Reasons I am right
==================
{right}

Reasons I may be wrong
======================
{wrong}

Sources
=======
{'\n'.join(sources)}"""