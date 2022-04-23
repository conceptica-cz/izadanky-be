from celery import states
from celery.result import AsyncResult


class TaskDoesNotExist(Exception):
    pass


class Task:
    def __init__(self, async_result: AsyncResult):
        if async_result.state == states.PENDING:
            raise TaskDoesNotExist()
        self.state = async_result.state
        self.result = None
        if self.state in [states.SUCCESS, states.FAILURE]:
            self.result = async_result.result
