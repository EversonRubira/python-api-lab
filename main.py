import anthropic
import os
import dotenv


dotenv.load_dotenv()
client = anthropic.Anthropic(
    api_key= os.environ.get("ANTHROPIC_API_KEY"),
)


message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    system="Listar apenas os nomes dos alimentos, sem adicionar descricao.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "3 alimentos com  Brocolis"
                }
            ]
        }
    ],
   
)
resposta = message.content[0].text
print(resposta)