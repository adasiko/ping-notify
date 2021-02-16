import json
from watcher import Watcher
from messager import SendJabberMsgBot, ShowMsgBot
import logging
from argparse import ArgumentParser


def main():
	# Setup the command line arguments
	parser = ArgumentParser()

	# Output verbosity options.
	parser.add_argument("-q", "--quiet", help="set logging to ERROR",
		action="store_const", dest="loglevel",
		const=logging.ERROR, default=logging.INFO)
	parser.add_argument("-d", "--debug", help="set logging to DEBUG",
		action="store_const", dest="loglevel",
		const=logging.DEBUG, default=logging.INFO)

	args = parser.parse_args()

	# Setup logging.
	logging.basicConfig(level=args.loglevel, format='%(levelname)-8s %(message)s')
	
	with open('settings.json') as settings_file:
		settings = json.loads(settings_file.read())

	im_server = settings['im_server']

	my_messanger = SendJabberMsgBot(im_server['login'], im_server['password'], im_server['host'], im_server['port'])
	# my_messanger = ShowMsgBot()

	my_watcher = Watcher(my_messanger, settings['loop_wait'])
	for ip, user_list in settings['ip_addresses'].items():
		for user in user_list:
			my_watcher.add(ip, user)
	my_watcher.run()


if __name__ == "__main__":
	main()

