from forecasting_tools import GeneralLlm
import asyncio

def call_metaculus_claude(prompt):
    model = "claude-3-5-sonnet-20240620"
    model = "gpt-4o"
    model = "o3-mini"
    return asyncio.run(GeneralLlm(model=f"metaculus/{model}", temperature=0).invoke(prompt))

if __name__=="__main__":
    import load_secrets
    load_secrets.load_secrets()
    print(call_metaculus_claude("What day is it?"))
