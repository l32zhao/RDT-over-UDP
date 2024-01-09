import os
import sys
import argparse
import socket
import math

from packet import Packet
from utils import get_ack_num


global expected_seq_num, seq_size, max_window_size, recv_buffer
expected_seq_num, seq_size, max_window_size, recv_buffer = None, None, None, None


# Writes the received content to file
def append_to_file(filename, data):
    file = open(filename, 'a')
    file.write(data)
    file.close()

def append_to_log(packet: Packet):
    """
    Appends the packet information to the log file
    """
    # raise NotImplementedError('append_to_log not implemented')
    if packet.typ == 0:
        raise NotImplementedError('ack is not allowed to be sent')
    if packet.typ == 1:
        append_to_file('arrival.log', f'{packet.seqnum}\n')
    if packet.typ == 2:
        append_to_file('arrival.log', 'EOT\n')
    if packet.typ == 3:
        append_to_file('arrival.log', 'SYN\n')
    

def send_ack(recv_packet: Packet, ne_addr: str, ne_port:str, socket: socket.socket): #Args to be added
    """
    Sends ACKs, EOTs, and SYN to the network emulator. and logs the seqnum.
    """
    
    # print("expected_seq_num: ", expected_seq_num)
    # print("recv_packet.seqnum: ", recv_packet.seqnum)
    # print("recv_packet.typ: ", recv_packet.typ)
    # print("recv_packet.data: ", recv_packet.data)
    global expected_seq_num, seq_size, max_window_size, recv_buffer

    if recv_packet.typ == 0:
        raise NotImplementedError('ack is not allowed to be sent')
    
    if recv_packet.typ == 1:
        # receive data
        # send ack
        # print("expected_seq_num: ", expected_seq_num)
        if recv_packet.seqnum == expected_seq_num:
            # write to file
            append_to_file(dest_filename, recv_packet.data)
            # update expected_seq_num
            expected_seq_num = (expected_seq_num + 1) % seq_size
            while True:
                if expected_seq_num in recv_buffer:
                    # expected_seq_num = (expected_seq_num + 1) % seq_size
                    append_to_file(dest_filename, recv_buffer[expected_seq_num])
                    del recv_buffer[expected_seq_num]
                    expected_seq_num = (expected_seq_num + 1) % seq_size
                else:
                    s.sendto(Packet(0, (expected_seq_num-1)%seq_size, 0, '').encode(), (ne_addr, ne_port))
                    # print(Packet(0, (expected_seq_num-1)%32, 0, ''))
                    break
        else:
            # if abs(recv_packet.seqnum-expected_seq_num) <= max_window_size or abs(recv_packet.seqnum-expected_seq_num) >= 32-max_window_size and recv_packet.seqnum not in recv_buffer:
            expect_window = [(expected_seq_num + i+1) % seq_size for i in range(max_window_size)]
            if recv_packet.seqnum in expect_window and recv_packet.seqnum not in recv_buffer:
                recv_buffer[recv_packet.seqnum] = recv_packet.data
            s.sendto(Packet(0, (expected_seq_num-1)% seq_size, 0, '').encode(), (ne_addr, ne_port))
                # print(Packet(0, (expected_seq_num-1)%32, 0, ''))



    if recv_packet.typ == 2:
        # Send EOT
        s.sendto(recv_packet.encode(), (ne_addr, ne_port))
        exit()

    if recv_packet.typ == 3:
        # Send SYNACK
        s.sendto(recv_packet.encode(), (ne_addr, ne_port))
    
    
if __name__ == '__main__':
    # Parse args
    parser = argparse.ArgumentParser(description="Congestion Controlled GBN Receiver")
    parser.add_argument("ne_addr", metavar="<NE hostname>", help="network emulator's network address")
    parser.add_argument("ne_port", metavar="<NE port number>", help="network emulator's UDP port number")
    parser.add_argument("recv_port", metavar="<Receiver port number>", help="network emulator's network address")
    parser.add_argument("dest_filename", metavar="<Destination Filename>", help="Filename to store received data")

    args = parser.parse_args()
    ne_addr: str = args.ne_addr
    ne_port: int = int(args.ne_port)
    recv_port: int = int(args.recv_port)
    dest_filename: str = args.dest_filename

    # Clear the output and log files
    open(dest_filename, 'w').close()
    open('arrival.log', 'w').close()


    expected_seq_num = 0 # Current Expected sequence number
    seq_size = 32 # Max sequence number
    max_window_size = 10 # Max number of packets to buffer
    recv_buffer = {}  # Buffer to store the received data

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('', recv_port))  # Socket to receive data

        while True:
            # Receive packets, log the seqnum, and send response
            recv_packet, addr = s.recvfrom(1024)
            recv_packet = Packet(recv_packet)
            append_to_log(recv_packet)
            send_ack(recv_packet, ne_addr, ne_port, s)