import java.io.*;
import java.nio.file.*;
import java.util.*;

public class Fuzzer {

    public static void create_seed_file(String seedFile) throws IOException {
        String defaultSeed = "Initial Seed Data";
        Files.write(Paths.get(seedFile), defaultSeed.getBytes()); //make file with binary contents of string
        System.out.println("Created a default seed file with content: " + defaultSeed);
    }

    public static void fuzzThisThing(int prngSeed, int iterations, String seedFile) throws IOException {
        // Check if the seed file exists, create it if not
        if (!Files.exists(Paths.get(seedFile))) {
            create_seed_file(seedFile);
        }

        byte[] data = Files.readAllBytes(Paths.get(seedFile));// Read the seed file into a byte array
        Random rng = new Random(prngSeed);

        for (int i = 0; i < iterations; i++) {
            for (int j = 0; j < data.length; j++) {
                if (rng.nextDouble() < 0.13) { // 13% chance to mutate a byte
                    data[j] = (byte) rng.nextInt(256); // Random byte (0x00 to 0xFF)
                }
            }

            // Every 500 iterations, extend the data buffer with 10 random bytes
            if (i % 500 == 0) {
                byte[] extraBytes = new byte[10];
                rng.nextBytes(extraBytes);
                data = Arrays.copyOf(data, data.length + extraBytes.length);
                System.arraycopy(extraBytes, 0, data, data.length - extraBytes.length, extraBytes.length);
            }
        }

        // Print the fuzzed data as raw bytes
        System.out.write(data.length);
    }

    public static void main(String[] args) {
        if (args.length != 2) {
            System.err.println("Usage: java Fuzzer <prng_seed> <iterations>");
            System.exit(1);
        }

        try {
            int prngSeed = Integer.parseInt(args[0]);
            int iterations = Integer.parseInt(args[1]);

            // Run the fuzzer with the seed file "_seed_"
            fuzzThisThing(prngSeed, iterations, "_seed_");
        } catch (NumberFormatException e) {
            System.err.println("Both arguments <prng_seed> and <iterations> must be integers.");
            e.printStackTrace();
            System.exit(1);
        } catch (IOException e) {
            System.err.println("An error occurred while reading or writing files.");
            e.printStackTrace();
            System.exit(1);
        }
    }
}
