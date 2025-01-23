import gradio as gr
import os
from lorax import Client
import sys
from datetime import datetime

# from .ui import css, only_html, header

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
.duplicate-button {
  margin: auto !important;
  color: white !important;
  background: black !important;
  border-radius: 100vh !important;
}

.modal-box {
  position: fixed !important;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%); /* center horizontally */
  max-width: 1000px;
  max-height: 750px;
  overflow-y: auto;
  background-color: var(--input-background-fill);
  flex-wrap: nowrap !important;
  border: 2px solid black !important;
  z-index: 1000;
  padding: 10px;
}

.dark .modal-box {
  border: 2px solid white !important;
}
.user-profile {
    display: flex;
    align-items: center;
    justify-content: end;
    gap: 10px;
}

.profile-image {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
}

.dropdown {
    position: relative;
    display: inline-block;
}

.dropbtn {
    background-color: transparent;
    border: none;
    cursor: pointer;
    padding: 8px;
}

.dropdown-content {
    display: none;
    position: absolute;
    color: white;
    background-color: #1f2937;
    min-width: 160px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    z-index: 1;
    right: 0;
}

.dropdown-content a {
    color: black;
    padding: 12px 16px;
    text-decoration: none;
    display: block;
}

.dropdown-content a:hover {
    background-color: transparent;
}

.dropdown:hover .dropdown-content {
    display: block;
}

#login-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
}


#web3auth-login {
    border-radius: var(--button-large-radius);
    padding: var(--button-large-padding);
    font-weight: var(--button-large-text-weight);
    font-size: var(--button-large-text-size);
    border: var(--button-border-width) solid var(--button-primary-border-color);
    background: var(--button-primary-background-fill);
    color: var(--button-primary-text-color);
}
.logo-text {
    font-size: 30px;
    margin-left: 10px;
    
}

.centered-image {
                margin-left: auto;
                margin-right: auto;
                margin-top:20px;
                background: transparent;
                border-color: transparent;
                }
                
footer {visibility: hidden}

