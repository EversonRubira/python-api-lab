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

def analisador_de_transacoes(transacoes):

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
    
        
    try:
        print('1 iniciou a analise de fraudes')
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
        resposta = resposta.strip().removeprefix("```json").removesuffix("```").strip()
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


def gerar_relatorio(transacao):

    prompt_do_sistema = f"""
    
    Para a seguinte transação, forneça um parecer, apenas se o status dela for de
    "Possível Fraude". Indique no parecer uma justificativa para que você identifique
    uma fraude.
    Transação: {transacao}

    ## Formato de Resposta
    "id": "id",
    "tipo": "crédito ou débito",
    "estabelecimento": "nome do estabelecimento",
    "horario": "horário da transação",
    "valor": "R$XX,XX",
    "nome_produto": "nome do produto",
    "localizacao": "cidade - estado (País)"
    "status": "",
    "parecer" : "Colocar Não Aplicável se o status for Aprovado"

    """
        
    try:
        print('3 Iniciou a geracao de parecer de fraudes')
        mensagem = cliente.messages.create(
            model=modelo,
            max_tokens=2000,
            temperature=0,
            ## system=prompt_do_sistema,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_do_sistema
                        }
                    ]
                }
            ]
        )
        resposta = mensagem.content[0].text
        print('4 Finlizou a geracao de parecer de fraudes')
        return resposta
       
    except anthropic.APIConnectionError as e:
        print("The server could not be reached", e.__cause__),
    except anthropic.RateLimitError as e:
        print("A 429 status code was received; Limit de acesso atingido")
    except anthropic.APIStatusError as e:
        print("Another non-200-range status code was received", e.status_code, "mais informacoes:", e.response)
    except Exception as e:
        print("An error occurred", e)  


def gerar_recomendacao(transacao):

    prompt_do_sistema = f"""
    
    Para a seguinte transação, forneça uma recomendação apropriada baseada no status e nos detalhes da Transação: {parecer}

    As recomendações podem ser "Notificar Cliente", "Acionar setor Anti-Fraude" ou "Realizar Verificação Manual".
    Elas devem ser escritas no formato técnico.

    Inclua também uma classificação do tipo de fraude, se aplicável.

    """
        
    try:
        print('5 Iniciou a geracao de recomendacao')
        mensagem = cliente.messages.create(
            model=modelo,
            max_tokens=2000,
            temperature=0,
            ## system=prompt_do_sistema,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_do_sistema
                        }
                    ]
                }
            ]
        )
        resposta = mensagem.content[0].text
        print('6 Finlizou a geracao de recomendacao')
        return resposta
       
    except anthropic.APIConnectionError as e:
        print("The server could not be reached", e.__cause__),
    except anthropic.RateLimitError as e:
        print("A 429 status code was received; Limit de acesso atingido")
    except anthropic.APIStatusError as e:
        print("Another non-200-range status code was received", e.status_code, "mais informacoes:", e.response)
    except Exception as e:
        print("An error occurred", e)        

            

transacoes = carrega('transacoes.csv')
transacoes_analisadas = analisador_de_transacoes(transacoes)

for transacao in transacoes_analisadas['transacoes']:
    if transacao['status'] == 'Possível Fraude':
        parecer = gerar_relatorio(transacao)
        recomendacao = gerar_recomendacao(parecer)
        salva(f"transacao-{transacao['id']}-{transacao[nome_produto]}-{transacao[status]}).txt", recomendacao)