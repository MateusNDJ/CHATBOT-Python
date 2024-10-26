import pytesseract
from PIL import Image
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuração de respostas padrão
respostas = {
    "embalado": "Olá, seu pedido está sendo embalado e logo chegará a você.",
    "a caminho": "Olá, seu pedido está a caminho.",
    "reembolso": "Para assuntos relacionados a reembolso, você precisa mediar diretamente com a Shopee, abrindo um chamado com eles."
}

# Função para extrair texto de imagem
def extrair_texto_da_imagem(caminho_da_imagem):
    imagem = Image.open(caminho_da_imagem)
    texto = pytesseract.image_to_string(imagem, lang='por')
    return texto

# Função para reconhecer e responder mensagens
def reconhecer_mensagem(mensagem):
    if any(palavra in mensagem for palavra in ["embalado", "embalagem", "preparação", "sendo preparado", "preparando"]):
        return respostas["embalado"]
    elif any(palavra in mensagem for palavra in ["caminho", "enviado", "transporte", "sendo entregue", "entrega"]):
        return respostas["a caminho"]
    elif any(palavra in mensagem for palavra in ["reembolso", "reembolsado", "defeito", "quebrado", "restituição"]):
        return respostas["reembolso"]
    else:
        return "Desculpe, não entendi sua mensagem. Vou encaminhar sua dúvida para um humano."

# Função para encaminhar mensagens complexas para um humano via email
def encaminhar_para_humano(mensagem, codigo_pedido):
    remetente = "seuemail@exemplo.com"
    destinatario = "humano@empresa.com"
    senha = "sua_senha"

    conteudo = f"""
    <html>
    <body>
        <p><strong>Mensagem do Cliente:</strong> {mensagem}</p>
        <p><strong>Código do Pedido:</strong> {codigo_pedido}</p>
    </body>
    </html>
    """
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Assistência Humana Necessária"
    msg["From"] = remetente
    msg["To"] = destinatario
    part = MIMEText(conteudo, "html")
    msg.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.sendmail(remetente, destinatario, msg.as_string())

# Teste do Chatbot com mensagens simuladas
mensagens_teste = [
    "Meu pedido está em preparação?",
    "Quando meu pedido vai ser enviado?",
    "Estou com um produto com defeito, como faço o reembolso?",
    "Meu pedido está sendo preparado?",
    "Quando vai chegar meu pacote?",
    "O produto chegou quebrado, como peço restituição?",
    "Estou aguardando a entrega",
    "Meu pedido está sendo embalado?",
    "Como posso pedir reembolso por um produto com defeito?",
    "Meu pedido está a caminho?",
    "Quando meu pedido será transportado?"
]

for msg in mensagens_teste:
    resposta = reconhecer_mensagem(msg.lower())
    print(f"Usuário: {msg}\nChatbot: {resposta}\n")

    if "Vou encaminhar sua dúvida para um humano" in resposta:
        encaminhar_para_humano(msg, "12345ABC")
