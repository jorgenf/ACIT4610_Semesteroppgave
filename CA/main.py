from multiprocessing import Process, Queue
import matplotlib
matplotlib.use("TkAgg")
from pylab import *
from os import getpid


print(__name__)
def __run_proc(self, DNA, queue):
    print("Started process " + getpid())
    result = ns.Neuron_model(DNA).run_simulation()
    queue.put((DNA,
               fitness.total_dist(result, data.get_firing_rate("Data/Small - 7-1-35.spk.txt"))))

def run():
    while len(DNAs) > 1:

        if __name__ == '__main__':
            print("ok")
            queue = Queue()
            jobs = []
            for DNA in self.DNAs:
                p = Process(target=self.__run_proc,
                            args=(DNA, queue))
                jobs.append(p)
                p.start()
            while p.is_alive() in enumerate(jobs):
                print("Running", flush=True)
            DNAs = []
            for q in queue:
                if len(DNAs) < len(self.DNAs):
                    DNAs.append(q)
                else:
                    for m in range(len(DNAs)):
                        if q[1] < DNAs[m][1]:
                            DNAs[m] = q
            self.DNAs = DNAs
    return self.DNAs



e = ev.Evolution(0.1)
e.run()