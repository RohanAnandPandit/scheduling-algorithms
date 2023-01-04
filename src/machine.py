from job import Job, Idle

JobList = list[Job]


class Machine:
    def __init__(self, index, jobs: JobList = None):
        self.index = index
        self.jobs: JobList = []
        self.job_ids = []
        self.makespan = 0

        if jobs:
            for j in jobs:
                self.add_job(j)

    def get_makespan(self) -> int:
        return self.makespan

    def set_idleness(self, job: Job) -> None:
        self.idle(max(0, job.release_time - self.makespan))

    def add_job(self, job: Job) -> None:
        self.set_idleness(job)

        if len(self.jobs) > 0 and self.jobs[-1].index == job.index:
            self.jobs[-1] = self.jobs[-1].merge_slice(job.processing_time)
        else:
            self.jobs.append(job)
            self.job_ids.append(job.index)
        self.makespan += job.get_processing_time()

        job.set_completion_time(self.makespan)

    def idle(self, time: int) -> None:
        if time <= 0:
            return
        self.add_job(Idle(time))

    def get_jobs(self):
        return self.jobs

    def random_neighbour(self):
        from random import randint

        jobs = list(filter(lambda j: not j.is_idle(), self.jobs))
        i = randint(0, len(jobs) - 1)
        j = randint(0, len(jobs) - 1)

        jobs[i], jobs[j] = jobs[j], jobs[i]

        return Machine(self.index, jobs)

    def swap_jobs(self, j1: int, j2: int):
        jobs = list(filter(lambda j: not j.is_idle(), self.jobs))
        job_index = list(map(lambda j: j.index, jobs))
        if j1 in job_index and j2 in job_index:
            i = job_index.index(j1)
            j = job_index.index(j2)
            jobs[i], jobs[j] = jobs[j], jobs[i]

        return Machine(self.index, jobs=jobs)
