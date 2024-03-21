from IPython.core.magic import register_cell_magic
import subprocess
import tempfile

@register_cell_magic
def java(line, cell):
    # Create a temporary directory for the classpath
    with tempfile.TemporaryDirectory() as temp_dir:
        # Write the Java code to a temporary file
        with open(f"{temp_dir}/Main.java", "w") as f:
            f.write(cell)
        
        # Execute the Java code using JShell with a custom classpath
        try:
            process = subprocess.Popen(["jshell", "--class-path", temp_dir], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = process.communicate(input=f"Main.java\n/exit\n")
            print(output)
            if error:
                print(f"Error:\n{error}")
        except subprocess.CalledProcessError as e:
            print(f"Error:\n{e.stderr}")

def load_ipython_extension(ipython):
    ipython.register_magic_function(java, 'cell')
