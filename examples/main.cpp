#include <julia.h>
JULIA_DEFINE_FAST_TLS()

int main(int, char *[])
{
	jl_init();

	jl_eval_string("println(sqrt(2.0))");

	jl_atexit_hook(0);

	return EXIT_SUCCESS;
}
