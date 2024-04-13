import os
import subprocess

def interactive_terminal():
    """
    Launch an interactive terminal-like interface in Google Colab.

    This function provides a simulated Ubuntu terminal experience within a Colab notebook.
    It allows users to execute basic Ubuntu commands, navigate directories, and manage files.

    Usage:
    - Run the function to start the interactive terminal.
    - Enter commands at the prompt to execute them.
    - Use 'cd' followed by a directory path to change the current working directory.
    - Use 'exit' to terminate the interactive terminal.

    Returns:
    None
    """
    def run_command(command):
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            return output
        except subprocess.CalledProcessError as e:
            return f"Error: {e.output}"

    def change_directory(directory):
        try:
            os.chdir(directory)
            return ""
        except FileNotFoundError:
            return f"Error: Directory '{directory}' not found."
        except NotADirectoryError:
            return f"Error: '{directory}' is not a directory."
        except PermissionError:
            return f"Error: Permission denied changing to '{directory}'."
        except Exception as e:
            return f"Error: {str(e)}"

    while True:
        # Get the current working directory
        cwd = os.getcwd()
        
        # Get the username
        username = os.environ.get('USER', 'colab')
        
        # Display the Ubuntu-like prompt
        prompt = f"{username}@colab:{cwd}$ "
        
        command = input(prompt)
        if command.lower() == 'exit':
            break
        
        if command.startswith('cd '):
            directory = command[3:]
            output = change_directory(directory)
        else:
            output = run_command(command)
        
        print(output)
