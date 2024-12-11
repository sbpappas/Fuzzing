import random
import sys 
import time
import os

def create_seed_file(): # usually just done the first time you run the fuzzer, creates a seed file 
    default_seed = b"InitialSeedData"
    with open("_seed_", "wb") as seeder:
        seeder.write(default_seed)
    print(f"Created a default seed file with content: {default_seed}", file=sys.stderr)

def fuzz_this_thing(prng_seed: int, iterations: int): # makes seed file if it is not located
    if not os.path.exists("_seed_"):
        create_seed_file()

    with open("_seed_", "rb") as seed:
        data = bytearray(seed.read())

    random.seed(prng_seed) # key for being deterministic

    for i in range(iterations): # I did not know if there was a quicker way to do this
        for j in range(len(data)): # double for loop takes soooo long but it works
            if random.random() < 0.13: # 13% chance of change
                data[j] = random.randint(0, 255)
        if (i + 1) % 500 == 0:         # every 500 passes extend by 10 
            data.extend(random.randint(0, 255) for _ in range(10))
    sys.stdout.buffer.write(data)

if __name__ == "__main__": # make sure we got the args
    if len(sys.argv) != 3:
        print("This is how you must run the fuzzer: ./fuzzer <prng_seed> <iterations>", file=sys.stderr)
        sys.exit(1)

    try: # validate
        prng_seed = int(sys.argv[1])
        iterations = int(sys.argv[2])
    except ValueError: # I ran into this a few times at the start so decided to add in a catch
        print("The input: <prng_seed> and <iterations> must be integers, try again.", file=sys.stderr)
        sys.exit(1)

    fuzz_this_thing(prng_seed, iterations)


