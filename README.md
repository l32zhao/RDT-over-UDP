# A congestion controlled pipelined RDT
> Assignment 2 of Fall 2023 CS 656 (Computer Networks) |  UWaterloo
## Introduction
* Designed and implemented a congestion controlled pipelined Reliable Data Transfer (RDT) protocol in Python to transfer files reliably over an unreliable network.
* Built sender and receiver programs to split data into packets, handle retransmissions, implement congestion control with adjustable window size, and reassemble packets
Used a network emulator program to simulate packet loss, delay, and reordering across the communication link.
* Logged timestamped transmission details like packet sequence numbers, window sizes, and acknowledgements for testing and evaluation.
* Ensured reliable, in-order delivery of files by implementing mechanisms to handle lost, duplicate, and out-of-order packets.
* Tested and debugged the end-to-end implementation on multiple systems within the university's computer science environment.


## Run network_emulator.py
Test with the following scripts:
```console
./run.sh network_emulator <Forward receiving port> <Receiver's network address> <Reciever’s receiving UDP port number> <Backward receiving port> <Sender's network address> <Sender's receiving UDP port number> <Maximum Delay> <drop probability> <verbose>
```
For example:
```console
./run.sh network_emulator 9991 host2 9994 9993 host3 9992 1 0.2 0
```

## Run sender.py
Please use the following scripts:
```console
./run.sh sender "ne_host" "ne_port" "port" "timeout" "filename"
```
For example:
```console
./run.sh sender host1 9991 9992 50 <input file>
```

## Run receiver.py
Please use the following scripts:
```console
./run.sh receiver "ne_addr" "ne_port" "recv_port" "dest_filename"
```
For example:
```console
./run.sh receiver host1 9993 9994 <output file>
```

