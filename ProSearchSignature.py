import dspy

class ProSearchSignature(dspy.Signature):
    """Generate Perplexity-style answer with strict temporal grounding"""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="Markdown formatted response with [N] citations")