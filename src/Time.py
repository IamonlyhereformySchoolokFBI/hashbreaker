import time

class Time():
    def __init__(self):
        self._start = 0
        self._stop = 0
        self._time_measured = 0

    def __repr__(self):
        if self._start == 0 and self._stop == 0:
            return "Object - Time. Not used yet" 
        return "Object - Time. Measured: {:07f} Start at: {:07f} Stop at: {:07f}".format(self._time_measured, self._start, self._stop )

    def start(self):
        self._start = time.time()

    def stop(self):
        self._stop = time.time()

    @property 
    def result(self):
        self._time_measured = self._stop - self._start
        if self._time_measured < 0:
            self._time_measured = 0
        return self._time_measured

    @result.deleter
    def result(self):
        self._start = 0
        self._stop = 0
        self._time_measured = 0