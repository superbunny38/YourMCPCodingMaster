import os
import glob
from fastmcp import FastMCP, Context
from pathlib import Path
from typing import List
import subprocess

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
    # Use glob to search for files with the given code_name and any extension
    search_pattern = os.path.join(CODE_STORAGE, f"{code_name}.*")
    matching_files = glob.glob(search_pattern)
    
    if matching_files:
        # Return the first matching file
        return matching_files[0]
    else:
        raise FileNotFoundError(f"No file found with name '{code_name}' in {CODE_STORAGE}")

def get_code(code_path: str)-> str:
    """
    Read the content of a code file.
    
    Args:
        code_path: The path to the code file.
    
    Returns:
        The content of the code file as a string.
    """
    with open(code_path, "r") as f:
        return f.read()

def get_all_code_paths(storage_dir: str = CODE_STORAGE) -> List[str]:
    """
    Get the paths to all code files in the specified storage directory.
    
    Args:
        storage_dir: The directory where code files are stored.
    
    Returns:
        A list of full paths to all code files in the directory.
    """
    # List all files in the directory
    code_files = [
        os.path.join(storage_dir, file)
        for file in os.listdir(storage_dir)
        if os.path.isfile(os.path.join(storage_dir, file))
    ]
    
    return code_files

def execute_code(code_path: str):
    """Execute the code and returns the dictionary containing output of the code, content of the code in text and the code file name

    Args:
        code_path (str): code path

    Returns:
        dictionary: {"code": code, "output": output, "code_file_name": code_file_name}
    """
    if not os.path.exists(code_path):
        raise FileNotFoundError(f"The file '{code_path}' does not exist.")
    
    # Read the content of the code file
    with open(code_path, "r") as file:
        code = file.read()
    
    # Get the file name
    code_file_name = os.path.basename(code_path)
    
    # Get the file extension
    _, file_extension = os.path.splitext(code_path)
    
    try:
        # Determine the command to execute based on the file extension
        if file_extension == ".py":
            # Execute Python file
            command = ["python3", code_path]
        elif file_extension == ".java":
            # Compile and execute Java file
            compile_command = ["javac", code_path]
            execute_command = ["java", os.path.splitext(code_file_name)[0]]
            subprocess.run(compile_command, check=True)
            command = execute_command
        elif file_extension == ".cs":
            compile_command = ["csc", code_path]
            execute_command = ["mono", os.path.splitext(code_file_name)[0] + ".exe"]
            subprocess.run(compile_command, check=True)
            command = execute_command
        elif file_extension == ".c":
            # Compile and execute C file
            executable = os.path.splitext(code_file_name)[0]
            compile_command = ["gcc", code_path, "-o", executable]
            subprocess.run(compile_command, check=True)
            command = [f"./{executable}"]
        elif file_extension in [".cpp", ".c++", ".cc"]:
            # Compile and execute C++ file
            executable = os.path.splitext(code_file_name)[0]
            compile_command = ["g++", code_path, "-o", executable]
            subprocess.run(compile_command, check=True)
            command = [f"./{executable}"]
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")
            
        # Execute the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True)
        output = result.stdout if result.returncode == 0 else result.stderr
        
        # Return the dictionary
        return {
            "code": code,
            "output": output,
            "code_file_name": code_file_name
        }
    except subprocess.CalledProcessError as e:
        # Handle errors during execution
        return {
            "code": code,
            "output": e.stderr,
            "code_file_name": code_file_name
        }
        
@mcp.tool()
def list_codes(directory: str = CODE_STORAGE) -> List[str]:
    """
    List all code files in the specified directory.
    
    Args:
        directory: The directory to search for code files.
    
    Returns:
        A list of code file names (without paths).
    """
    # Get all code file paths
    code_files = get_all_code_paths(directory)
    
    # Extract only the file names from the full paths
    code_names = [os.path.basename(file) for file in code_files]
    
    return code_names

@mcp.tool()
def run_code(code_name: str) -> dict:
    """
    Execute a code file and return its output.
    
    Args:
        code_name: The name of the code file (without extension).
    
    Returns:
        A dictionary containing the code content, output, and file name.
    """
    # Get the full path to the code file
    code_path = get_code_path(code_name)
    
    # Execute the code and get the output
    try:
        result = execute_code(code_path)
    except Exception as e:
        print("Error executing code:", e)
        content = get_code(code_path)
        result = {
            "code": content,
            "output": str(e),
            "code_file_name": os.path.basename(code_path)
        }
    return result


if __name__ == "__main__":
    mcp.run() 