import time


class ExecutionMonitor:

    def start(self):

        self.start_time = (
            time.time()
        )

    def stop(self):

        return round(
            time.time()
            - self.start_time,
            2
        )
