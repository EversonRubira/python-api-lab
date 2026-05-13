import anthropic
import os
import dotenv


dotenv.load_dotenv()
client = anthropic.Anthropic(
    api_key= os.environ.get("ANTHROPIC_API_KEY"),
)

#modelo = "claude-sonnet-4-6"
modelo = "claude-haiku-4-5"

def categoriza_alimento(lista_de_categorias_validas, nome_do_alimento):

    prompt_de_sistema = f"""

    Você é um categorizador de alimentos.
    Você deve assumir as categorias presentes na lista abaixo.
    Você nao deve responder outros itens que nao sejam alimentos, 
    caso o item nao seja um alimento, responda "Item não é um alimento".

    # Lista de Categorias Válidas
    {lista_de_categorias_validas.split(",")}

    # Formato da Saída
    Produto: Nome do Produto
    Categoria: apresente a categoria do produto

    # Exemplo de Saída
    Produto: Maçã
    Categoria: Frutas

    """

    prompt_do_usuario = nome_do_alimento


    message = client.messages.create(
        model= modelo,
        max_tokens=1000,
        system = prompt_de_sistema,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_do_usuario,
                    }
                ]
            }
        ],
    )
    resposta = message.content[0].text
    return resposta

categorias_validas = input("Digite as categorias válidas, separadas por vírgula: ")

while True:
    nome_do_alimento = input("Digite o nome do alimento, ou 'sair' para encerrar: ") 
    texto_da_reposta = categoriza_alimento(categorias_validas, nome_do_alimento)
    print(texto_da_reposta)

    if nome_do_alimento.lower() == "sair":
        print("tchau!")
        break
 