import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.readonly']

def my_oauth():
    creds = None

    # Verifica se há tokens de acesso salvos no arquivo token.json
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Se não houver tokens válidos disponíveis, faça o login pfv
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credencial.json', SCOPES)
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
        # buscando no meu drive se existe algum arquivo(menos lixeira) com esse x nome
        search_folder = f"name='PostMortem-{month_and_year}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        lista = service.files().list(q=search_folder, spaces='drive').execute()

        if 'files' in lista and len(lista['files']) > 0:
            existing_folder = lista['files'][0]
            print(f'Pasta já existe com o mesmo nome: "{existing_folder["name"]}", ID: "{existing_folder["id"]}"')
            return existing_folder["id"]
        else:
            # Se não, criar a pasta com o mes/ano corretamente
            file_metadata = {
                'name':F'PostMortem-{month_and_year}',
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [id_folder]
            }
            file = service.files().create(body=file_metadata, fields='id').execute()
            print(f'Pasta criada com o nome: "{file_metadata["name"]}", ID: "{file["id"]}"')
            return file["id"]

    except HttpError as error:
        print(F'An error occurred: {error}')
        return None

folder_id = create_folder()

# Função de copiar o arquivo existente, mover para a pasta e gerar link
def copy_file_move_folder_generate_link():
    credentials = my_oauth()
    service = build('drive', 'v3', credentials=credentials)
    file_id = '1fceJGgUpHcJsqxi_wY172q8xCEGDLftIpe41rsZpRes'
    source_folder = '1OvOba2dTsZRy-vVuIX6gIVB5m52ucfCI'
    target_folder = folder_id
    number_incident = 'Pamela'
    incident = 'testando'
    title = f'INC{number_incident}-{incident}'

    copied_file = {'name': title}

    try:
        new_file = service.files().copy(fileId=file_id, body=copied_file).execute()
        new_id = new_file['id']

        # Move o arquivo para o diretório de destino
        file = service.files().get(fileId=new_file['id'], fields='parents').execute()
        file = service.files().get(fileId=file_id, fields='parents').execute()
        file = service.files().update(fileId=new_file['id'], 
                                      addParents=target_folder,
                                      removeParents=source_folder,
                                      fields='id, parents').execute()

        # Cria uma permissão para permitir que qualquer usuário com o link possa acessar o arquivo
        permission = {
            'type': 'anyone',
            'role': 'reader',
        }
        service.permissions().create(fileId=new_id, body=permission).execute()

        # Gera o link para o arquivo recém criado
        file = service.files().get(fileId=new_id, fields='webViewLink').execute()
        link = file.get('webViewLink')

        return link
    except HttpError as error:
        print(F'An error occurred: {error}')
        return None