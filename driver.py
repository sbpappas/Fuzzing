import time
import subprocess
import os  
import matplotlib.pyplot as plt


# throughout this file, I am writing function that run the fuzzer in each language
# then in the main function, call each function

#the times and specifications of each "fuzz" will be placed into this dict:

def run_python_fuzzer(script, args):
    print(f"Running script: fuzzer.py with arguments: {args}")

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

        if execution_time is not None:
            print(f"\n Python Execution Time: {execution_time:.6f} seconds")
        #print("\nScript Output (decoded):")
        #print(stdout)  # Decoded output from the script
        #print("\nScript Errors (if any):")
        print(stderr)  # Decoded errors from the script
        #print(f"\nReturn Code: {return_code}") 

        return execution_time
        #return execution_time, stdout, stderr, result.returncode

    except Exception as e:
        print(f"Error while running python script {script}: {e}")
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
        print(f"Running C {output_binary} with arguments: {prng_seed} {iterations}...")
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
        print(f"\nC Compile + run time: {all_end_time - all_start_time:.6f} seconds\n")
        execution_time = all_end_time - all_start_time
        return execution_time

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
        
        #print("=== Output ===")
        #print(stdout)
        #print("=== Errors ===")
        if stderr: print(stderr)
        
        # Check for errors
        if result.returncode != 0:
            print(f"Scala script failed with exit code {result.returncode}")
        else:
            print(f"\nScala execution time: {end_time - start_time:.6f} seconds\n")
            return end_time - start_time
    except Exception as e:
        print(f"An error occurred while running the Scala script: {e}")

def run_script(script_name, args, interpreter):
    """
    Abstract unction to run a script from any language with a specified interpreter
    
    :param script_name: Name of the script to run.
    :param args: List of arguments to pass to the script.
    :param interpreter: Interpreter to use for running the script (e.g., "python3", "julia").
    :return: None
    """
    print(f"Running script: {script_name} with arguments: {args}")
    
    command = [interpreter, script_name] + args  # Construct the command
    
    start_time = time.time()  # Start timing
    try:
        result = subprocess.run(
            command, 
            stdout=subprocess.PIPE,  # Capture standard output
            stderr=subprocess.PIPE,  # Capture errors
            #text=True,  # including this line makes an error
            check=True  # Raise exception if the command fails
        )
        end_time = time.time()  # End timing
        
        # Print output and timing information
        print(f"\n {interpreter} Execution Time: {end_time - start_time:.6f} seconds\n")
        #print(f"Script Output:\n{result.stdout}")
        #print(f"Script Errors (if any):\n{result.stderr}")
        return end_time - start_time
    except subprocess.CalledProcessError as e:
        end_time = time.time()  # End timing in case of errors
        print(f"\nAn error occurred while running the script: {e}\n")
        print(f"Execution Time: {end_time - start_time:.6f} seconds")
        print(f"Script Errors:\n{e.stderr}")
        

def compile_run_java_file(java_file, class_name, args):
    start_time = time.time()
    try:
        subprocess.run(["javac", java_file], check=True)
        print(f"Successfully compiled {java_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during compilation: {e}")
        exit(1)
    try:
        result = subprocess.run(
            ["java", class_name] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            #text=True,
            check=True
        )
        end_time = time.time()
        print(f"Successfully executed {class_name}")
        print(f"\n Java Compile and Execution Time: {end_time - start_time:.6f} seconds\n")
        return end_time - start_time
        #print(f"Program Output:\n{result.stdout}")
        #print(f"Program Errors (if any):\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Error while running Java program: {e}")
        print(f"Error Output:\n{e.stderr}")

