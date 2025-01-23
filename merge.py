# this is the basic structure
from lorax import Client
client = Client("http://127.0.0.1:8080")
prompt = "[INST] Which keyword is used to declare a module in Move? [/INST]"

response = client.generate(
    prompt,
    max_new_tokens=64,
    adapter_id="/adapters",  
    adapter_source="local"   
)
print(response.generated_text)
