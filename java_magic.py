from IPython.core.magic import register_cell_magic
import subprocess
import tempfile

@register_cell_magic
def java(line, cell):
    # Create a temporary file for the Java code
    with tempfile.NamedTemporaryFile(suffix=".java", delete=False) as temp_file:
        temp_file.write(cell.encode("utf-8"))
        temp_file.flush()
        temp_file_name = temp_file.name
    
    # Execute the Java code using JShell
    try:
        process = subprocess.Popen(["jshell", "-q"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate(input=f"/open {temp_file_name}\n/exit\n")
        print(output)
        if error:
            print(f"Error:\n{error}")
    except subprocess.CalledProcessError as e:
        print(f"Error:\n{e.stderr}")
    finally:
        # Clean up the temporary file
        subprocess.run(["rm", temp_file_name], check=True)

def load_ipython_extension(ipython):
    ipython.register_magic_function(java, 'cell')
