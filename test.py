from utils import RepeatTimer

timer = RepeatTimer(interval=1, function=print, args=['hello'])
timer.start()

timer.cancel()