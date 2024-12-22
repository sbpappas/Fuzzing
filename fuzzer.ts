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

    let data: Buffer = Buffer.from(fs.readFileSync("_seed_")); // expliciting typing this is necessary for concat later
    //needs to be let, not const bc it will update

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
            const additionalData = Buffer.alloc(10); // Create a buffer of size 10
            for (let k = 0; k < 10; k++) {
                additionalData[k] = Math.floor(random() * 256);
            }
            // concat original data with new data. TS has no dynamic resizing, need to create new arrays
            data = Buffer.concat([data as Buffer, additionalData as Buffer]);
        }
        
    }

    // Output the fuzzed data
    process.stdout.write(data);
    console.log(data.length)
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
    console.log(iterations)
    fuzzThisThing(prngSeed, iterations);
}

main();