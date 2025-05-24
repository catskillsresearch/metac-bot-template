import dspy, os, pickle
from datetime import datetime
from ResearchProModule import ResearchProModule
from RAGForecaster import RAGForecaster

class EnhancedResearchPro(ResearchProModule):
    def __init__(self, rag_forecaster):
        super().__init__()
        self.rag = rag_forecaster
        self.retrieval_cache = {}
        self._last_index_mtime = 0
        self._last_metadata_mtime = 0

    def refresh_if_needed(self):
        """Hot-reload if files changed"""
        if self.rag.check_for_updates():
            print(f"Detected RAG file updates at {datetime.now()}")
            self.rag = RAGForecaster()
            self.retrieval_cache.clear()  # Clear stale context
        
    def get_answer(self, question, cutoff_date=None):
        # Retrieve similar historical forecasts
        cached = self.retrieval_cache.get(question)
        if not cached:
            with open('question.pkl', 'wb') as f:
                pickle.dump(question, f)
            context, _ = self.rag.retrieve_context(question)
            cached = self._format_context(context)
            self.retrieval_cache[question] = cached
            
        # Dynamic temperature scaling
        temp = 0.2 + (1 - len(context)/3)*0.5 if context else 0.7
        temp = min(0.7, max(0.1, temp))
        
        # Enhanced system prompt
        system_prompt = f"""You are a forecasting analyst. Use this historical context:
{cached}

1. Compare current situation to reference cases
2. Note key differences affecting the forecast
3. Generate adjusted probabilistic assessment"""
        
        # Modified API config
        api_config = {
            "model": "sonar-pro",
            "search_focus": "internet",
            "temperature": temp,
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

        full_system_prompt = (
            f"{system_prompt}\n"
            "Format your response in markdown with citations. "
            "Include a 'References' section listing sources."
        )

        with dspy.context(lm=lm):
            response = self.generate(question=full_system_prompt + "\n\n" + question)
            
        return response.answer
        
    def _format_context(self, context):
        if not context or len(context[0]) == 0:
            return "No historical context available"

        bits = []
        for i, (m, sim) in enumerate(context):
            bits.append(f"• Reference {i+1} (similarity: {sim:.2f}): {m['id_of_question']}")
            
        result = "\n".join(bits)

        return result 

if __name__=="__main__":
    rag = RAGForecaster()
    research_bot = EnhancedResearchPro(rag)
    import pandas as pd
    df = pd.read_json('debug.json')
    research_bot.process_dataframe(df, use_cutoff=False)

    
