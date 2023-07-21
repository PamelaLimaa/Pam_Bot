import os
from slack_bolt import App
from pathlib import Path
from dotenv import load_dotenv
from slack_sdk import WebClient

env_path = Path('.') / '.env'
load_dotenv(override=True)

# credenciais da api do slack
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

number_incident = 298374
incident = 'Indisponibilidade no Pix'
title = f'INC{number_incident}-{incident}'
id_file = '1M6sg06TrB2hSk3WSwe_LZoP0rBRFU5Iw'

attachments =  [
		{
			"color": "#f2c744",
			"blocks": [
				{
					"type": "section",
					"fields": [
					{
						"type": "mrkdwn",
						"text": f" *Número*: INC{number_incident}\n *Incidente:* {incident}\n *Impacto*: Alguns clientes não conseguem fazer o bot rodar\n *Diagnóstico*: Instabilidade no Bot da Pam\n *Sala de Crise*: <http://meet.google.com/new|http://meet.google.com/new>\n *PostMortem*: {title}\n *Comunica NOC*: Clique Aqui"
					}
				]
			}
		]
	}
]

# Ele escuta o canal, caso tenha mensagem ele nos retorna o payload
@app.event('message')
def update_home_tab(client, event):
    client.chat_postMessage(channel=event['channel'], attachments=attachments, text='✅ *FECHADO - 14/07 a 04/07*')

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))