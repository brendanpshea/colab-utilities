from IPython.core.magic import register_cell_magic
import subprocess
import tempfile

@register_cell_magic
def java(line, cell):
 # Write the Java code to a temporary file
    with open("script.java", "w") as f:
        f.write(cell)
    
    # Execute the Java code using JShell with quiet mode and startup file
    try:
        output = subprocess.run(["jshell", "-q", "script.java"], capture_output=True, text=True, check=True)
        print(output.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error:\n{e.stderr}")
    
    # Clean up the temporary file
    subprocess.run(["rm", "script.java"], check=True)   

def load_ipython_extension(ipython):
    ipython.register_magic_function(java, 'cell')
