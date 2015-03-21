import threading
from queue import Queue
import time
from random import randint
from faker import Factory


class Banker:
    number_of_bankers = 0

    def __init__(self, number):
        # serialize console output, s.t. messages from threads don't intertwine
        self.lock = threading.Lock()
        self.q = Queue()
        self.number = number
        Banker.number_of_bankers = Banker.number_of_bankers + 1

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
        while True:
            item = self.q.get()
            self.serve(item)
            self.q.task_done()


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

    def __init__(self, bankers, max_no):
        self.bankers = bankers
        self.max_no = max_no

    def generate(self):
        while Person.number < self.max_no:
            Generator.generation_no = Generator.generation_no + 1
            p = Person()
            banker = self.bankers[Person.number % Banker.number_of_bankers]
            banker.q.put(p)
            # print the list of people that are currently in queue
            print("Banker no. " + str(banker.number) + ": " +
                  'has the current queue:' +
                  ", ".join([elem.name for elem in list(banker.q.queue)]))
            time.sleep(0.2)

            # randomly open a new office at fourth iteration
            if Generator.generation_no == 4:
                b = Banker(Banker.number_of_bankers)
                self.bankers.insert(Banker.number_of_bankers, b)
                t = threading.Thread(target=b.do_banky_stuff)
                # thread dies when main thread (only non-daemon thread) exits.
                t.daemon = True
                t.start()


class Main:
    def run_stuff(self, no_of_threads, no_of_people):
        # initialize a list of cashiers
        bankers = []

        for i in range(no_of_threads):
            b = Banker(i)
            bankers.insert(i, b)
            t = threading.Thread(target=b.do_banky_stuff)
            # thread dies when main thread (only non-daemon thread) exits.
            t.daemon = True
            t.start()

        start_time = time.perf_counter()

        # I just like to use this word a lot :)
        generator = Generator(bankers, no_of_people)
        generation = threading.Thread(target=generator.generate)
        generation.daemon = True
        generation.start()

        print('Total time of system:', time.perf_counter() - start_time)
