import threading
from queue import Queue
import time
from random import randint
from faker import Factory

class Banker:
	def __init__(self, number):
		# serialize console output, s.t. messages from threads don't intertwine
		self.lock = threading.Lock()
		self.q = Queue()
		self.number = number

	def serve(self,person):
		# serve client - here we only pretend to do work by calling sleep
		time.sleep(person.time_for_service) 
		with self.lock:
			# print the list of people that are currently in queue
			print("Banker no. " + str(self.number) + ": " + 'btw my list of people is now:' + ",".join([elem.name for elem in list(self.q.queue)]))
			# print who am I serving now?
			print("Banker no. " + str(self.number) + ": ",person.name)

	def do_banky_stuff(self):
		# take the person at top of own queue and serve it
		while True:
			item = self.q.get()
			self.serve(item)
			self.q.task_done()

class Person:
	def __init__(self):
		# each customer takes different time to serve, here btw. 0,1 and 0,9 seconds
		self.time_for_service = randint(1,9)/10
		# generating a random name, for pretty printing
		fakeNameGen = Factory.create()
		self.name = fakeNameGen.name()

class Main:
	def run_stuff(self, no_of_threads, no_of_people):
		# initialize a list of cashiers
		bankers = []

		for i in range(no_of_threads):
			b = Banker(i)
			bankers.insert(i, b)
			t = threading.Thread(target=b.do_banky_stuff)
			t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
			t.start()

		start_time = time.perf_counter()

		# put people in queues uniformly
		for item in range(no_of_people):
			p = Person()
			bankers[item%no_of_threads].q.put(p)

		# each q is blocked until all tasks are done
		for i in range(no_of_threads):
			bankers[i].q.join()

		print('Total time of system:',time.perf_counter() - start_time)