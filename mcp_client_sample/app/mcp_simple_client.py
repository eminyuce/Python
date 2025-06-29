from mcp import MCPClient
from langchain_community.llms import Ollama

# MCP sunucuyu bir alt process olarak başlat
client = MCPClient.from_stdio_command(["python", "my_simple_server.py"])

# OpenAI / Ollama gibi bir LLM istemcisi tanımla
llm = Ollama(
    model="llama3.1:8b",
    base_url="http://localhost:11434",
    temperature=0.7,
)

# LLM prompt'u
prompt = """
Küçük bir e-posta gönder: Alıcı 'example@domain.com', konu 'Selam', mesaj gövdesi 'Nasılsın?'
"""

# LLM'e MCP tool'larını tanıt (client üzerinden)
tools = client.openai_tools()
response = llm.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    tools=tools,
    tool_choice="auto"
)

# Tool çağrısını al, MCP Server'a gönder
tool_call = response.choices[0].message.tool_calls[0]
result = client.run(tool_call)

# Sonuçları göster
print("LLM Tool sonucu:", result)
