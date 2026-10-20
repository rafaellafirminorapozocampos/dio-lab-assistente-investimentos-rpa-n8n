import requests
from bs4 import BeautifulSoup

URL_PAGINA = "https://digitalinnovationone.github.io/dio-lab-assistente-investimentos-rpa-n8n/"

# 1) Baixar a página de clientes
print("Baixando página de clientes...")
html = requests.get(URL_PAGINA).text

# 2) Ler a tabela de clientes
soup = BeautifulSoup(html, "html.parser")
linhas = soup.select("#clientes tbody tr")

clientes = []

for linha in linhas:
    colunas = linha.find_all("td")
    cliente = {
        "nome":  colunas[0].get_text(strip=True),
        "email": colunas[1].get_text(strip=True),
        "saldo": colunas[2].get_text(strip=True),
        "perfil": colunas[3].get_text(strip=True),
    }
    clientes.append(cliente)

print(f"Sucesso! Encontrados {len(clientes)} clientes:")
for c in clientes:
    print(f" - {c['nome']} ({c['perfil']}) | Saldo: {c['saldo']}")

# 3) Enviar diretamente para o Webhook do n8n local
N8N_WEBHOOK = "http://localhost:5678/webhook-test/clientes"

print(f"\nEnviando dados para o n8n ({N8N_WEBHOOK})...")
resposta = requests.post(N8N_WEBHOOK, json={"clientes": clientes})

print("Status do envio:", resposta.status_code)
print("Resposta do n8n:", resposta.text)
