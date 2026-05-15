import anthropic
import dotenv
import os
from helpers import *
import json


dotenv.load_dotenv()
cliente = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
modelo = "claude-sonnet-4-6"

def analisar_transacoes(transacoes):

    prompt_do_sistema = """
    
    Analise as transações financeiras a seguir e identifique se cada uma delas é uma "Possível Fraude" ou deve ser "Aprovada". 
    Adicione um atributo "Status" com um dos valores: "Possível Fraude" ou "Aprovado".

    Cada nova transação deve ser inserida dentro da lista do JSON.

    # Possíveis indicações de fraude
    - Transações com valores muito discrepantes
    - Transações que ocorrem em locais muito distantes um do outro
    
    Adote o formato de resposta abaixo para compor sua resposta.
        
    # Formato Saída 
    {
        "transacoes": [
            {
            "id": "id",
            "tipo": "crédito ou débito",
            "estabelecimento": "nome do estabelecimento",
            "horário": "horário da transação",
            "valor": "R$XX,XX",
            "nome_produto": "nome do produto",
            "localização": "cidade - estado (País)"
            "status": ""
            },
        ]
    } 

    """
    prompt_do_usuario = f"""
    Considere o CSV abaixo, onde cada linha é uma transação diferente: {transacoes}. 
    Sua resposta deve adotar o #Formato de Resposta (apenas um json sem outros comentários)
    """
    
    print('Iniciando análise de sentimentos para o restaurante:', restaurante)
    
    try:
        mensagem = cliente.messages.create(
            model=modelo,
            max_tokens=2000,
            temperature=0,
            system=prompt_do_sistema,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_do_usuario
                        }
                    ]
                }
            ]
        )
        resposta = mensagem.content[0].text
        json_resposta = json.loads(resposta)
        salva('transacoes.json', resposta)
        return json_resposta
       
    except anthropic.APIConnectionError as e:
        print("The server could not be reached", e.__cause__),
    except anthropic.RateLimitError as e:
        print("A 429 status code was received; Limit de acesso atingido")
    except anthropic.APIStatusError as e:
        print("Another non-200-range status code was received", e.status_code, "mais informacoes:", e.response)
    except Exception as e:
        print("An error occurred", e)   

transacoes = carrega('transacoes.csv')
transacoes_analisadas = analisar_de_transacoes(transacoes)