# import time

# class Timer:
#     def __init__(self, func=time.perf_counter):
#         self._func = func
#         self._start = None

#     def start(self):
#         if self._start is not None:
#             raise RuntimeError('Already started')
#         self._start = self._func()

#     def reset(self):
#         self._start = self._func()

#     def elapsed(self):
#         if self._start is None:
#             raise RuntimeError('Not started')
#         return self._func() - self._start