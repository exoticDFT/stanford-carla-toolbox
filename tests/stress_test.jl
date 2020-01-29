function stress_test()::Float64
    sum::Float64 = 0.0
 
    for j = 1:1234567890
        sum = sum + j
    end

    return sum
end

# Call the function and print the result
sum = stress_test()

println("Sum:", sum)