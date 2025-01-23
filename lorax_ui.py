import gradio as gr
import os
from lorax import Client
import sys
from datetime import datetime

class Logger:
    def __init__(self):
        self.logs = []

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        return "\n".join(self.logs)

logger = Logger()

css = r"""
.logo-text {
    font-size: 30px;
    color: #ff6600;
    font-weight: bold;
    display: inline-block;
    vertical-align: middle;
    position: absolute;
    inset: 0;
    display: flex;
    justify-content: center;
        align-items: center;
}

.logo-container {
    display: flex;
    align-items: center; /* Centers logo and text vertically */
    justify-content: space-between; /* Adjust spacing */
    padding: 10px; /* Adds some spacing around the container */
    background-color: transparent; /* Light background for better contrast */
    position: relative;
}

.logo-image {
    height: 50px;
    margin-right: 10px;
}
"""

only_html = '''
   <div id="web3auth-container" class="logo-container">
       <img class="logo-image" src="https://cdn.openledger.xyz/logo-orange.png" alt="openledger-logo">
       <span class="logo-text">Model Multiplexer</span>
   </div>
'''

client = Client("http://127.0.0.1:8080")

BASE_MODELS = {
    "Mistral-7B-Instruct-v0.1": "mistralai/Mistral-7B-Instruct-v0.1",
    "Meta-Llama-3.2-1B":"meta-llama/Llama-3.2-1B",
}

def get_local_adapters(base_path="/home/ubuntu/Apps/LLamafactory-web3/saves"):
    adapters = {}
    if os.path.exists(base_path):
        for model_dir in os.listdir(base_path):
            model_path = os.path.join(base_path, model_dir, "lora")
            if os.path.exists(model_path):
                for adapter_dir in os.listdir(model_path):
                    adapter_path = os.path.join(model_path, adapter_dir)
                    if os.path.exists(os.path.join(adapter_path, "adapter_config.json")):
                        adapters[adapter_dir] = adapter_path
    return adapters

LOCAL_ADAPTERS = get_local_adapters()

def generate_response(model_name, adapter_name, prompt, max_tokens=64):
    try:
        logger.log(f"Selected model: {model_name}")
        logger.log(f"Selected adapter: {adapter_name}")
        logger.log(f"Prompt: {prompt}")
        logger.log(f"Max tokens: {max_tokens}")

        if adapter_name != "None" and adapter_name in LOCAL_ADAPTERS:
            container_adapter_path = f"/adapters/{model_name}/lora/{adapter_name}"
            logger.log(f"Using adapter: {container_adapter_path}")
            response = client.generate(
                prompt,
                max_new_tokens=max_tokens,
                adapter_id=container_adapter_path,
                adapter_source="local"
            )
        else:
            logger.log("No adapter selected, using base model")
            response = client.generate(
                prompt,
                max_new_tokens=max_tokens
            )
        logger.log("Generation completed successfully")
        return response.generated_text, logger.logs[-10:]
    except Exception as e:
        return f"Error: {str(e)}"


with gr.Blocks(css=css) as demo:
    with gr.Row():
        html = gr.HTML(value=only_html)

    with gr.Row():
        with gr.Column():
            model_dropdown = gr.Dropdown(
                choices=list(BASE_MODELS.keys()),
                value=list(BASE_MODELS.keys())[0],
                label="Select Base Model"
            )

            adapter_dropdown = gr.Dropdown(
                choices=["None"] + list(LOCAL_ADAPTERS.keys()),
                value="None",
                label="Select LoRA Adapter"
            )

            max_tokens = gr.Slider(
                minimum=16,
                maximum=2048,
                value=64,
                step=16,
                label="Max Tokens"
            )

    with gr.Row():
        input_text = gr.Textbox(
            lines=4,
            label="Input Prompt",
            placeholder="Enter your prompt here..."
        )

    with gr.Row():
        submit_btn = gr.Button("Generate", variant="primary")

    with gr.Row():
        output_text = gr.Textbox(
            lines=6,
            label="Model Response"
        )

    with gr.Row():
            log_box = gr.Textbox(
                lines=10,
                label="Logs",
                interactive=False
            )

    submit_btn.click(
        fn=generate_response,
        inputs=[model_dropdown, adapter_dropdown, input_text, max_tokens],
        outputs=[output_text, log_box]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", share=True)
