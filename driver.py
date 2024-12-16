import time
import subprocess

def run_python_fuzzer(script, args):
    """
    Run a Python script with arguments and time its execution.

    Parameters:
        script (str): Path to the Python script to run.
        args (list): List of arguments to pass to the script.

    Returns:
        tuple: (execution_time, stdout, stderr, return_code)
    """
    start_time = time.perf_counter()
    try:
        # Run the script and capture binary output
        result = subprocess.run(
            ["python3", script] + args,
            capture_output=True,
            text=False  # Set to False to capture raw bytes
        )
        end_time = time.perf_counter()
        execution_time = end_time - start_time

        # Decode stdout and stderr, handle decoding errors gracefully
        stdout = result.stdout.decode("utf-8", errors="replace")
        stderr = result.stderr.decode("utf-8", errors="replace")

        return execution_time, stdout, stderr, result.returncode

    except Exception as e:
        print(f"Error while running script {script}: {e}")
        return None, None, None, None

def run_c_fuzzer(c_file, output_binary, prng_seed, iterations):
    # compile the C file
    try:
        print(f"Compiling {c_file}...")
        all_start_time = time.perf_counter()
        compile_process = subprocess.run(
            ["gcc", "-o", output_binary, c_file],
            capture_output=True,
            text=True
        )
        if compile_process.returncode != 0:
            print("Compilation failed:")
            print(compile_process.stderr)
            return
        print("Compilation successful.")
    except Exception as e:
        print(f"Error during compilation: {e}")
        return

    # run the compiled binary
    try:
        print(f"Running {output_binary} with arguments: {prng_seed} {iterations}...")
        start_time = time.perf_counter()
        run_process = subprocess.run(
            [f"./{output_binary}", str(prng_seed), str(iterations)],
            capture_output=True,
            text=False  # Output might kinda crazy
        )
        all_end_time = time.perf_counter()
        end_time = time.perf_counter()
        
        if run_process.returncode != 0:
            print("Execution failed:")
            print(run_process.stderr.decode('utf-8', errors='replace'))
        else:
            print("Execution of C fuzzer successful:")
            #print("Output:")
            #print(run_process.stdout.decode('utf-8', errors='replace'))

        print(f"C Run time: {end_time - start_time:.6f} seconds")
        print(f"C Compile + run time: {all_end_time - all_start_time:.6f} seconds")
    except Exception as e:
        print(f"Error during execution: {e}")

def run_scala_script(scala_file, *args):
    try:
        # Construct the command to run scala-cli with arguments
        command = ["scala-cli", "run", scala_file, "--"] + list(args)
        print(f"Running command: {' '.join(command)}")
        
        # Measure execution time
        start_time = time.time()
        
        # Execute the command
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        end_time = time.time()
        
        # Decode output using 'replace' to handle encoding errors gracefully
        stdout = result.stdout.decode(errors="replace")
        stderr = result.stderr.decode(errors="replace")
        
        print("=== Output ===")
        print(stdout)
        print("=== Errors ===")
        print(stderr)
        
        # Check for errors
        if result.returncode != 0:
            print(f"Scala script failed with exit code {result.returncode}")
        else:
            print(f"Scala script ran successfully in {end_time - start_time:.6f} seconds!")
    except Exception as e:
        print(f"An error occurred while running the Scala script: {e}")


if __name__ == "__main__":
    # define the script to run and its arguments
    python_script = "fuzzer.py"
    prng_seed = "12345"
    iterations = "30005"
    args = [prng_seed, iterations]

    print(f"Running script: {python_script} with arguments: {args}")

    # run the script and time it
    execution_time, stdout, stderr, return_code = run_python_fuzzer(python_script, args)

    if execution_time is not None:
        print(f"\nExecution Time: {execution_time:.6f} seconds")
        #print("\nScript Output (decoded):")
        #print(stdout)  # Decoded output from the script
        print("\nScript Errors (if any):")
        print(stderr)  # Decoded errors from the script
        #print(f"\nReturn Code: {return_code}") 

    c_fuzzer_file = "fuzzer.c"
    output_binary = "fuzzer"
    #prng_seed = int(prng_seed)
    #iterations = iterations

    run_c_fuzzer(c_fuzzer_file, output_binary, prng_seed, iterations)

    scala_fuzzer_file = "fuzzer.scala"
    run_scala_script(scala_fuzzer_file, prng_seed, iterations)


