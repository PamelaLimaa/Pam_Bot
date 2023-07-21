import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/drive']

def my_oauth():
    creds = None

    # Verifica se há tokens de acesso salvos no arquivo token.json
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Se não houver tokens válidos disponíveis, faça o login pfv
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'C:\\Users\\layan\\Estudos\\Python\\slack_bot\\bot_python_slack\\credenciais\\credencial.json', SCOPES)
        creds = flow.run_local_server(port=0)

        # Salve os tokens de acesso no arquivo token.json para uso futuro
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def create_folder():
    credentials = my_oauth()
    service = build('drive', 'v3', credentials=credentials)
    id_folder = '1OvOba2dTsZRy-vVuIX6gIVB5m52ucfCI'
    month_and_year = datetime.now().strftime('%m/%Y')

    try:
        # olhando se na lista no meu drive tem o mesmo nome da pasta que está sendo criada
        search_folder = f"name='PostMortem-{month_and_year}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        lista = service.files().list(q=search_folder, spaces='drive').execute()

        if 'files' in lista and len(lista['files']) > 0:
            print(F'essa pasta já existe com o mesmo nome {month_and_year}')
        else:
            # Se não, criar a pasta com o mes/ano corretamente
            file_metadata = {
                'name':F'PostMortem-{month_and_year}',
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [id_folder]
            }
            file = service.files().create(body=file_metadata, fields='id').execute()
            print(f'Folder ID: "{file.get("id")}"')
            return file.get('id')

    except HttpError as error:
        print(F'An error occurred: {error}')
        return None
folder_id = create_folder()
