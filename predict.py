import os
from combined_forecast import combined_forecast

def predict(dfn, question, iterations = 3):
    ffn = f'{dfn}/{question.id_of_question}.md'
    
    # New: Check for existing RAG context in learning field
    if hasattr(question, 'learning') and len(question.learning) > 0:
        if os.path.exists(ffn):
            os.remove(ffn)  # Force regeneration
    
    if os.path.exists(ffn):
        with open(ffn, 'r') as f:
            return f.read()
    else:
        # Generate new forecast
        api_key = os.getenv('PERPLEXITY_API_KEY')
        forecast = combined_forecast(question, iterations)
        with open(ffn, 'w') as f:
            f.write(forecast)
        return forecast