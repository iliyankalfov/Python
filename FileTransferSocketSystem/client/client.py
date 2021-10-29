import socket
import os
import sys

parent_dir = os.path.split(os.getcwd())[0]
sys.path.append(parent_dir.replace('\\', '/') + "/server")
from socketMethods import send_file, recv_file, send_listing, recv_listing

# Create the socket with which we will connect to the server
cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Maximum time for sending data
cli_sock.settimeout(3)

# The server's address is a tuple, comprising the server's IP address or hostname, and port number
srv_addr = (sys.argv[1], int(sys.argv[2])) # sys.argv[x] is the x'th argument on the command line

# Convert to string, to be used shortly
srv_addr_str = str(srv_addr)

try:
	print("Connecting to " + srv_addr_str + "... ")

	# Connect our socket to the server
	cli_sock.connect(srv_addr)
	print("Connected...")

	# The operation requested
	command = str(sys.argv[3])

	# If the arguments are too many - throw an exception
	if len(sys.argv) > 5:
		raise IndexError()

	if len(sys.argv) == 5:
		# The filename to be worked on

		filename = str(sys.argv[4])

		# If the filename is too large, prints the appropriate message and exits
		if len(str.encode(filename)) > 64:
			print("Filename is too large! Connection closed!")
			exit(1)

		cmd_filename = command + " " + filename

		# Sends operation and filename as an array
		cli_sock.sendall(str.encode(cmd_filename, 'utf-8'))
	elif len(sys.argv) == 4:
		# Sends only the operation if the number of arguments is 4
		cli_sock.sendall(str.encode(command, 'utf-8'))

except IndexError:
	print("The command is either insufficient, too many arguments are passed or invalid!")
	exit(1)

except socket.error:
	# If a connection drop occurs, prints the appropriate message and closes the connection
	print("Connection dropped!")
	cli_sock.close()
	exit(1)

except Exception as e:
	# Print the exception message
	print(e)
	# Exit with a non-zero value, to indicate an error condition
	exit(1)

try:

	if command == "get":

		# Sends the server if the file exists on the client side.
		cli_sock.sendall(str.encode(str(os.path.isfile("./" + filename))))
		print_msg = str(cli_sock.getsockname()) + " with port number " + sys.argv[2] + ", GET request - "

		# If it exists, it prints the appropriate message that the file cannot be overwritten.
		if os.path.isfile("./" + filename):
			print(print_msg + "FAILURE! " + "File " + filename + " cannot be overwritten because it already exists!")
			exit(1)

		# Receives the response if it exists on the server side. If it does, it prints the appropriate message that
		# the file already exists.
		server_file_existence = cli_sock.recv(1024)
		if server_file_existence.decode() == "False":
			print(print_msg + "FAILURE! " + "File " + filename + " cannot be downloaded because it does not exist!")
			exit(1)

		# Otherwise, it starts receiving data from the server. If the file-size is 0, prints a warning!
		bytes_read = recv_file(cli_sock, filename)
		if bytes_read == 0:
			print("Warning! The size of the file is 0 bytes!")

		print(print_msg + "SUCCESS!")


	elif command == "put":
		# Receives from server, if the file exists on the server side.
		server_file_existence = cli_sock.recv(1024)

		# Sends the server, if the file exists on the client side.
		cli_sock.sendall(str.encode(str(os.path.isfile("./" + filename))))
		print_msg = str(cli_sock.getsockname()) + " with port number " + sys.argv[2] + ", PUT request - "

		# if the file does not exist, then it prints the appropriate message and the program exits.
		if not os.path.isfile("./" + filename):
			print(print_msg + "FAILURE! " + "File " + filename + " does not exist!")
			exit(1)

		# If it exists on the server side, then the appropriate message is printed and the program exits.
		if server_file_existence.decode() == "True":
			print(print_msg + "FAILURE! " + "File " + filename + " has already been uploaded!")
			exit(1)

		# Otherwise, it starts sending data to the server.
		bytes_sent = send_file(cli_sock, filename)
		if bytes_sent == 0:
			print("Warning! The size of the file is 0 bytes!")

		print(print_msg + "SUCCESS!")


	elif command == "list":
		# Receives the listing from the server and prints it.
		bytes_read = recv_listing(cli_sock)

		result = "SUCCESS!"
		if bytes_read == 0:
			result = "FAILURE!"

		print(str(cli_sock.getsockname()) + " with port number " + sys.argv[1] + " requested LIST operation - " + result)

	else:
		print("Unknown operation!")
		exit(1)

except NameError:
	print("The command is either insufficient, too many arguments are passed or wrong!")

except socket.timeout:
	print("Connection dropped!")
	exit(1)

except Exception as e:
	print(e)

finally:
	cli_sock.close()

# Exit with a zero value, to indicate success
exit(0)