README.txt - Simple UDP Program
--------------------------------------------------------------------
All included files are completed in, and run successfully using Python 3.8.


Included files:


- pg1lib.py - Library that contains four cryptography-related methods ( getPubKey(), encrypt(message, pubkey), 
            decrypt(cipher), and checksum(data) ) necessary for successful use of the other two included files. 
            This library did not and will not require any altering to function as intended.


- udpserver.py - Allows for completion of Part 1 (UDP Practice) when ran without arguments, and Part 2 
                (Simple Secure UDP Program) when ran with arguments. In both scenarios, running this code will 
                create a basic "server" on a machine, which listens for a connection from the "client" machine 
                which is running udpclient.py. Depending on which arguments are provided, this program will 
                perform a different series of actions, either sending a simple hello message to the client or 
                receiving and decrypting a message from the client.

To run this program for Part 1, simply run the following command-line string on your machine after installing:
            [user@machine ~] $ python3 ./udpserver.py

To run this program for Part 2, run the same command-line string followed by a specific port to listen on:
            [user@machine ~] $ python3 ./udpserver.py [port]


- udpclient.py - Allows for completion of Part 1 (UDP Practice) when ran without arguments, and Part 2 (Simple 
                Secure UDP Program) when ran with arguments. In both scenarios, running this code will create a 
                basic "client" on a machine, which then can send communications towards the machine running 
                udpserver.py. Depending on the arguments provided, this program will interact with the server 
                differently, either simply receiving a basic message and acknowledgement or sending its own encrypted 
                message to be decrypted on the server-side.

To run this program for Part 1, simply run the following command-line string on your machine after installing:
            [user@machine ~] $ python3 ./udpclient.py

To run this program for Part 2, run the same command-line string followed by a specific hostname, port, 
and test message:
            [user@machine ~] $ python3 ./udpclient.py [hostname] [port] [test message]
