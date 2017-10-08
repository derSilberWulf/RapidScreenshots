#TO DO make it so signal can kill program, but all queued images will be saved
#Process command line arguments
#ERRORS. The kill signal might be going to the child thread or something. Issue 846817 on https://bugs.python.org/issue846817
import pyscreenshot
from timeit import default_timer as timer
from Queue import Queue
from threading import Thread
import threading
from time import sleep
#import signal
#import sys

class KillSignalHandler:
    def __init__(self, image_producer_thread, image_consumer_thread):
        self.image_consumer_thread = image_consumer_thread
        self.image_producer_thread = image_producer_thread
    def kill_signal_handler(self, signal, frame):
        print('You pressed CTRL+C')
        self.image_producer_thread.stop()
        self.image_producer_thread.join()
        self.image_consumer_thread.join()
        sys.exit(0)

DEFAULT_TIME_LIMIT = 10
DEFAULT_LOOP_TIME_LIMIT = 0
DEFAULT_SCREENSHOTS_MAX = 0
class ScreenshotProducerThread(Thread):
    def __init__(self, img_queue, consumer_process, time_limit):
        Thread.__init__(self)
        self.img_queue = img_queue
        self.consumer_process = consumer_process
        self.time_limit = time_limit
        self.stop_event = threading.Event()
    def run(self):
        start_time = timer()
        new_time = timer()
        while(new_time - start_time < self.time_limit or self.time_limit <= 0 and not self.stop_event.is_set()):
            img = pyscreenshot.grab()
            #send to another process
            ##imgnum = imgnum + 1
            ##img.save(str(imgnum) + '.png')
            self.img_queue.put(img)
            new_time = timer()
        self.consumer_process.stop()
        #self.consumer_process.join()
    def stop(self):
        """
        Stop the producer process
        """
        self.stop_event.set()

class ImageConsumerThread(Thread):
    def __init__(self, imgQueue, loop_time_limit, images_max):
        Thread.__init__(self)
        self.imgQueue = imgQueue
        self.loop_time_limit = loop_time_limit
        self.images_max = images_max
        self.stop_event = threading.Event()

    def run(self):
        #check if there are images to consume
        #if not, then sleep
        imgnum = 1
        start_timer = timer()
        while(not self.stop_event.is_set() or not self.imgQueue.empty()):
            while(not self.imgQueue.empty()):
                try:
                    img = self.imgQueue.get(False)
                    img.save(str(imgnum) + '.png')
                    imgnum = imgnum + 1
                    
                    #check if its time to loop back to first image
                    if(imgnum > self.images_max and self.images_max > 0):
                        print('time for a new loop: image count: ' + str(imgnum))
                        imgnum = 1
                    elif(timer() - start_timer > self.loop_time_limit and self.loop_time_limit > 0):
                        print('timed for a new loop: timer: ' + str(timer() - start_timer))
                        imgnum = 1
                        start_timer = timer()
                except Queue.Empty:
                    print('the queue is empty')
            sleep(1)
    
    def stop(self):
        """
        Stop the consumer process
        """
        self.stop_event.set()

def main_method(time_limit, loop_time_limit, screenshots_max):
    """
    Rapidly takes screenshots and queues them to be saved as image files
    @param time_limit a time in seconds indicating how long the program should run
    if it is set to zero or less then the program will run forever
    @param loop_time_limit a time in seconds indicating when the program should loop
    if it is set to zero or less then there will be no time limit
    @param screenshots_max an integer value indicating the maximum number of pictures to keep
    if it is set to zero or less there will be no limit
    """
    start_time = timer()
    new_time = timer()
    #imgnum = 0
    img_queue = Queue()
    consumer_process = ImageConsumerThread(img_queue, loop_time_limit, screenshots_max)
    consumer_process.start()
    producer_process = ScreenshotProducerThread(img_queue, consumer_process, time_limit)
    producer_process.start()
    #ksh = KillSignalHandler(producer_process, consumer_process)
    #signal.signal(signal.SIGINT, ksh.kill_signal_handler)
    #print(threading.enumerate())
    #producer_process.join()
    #consumer_process.join()
    try:
        #producer_process.join()
        #consumer_process.join()
        while(True):
            sleep(1)
    except KeyboardInterrupt:
        print('pressed CTRL+C')
        producer_process.stop()
        producer_process.join()
        consumer_process.join()

if __name__ == '__main__':
    #rapidly take screenshots and queue them to be saved as images
    #if the time limit is reached or the maximum number of screenshots then
    #overwrite old files
    main_method(DEFAULT_TIME_LIMIT, DEFAULT_LOOP_TIME_LIMIT, DEFAULT_SCREENSHOTS_MAX)