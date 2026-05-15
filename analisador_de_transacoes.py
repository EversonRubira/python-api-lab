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

def chamar_api(prompt_do_sistema, prompt_do_usuario):
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
        return mensagem.content[0].text
    except anthropic.APIConnectionError as e:
        print("The server could not be reached", e.__cause__)
    except anthropic.RateLimitError as e:
        print("A 429 status code was received; Limit de acesso atingido")
    except anthropic.APIStatusError as e:
        print("Another non-200-range status code was received", e.status_code, "mais informacoes:", e.response)
    except Exception as e:
        print("An error occurred", e)


def analisador_de_transacoes(transacoes):
    prompt_do_sistema = """
    Analise as transações financeiras a seguir e identifique se cada uma delas é uma "Possível Fraude" ou deve ser "Aprovada". 
    Adicione um atributo "Status" com um dos valores: "Possível Fraude" ou "Aprovado".
    Cada nova transação deve ser inserida dentro da lista do JSON.

    # Possíveis indicações de fraude
    - Transações com valores muito discrepantes
    - Transações que ocorrem em locais muito distantes um do outro
    
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
            "localização": "cidade - estado (País)",
            "status": ""
            }
        ]
    }
    """
    prompt_do_usuario = f"""
    Considere o CSV abaixo, onde cada linha é uma transação diferente: {transacoes}. 
    Sua resposta deve adotar o #Formato de Saída (apenas um json sem outros comentários)
    """
    print('1 Iniciou a analise de fraudes')
    resposta = chamar_api(prompt_do_sistema, prompt_do_usuario)
    resposta = resposta.strip().removeprefix("```json").removesuffix("```").strip()
    json_resposta = json.loads(resposta)
    salva('transacoes.json', resposta)
    print('2 Finalizou a analise de fraudes')
    return json_resposta


def gerar_relatorio(transacao):
    prompt_do_sistema = """
    Para a seguinte transação, forneça um parecer apenas se o status for "Possível Fraude".
    Indique uma justificativa para a identificação da fraude.

    ## Formato de Resposta (apenas json sem outros comentários)
    {
        "id": "id",
        "tipo": "crédito ou débito",
        "estabelecimento": "nome do estabelecimento",
        "horario": "horário da transação",
        "valor": "R$XX,XX",
        "nome_produto": "nome do produto",
        "localizacao": "cidade - estado (País)",
        "status": "",
        "parecer": "Colocar Não Aplicável se o status for Aprovado"
    }
    """
    prompt_do_usuario = f"Analise esta transação: {transacao}"
    print('3 Iniciou a geracao de parecer')
    resposta = chamar_api(prompt_do_sistema, prompt_do_usuario)
    resposta = resposta.strip().removeprefix("```json").removesuffix("```").strip()
    json_resposta = json.loads(resposta)
    salva(f"parecer-{transacao['id']}-{transacao['nome_produto']}-{transacao['status']}.json", resposta)
    print('4 Finalizou a geracao de parecer')
    return json_resposta


def gerar_recomendacao(parecer):
    prompt_do_sistema = """
    Para a seguinte transação, forneça uma recomendação apropriada baseada no status e nos detalhes.
    As recomendações podem ser "Notificar Cliente", "Acionar setor Anti-Fraude" ou "Realizar Verificação Manual".
    Escritas em formato técnico. Inclua também uma classificação do tipo de fraude, se aplicável.
    """
    prompt_do_usuario = f"Gere a recomendação para esta transação: {parecer}"
    print('5 Iniciou a geracao de recomendacao')
    resposta = chamar_api(prompt_do_sistema, prompt_do_usuario)
    salva(f"recomendacao-{parecer['id']}-{parecer['nome_produto']}-{parecer['status']}.json", resposta)
    print('6 Finalizou a geracao de recomendacao')
    return resposta


transacoes = carrega('transacoes.csv')
transacoes_analisadas = analisador_de_transacoes(transacoes)

for transacao in transacoes_analisadas['transacoes']:
    if transacao['status'] == 'Possível Fraude':
        parecer = gerar_relatorio(transacao)
        recomendacao = gerar_recomendacao(parecer)