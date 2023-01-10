import heapq
from math import ceil
from enum import Enum
from schedule import Schedule
from job import Job

JobList = list[Job]


class SchedulingOrder(Enum):
    ROUND_ROBIN = 1
    LIST = 2


class Scheduler:
    def __init__(self, schedule: Schedule = None, machines: int = 1,
                 order: SchedulingOrder = SchedulingOrder.ROUND_ROBIN):
        if schedule is None:
            schedule = Schedule(total_machines=machines)

        self.schedule = schedule
        self.total_machines = machines
        self.order = order
        self.current_machine = 0

    def get_current_machine(self) -> int:
        if self.order == SchedulingOrder.ROUND_ROBIN:
            self.current_machine = \
                (self.current_machine + 1) % self.total_machines
            return self.current_machine
        elif self.order == SchedulingOrder.LIST:
            self.current_machine = self.schedule.first_available_machine()

        return self.current_machine

    def shortest_processing_time(self, jobs: JobList):
        """
        Schedules in ascending order of the processing times
        Minimises total completion times for non-preemptive jobs
        :param jobs:
        :return:
        """
        jobs.sort(key=lambda j: (j.get_processing_time(), j.index))

        return self.schedule_jobs(jobs)

    def weighted_shortest_processing_time(self, jobs: JobList):
        jobs.sort(
            key=lambda j: (j.get_processing_time() / j.get_weight(), j.index))

        return self.schedule_jobs(jobs)

    def longest_processing_time(self, jobs: JobList) -> Schedule:
        """
        Schedules jobs in descending order of their processing times.
        Used to reduce makespan for non-preemptive jobs parallel machines.
        :param jobs: list of jobs
        :return:
        """
        jobs.sort(key=lambda j: (-j.get_processing_time(), j.index))

        return self.schedule_jobs(jobs)

    def wrap_around_rule(self, jobs: JobList) -> Schedule:
        """
        Schedules jobs preemptively to minimise makespan
        :param jobs: list of jobs
        :return: current Schedule
        """
        processing_times = list(map(lambda j: j.get_processing_time(), jobs))
        longest_job = max(processing_times)
        makespan = max(longest_job,
                       ceil(sum(processing_times) / self.total_machines))

        self.schedule.schedule_preemptively(jobs, makespan)

        return self.schedule

    def earliest_due_date(self, jobs: JobList):
        """
        Schedules jobs in order of their due dates
        :param jobs:
        :return: current schedule
        """
        jobs.sort(key=lambda j: (j.get_due_date(), j.index))

        return self.schedule_jobs(jobs)

    def schedule_jobs(self, jobs: JobList):
        """
        Adds jobs to schedule at the required machine
        :param jobs:
        :return:
        """
        while jobs:
            self.schedule.add_job(jobs.pop(0), self.get_current_machine())

        return self.schedule

    def shortest_remaining_processing_time(self, jobs: JobList):
        """
        Minimises total completion time for preemptive jobs with release times
        :param jobs:
        :return:
        """
        jobs.sort(key=lambda j: j.get_release_time())
        pending_jobs = []
        t = 0
        while jobs or pending_jobs:
            while jobs and jobs[0].get_release_time() <= t:
                pending_jobs.append(jobs.pop(0))

            pending_jobs.sort(key=lambda j: j.get_processing_time())

            for i in range(self.total_machines):
                if i < len(pending_jobs):
                    j = pending_jobs[i]
                    self.schedule.add_job(j.get_slice(1), machine_index=i)
                    pending_jobs[i] = j.get_slice(j.processing_time - 1)
                else:
                    self.schedule.idle(1, i)

            pending_jobs = list(
                filter(lambda j: j.get_processing_time() > 0, pending_jobs))

            t += 1

        return self.schedule

    def moore_hodgson(self, jobs: JobList):
        """
        Minimises the total number of late jobs
        :param jobs: list of jobs
        :return: current schedule
        """
        jobs.sort(key=lambda j: j.get_due_date())
        maxHeap = []
        current = []
        late = []
        time = 0
        for j in jobs:
            current.append(j)
            heapq.heappush(maxHeap, (-j.get_processing_time(), j.index, j))
            time += j.get_processing_time()

            if time > j.get_due_date():
                _, _, longest_job = heapq.heappop(maxHeap)

                late.append(longest_job)
                current.remove(longest_job)
                time -= longest_job.get_processing_time()

        late.sort(key=lambda j: j.index)

        return self.schedule_jobs(current + late)
