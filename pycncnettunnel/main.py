import argparse
import asyncio
import struct
from datetime import datetime


class ClientState:
    def __init__(self, addr):
        self.addr = addr
        self.last_received = datetime.now()

    def update_received(self):
        self.last_received = datetime.now()


class TunnelProtocol:
    """CnCNet tunnel protocol implementation

    This is currently just an UDP packet forwarder.
    """

    def __init__(self):
        self.clients = {}
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        if len(data) < 4:
            return
        sender_id, receiver_id = struct.unpack(">hh", data[:4])

        if sender_id not in self.clients:
            self.clients[sender_id] = ClientState(addr)
        self.clients[sender_id].update_received()

        if receiver_id not in self.clients:
            return

        self.transport.sendto(data, self.clients[receiver_id].addr)


def parse_args():
    a = argparse.ArgumentParser(
        description="CNCnet test tunnel",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    a.add_argument(
        "-i",
        "--ip",
        type=str,
        default="127.0.0.1",
        help="Host address",
    )
    a.add_argument(
        "-p",
        "--port",
        type=int,
        default=50000,
        help="Port",
    )

    return a.parse_args()


async def amain(args):
    print("Starting UDP server")

    loop = asyncio.get_running_loop()

    transport, _ = await loop.create_datagram_endpoint(
        lambda: TunnelProtocol(),
        local_addr=(args.ip, args.port),
    )

    try:
        await asyncio.sleep(3600)  # Serve for 1 hour.
    finally:
        transport.close()


def main():
    asyncio.run(amain(parse_args()))


if __name__ == "__main__":
    main()
