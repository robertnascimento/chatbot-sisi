from django.http.response import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dialogflowfolder import api
import google.generativeai as ia
import json
from django.shortcuts import render
import uuid


def chat(request):
    # Verifica se o session_id está nos cookies ou cria um novo
    session_id = request.COOKIES.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())  # Gera um novo session_id
        response = HttpResponse(f"ID da sessão: {session_id}")
        response.set_cookie('session_id', session_id, max_age=3600)
    else:
        response = HttpResponse(f"ID da sessão: {session_id}")

    # Processa o POST se houver uma mensagem
    if request.method == 'POST':
        message = request.POST.get('message', '')
        if message:
            response_text = api.main(session_id, message)  # Substitua com a lógica real
            return JsonResponse({'message': response_text})
        else:
            return JsonResponse({'message': 'Mensagem não pode ser vazia.'}, status=400)

    # Renderiza o template com session_id
    return render(request, 'chatbot/chat.html', {'session_id': session_id})

@csrf_exempt
def webhook(requests):


    print(requests.body)
    print("-----------------------")
    print("^^^^^^^^^^JSON^^^^^^^^^")
    print("-----------------------")
    print("vvvvvDADOS DO USERvvvvv")
    print("-----------------------")
    data = json.loads(requests.body)
    # Acessar o dicionário de parâmetros
    parameters = data['queryResult']['parameters']

    # Extrair valores individuais
    nome = parameters.get('nome')
    matricula = int(parameters.get('matricula'))
    matricula = parameters.get('disciplina')
    print("Nome:", nome)
    print("Matrícula:", matricula)
    print("Disciplina:", matricula)

    data['fulfillmentText'] = 'Confirmado. Seu pedido está sendo preparado.'

    return JsonResponse(data)

import logging

# Configure o logging
logger = logging.getLogger(__name__)
def gemini(request, session_id):
    print(f"Session ID: {session_id}")

    if request.method == 'POST':
        pergunta = request.POST.get('message', '')
        if pergunta:
            try:
                GOOGLE_GEMINI_API_KEY = "AIzaSyDeMEs15l3qVwajD4nVkj2DmDbeSLciA9E"
                ia.configure(api_key=GOOGLE_GEMINI_API_KEY)
                model = ia.GenerativeModel("models/gemini-1.0-pro")

                # Adicione mais detalhes sobre o que está sendo enviado
                logger.info(f"Pergunta enviada: {pergunta}")

                response = model.generate_content(pergunta)
                
                # Adicione detalhes sobre a resposta recebida
                if response:
                    logger.info(f"Resposta da API: {response}")
                else:
                    logger.error("Resposta da API está vazia.")

                if response and response.candidates:
                    return JsonResponse({'message': response.candidates[0].content.parts[0].text})
                else:
                    logger.error("Resposta da API não contém candidatos.")
                    return JsonResponse({'message': 'Desculpe, não consegui encontrar uma resposta.'}, status=500)
            except Exception as e:
                # Log o erro com traceback
                logger.error(f"Erro ao chamar a API: {e}", exc_info=True)
                return JsonResponse({'message': 'Ocorreu um erro ao processar sua solicitação.'}, status=500)
        else:
            return JsonResponse({'message': 'Mensagem não pode ser vazia.'}, status=400)

    return render(request, 'chatbot/gemini_chat.html', {'session_id': session_id})


# def consultar_gemini(pergunta):

#     get_session = request.COOKIES.get('session_id', 'Não definido')
#     if request.method == 'POST':
#         GOOGLE_GEMINI_API_KEY = "AIzaSyA_kBjA4B0_RohyMwLkBUsQ0LJ-aJeMdsc"
#         ia.configure(api_key=GOOGLE_GEMINI_API_KEY)
#         model = ia.GenerativeModel("models/gemini-1.5-pro")
#         response = model.generate_content(pergunta)
#         if response and response.candidates:
#             return response.candidates[0].content.parts[0].text
#         return "Desculpe, não consegui encontrar uma resposta."