import time
import subprocess

def run_script(script, args):
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

if __name__ == "__main__":
    # Define the script to run and its arguments
    script = "fuzzer.py"
    prng_seed = "1234"
    iterations = "1000"
    args = [prng_seed, iterations]

    print(f"Running script: {script} with arguments: {args}")

    # Run the script and time it
    execution_time, stdout, stderr, return_code = run_script(script, args)

    if execution_time is not None:
        print(f"\nExecution Time: {execution_time:.6f} seconds")
        print("\nScript Output (decoded):")
        print(stdout)  # Decoded output from the script
        print("\nScript Errors (if any):")
        print(stderr)  # Decoded errors from the script
        print(f"\nReturn Code: {return_code}")
