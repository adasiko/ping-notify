#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import aioxmpp
import asyncio
from getpass import getpass
from argparse import ArgumentParser


async def main(server, from_jid, to_jid, password, message):

    server_and_port = server.split(':')
    server_only = server_and_port[0]
    port = server_and_port[1]

    client = aioxmpp.PresenceManagedClient(
        aioxmpp.JID.fromstr(from_jid),
        aioxmpp.make_security_layer(password, no_verify=True),
        override_peer=[(server_only, port, aioxmpp.connector.STARTTLSConnector())]
    )

    async with client.connected() as stream:
        msg = aioxmpp.Message(
            to=aioxmpp.JID.fromstr(to_jid),
            type_=aioxmpp.MessageType.CHAT,
        )
        msg.body[None] = message
        await stream.send(msg)


if __name__ == '__main__':
    # Setup the command line arguments.
    parser = ArgumentParser(description='Authenticate with XMPP server and send simple message')


    # JID and password options.
    parser.add_argument("-s", "--server", dest="server",
                        help="server with port")
    parser.add_argument("-j", "--jid", dest="jid",
                        help="JID to use")
    parser.add_argument("-p", "--password", dest="password",
                        help="password to use")
    parser.add_argument("-t", "--to", dest="to",
                        help="JID to send the message to")
    parser.add_argument("-m", "--message", dest="message",
                        help="message to send")

    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(args.server, args.jid, args.to, args.password, args.message))
    finally:
        loop.close()