def compile_and_run_typescript(ts_file: str, prng_seed: int, iterations: int):
    try:
        # Measure time for execution using ts-node
        start_ts_time = time.time()
        run_result = subprocess.run(
            ["npx", "ts-node", ts_file, str(prng_seed), str(iterations)],
            capture_output=True,
            #text=True # must be commented because text is not returned, weird bin chars are returned 
        )
        end_ts_time = time.time()

        # error checking
        if run_result.returncode != 0:
            print("TypeScript Execution Errors:")
            print(run_result.stderr)
            return

        print(f"TypeScript Compile Plus Execution Time: {end_ts_time - start_ts_time:.6f} seconds")
        # Uncomment below to see fuzzer output
        # print("Fuzzer Output:")
        # print(run_result.stdout)

        return end_ts_time - start_ts_time

    except FileNotFoundError as e:
        print("Error: Required command or file not found. Make sure Node.js, TypeScript, and ts-node are installed.")
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def compile_and_run_rust(args):
    start_time = time.time()
    original_dir = os.getcwd()
    try:
        os.chdir("./rust_fuzzer")
        print("running rust project...")
        subprocess.run(
            ["cargo", "run", "--"] + args,  #had issues here, no need to include spaces 
            stdout=subprocess.PIPE,         # get standard output
            stderr=subprocess.PIPE,         #get errors
            check=True                      #raise exception if the command fails
        )
    except subprocess.CalledProcessError as e:
        print(f"Error during rust running: {e}")
        print(f"Error Output:\n{e.stderr}")
        exit(1)
    finally:
        os.chdir(original_dir)
    end_time = time.time()
    print(f"Successfully executed Rust project")
    print(f"\nRust Compile and Execution Time: {end_time - start_time:.6f} seconds\n")
    return end_time - start_time
        #print(f"Program Output:\n{result.stdout}")
        #print(f"Program Errors (if any):\n{result.stderr}")

def run_all_fuzzers(prng_seed, iteration_counts):
    results = {}

    # Define the fuzzers as a mapping of language name to their runner functions
    fuzzers = {
        "Python": lambda iters: run_python_fuzzer("fuzzer.py", [prng_seed, str(iters)]),
        "C": lambda iters: run_c_fuzzer("fuzzer.c", "fuzzer", prng_seed, iters),
        "Scala": lambda iters: run_scala_script("fuzzer.scala", prng_seed, str(iters)),
        "Julia": lambda iters: run_script("fuzzer.jl", [prng_seed, str(iters)], "julia"),
        "Java": lambda iters: compile_run_java_file("Fuzzer.java", "Fuzzer", [prng_seed, str(iters)]),
        "JavaScript": lambda iters: run_script("fuzzer.js", [prng_seed, str(iters)], "node"),
        "TypeScript": lambda iters: compile_and_run_typescript("fuzzer.ts", prng_seed, iters),
        "Rust": lambda iters: compile_and_run_rust([prng_seed, str(iters)])
    }

    for lang, fuzzer_func in fuzzers.items():
        results[lang] = []
        for iters in iteration_counts:
            print(f"\nRunning {lang} fuzzer with {iters} iterations...")
            execution_time = fuzzer_func(iters)
            if execution_time:
                results[lang].append(execution_time)
            else:
                results[lang].append(None)  # Handle errors gracefully

    return results

def plot_results(results, iteration_counts):
    plt.figure(figsize=(10, 6))

    for lang, times in results.items():
        plt.plot(iteration_counts, times, label=lang, marker='o')

    plt.xlabel("Number of Iterations")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Fuzzer Execution Times by Language")
    plt.xscale("log")  # Use a logarithmic scale for iterations
    plt.yscale("log")  # Optional: Log scale for execution times
    plt.legend()
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.tight_layout()

    plt.savefig("fuzzer_execution_times.png")  # Save the plot
    plt.show()


if __name__ == "__main__":
    
    prng_seed = "12345"
    #iterations = input("enter the amount of iterations: ")
    
    #args = [prng_seed, iterations] #this will set up only the python fuzzers
    #run_python_fuzzer("fuzzer.py", args)
    #run_c_fuzzer("fuzzer.c", "fuzzer", prng_seed, int(iterations)) # the c call needs an int
    #run_scala_script("fuzzer.scala", prng_seed, iterations)
    #run_script("fuzzer.jl", [prng_seed, iterations], "julia") #julia script
    #compile_run_java_file("Fuzzer.java", "Fuzzer", [prng_seed, iterations])
    #run_script("fuzzer.js", [prng_seed, iterations], "node")
    #compile_and_run_typescript("fuzzer.ts", prng_seed, iterations)
    #compile_and_run_rust([prng_seed, iterations])

    iteration_counts = [10000, 50000, 100000, 500000, 750000, 1000000, 1500000] # can modify this to shorten or get more data points

    results = run_all_fuzzers(prng_seed, iteration_counts)
    print(results)
    plot_results(results, iteration_counts)


    
