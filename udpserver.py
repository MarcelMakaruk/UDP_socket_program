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
from pg1lib import *


# Define a buffer size for the message to be read from the UDP socket
BUFFER = 2048


def part1():
    print("********** PART 1 **********")
    # Declare hostname and port and combine them to create the address
    host = "student00.ischool.illinois.edu"
    port = 41014
    sin = (host, port)

    # Create a datagram socket
    try:
        udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    except socket.error as e:
        print('Failed to create socket.')
        sys.exit()

    # Bind the socket to address
    try:
        udp_server_socket.bind(sin)
    except socket.error as e:
        print('Failed to bind socket.')
        sys.exit()

    print("Waiting ...")

    # Receive message from the client and record the address of the client socket
    try:
        message, address = udp_server_socket.recvfrom(BUFFER)
    except socket.error as e:
        print('Error receiving data.')
        sys.exit()

    # Convert the message from byte to string and print it to the screen
    print(f'Client Message: {message.decode()}')

    # Send acknowledge statement to the client
    try:
        acknowledgement = socket.htons(1)
        acknowledgement_bytes = acknowledgement.to_bytes(5, 'little')
        udp_server_socket.sendto(acknowledgement_bytes, address)
    except socket.error as e:
        print('Error sending data.')
        sys.exit()

    # Close the socket
    udp_server_socket.close()


def part2(port):
    print("********** PART 2 **********")
    host = "student00.ischool.illinois.edu"
    sin = (host, int(port))

    # Create a datagram socket
    try:
        udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    except socket.error as e:
        print('Failed to create socket.')
        sys.exit()

    # Bind the socket to address
    try:
        udp_server_socket.bind(sin)
    except socket.error as e:
        print('Failed to bind socket.')
        sys.exit()

    print("Waiting ...\n")

    # Receive client's public key, create public key, send encrypted public key to the client
    try:
        client_pub_key, address = udp_server_socket.recvfrom(BUFFER)
    except socket.error as e:
        print('Error receiving data.')
        sys.exit()

    try:
        pub_key = getPubKey()
        pub_key_encrypt = encrypt(pub_key, client_pub_key)
        udp_server_socket.sendto(pub_key_encrypt, address)
    except socket.error as e:
        print('Error sending data.')

    # Receive encrypted message and checksum, decrypt it and print out checksum and message
    try:
        message_and_address = udp_server_socket.recvfrom(BUFFER)
        message_encrypt = message_and_address[0]
        message = decrypt(message_encrypt)
        message_decrypt_string = message.decode()
        print('******* New Message *******\n')
        print(f'Received message:\n{message_decrypt_string}')
    except socket.error as e:
        print('Error receiving data.')
        sys.exit()

    try:
        checksum_and_address = udp_server_socket.recvfrom(BUFFER)
        checksum_client_bytes = checksum_and_address[0]
        message_checksum_client = int.from_bytes(checksum_client_bytes, 'little')
        print(f'\nReceived Client Checksum: {message_checksum_client}')
    except socket.error as e:
        print('Error receiving data.')
        sys.exit()

    message_checksum_server = checksum(str.encode(message_decrypt_string))
    print(f'Calculated Checksum: {message_checksum_server}')

    # Create an acknowledgement based on both checksum results
    if message_checksum_client == message_checksum_server:
        acknowledgement = socket.htons(1)
        acknowledgement_bytes = acknowledgement.to_bytes(5, 'little')
        udp_server_socket.sendto(acknowledgement_bytes, address)
    else:
        acknowledgement = socket.htons(0)
        acknowledgement_bytes = acknowledgement.to_bytes(5, 'little')
        udp_server_socket.sendto(acknowledgement_bytes, address)

    # Close the socket
    udp_server_socket.close()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        part1()
    else:
        part2(sys.argv[1])
