import socket
import sys
from socketMethods import *

srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Registering the socket
    srv_sock.bind(("0.0.0.0", int(sys.argv[1])))  # sys.argv[1] is the 1st argument on the command line

    # Create a queue where new connection requests will be added by
	# the OS kernel.
    srv_sock.listen(5)
    print("Server up and running!")

# If any errors occur, they are printed.
except Exception as e:
    # Print the exception message
    print(e)
    # Exit with a non-zero value, to indicate an error condition
    exit(1)

while True:
    try:
        print("Waiting for clients...")

        # A new socket to communicate with the client connected.
        cli_sock, cli_addr = srv_sock.accept()
        cli_addr_str = str(cli_addr)  # Translate the client address to a string (to be used shortly)

        print("Client " + cli_addr_str + " connected.")

        # The operation and filename string received.
        cmd_filename = cli_sock.recv(64)

        # If no operation and filename are provided then it closes the connection.
        if len(cmd_filename) == 0:
            print("No filename or operation provided!")
            cli_sock.close()
            exit(1)

        cmd_filename_array = cmd_filename.decode('utf-8').split(' ')
        cmd = cmd_filename_array[0]

        if len(cmd_filename_array) > 1:
            filename = cmd_filename_array[1]

        # Loop until either the client closes the connection or the user requests termination
        if cmd == "get":

            # Server checks if the file exists and sends it to the client
            server_file_existence = os.path.isfile("./" + filename)
            cli_sock.sendall(str.encode(str(server_file_existence)))

            result = "SUCCESS!"
            error = ""
            # If the file exists on the server and it does not exist on the client,
            # then proceed with sending data over the socket. Otherwise, the error and why the error occurred are printed.
            if server_file_existence:
                client_file_existence = cli_sock.recv(32)
                if client_file_existence.decode() == "False":
                    bytes_sent = send_file(cli_sock, filename)
                    if bytes_sent == 0:
                        print("Warning! The size of the file is 0 bytes!")
                else:
                    result = "FAILURE!"
                    error = " File " + filename + " cannot be overwritten because it already exists!"
            else:
                result = "FAILURE!"
                error = " File " + filename + " does not exist!"

            print(cli_addr_str + " with port number " + sys.argv[1] + " requested GET operation - " + result + error)


        elif cmd == "put":
            # Server checks if the file exists and sends it to the client.
            # The server receives if the file exists on the client side.
            server_file_existence = os.path.isfile("./" + filename)
            cli_sock.sendall(str.encode(str(server_file_existence)))
            client_file_existence = cli_sock.recv(32)

            result = "SUCCESS!"
            error = ""
            # If the file does not exist, it checks if it exists on the client and if it does,
            # proceed with receiving data. Otherwise, print the error and why the error occurred.
            if not server_file_existence:
                if client_file_existence.decode() == "True":
                    bytes_read = recv_file(cli_sock, filename)
                    if bytes_read == 0:
                        print("Warning! The size of the file is 0 bytes!")
                else:
                    result = "FAILURE!"
                    error = " The user requested to upload non-existing file!"
            else:
                result = "FAILURE!"
                error = " File " + filename + " has already been uploaded!"

            print(cli_addr_str + " with port number " + sys.argv[1] + " requested PUT operation - " + result + error)


        elif cmd == "list":
            # Server sends the listing to the client.
            bytes_sent = send_listing(cli_sock)

            result = "SUCCESS"
            if bytes_sent == 0:
                result = "FAILURE"

            print(cli_addr_str + " with port number " + sys.argv[1] + " requested LIST operation - " + result)

        else:
            print("Unknown operation!")

    except Exception as e:
        print(e)

    finally:
        cli_sock.close()
        print("Connection closed!")

srv_sock.close()
exit(0)