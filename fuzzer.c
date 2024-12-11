#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <unistd.h> // including this for `access` and `F_OK`


#define SEED_FILE "_seed_"
#define DEFAULT_SEED "InitialSeedData"

// Function to create the seed file if it does not exist
void create_seed_file() {
    FILE *seeder = fopen(SEED_FILE, "wb");
    if (!seeder) {
        perror("Error creating seed file");
        exit(EXIT_FAILURE);
    }
    fwrite(DEFAULT_SEED, sizeof(char), strlen(DEFAULT_SEED), seeder);
    fclose(seeder);
    fprintf(stderr, "Created a default seed file with content: %s\n", DEFAULT_SEED);
}

// Function to read the seed file into a dynamically allocated buffer
uint8_t *read_seed_file(size_t *size) {
    FILE *seed = fopen(SEED_FILE, "rb");
    if (!seed) {
        perror("Error opening seed file");
        exit(EXIT_FAILURE);
    }

    fseek(seed, 0, SEEK_END);
    *size = ftell(seed);
    rewind(seed);

    uint8_t *data = (uint8_t *)malloc(*size);
    if (!data) {
        perror("Error allocating memory for seed data");
        fclose(seed);
        exit(EXIT_FAILURE);
    }

    fread(data, sizeof(uint8_t), *size, seed);
    fclose(seed);
    return data;
}

// Function to fuzz the data
void fuzz_this_thing(unsigned int prng_seed, int iterations) {
    size_t data_size;
    if (access(SEED_FILE, F_OK) != 0) {
        create_seed_file();
    }

    uint8_t *data = read_seed_file(&data_size);

    srand(prng_seed); // Initialize random number generator

    for (int i = 0; i < iterations; i++) {
        for (size_t j = 0; j < data_size; j++) {
            if ((rand() / (double)RAND_MAX) < 0.13) { // 13% chance of change
                data[j] = rand() % 256;
            }
        }

        // Extend data every 500 iterations
        if ((i + 1) % 500 == 0) {
            data = (uint8_t *)realloc(data, data_size + 10);
            if (!data) {
                perror("Error reallocating memory");
                exit(EXIT_FAILURE);
            }
            for (int k = 0; k < 10; k++) {
                data[data_size + k] = rand() % 256;
            }
            data_size += 10;
        }
    }

    // Write the fuzzed data to stdout
    fwrite(data, sizeof(uint8_t), data_size, stdout);
    free(data);
}

// Main function
int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "This is how you must run the fuzzer: ./fuzzer <prng_seed> <iterations>\n");
        return EXIT_FAILURE;
    }

    unsigned int prng_seed;
    int iterations;

    // Validate input arguments
    if (sscanf(argv[1], "%u", &prng_seed) != 1 || sscanf(argv[2], "%d", &iterations) != 1) {
        fprintf(stderr, "The input: <prng_seed> and <iterations> must be integers, try again.\n");
        return EXIT_FAILURE;
    }

    fuzz_this_thing(prng_seed, iterations);
    return EXIT_SUCCESS;
}
