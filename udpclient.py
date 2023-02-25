"""
This is a UDP program that comprises of two parts:
Part I: A simple UDP server and client where the server can successfully 1) establish the connection with 
        the client, and 2) send a string (e.g., "Hello World") to the client
Part II: A more complex program that involves cryptography for secure connection (using the pg1lib.py library)
        and enables the client to choose which host does it want to connect to, on which port, and exactly
        what the message will be. It also involves checksum to make sure that no packets were lost in the process.
"""

import socket
import sys
import time
from pg1lib import *

# Define a buffer size for the message to be read from the UDP socket
BUFFER = 2048


def part1():
    print("********** PART 1 **********")
    # Declare hostname and port and combine them to create the address
    host = "student00.ischool.illinois.edu"
    port = 41014
    sin = (host, port)

    # Create a message to be sent to the server
    message = b"Hello World"

    # Create a datagram socket
    try:
        udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    except socket.error as msg:
        print('Failed to create socket.')
        sys.exit()

    # Convert the message from string to byte and send it to the server
    try:
        udp_client_socket.sendto(message, sin)
    except socket.error as e:
        print("Error sending data.")
        sys.exit()

    # Receive acknowledgement from the server and print the acknowledgement to the screen
    try:
        message_address = udp_client_socket.recvfrom(BUFFER)
        message_bytes = message_address[0]
        message_int = int.from_bytes(message_bytes, 'little')
        acknowledgement = socket.ntohs(message_int)
        print(f'Acknowledgment: {acknowledgement}')
    except socket.error as e:
        print('Error receiving data.')
        sys.exit()

    # Close the socket
    udp_client_socket.close()


def part2(hostname, port, message):
    print("********** PART 2 **********")
    sin = (hostname, int(port))

    # Create a datagram socket
    try:
        udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    except socket.error as msg:
        print('Failed to create socket.')
        sys.exit()

    # Create public key and send it to the server
    try:
        pub_key = getPubKey()
        udp_client_socket.sendto(pub_key, sin)
    except socket.error as e:
        print('Error sending data.')
        sys.exit()

    # Receive server's public key and decrypt it using client's key
    try:
        server_key_encrypt, address = udp_client_socket.recvfrom(BUFFER)
        server_key = decrypt(server_key_encrypt)
    except socket.error as e:
        print('Error receiving data.')
        sys.exit()

    # Calculate checksum of the message and print it out
    data_checksum = checksum(str.encode(message))
    print(f'Checksum: {data_checksum}.')
    checksum_bytes = data_checksum.to_bytes(data_checksum.bit_length(), 'little')

    # Calculating time
    sending_time = time.time()
    sending_time_micro = sending_time * 1000000

    # Encrypt the message and send it to the server with the checksum
    message_bytes = bytes(message, 'utf-8')
    message_encrypt = encrypt(message_bytes, server_key)

    try:
        udp_client_socket.sendto(message_encrypt, sin)
    except socket.error as e:
        print('Error sending data.')
        sys.exit()

    try:
        udp_client_socket.sendto(checksum_bytes, sin)
    except socket.error as e:
        print('Error sending data.')
        sys.exit()

    # Checksum comparison
    message_address = udp_client_socket.recvfrom(BUFFER)
    receiving_time = time.time()
    receiving_time_micro = receiving_time * 1000000
    message_bytes = message_address[0]
    message_int = int.from_bytes(message_bytes, 'little')
    acknowledgement = socket.ntohs(message_int)
    if acknowledgement == 1:
        print('Server has successfully received the message.')
        print(f'RTT {receiving_time_micro - sending_time_micro} us')
    else:
        print(f'Acknowledgment: {acknowledgement}')

    # Convert the message from string to byte and send it to the server
    try:
        message_bytes = bytes(message, 'utf-8')
        udp_client_socket.sendto(message_bytes, sin)
    except socket.error as e:
        print('Error sending data.')
        sys.exit()

    # Close the socket
    udp_client_socket.close()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        part1()
    else:
        part2(sys.argv[1], sys.argv[2], sys.argv[3])
