import dspy
import os
import pandas as pd
from datetime import datetime
from pathlib import Path
from generate_prompt_and_date import generate_prompt_and_date
from ProSearchSignature import ProSearchSignature

class ResearchProModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate = dspy.ChainOfThought(ProSearchSignature)
    
    def process_dataframe(self, df, use_cutoff = True, output_dir="research"):
        """Process all rows in dataframe and save results"""
        Path(output_dir).mkdir(exist_ok=True)
        
        for idx, row in df.iterrows():
            path = Path(output_dir) / f"{row['id_of_question']}.md"
            if path.exists():
                continue
            print("processing", row['id_of_question'], row['title'])

            # Generate question and cutoff date from row
            question, cutoff_date = generate_prompt_and_date(row)
            cutoff_date = cutoff_date if use_cutoff else None
            
            # Get answer from Perplexity
            answer = self.get_answer(question, cutoff_date)
            
            # Save to file
            self.save_answer(row['id_of_question'], answer, output_dir)
      
    def get_answer(self, question, cutoff_date=None):
        """Get answer for a single question"""
        api_config = {
            "model": "sonar-pro",
            "search_focus": "internet",
            "temperature": 0.2,
            "max_tokens": 2000
        }
        
        if cutoff_date:
            pplx_date = datetime.strptime(cutoff_date, "%Y-%m-%d").strftime("%m/%d/%Y")
            api_config["search_before_date_filter"] = pplx_date
            question += f" [Knowledge cutoff: {pplx_date}]"

        lm = dspy.LM(
            base_url="https://api.perplexity.ai",
            api_key=os.getenv("PERPLEXITY_API_KEY"),
            **api_config
        )

        system_prompt = (
            "You are a research assistant with knowledge up to {cutoff}. "
            "Answer using ONLY information available before {cutoff}. " if cutoff_date else ''
            "Format your response in markdown, using in-text citations like [1], [2], etc. "
            "At the end of your answer, include a section titled 'References' listing each source cited, in markdown list format, matching the in-text citation numbers, with each entry as: [number]. [Title] ([URL]). If a URL is not available, just include the title."            
            "NEVER mention post-cutoff dates."
        ).format(cutoff=pplx_date if cutoff_date else "the current date")

        with dspy.context(lm=lm):
            cmd = system_prompt + "\n\n" + question
            response = self.generate(question=cmd)
        return response.answer
    
    def save_answer(self, question_id, content, output_dir):
        """Save answer to research/{id}.txt"""
        path = Path(output_dir) / f"{question_id}.md"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Saved research for question {question_id}")

# Updated Usage
if __name__ == "__main__":
    from load_secrets import load_secrets
    load_secrets()

    # Load your dataframe (example)
    df = pd.read_json("resolved.json")  # Update with your actual dataframe
    
    bot = ResearchProModule()
    bot.process_dataframe(df)
