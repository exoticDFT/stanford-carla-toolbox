#include <iostream>

double stressTest()
{
	double sum = 0.0;

	for (long int i = 1; i <= 1234567890; ++i)
	{
		sum += i;
	}

	return sum;
}

// Call the function and print the result
int main(int, char *[])
{
    auto sum = stressTest();

	std::cout << "Sum: " << sum << std::endl;

    return EXIT_SUCCESS;
}