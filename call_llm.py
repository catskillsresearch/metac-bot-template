import ollama

def call_llm(prompt, conversation, model = 'Qwen3:32b-q4_K_M'):
    # Add system message if missing
    if not any(msg['role'] == 'system' for msg in conversation):
        conversation.insert(0, {"role": "system", "content": "You are a helpful assistant."})
    conversation.append({"role": "user", "content": prompt})
    reply = ollama.chat(model=model, messages=conversation)
    answer = reply.message.content
    conversation.append({"role": "assistant", "content": answer})
    return answer

if __name__ == "__main__":
    conversation = []
    print(call_llm("Hello, how are you?", conversation))
    print(call_llm("What's the weather today?", conversation))
