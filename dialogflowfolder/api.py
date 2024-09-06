from google.cloud import dialogflow_v2 as dialogflow
import os

def enviar_msg(project_id, session_id, text):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code='pt-br')
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(request={"session": session, "query_input": query_input})

    return response.query_result.fulfillment_text

def main(client_session, client_message):
    project_id = 'sissi-a9oj'
    session_id = client_session #GERAR SESSAO INDIVIDUAL
    text = client_message  # Texto para enviar ao Dialogflow

    response_text = enviar_msg(project_id, session_id, text)

    print("SISI:", response_text)
    return response_text

if __name__ == "__main__":
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\Users\\rober\\Downloads\\sissi-a9oj-29524dad09e2.json'
    main()
