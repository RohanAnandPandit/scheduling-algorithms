from random import randint
from machine import Machine
from src.job import Job, Idle
import matplotlib.pyplot as plt

JobList = list[Job]


class Schedule:
    def __init__(self, total_machines: int = 1, machines: list[Machine] = None):
        if machines is None:
            machines: list[Machine] = []
            for i in range(total_machines):
                machines.append(Machine(i))
        self.machines = machines
        self.total_machines = len(machines)
        self.jobs = {}
        self.job_colour = {0: (1.0, 1.0, 1.0)}

    def available_machines(self) -> int:
        return len(self.machines)

    def makespan(self) -> int:
        return max(map(lambda m: m.get_makespan(), self.machines))

    def calculate_completion_times(self):
        completion_times = {}
        for machine in self.machines:
            for job in machine.jobs:
                if job.index not in completion_times:
                    completion_times[job.index] = 0
                completion_times[job.index] = max(completion_times[job.index],
                                                  job.get_completion_time())

        return completion_times

    def total_tardiness(self):
        completion_times = self.calculate_completion_times()
        tardiness = 0
        for i in completion_times:
            if i == 0:
                continue
            tardiness += max(0,
                             completion_times[i] - self.jobs[i].get_due_date())

        return tardiness

    def total_lateness(self):
        completion_times = self.calculate_completion_times()
        lateness = 0
        for i in completion_times:
            lateness += completion_times[i] - self.jobs[i].get_due_date()

        return lateness

    def first_available_machine(self) -> int:
        return min(self.machines, key=lambda m: m.get_makespan()).index

    def assign_colour(self, job: Job):
        """
        Generates a unique random colour for the given job
        :param job:
        :return:
        """
        if job.index not in self.job_colour:
            r, g, b = randint(25, 75) / 100, randint(25, 75) / 100, \
                      randint(25, 75) / 100
            self.job_colour[job.index] = (r, g, b)

    def idle(self, time: int, machine_index):
        self.add_job(Idle(time), machine_index)

    def add_job(self, job: Job, machine_index: int = 0):
        """
        Adds job to the machine at the given index
        :param job:
        :param machine_index:
        :return:
        """
        self.assign_colour(job)

        machine = self.machines[machine_index]
        machine.add_job(job)

        self.jobs[job.index] = job

        return self

    def plot(self, fname):
        """
        Creates and saves the gantt chart for the schedule with the given
        file name
        :param fname:
        :return:
        """
        fig, gnt = plt.subplots()
        # fig.set_figheight(20)
        fig.set_figwidth(9)
        gap_y = 10
        gap_x = 1
        # Setting Y-axis limits
        gnt.set_ylim(0, gap_y * (self.available_machines() + 1))

        # Setting X-axis limits
        gnt.set_xlim(0, self.makespan() + 1)

        # Setting labels for x-axis and y-axis
        gnt.set_xlabel('Time')
        # gnt.set_ylabel('Machine')

        # Setting ticks on y-axis
        gnt.set_yticks(
            [gap_y * (i + 1) for i in range(self.available_machines())])
        # Labelling tickers of y-axis
        gnt.set_yticklabels(
            [f'M{str(i + 1)}' for i in range(self.available_machines())][::-1])
        gnt.set_xticks([gap_x * i for i in range(self.makespan() + 1)])
        gnt.set_xticklabels(
            [str(i) for i in range(self.makespan() + 1)])
        # Setting graph attribute
        # gnt.grid(True)
        bar_height = 10
        for i in range(self.available_machines()):
            m = self.machines[i]
            curr = 0
            for j in m.get_jobs():
                y = (self.available_machines() - i) * gap_y - int(
                    (bar_height - 2) / 2)
                if not j.is_idle():
                    gnt.broken_barh([(curr, gap_x * j.get_processing_time())],
                                    (y, bar_height - 2),
                                    facecolors=self.job_colour[j.index],
                                    edgecolor='black')
                    gnt.text(curr + 0.1, y + 1, f'J{j.index}', color='white')
                curr += j.get_processing_time()

        plt.savefig(f"{fname}.png", dpi=300)

    def schedule_preemptively(self, jobs: JobList, max_makespan: int):
        """
        Preemptive schedules jobs with up to the given limit for makespan
        before moving on to the next machine
        :param jobs:
        :param max_makespan:
        :return:
        """
        for machine in self.machines:
            if not jobs:
                break
            while machine.get_makespan() < max_makespan:
                if not jobs:
                    break

                j = jobs.pop(0)
                rem = max_makespan - machine.get_makespan()

                if rem >= j.get_processing_time():
                    self.add_job(j, machine_index=machine.index)
                else:
                    self.add_job(j.get_slice(rem), machine_index=machine.index)
                    jobs.insert(0, Job(j.index, j.get_slice(
                        j.get_processing_time() - rem)))

    def get_jobs(self):
        return list(map(lambda m: m.get_jobs(), self.machines))
