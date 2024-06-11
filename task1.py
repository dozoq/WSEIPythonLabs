import functools
import logging
import inspect


logger = logging.getLogger("Input Logger")


def input_parameters_logging_wrapper(func):
    @functools.wraps(func)
    def internal_function(*args, **kwargs):
        parsed_args = '{'
        for ind, (arg, name) in enumerate(zip(args, inspect.signature(func).parameters.values())):
            parsed_args += f"{name}:{type(arg)}{',' if ind != len(args)-1 else ''}"
        parsed_args += '}'
        logger.info(parsed_args)
        result = func(*args, **kwargs)
        return result
    return internal_function


@input_parameters_logging_wrapper
def function_to_decorate(a, b, c):
    pass


def main():
    logging.basicConfig(level=logging.INFO)
    function_to_decorate(1, "c", True)
    function_to_decorate((i for i in range(0,100)), input_parameters_logging_wrapper, (True, False))


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
