from random import seed, randint
from src.job import Job
from src.scheduler import Scheduler, SchedulingOrder


def SRPT():
    jobs = []
    processing_times = [6, 4, 2, 1, 3, 2]
    release_times = [1, 2, 3, 4, 5, 6]
    for i, (p, r) in enumerate(zip(processing_times, release_times)):
        jobs.append(Job(i + 1, processing_time=p, release_time=r))

    for m in range(1, 4):
        s = Scheduler(machines=m)
        sch = s.shortest_remaining_processing_time(jobs.copy())
        sch.plot(f'SRPT-{m}')
        # print(f'tardiness: {sch.total_tardiness()}')


if __name__ == '__main__':
    SRPT()
    # s = Scheduler(machines=5, order=SchedulingOrder.LIST)
    # jobs = []
    #
    seed(11)
    # for i in range(1, 10):
    #     j = Job(i, processing_time=randint(1, 5), due_date=randint(1, 5))
    #     # print(j.index, j.processing_time)
    #     jobs.append(j)
    #
    # sch = s.wrap_around_rule(jobs)
    # sch.plot('gantt')
    # print(f'tardiness: {sch.total_tardiness()}')
