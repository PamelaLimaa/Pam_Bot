import os
from slack_bolt import App
from pathlib import Path
from dotenv import load_dotenv
from slack_sdk import WebClient
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from drive import copy_file_move_folder_generate_link
from docs import inserir_texto

env_path = Path('.') / '.env'
load_dotenv(override=True)

# Credenciais da API do Slack
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Função para escutar o canal e responder com o link do arquivo
@app.event('message')
def update_home_tab(client, event):
    number_incident = 928373
    incident = 'testando'
    descricao = 'Alguns clientes não conseguem fazer o bot rodar'

    link, new_id = copy_file_move_folder_generate_link()

    inserir_texto(new_id, number_incident, incident, descricao)

    # bloco de mensagem de crise
    attachments =  [
        {
            "color": "#f2c744",
            "blocks": [
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f" *Número*:INC{number_incident}\n *Incidente: {incident}* \n *Impacto*: {descricao}\n *Diagnóstico*: Instabilidade no Bot da Pam\n *Sala de Crise*: <http://meet.google.com/new|http://meet.google.com/new>\n *PostMortem*: <{link}|_Clique Aqui_>\n *Comunica NOC*: Clique Aqui"
                        }
                    ]
                }
            ]
        }
    ]

    # Enviando a mensagem no canal
    client.chat_postMessage(channel=event['channel'], attachments=attachments, text='✅ *FECHADO - 14/07 a 04/07*')

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))

