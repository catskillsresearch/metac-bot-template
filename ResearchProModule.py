import dspy
import os
from datetime import datetime

class ProSearchSignature(dspy.Signature):
    """Generate Perplexity-style answer with strict temporal grounding"""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="Markdown formatted response with [N] citations")

class ResearchProModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate = dspy.ChainOfThought(ProSearchSignature)
    
    def forward(self, question, cutoff_date=None):
        # Configure API parameters
        api_config = {
            "model": "sonar-pro",
            "search_focus": "internet",
            "temperature": 0.2,
            "max_tokens": 2000
        }
        
        if cutoff_date:
            # Convert to Perplexity's required format
            pplx_date = datetime.strptime(cutoff_date, "%Y-%m-%d").strftime("%m/%d/%Y")
            api_config["search_before_date_filter"] = pplx_date
            
            # Update question with cutoff context
            question += f" [Knowledge cutoff: {pplx_date}]"

        # Create LM with temporal filtering
        lm = dspy.LM(
            base_url="https://api.perplexity.ai",
            api_key=os.getenv("PERPLEXITY_API_KEY"),
            **api_config
        )

        # System prompt to enforce temporal constraints
        system_prompt = (
            "You are a research assistant with knowledge up to {cutoff}. "
            "Answer using ONLY information available before {cutoff}. "
            "Format response in markdown with citations. NEVER mention post-cutoff dates."
        ).format(cutoff=pplx_date if cutoff_date else "the current date")

        with dspy.context(lm=lm):
            response = self.generate(
                question=system_prompt + "\n\n" + question
            )
            
        return response.answer

# Usage Test
if __name__ == "__main__":

    from load_secrets import load_secrets
    load_secrets()

    bot = ResearchProModule()
    
    # Test 1: Temporal query with cutoff
    result = bot(
        question="Is tomorrow a Saturday?",
        cutoff_date="2025-03-02"  # Should NOT know about May dates
    )
    print(result)
