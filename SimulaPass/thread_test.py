import threading
import time
from django.conf import settings
from passageiros.models import Passageiro
 
class MyThread(threading.Thread):
    def run(self):
        print("%s started!" % self.getName())              # "Thread-x started!"
        time.sleep(1)                                      # Pretend to work for a second
        print("%s finished!" % self.getName())             # "Thread-x finishsed!"
 
if __name__ == '__main__':
    for x in range(4):                                     # Four times...
        mythread = MyThread(name = "Thread-%d" % (x + 1))  # ...Instantiate a thread and pass a unique ID to it
        mythread.start()                                   # ...Start the thread
        passageiro = Passageiro()
        passageiro.nome = 'Passageiro_%d'%x
        passageiro.start()
        time.sleep(.9)                                     # ...Wait 0.9 seconds before starting another