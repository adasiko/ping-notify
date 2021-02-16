from abc import ABC, abstractmethod
import subprocess


class MsgBot(ABC):

	@abstractmethod
	def send_message(self, recipent, message):
		pass 


class ShowMsgBot(MsgBot):

	def send_message(self, recipent, message):
		full_message = "for user {}: {}".format(recipent, message)


class SendJabberMsgBot(MsgBot):

	def __init__(self, login, password, server, port):
		self.login = login
		self.password = password
		self.server = server + ':' + port

	def send_message(self, recipent, message):

		s_cmd = 'python3 send_client.py -s {} -j {} -p {} -t {} -m "{}"'.format(self.server, self.login, self.password, recipent, message)
		try:
			subprocess.run(s_cmd, shell=True, timeout=60)
		except subprocess.TimeoutExpired:
			pass

