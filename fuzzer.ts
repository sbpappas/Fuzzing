import * as fs from "fs";

function createSeedFile(): void {
    const defaultSeed = Buffer.from("InitialSeedData");
    fs.writeFileSync("_seed_", defaultSeed);
    console.error(`Created a default seed file with content: ${defaultSeed.toString()}`);
}

function fuzzThisThing(prngSeed: number, iterations: number): void {
    // Create seed file if it doesn't exist
    if (!fs.existsSync("_seed_")) {
        createSeedFile();
    }

    // Read the seed file into a buffer
    const data = Buffer.from(fs.readFileSync("_seed_"));

    // Set up PRNG
    const random = seededRandom(prngSeed);

    // Fuzzing logic
    for (let i = 0; i < iterations; i++) {
        for (let j = 0; j < data.length; j++) {
            if (random() < 0.13) { // 13% chance of mutation
                data[j] = Math.floor(random() * 256); // Random byte
            }
        }
        if ((i + 1) % 500 === 0) { // Every 500 iterations, extend the data
            for (let k = 0; k < 10; k++) {
                data[data.length] = Math.floor(random() * 256);
            }
        }
    }

    // Output the fuzzed data
    process.stdout.write(data);
}

function seededRandom(seed: number): () => number {
    // Simple seeded random number generator
    return () => {
        const x = Math.sin(seed++) * 10000;
        return x - Math.floor(x);
    };
}

function main(): void {
    const args = process.argv.slice(2);

    if (args.length !== 2) {
        console.error("Usage: node fuzzer.js <prng_seed> <iterations>");
        process.exit(1);
    }

    const prngSeed = parseInt(args[0], 10);
    const iterations = parseInt(args[1], 10);

    if (isNaN(prngSeed) || isNaN(iterations)) {
        console.error("Both <prng_seed> and <iterations> must be valid integers.");
        process.exit(1);
    }

    fuzzThisThing(prngSeed, iterations);
}

main();