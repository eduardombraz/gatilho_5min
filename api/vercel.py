from flask import Flask
import requests
import os

app = Flask(__name__)

# Pega o token do ambiente
TOKEN = os.getenv("GH_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# Lista de workflows a serem acionados
WORKFLOWS = [
    {"repo": "Base-TOPacked", "workflow": "main_base_to_packed.yaml"},
    {"repo": "Base-Sacas2.0", "workflow": "main_base_sacas2.0.yaml"},
    {"repo": "Base-FIFO", "workflow": "main_base_fifo.yaml"},
    {"repo": "ToPackedSP7", "workflow": "main_base_to_packedSP7.yaml"},
    {"repo": "piso_exp_sp7", "workflow": "piso10.yml"},
]

# Rota principal para verificar se o app está no ar
@app.route('/')
def home():
    return "Servidor do agendador de workflows do GitHub está no ar."

# Rota que será chamada pelo Cron Job da Vercel
@app.route('/api/trigger')
def trigger_workflows():
    # Loop que executa a lógica UMA VEZ por chamada
    for wf in WORKFLOWS:
        url = f"https://api.github.com/repos/eduardombraz/{wf['repo']}/actions/workflows/{wf['workflow']}/dispatches"
        data = {"ref": "main"}
        try:
            res = requests.post(url, headers=HEADERS, json=data)
            print(f"[OK] {wf['workflow']} -> {res.status_code}")
        except Exception as e:
            print(f"[ERRO] {wf['workflow']} -> {e}")
    
    return "Workflows acionados com sucesso!", 200
