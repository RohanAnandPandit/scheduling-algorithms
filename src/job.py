from utils import number, inf


class Job:
    def __init__(self, index: int, processing_time: int = 1, weight: int = 1,
                 release_time: int = 0, due_date: number = inf):
        self.index: int = index
        self.processing_time = processing_time
        self.weight: int = weight
        self.release_time: int = release_time
        self.due_date: number = due_date
        self.completion_time = -1

    def get_processing_time(self):
        return self.processing_time

    def get_due_date(self):
        return self.due_date

    def get_release_time(self, ):
        return self.release_time

    def lateness(self) -> int:
        return self.completion_time - self.due_date

    def tardiness(self) -> int:
        return max(0, self.lateness())

    def is_idle(self) -> bool:
        return self.index == -1

    def set_completion_time(self, time: int) -> None:
        self.completion_time = max(self.completion_time, time)

    def get_completion_time(self):
        return self.completion_time

    def get_slice(self, time: int):
        return Job(index=self.index, processing_time=time, weight=self.weight,
                   release_time=self.release_time, due_date=self.due_date)

    def merge_slice(self, time: int):
        return Job(index=self.index,
                   processing_time=(self.processing_time + time),
                   weight=self.weight,
                   release_time=self.release_time, due_date=self.due_date)

    def __str__(self):
        return f'({self.index})'

    def __repr__(self):
        return f'({self.index})'


class Idle(Job):
    def __init__(self, time: int):
        super().__init__(-1, time)

    def is_idle(self) -> bool:
        return True
