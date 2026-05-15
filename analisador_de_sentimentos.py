import anthropic
import dotenv
import os
from helpers import *


dotenv.load_dotenv()
cliente = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
modelo = "claude-sonnet-4-6"

def analisar_sentimentos(restaurante):

    prompt_do_sistema = f"""
    
    Você é um analisador de sentimentos de avaliações de restaurantes.
    Escreva um parágrafo com até 50 palavras resumindo as avaliações e
    depois atribua qual o sentimento geral para o produto.
    Identifique também 3 pontos fortes e 3 pontos fracos identificados a partir das avaliações.

    # Formato de Saída
    
    Nome do Restaurante: {restaurante}
    Resumo das Avaliações:
    Sentimento Geral: [utilize aqui apenas Positivo, Negativo ou Neutro]
    Ponto fortes: lista com três bullets
    Pontos fracos: lista com três bullets


    """
    prompt_do_usuario = carrega(f"./dados/avaliacoes/avaliacoes-{restaurante}.txt")

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
        salva(f'./dados/avaliacoes/analise-{restaurante}.txt', resposta)
        print('Análise de sentimentos concluída com sucesso para o restaurante:', restaurante)
    except anthropic.APIConnectionError as e:
        print("The server could not be reached", e.__cause__),
    except anthropic.RateLimitError as e:
        print("A 429 status code was received; Limit de acesso atingido")
    except anthropic.APIStatusError as e:
        print("Another non-200-range status code was received", e.status_code, "mais informacoes:", e.response)
    except Exception as e:
        print("An error occurred", e)   

lista_de_restaurantes = [
    'Restaurante de Comida Chinesa',
    'Restaurante de Bolos e Doces',
    'Restaurante de Comida Vegana'
]
for restaurante in lista_de_restaurantes:
    analisar_sentimentos(restaurante)