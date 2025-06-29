from mcp.client import MCPClient

# Initialize the client
client = MCPClient()

# Connect to the local server
with client.connect(transport="stdio") as session:
    # Call the 'add' tool
    result = session.call_tool("add", {"a": 5, "b": 7})
    print(f"Result: {result}")