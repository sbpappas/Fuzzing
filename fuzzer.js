"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var fs = require("fs");
function createSeedFile() {
    var defaultSeed = Buffer.from("InitialSeedData");
    fs.writeFileSync("_seed_", defaultSeed);
    console.error("Created a default seed file with content: ".concat(defaultSeed.toString()));
}
function fuzzThisThing(prngSeed, iterations) {
    // Create seed file if it doesn't exist
    if (!fs.existsSync("_seed_")) {
        createSeedFile();
    }
    var data = Buffer.from(fs.readFileSync("_seed_")); // expliciting typing this is necessary for concat later
    //needs to be let, not const bc it will update
    // Set up PRNG
    var random = seededRandom(prngSeed);
    // Fuzzing logic
    for (var i = 0; i < iterations; i++) {
        for (var j = 0; j < data.length; j++) {
            if (random() < 0.13) { // 13% chance of mutation
                data[j] = Math.floor(random() * 256); // Random byte
            }
        }
        if ((i + 1) % 500 === 0) { // Every 500 iterations, extend the data
            var additionalData = Buffer.alloc(10); // Create a buffer of size 10
            for (var k = 0; k < 10; k++) {
                additionalData[k] = Math.floor(random() * 256);
            }
            // concat original data with new data. TS has no dynamic resizing, need to create new arrays
            data = Buffer.concat([data, additionalData]);
        }
    }
    // Output the fuzzed data
    process.stdout.write(data);
    console.log(data.length);
}
function seededRandom(seed) {
    // Simple seeded random number generator
    return function () {
        var x = Math.sin(seed++) * 10000;
        return x - Math.floor(x);
    };
}
function main() {
    var args = process.argv.slice(2);
    if (args.length !== 2) {
        console.error("Usage: node fuzzer.js <prng_seed> <iterations>");
        process.exit(1);
    }
    var prngSeed = parseInt(args[0], 10);
    var iterations = parseInt(args[1], 10);
    if (isNaN(prngSeed) || isNaN(iterations)) {
        console.error("Both <prng_seed> and <iterations> must be valid integers.");
        process.exit(1);
    }
    console.log(iterations);
    fuzzThisThing(prngSeed, iterations);
}
main();
