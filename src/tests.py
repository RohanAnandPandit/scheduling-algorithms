import unittest

from src.job import Job
from src.scheduler import Scheduler


class TestSchedulingAlgorithms(unittest.TestCase):

    def test_moore_hodgson(self):
        processing_times = [7, 8, 4, 6, 6]
        due_dates = [9, 17, 18, 19, 20]
        jobs = [Job(index=(i + 1), processing_time=p, due_date=d) for i, (p, d)
                in enumerate(zip(processing_times, due_dates))]
        s = Scheduler().moore_hodgson(jobs)
        s.plot('moore-hodgson')
        job_ids = list(map(lambda j: j.index, s.get_jobs()[0]))
        self.assertEqual([3, 4, 5, 1, 2], job_ids)


if __name__ == '__main__':
    unittest.main()
