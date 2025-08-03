import ollama

client = ollama.Client()

model = "llama3.2"
prompt = "what is python"

response = client.generate(model=model, prompt=prompt)

print(response.response)