from multiprocessing import Process, Manager
import logging

logger = logging.getLogger("Twin Prime Number")
logging.basicConfig(level=logging.INFO)


def isPrime(n):
    if n <= 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            logger.debug(f"{n}%{i} not prime")
            return False
    logger.debug(f"{n} prime")
    return True


def calculate_partial(shared_list, range_from_calculate, range_to_calculate):
    logger.debug(f"calculating from {range_from_calculate} to {range_to_calculate}")
    for i in range(range_from_calculate, range_to_calculate + 1):
        if isPrime(i):
            shared_list.append(i)


def search_for_twins_in_range(shared_list, prime_list, range_from_calculate, range_to_calculate):
    logger.debug(f"calculating from {range_from_calculate} to {range_to_calculate}")
    if range_to_calculate == range_from_calculate:
        if len(prime_list) > range_to_calculate + 1 and abs(
                prime_list[range_to_calculate] - prime_list[range_to_calculate + 1]) == 2:
            shared_list.append(prime_list[range_to_calculate])
            shared_list.append(prime_list[range_to_calculate + 1])
    for i in range(range_from_calculate, range_to_calculate):
        if len(prime_list) > i + 1 and abs(prime_list[i] - prime_list[i + 1]) == 2:
            shared_list.append(prime_list[i])
            shared_list.append(prime_list[i + 1])


def calculate_range(range_to_calculate, processes_number):
    with Manager() as manager:
        prime_list = manager.list()
        twin_prime_list = manager.list()

        processes = []
        for i in range(processes_number):
            process = Process(target=calculate_partial(prime_list, int(range_to_calculate / processes_number * i),
                                                       int(range_to_calculate / processes_number * (i + 1) - 1)))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        processes = []
        for i in range(processes_number):
            process = Process(
                target=search_for_twins_in_range(twin_prime_list, prime_list,
                                                 int(len(prime_list) / processes_number * i),
                                                 int(len(prime_list) / processes_number * (i + 1) - 1)))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        logger.info(prime_list)
        logger.info(twin_prime_list)


def main():
    calculate_range(100000, 16)


if __name__ == '__main__':
    main()
