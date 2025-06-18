import os
import json
import requests
from dotenv import load_dotenv

# 📥 Load environment variables
load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
OLLAMA_API_GENERATE_URL = os.getenv("OLLAMA_API_GENERATE_URL", "http://localhost:11434/api/generate")
OLLAMA_API_CHAT_URL = os.getenv("OLLAMA_API_CHAT_URL", "http://localhost:11434/api/chat")

MCP_API_KEY = os.getenv("MCP_API_KEY")
MCP_DISCOVERY_URL = os.getenv("MCP_DISCOVERY_URL")
MCP_TOOL_CALL_URL = os.getenv("MCP_TOOL_CALL_URL")
MCP_PROMPT_URL = os.getenv("MCP_PROMPT_URL")

HEADERS = {
    "Content-Type": "application/json",
}
if MCP_API_KEY:
    HEADERS["X-API-KEY"] = MCP_API_KEY

# 📡 Step 1: Fetch prompts from MCP and return as dict {name: content}
def fetch_prompts_from_mcp():
    try:
        response = requests.get(MCP_PROMPT_URL, headers=HEADERS, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"❌ Error fetching MCP prompts: {str(e)}")

    prompts = response.json()
    prompt_dict = {p["name"]: p["content"] for p in prompts if "name" in p and "content" in p}
    return prompt_dict
    
# 📡 Step 2: Fetch available tool definitions and format as string for prompt
def fetch_function_definitions_from_mcp():
    try:
        response = requests.get(MCP_DISCOVERY_URL, headers=HEADERS, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"❌ Error fetching MCP tools: {str(e)}")

    tools = response.json()
    tool_info_text = ""
    for tool in tools:
        name = tool.get("name", "unknown")
        description = tool.get("description", "No description provided")
        schema = tool.get("inputSchema", "{}").replace("\r\n", "").replace("\n", "").strip()
        tool_info_text += f"- {name}: {description}\n  Input schema: {schema}\n\n"

    print("📦 MCP Tools for system prompt:\n")
    print(tool_info_text)
    return tool_info_text

# ⚙️ Step 3: Call MCP function with JSON args
def call_mcp_function(function_name, arguments):
    try:
        payload = {
            "tool": function_name,
            "parameters": arguments
        }
        response = requests.post(MCP_TOOL_CALL_URL, headers=HEADERS, json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": f"❌ MCP Error: {str(e)}"}

# 🧠 Step 4: Call Ollama chat endpoint with messages
def call_ollama_chat(messages):
    response = requests.post(OLLAMA_API_CHAT_URL, json={
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False
    })
    response.raise_for_status()
    return response.json()["message"]["content"]

# 🧠 Step 5: Call Ollama generate endpoint with prompt string
def call_ollama_generate(prompt):
    response = requests.post(OLLAMA_API_GENERATE_URL, json={
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    })
    response.raise_for_status()
    data = response.json()
    return data.get("response", "")

# 🚀 Main agent flow
def main():
    user_message = "What's the weather like in Istanbul?"
    print("🔎 Fetching tool definitions from MCP server...")
    tool_info_text = fetch_function_definitions_from_mcp()

    print("🔎 Fetching prompts from MCP server...")
    prompts_map = fetch_prompts_from_mcp()

    # Use dynamic system prompt from MCP prompts; fallback if not found
    system_prompt_template = prompts_map.get("unstructured-tool-system-prompt")
    if system_prompt_template:
        system_prompt = system_prompt_template.replace("[TOOL_INFO_TEXT]", tool_info_text)
    else:
        raise RuntimeError("❌ Required prompt 'unstructured-tool-system-prompt' not found in MCP prompts")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    print("💬 Sending message to Ollama chat endpoint...")
    reply = call_ollama_chat(messages)
    print(f"🤖 Ollama Response:\n{reply}")

    if reply.strip().startswith("CALL"):
        try:
            _, func_name, json_str = reply.strip().split(" ", 2)
            args = json.loads(json_str)
            print(f"📞 Ollama wants to call MCP function: {func_name} with args {args}")

            tool_response = call_mcp_function(func_name, args)

            # Use final response prompt from MCP prompts; fallback if missing
            final_response_prompt_template = prompts_map.get("final-response-prompt")
            if final_response_prompt_template:
                # Replace placeholder with serialized tool_response JSON string
                tool_response_prompt = final_response_prompt_template.replace("[TOOL_RESPONSE]", json.dumps(tool_response))
            else:
                raise RuntimeError("❌ Required prompt 'final-response-prompt' not found in MCP prompts")

            print("💬 Sending tool response back to Ollama for final user-friendly answer...")
            final_response = call_ollama_generate(tool_response_prompt)
            print("\n✅ Final answer from Ollama:")
            print(final_response)

        except Exception as e:
            print(f"❌ Failed to parse or execute tool call: {e}")
    else:
        print("\n✅ Final answer from Ollama:")
        print(reply)

# Entry point
if __name__ == "__main__":
    main()
