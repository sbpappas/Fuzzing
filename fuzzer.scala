import java.io.File 
import java.io.PrintWriter 
import java.io.{File, FileInputStream, FileOutputStream}
import scala.util.Random
import scala.util.Using

object Fuzzer {
    def create_seed_file(): Unit =  {// usually just done the first time you run the fuzzer, creates a seed file 
        val defaultSeed = "InitialSeedData".getBytes("UTF-8")        
        val seed_file = new File("_seed_" )    
        val print_Writer = new PrintWriter(seed_file)  
        // Writing to the file        
        //print_Writer.write(defaultSeed)  
        //print_Writer.close()      
        //println(s"Created a default seed file with content: $defaultSeed ")
        Using(new FileOutputStream(seed_file)) { fos =>
            fos.write(defaultSeed)
        }
        //println(s"Created a default seed file with content: ${new String(defaultSeed)}", Console.err)
        Console.err.println(s"Created a default seed file with content: ${new String(defaultSeed)}")
    } 

    def fuzzThisThing(prngSeed: Int, iterations: Int): Unit = {
        val seed_file = new File("_seed_")
        if (!seed_file.exists()) {
            create_seed_file()
        } 
        val data = Using(new FileInputStream(seed_file)) { fis =>
            val bytes = Array.fill[Byte](seed_file.length().toInt)(0)
            fis.read(bytes)
            bytes
        }.getOrElse {
            throw new RuntimeException("Failed to read seed file")
        }
        val random = new Random(prngSeed)
        val byteArray = data.toBuffer

        for (i <- 1 to iterations){
            for (j <- byteArray.indices){
                if (random.nextDouble() < 0.13) { // 13% chance to mutate
                     byteArray(j) = random.nextInt(256).toByte
                }
            }
            if ((i + 1) % 500 == 0) { // Extend the buffer every 500 iterations
                byteArray ++= Array.fill(10)(random.nextInt(256).toByte)
            }
        }
        // Write the fuzzed data to standard output
        println(byteArray.length)
        System.out.write(byteArray.toArray)


    }

 
    def main(args: Array[String]) = {
        println("Hello, world")
        println("Received arguments: " + args.mkString(", "))
        if (args.length != 2) {
            System.err.println("Two arguments required")
            System.exit(1)    
        }
        val prngSeed = try {
            args(0).toInt
        } catch {
            case _: NumberFormatException =>
                System.err.println("<prng_seed> must be an integer.")
                System.exit(1)
                0 // Unreachable
        }

        val iterations = try {
            args(1).toInt
        } catch {
            case _: NumberFormatException =>
                System.err.println("<iterations> must be an integer.")
                System.exit(1)
                0 // Unreachable
        }

        // Call the fuzzing function
        fuzzThisThing(prngSeed, iterations)
    }
}