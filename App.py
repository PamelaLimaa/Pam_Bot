import os
from slack_bolt import App
from pathlib import Path
from dotenv import load_dotenv
from slack_sdk import WebClient
from drive import copy_file_move_folder_generate_link

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
    # Chamando a função para gerar o link do arquivo
    file_link = copy_file_move_folder_generate_link()

    # Criando o bloco de mensagem com o link do arquivo
    attachments =  [
		{
			"color": "#f2c744",
			"blocks": [
				{
					"type": "section",
					"fields": [
					{
						"type": "mrkdwn",
						"text": f" *Número*: INC\n *Incidente:* \n *Impacto*: Alguns clientes não conseguem fazer o bot rodar\n *Diagnóstico*: Instabilidade no Bot da Pam\n *Sala de Crise*: <http://meet.google.com/new|http://meet.google.com/new>\n *PostMortem*: <{file_link}|_Clique Aqui_>\n *Comunica NOC*: Clique Aqui"
					}
				]
			}
		]
	}
]

    # Enviando a mensagem com o link do arquivo
    client.chat_postMessage(channel=event['channel'], attachments=attachments, text='✅ *FECHADO - 14/07 a 04/07*')

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
