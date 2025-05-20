import os
import glob
from fastmcp import FastMCP

WORKSPACE_DIR = os.getcwd()
CODE_STORAGE = os.path.join(WORKSPACE_DIR, "example_codes")
print("Default workspace directory:", WORKSPACE_DIR)

mcp = FastMCP("🛠️🤖 Your Coding Master 🤖🛠️")

def get_code_path(code_name: str) -> str:
    """
    Get the path to the code file based on the code name.
    
    Args:
        code_name: The name of the code file (without extension).
    
    Returns:
        The full path to the code file.
    """
    

@mcp.tool()
def hello(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="sse", host="127.0.0.1", port=8000)