from mcp.server.fastmcp import FastMCP

# Initialize the MCP server with a name
mcp = FastMCP("CalculatorServer")

# Define a tool for adding two numbers
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Run the MCP server locally with stdio transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="localhost", port=8000)