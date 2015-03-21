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
        self.q = Queue()
        self.currently_serving = None
        self.active = True
        self.number = Banker.number_of_bankers = Banker.number_of_bankers + 1
        Banker.active_bankers.append(self)

    def serve(self, person):
        # serve client - here we only pretend to do work by calling sleep
        time.sleep(person.time_for_service)
        Observer.notify()

    def do_banky_stuff(self):
        # take the person at top of own queue and serve it
        while self.active:
            item = self.q.get()
            self.currently_serving = item
            self.serve(item)
            self.currently_serving = None
            self.q.task_done()

    def stop(self):
        print("Banker no. " + str(self.number) + ": I quit this damn job!")
        Banker.active_bankers.remove(self)
        self.active = False
        Regulator.spread_queue(self)


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


class Observer:
    @staticmethod
    def notify():
        print('-----------------------------------------------------\n')
        for banker in Banker.active_bankers:
            in_service = banker.currently_serving
            print("Banker no. " + str(banker.number) + ": " +
                  '(' + (in_service.name if in_service else "-") + ')'
                  'has the current queue:' +
                  ", ".join([item.name for item in list(banker.q.queue)]))
        print('-----------------------------------------------------\n')


class Regulator:
    @staticmethod
    def add_to_some_queue(elem):
        banker = random.choice(Banker.active_bankers)
        banker.q.put(elem)
        Observer.notify()

    @staticmethod
    def stop_random_banker():
        banker = random.choice(Banker.active_bankers)
        banker.stop()
        Observer.notify()

    @staticmethod
    def add_new_banker():
        b = Banker()
        t = threading.Thread(target=b.do_banky_stuff)
        # thread dies when main thread (only non-daemon thread) exits.
        t.daemon = True
        t.start()
        Observer.notify()

    @staticmethod
    def spread_queue(banker):
        for elem in list(banker.q.queue):
            Regulator.add_to_some_queue(elem)

        banker.q.queue.clear()
        Observer.notify()


class Generator:
    generation_no = 0

    def __init__(self, max_no):
        self.max_no = max_no

    def generate(self):
        while Person.number < self.max_no:
            Generator.generation_no = Generator.generation_no + 1
            p = Person()
            Regulator.add_to_some_queue(p)
            time.sleep(0.1)

            # randomly open a new office at fourth iteration
            if Generator.generation_no == 4:
                Regulator.add_new_banker()

            # randomly kill a new office at 6th generation
            if Generator.generation_no == 6:
                Regulator.stop_random_banker()


class Main:
    def run_stuff(self, no_of_threads, no_of_people):
        for i in range(no_of_threads):
            Regulator.add_new_banker()

        # I just like to use this word a lot :)
        generator = Generator(no_of_people)
        generation = threading.Thread(target=generator.generate)
        generation.daemon = True
        generation.start()
