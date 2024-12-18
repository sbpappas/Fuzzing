using Random
using Printf

function create_seed_file(seed_file::String) #pass in the name of our seed file because so we can name it whatever
    default_seed = "Initial Seed Data"
    open(seed_file, "w") do io
        write(io, default_seed)
    end
    @warn "Created a default seed file with content: $default_seed"
end

function fuzz_this_thing(prng_seed::Int, iterations::Int, seed_file::String)
    if !isfile(seed_file)
        create_seed_file(seed_file)
        println("Created seed file.")
        printstyled(io, "seed file created: $seed_file", color=:red)
    end

    
    data = Vector{UInt8}(read(seed_file)) # read seed file into a mutable byte array

    rng = MersenneTwister(prng_seed) #julia docs say this is a quick prng
    #however, may as well try another one for speed commparison

    for i in 1:iterations
        for j in eachindex(data)
            if rand(rng) < 0.13  # 13% chance to mutate a byte
                data[j] = rand(rng, UInt8)  # random between 0x00 and 0xFF
            end
        end

        if i % 500 == 0 # Every 500 iterations, extend the data buffer with 10 random bytes
            append!(data, [rand(rng, UInt8) for _ in 1:10]) 
        end
    end
    # Write the fuzzed data to standard output
    write(stdout, data) # what is the difference here to println() ?
end

function main()
    if length(ARGS) != 2 # parse arguments
        @error "Usage: julia fuzzer.jl <prng_seed> <iterations>"
        exit(1)
    end

    try
        prng_seed = parse(Int, ARGS[1])
        iterations = parse(Int, ARGS[2])

        fuzz_this_thing(prng_seed, iterations, "_seed_") #call the fuzzer
    catch e
        @error "Both arguments <prng_seed> and <iterations> must be integers." exception=(e, catch_backtrace())
        exit(1)
        #i am running into this error if I delete the seed file and run just the julia file
        #however, if I run it again after the seed is created, it works. ??
    end
end

# Run the program if executed as a script
if abspath(PROGRAM_FILE) == @__FILE__
    main()
end