.slider_submit {
    justify-content: space-between;
}
"""

only_html = '''
   <div id="web3auth-container" style="text-align: right;">
       <div id="login-container">
            <img class="logo-image" src="https://cdn.openledger.xyz/logo-orange.png" alt="openledger-logo">
            <div>
            <i class="fa-solid fa-layer-group" style="font-size:28px;"></i>
            <span class="logo-text">Model Multiplexer</span>
            </div>
           <button id="web3auth-login" class="lg primary">Connect Wallet</button>
           <div id="user-info" style="display:none;">
           <div class="user-profile">
               <img id="user-image" class="profile-image" src="" alt="Profile">
               <div class="dropdown">
                   <button class="dropbtn" id="user-name"></button>
                   <div class="dropdown-content">
                       <a href="#" style="color: white;" id="profile-link">Profile</a>
                       <a href="#" style="color: white;" id="wallet-address"></a>
                       <a href="#" style="color: white;" id="web3auth-logout">Logout</a>
                   </div>
               </div>
           </div>
       </div>
       </div>
       
   </div>
   '''
   
header='''
    <title>Gradio with Web3Auth</title>
    <script src="https://cdn.jsdelivr.net/npm/@web3auth/modal@9.5.1/dist/modal.umd.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@web3auth/ethereum-provider@9.5.1/dist/ethereumProvider.umd.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css">
    <script type="text/javascript">

    setTimeout(function() {
    let btn = document.getElementById('tg-button');
    if(btn) {
        btn.click();
    }
    }, 2000)


function shortcuts(e) {
    console.log('key pressed')
    var event = document.all ? window.event : e;
    switch (e.target.tagName.toLowerCase()) {
        case "input":
        case "textarea":
        break;
        default:
        if (e.key.toLowerCase() == "s" && e.shiftKey) {
            document.getElementById("my_btn").click();
        }
    }
}
document.addEventListener('keypress', shortcuts, false);
setTimeout(function() {
function check() {
console.log("data")
}
const chainConfig = {
  chainNamespace: 'eip155',
  chainId: "0xaa36a7",
  rpcTarget: "https://rpc.ankr.com/eth_sepolia",
  displayName: "Ethereum Sepolia Testnet",
  blockExplorerUrl: "https://sepolia.etherscan.io",
  ticker: "ETH",
  tickerName: "Ethereum",
  decimals: 18,
  logo: "https://cryptologos.cc/logos/ethereum-eth-logo.png",
};

console.log("wind", window.EthereumProvider)
    const ethereumProvider = new window.EthereumProvider.EthereumPrivateKeyProvider({
        config: { chainConfig: {
            chainId: "0xaa36a7",
  rpcTarget: "https://rpc.ankr.com/eth_sepolia",
  chainNamespace: "eip155",
        } },
    });
    const web3auth = new window.Modal.Web3Auth({
        privateKeyProvider: ethereumProvider,
        web3AuthNetwork: "sapphire_devnet",
        clientId: "BD_mes2shHCQIycGpb1E6o8OWYzLOnjFBHgv9nYd3xHl5xE3XjG8qjaT5g1_jEVPWJ8ZTexeZiuXFwYb-9avE1Y", // Get from Web3Auth Dashboard
        chainConfig: {
            chainNamespace: "eip155",
            chainId: "0xaa36a7",
            rpcTarget: "https://rpc.ankr.com/eth_sepolia"
        }
    });
    console.log(document.getElementById('login'))
   async function login() {

        !web3auth.provider ? await web3auth.initModal() : console.log("Already provider initiated");
        const provider = await web3auth.connect();

        // Get user info from Web3Auth
        const userInfo = await web3auth.getUserInfo();
        console.log("User info:", userInfo);

        const address = await ethereumProvider.request({ method: "eth_accounts" });

        // Update UI with user info
        if (userInfo.profileImage) {
            document.getElementById('user-image').src = userInfo.profileImage;
        }
        if(document.querySelector('#wallet-address')) {
        let box = document.querySelector('#wallet-address-textbox label textarea');
            box.value = address[0];
            box.dispatchEvent(new Event('input'));
        }

        document.getElementById('user-name').textContent = userInfo.name || address[0].slice(0, 6) + '...';
        document.getElementById('wallet-address').textContent = address[0]
        document.getElementById('user-info').style.display = 'flex';
        document.getElementById('web3auth-login').style.display = 'none';

        window.top.postMessage({ action: 'sendData', data: 'Hello from iframe!' }, '*');
        return address;
}

async function logout() {
    await web3auth.logout();
    document.getElementById('user-info').style.display = 'none';
    document.getElementById('web3auth-login').style.display = 'block';
    document.getElementById('user-image').src = '';
    document.getElementById('user-name').textContent = '';
    if(document.querySelector('#wallet-address')) {
        let box = document.querySelector('#wallet-address-textbox label textarea');
            box.value = '';
            box.dispatchEvent(new Event('input'));
        }
}
    setTimeout(function(){
        console.log('id inside settimeout :', document.getElementById('login'))
        document.getElementById('web3auth-login').onclick = login;
        document.getElementById('web3auth-logout').onclick = logout;
    }, 3000)
    console.log('id is :', document.getElementById('login'))
    }, 2000);

</script>

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


with gr.Blocks(css=css, head=header) as demo:
    wallet_address = gr.Textbox(value=None, elem_id="wallet-address-textbox", visible=False)
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

    with gr.Row():
        input_text = gr.Textbox(
            lines=4,
            label="Input Prompt",
            placeholder="Enter your prompt here..."
        )
        with gr.Column(elem_classes="slider_submit"):
            max_tokens = gr.Slider(
                minimum=16,
                maximum=2048,
                value=64,
                step=16,
                label="Max Tokens"
                
            )
            
            
            submit_btn = gr.Button("Generate", variant="primary")

    with gr.Row():
        output_text = gr.Textbox(
            lines=6,
            label="Model Response"
        )

    with gr.Row():
            log_box = gr.Markdown()

    submit_btn.click(
        fn=generate_response,
        inputs=[model_dropdown, adapter_dropdown, input_text, max_tokens],
        outputs=[output_text, log_box]
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", share=True)
