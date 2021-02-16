from collections import defaultdict
import subprocess, platform
import time

def pingOk(sHost):
	if platform.system().lower()=="windows":
		args = "-n 1 "
	else:
		args = "-c 1 -w 10"
	try:
		output = subprocess.check_output("ping {} {}".format(args, sHost), shell=True)
	except:
		return False
	return True


class Watcher:
	_IP_ADDRESSES = defaultdict(lambda: [])

	def __init__(self, Messanger, loop_wait):
		self._Messanger = Messanger
		self._WAIT_TIME = loop_wait

	def add(self, ip, user):
		self._IP_ADDRESSES[ip].append(user)

	def check(self, ip):
		return pingOk(ip)

	def run(self):
		while True:
			time.sleep(self._WAIT_TIME)
			for ip, user_list in self._IP_ADDRESSES.items():
				if not pingOk(ip):
					for user in user_list:
						self._Messanger.send_message(user, "{} failed".format(ip))
