from random import seed, randint
from src.job import Job
from src.scheduler import Scheduler, SchedulingOrder


if __name__ == '__main__':
    jobs = []
    processing_times = [6, 4, 2, 1, 3, 2]
    release_times = [1, 2, 3, 4, 5, 6]
    for i, (p, r) in enumerate(zip(processing_times, release_times)):
        jobs.append(Job(i + 1, processing_time=p, release_time=r))

    for m in range(1, 4):
        s = Scheduler(machines=m, order=SchedulingOrder.LIST)
        sch = s.longest_processing_time(jobs.copy())
        sch.plot(f'gantt-chart-{m}')