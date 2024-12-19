use std::env;
//use std::fs::{File, OpenOptions};
use std::fs::File;
use std::io::{Read, Write};
use std::process;
//use std::time::SystemTime;
use rand::{Rng, SeedableRng};
use rand::rngs::StdRng;

fn create_seed_file() {
    // Create a seed file with default content
    let default_seed = b"InitialSeedData";
    let mut file = File::create("_seed_").expect("Failed to create seed file");
    file.write_all(default_seed).expect("Failed to write to seed file");
    eprintln!("Created a default seed file with content: {:?}", default_seed);
}

fn fuzz_this_thing(prng_seed: u64, iterations: usize) {
    // Ensure the seed file exists
    if !std::path::Path::new("_seed_").exists() {
        create_seed_file();
    }

    // Read the seed file into a byte array
    let mut seed_data = Vec::new();
    {
        let mut file = File::open("_seed_").expect("Failed to open seed file");
        file.read_to_end(&mut seed_data).expect("Failed to read seed file");
    }

    // Initialize the random number generator with the provided seed
    let mut rng = StdRng::seed_from_u64(prng_seed);

    for i in 0..iterations {
        for byte in seed_data.iter_mut() {
            if rng.gen::<f64>() < 0.13 {
                *byte = rng.gen_range(0..=255);
            }
        }

        // Extend the seed data every 500 iterations
        if (i + 1) % 500 == 0 {
            seed_data.extend((0..10).map(|_| rng.gen_range(0..=255)));
        }
    }

    // Write the mutated data to standard output
    std::io::stdout().write_all(&seed_data).expect("Failed to write mutated data to stdout");
}

fn main() {
    // Ensure the correct number of arguments is provided
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: {} <prng_seed> <iterations>", args[0]);
        process::exit(1);
    }

    // Parse the command-line arguments
    let prng_seed: u64 = args[1].parse().unwrap_or_else(|_| {
        eprintln!("Error: <prng_seed> must be a valid integer.");
        process::exit(1);
    });

    let iterations: usize = args[2].parse().unwrap_or_else(|_| {
        eprintln!("Error: <iterations> must be a valid integer.");
        process::exit(1);
    });

    // Run the fuzzer
    fuzz_this_thing(prng_seed, iterations);
}
