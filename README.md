# Fuzzing
This project uses fuzz testing ("fuzzing"), a computatationally lengthy process, to measure the performance difference between different major programming languages.

To run: Download the github project, make sure all of the languages (C++, Julia, Javascript, Java, TypeScript, Scala, Python, Rust) are installed on your computer, and run the command 'python3 driver.py'

What is fuzz testing? Essentially, it is intentionally feeding programs with invalid, unexpected, or random data to identify potential vulnerabilities by observing if the program crashes or exhibits abnormal behavior when processing the strange inputs. 

In this program, the output of each "fuzzer" are varying amounts of binary. If you would like, you can change the size of the outputted files (and thus the time that it will take to "fuzz") in the driver function.

Finally, the script creates a visualization using the python matplotlib library to display the results on a simple line graph.