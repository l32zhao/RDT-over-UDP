import time
from threading import Timer
from io import TextIOWrapper
from packet import Packet

class Watcher:

    def __init__(self, func=time.perf_counter):
        self._func = func
        self._start = None

    def start(self):
        if self._start is not None:
            raise RuntimeError('Already started')
        self._start = self._func()

    def elapsed(self):
        if self._start is None:
            raise RuntimeError('Not started')
        return self._func() - self._start
    
    def cancel(self):
        self._start = None
    
    def restart(self):
        if self._start is None:
            raise RuntimeError('Not started')
        self.cancel()
        self.start()



class RepeatTimer(Timer):

    def __init__(self, interval, function, args=None, kwargs=None):
        super().__init__(interval=interval, function=function, args=args, kwargs=kwargs)
        self.run_started = False
        self.run_finished = False

    def run(self):
        self.run_started = True
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
        self.run_finished = True


def log_file(t: int, content: str, file: TextIOWrapper, file_name: str):
        # print("logging file")
        # print("file name: ", file_name)
        if file_name == 'seqnum':
            file.write(f't={t} {content}\n')
            file.flush()
        elif file_name == 'N':
            file.write(f't={t} {content}\n')
            file.flush()
        elif file_name == 'ack':
            # print("write to ack...")
            # print("content: ", content)
            # print("content type: ", type(content))
            # print("t: ", t)
            file.write(f't={t} {content}\n')
            file.flush()
        else:
            raise ValueError('Invalid file name')
        

def get_ack_num(recv_packet: Packet, recv_buffer: set, expected_seq_num: int, seq_size: int):
    """
    Returns the ack number of the packet.
    """
    # raise NotImplementedError('get_ack_num not implemented')
    window = [(expected_seq_num + i) % 32 for i in range(len(seq_size))]
    for pkt in recv_buffer:
        if pkt.seqnum in window:
            window.remove(pkt.seqnum)
    if recv_packet.seqnum in window:
        window.remove(recv_packet.seqnum)

    if len(window) == 0:
        return (expected_seq_num+seq_size-1) % 32
    else:
        return (window[0]-1) % 32

