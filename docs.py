from googleapiclient.discovery import build
from drive import my_oauth

def inserir_texto(new_id, number_incident, incident, descricao):
    credentials = my_oauth()
    service = build('docs', 'v1', credentials=credentials)

    try:
        result = service.documents().batchUpdate(documentId=new_id, body={
            'requests': [
                {
                    'replaceAllText': {
                        'containsText': {
                            'text': 'Número:'
                        },
                        'replaceText': f'Número: INC{number_incident}'
                    }
                },
                {
                    'replaceAllText': {
                        'containsText': {
                            'text': 'Incidente:'
                        },
                        'replaceText': f'Incidente: {incident}'
                    }
                },
                {
                    'replaceAllText': {
                        'containsText': {
                            'text': 'Impacto:'
                        },
                        'replaceText': f'Impacto: {descricao}'
                    }
                }
            ]
        }).execute()

        print("Atualização bem-sucedida!")
        print(result)
    except Exception as e:
        print("Ocorreu um erro:")
        print(e)