import threading
from queue import Queue
import time
from random import randint
from faker import Factory
import random


class Banker:
    number_of_bankers = 0
    active_bankers = []

    def __init__(self):
        # serialize console output, s.t. messages from threads don't intertwine
        self.lock = threading.Lock()
        self.q = Queue()
        self.active = True
        self.number = Banker.number_of_bankers = Banker.number_of_bankers + 1
        Banker.active_bankers.append(self)

    def serve(self, person):
        # serve client - here we only pretend to do work by calling sleep
        time.sleep(person.time_for_service)
        with self.lock:
            if self.q:
                # print who am I serving now?
                print("Banker no. " + str(self.number) + ": ", person.name)
            else:
                print("Nobody loves me :(")

    def do_banky_stuff(self):
        # take the person at top of own queue and serve it
        while self.active:
            item = self.q.get()
            self.serve(item)
            self.q.task_done()

    def stop(self):
        # TODO: move queue, add logic all over, only active queues to add
        print("Banker no. " + str(self.number) + ": I quit this damn job!")
        Banker.active_bankers.remove(self)
        self.active = False
        self.spread_queue()

    def spread_queue(self):
        for elem in list(self.q.queue):
            banker = random.choice(Banker.active_bankers)
            banker.q.put(elem)

        self.q.queue.clear()


class Person:
    number = 0

    def __init__(self):
        # each customer takes different time to serve, here btw.
        # 0,1 and 0,9 seconds
        self.time_for_service = randint(1, 9) / 10
        Person.number = Person.number + 1
        # generating a random name, for pretty printing
        fake_name_gen = Factory.create()
        self.name = fake_name_gen.name()


class Generator:
    generation_no = 0

    def __init__(self, max_no):
        self.max_no = max_no

    def generate(self):
        while Person.number < self.max_no:
            Generator.generation_no = Generator.generation_no + 1
            p = Person()
            banker = random.choice(Banker.active_bankers)
            banker.q.put(p)

            # print the list of people that are currently in that queue
            print("Banker no. " + str(banker.number) + ": " +
                  'has the current queue:' +
                  ", ".join([elem.name for elem in list(banker.q.queue)]))
            time.sleep(0.1)

            # randomly open a new office at fourth iteration
            if Generator.generation_no == 4:
                b = Banker()
                t = threading.Thread(target=b.do_banky_stuff)
                # thread dies when main thread (only non-daemon thread) exits.
                t.daemon = True
                t.start()

            # randomly kill a new office at 6th generation
            if Generator.generation_no == 6:
                banker = random.choice(Banker.active_bankers)
                banker.stop()


class Main:
    def run_stuff(self, no_of_threads, no_of_people):
        for i in range(no_of_threads):
            b = Banker()
            t = threading.Thread(target=b.do_banky_stuff)
            # thread dies when main thread (only non-daemon thread) exits.
            t.daemon = True
            t.start()

        start_time = time.perf_counter()

        # I just like to use this word a lot :)
        generator = Generator(no_of_people)
        generation = threading.Thread(target=generator.generate)
        generation.daemon = True
        generation.start()

        print('Total time of system:', time.perf_counter() - start_time)
