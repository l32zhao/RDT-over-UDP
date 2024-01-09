#!/bin/bash

python_file=$1.py;
shift;
python3 $python_file "$@" & 
# echo $1.py "$@"

# python3 "$1.py" "$@"  &

# if [ $1 == "network_emulator" ]
# # then python3 network_emulator.py "<Forward receiving port>" $2 \
# #                                  "<Receiver's network address>" $3 \
# #                                  "<Reciever’s receiving UDP port number>" $4 \
# #                                  "<Backward receiving port>" $5 \
# #                                  "<Sender's network address>" $6 \
# #                                  "<Sender's receiving UDP port number>" $7 \
# #                                  "<Maximum Delay>" $8 \
# #                                  "<drop probability>" $9 \
# #                                  "<verbose>" $10 &

# then python3 $1.py  "$@" &

# elif [ $1 == "receiver" ]
# # then python3 receiver.py "ne_addr" $2 \
# #                          "ne_port" $3 \
# #                          "recv_port" $4 \
# #                          "dest_filename" $5 &
# then python3 receiver.py $2 $3 $4 $5 &



# elif [ $1 == "sender" ]
# # then python3 sender.py "ne_host" $2 \
# #                        "ne_port" $3 \
# #                        "port" $4 \
# #                        "timeout" $5 \
# #                        "filename" $6 &

# then python3 sender.py $2 $3 $4 $5 $6 &
# else
#     echo "Invalid argument. Please enter either network_emulator, receiver, or sender."
# fi