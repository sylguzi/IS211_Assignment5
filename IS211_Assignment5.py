#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignment 5"""

from Queue import *
import argparse
import csv
import decimal


class Server(object):
	def __init__(self):
		self.current_request = None
		self.time_elapsed = 0
	def tick(self):
		if self.current_request != None:
			self.time_elapsed += 1
			if self.time_elapsed >= self.current_request.get_process_time():
				self.current_request = None
	def busy(self):
		return self.current_request != None
	def start_next(self, new_request):
		self.current_request = new_request
		self.time_elapsed = 0

class Request(object):
	def __init__(self, timestamp, file_path, process_time):
		self.timestamp = timestamp
		self.file_path = file_path
		self.process_time = process_time
	def get_file_path(self):
		return self.file_path
	def get_process_time(self):
		return self.process_time
	def wait_time(self, current_time):
		return current_time - self.timestamp

def simulateOneServer(filename):
	server = Server()
	q = Queue()
	(requests, count) = parseFile(filename)
	processed = 0
	net_waiting_time = 0
	tick = 0

	while(True):
		if ((server.busy() is False) and (processed == count)):
			break
		if (tick in requests):
			list_of_requests = requests[tick]
			for request in list_of_requests:
				q.put(request)

		if (server.busy()):
			server.tick()
		elif (q.empty() is False):
			request = q.get()
			net_waiting_time += request.wait_time(tick)
			server.start_next(request)
			processed += 1
		tick += 1
	return decimal.Decimal(net_waiting_time) / decimal.Decimal(count)

def simulateManyServer(filename, server_number):
	servers = [Server() for i in range(server_number)]
	q = Queue()
	(requests, count) = parseFile(filename)
	processed = 0
	net_waiting_time = 0
	tick = 0

	while(True):
		if (tick in requests):
			list_of_requests = requests[tick]
			for request in list_of_requests:
				q.put(request)

		server_are_not_busy = True
		for server in servers:
			if (server.busy() is True):
				server_are_not_busy = False
				server.tick()
			elif (q.empty() is False):
				request = q.get()
				net_waiting_time += request.wait_time(tick)
				server.start_next(request)
				processed += 1
		if (server_are_not_busy and (processed == count)):
			break
		tick += 1
	return decimal.Decimal(net_waiting_time) / decimal.Decimal(count)

def parseArg():
	parser = argparse.ArgumentParser(description='wtb script desc')
	parser.add_argument('-f','--file', help='wtb file', required=True)
	parser.add_argument('-s','--server', help='wtb server number', 
		required=False)
	return parser.parse_args()

def parseFile(filename):
	requests = {}
	count = 0

	with open(filename) as input_file:
		for i, line in enumerate(input_file):
			strippedLine = line.strip('\r\n')
			[timestamp, file_path, process_time] = strippedLine.split(',')
			timestamp = int(timestamp)

			if timestamp not in requests:
				requests[timestamp] = []
			requests[timestamp].append(Request(timestamp, file_path, 
				int(process_time)))
			count += 1

	return (requests, count)

if __name__ == '__main__':
	params = parseArg()
	if (params.server is None):
		print('avg time is {}'.format(simulateOneServer(params.file)))
	else:
		print('avg time is {}'.format(simulateManyServer(params.file, 
			int(params.server))))