import logging

logger = logging.getLogger("Power Of A Generator")
logging.basicConfig(level=logging.INFO)


class PowerOfAGenerator:
    a: int
    n: int
    index: int

    def __init__(self, a: int, n: int):
        self.a = a
        self.n = n
        self.index = 0

    def __next__(self):
        if self.index > self.n:
            raise StopIteration
        self.index += 1
        return self.a ** self.index

    def __iter__(self):
        return self


def main():
    power_of_a_gen = PowerOfAGenerator(5, 5)
    for i in power_of_a_gen:
        logger.info(i)
    power_of_a_gen = PowerOfAGenerator(-2, 7)
    for i in power_of_a_gen:
        logger.info(i)
    power_of_a_gen = PowerOfAGenerator(0, 12)
    for i in power_of_a_gen:
        logger.info(i)
    power_of_a_gen = PowerOfAGenerator(1, 3)
    for i in power_of_a_gen:
        logger.info(i)


if __name__ == '__main__':
    main()
