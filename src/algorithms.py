from typing import Callable
from job import Job
from schedule import Schedule
from machine import Machine

JobList = list[Job]


def simulated_annealing(*, initial_schedule: Machine,
                        temperature: int,
                        cooling_rate: float, iterations: int,
                        cost_function: Callable[[Machine], int]) -> Schedule:
    """
    Probabilistically selects neighbours to find the global optimum for the
    given cost function
    :param initial_schedule:
    :param temperature:
    :param cooling_rate:
    :param iterations:
    :param cost_function:
    :return:
    """
    assert 0 < cooling_rate < 1
    assert iterations >= 0

    from random import random
    from math import e

    best_schedule = initial_schedule
    current_schedule = initial_schedule
    best_cost = cost_function(best_schedule)

    for _ in range(iterations):
        random_neighbour = current_schedule.random_neighbour()
        current_cost = cost_function(current_schedule)
        neighbour_cost = cost_function(random_neighbour)

        delta = current_cost - neighbour_cost

        if delta >= 0 or random() < e ** (delta / temperature):
            current_schedule = random_neighbour
            if neighbour_cost < best_cost:
                best_cost = neighbour_cost
                best_schedule = random_neighbour

        temperature *= cooling_rate

    return best_schedule


def tabu_search(*, initial_schedule: Machine, tabu_list_size: int,
                threshold: int, iterations: int,
                cost_function: Callable[[Machine], int]):
    """
    A deterministic heuristic method for finding the global optimum schedule
    for the cost function while tracking forbidden job swaps
    :param initial_schedule:
    :param tabu_list_size:
    :param threshold:
    :param iterations:
    :param cost_function:
    :return:
    """
    assert tabu_list_size >= 0
    assert threshold > 0

    best_schedule = initial_schedule
    current_schedule = initial_schedule
    best_cost = cost_function(initial_schedule)
    swap_index = 0
    tabu_list: list[(int, int)] = []

    for _ in range(iterations):
        delta = float('-inf')
        job_ids = current_schedule.job_ids
        current_cost = cost_function(current_schedule)
        j1, j2 = job_ids[swap_index], job_ids[swap_index + 1]
        random_neighbour = current_schedule
        while delta < -threshold:
            j1, j2 = job_ids[swap_index], job_ids[swap_index + 1]
            if (j1, j2) in tabu_list:
                swap_index = (swap_index + 1) % (len(job_ids) - 1)
                continue
            random_neighbour = current_schedule.swap_jobs(swap_index,
                                                          swap_index + 1)
            neighbour_cost = cost_function(random_neighbour)
            if neighbour_cost < best_cost:
                best_schedule = random_neighbour
                best_cost = neighbour_cost
                break
            delta = current_cost - neighbour_cost
            swap_index = (swap_index + 1) % (len(job_ids) - 1)

        current_schedule = random_neighbour
        tabu_list.append((j1, j2))
        if len(tabu_list) > tabu_list_size:
            tabu_list.pop(0)

    return best_schedule
