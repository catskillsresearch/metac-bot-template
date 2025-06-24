import dspy, pickle, os
import pandas as pd
from datetime import datetime
from pathlib import Path
from generate_prompt_and_date import generate_prompt_and_date
from ProSearchSignature import ProSearchSignature
from call_local_llm import call_local_llm
class ResearchProModule(dspy.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.generate = dspy.ChainOfThought(ProSearchSignature)
    
    def process_dataframe(self, df, use_cutoff = True, output_dir="research"):
        """Process all rows in dataframe and save results"""
        Path(output_dir).mkdir(exist_ok=True)
        
        for idx, row in df.iterrows():
            path = Path(output_dir) / f"{row['id_of_question']}.md"
            if path.exists():
                continue
            print(f"processing post_id {row.id_of_post} question_id {row.id_of_question} title {row.title}")

            # Generate question and cutoff date from row
            question, cutoff_date = generate_prompt_and_date(row)
            cutoff_date = cutoff_date if use_cutoff else None
            
            # Get answer from Perplexity
            with open('foo.txt', 'w') as f:
                f.write(question)
            answer = self.get_answer(question)

            # Save to file
            self.save_answer(row['id_of_question'], answer, output_dir)
      
    def get_answer(self, question):
        """Get answer for a single question"""
        return call_local_llm(question, self.model)
    
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
    with open('foo.pkl', 'rb') as f:
        (question, cutoff_date) = pickle.load(f)
    use_cutoff=False
    bot = ResearchProModule('gemma3:latest')
    answer = bot.get_answer(question, cutoff_date)
    print(answer)
