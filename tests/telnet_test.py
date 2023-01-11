"""CMNDJKSNCVJKDF"""
import asyncio
import telnetlib3

@asyncio.coroutine
def register_telnet_command(loop, Client, host, port, command):
    transport, protocol = yield from loop.create_connection(Client, host, port)

    print("{} async connection OK for command {}".format(host, command))

    def send_command():
        EOF = chr(4)
        EOL = '\n'
        # adding newline and end-of-file for this simple example
        command_line = command + EOL + EOF
        protocol.stream.write(protocol.shell.encode(command_line))

    # one shot invokation of the command
    loop.call_soon(send_command)
    # what does this do exactly ?
    yield from protocol.waiter_closed


def main():
    def ClientFactory():
        return telnetlib3.TelnetClient(encoding='utf-8', shell = telnetlib3.TerminalShell)
    # create as many clients as we have hosts

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        register_telnet_command(loop, log, ClientFactory,
                                host = 'localhost', port = 5410,
                                command = "id"))
    return 0
