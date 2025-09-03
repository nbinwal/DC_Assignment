# server1.py
import socket
import os
import threading

# --- CONFIGURATION ---
HOST = '0.0.0.0'         # Listen on all available network interfaces
PORT = 65001             # Port to listen on for client connections
SERVER2_HOST = '127.0.0.1' # IP address of SERVER 2
SERVER2_PORT = 65002       # Port for SERVER 2
FILE_DIR = "server1_files" # Directory to store files for this server
BUFFER_SIZE = 4096

def get_file_from_server2(filename):
    """ Acts as a client to request a file from SERVER 2. """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
            print(f"Connecting to SERVER 2 to request '{filename}'...")
            s2.connect((SERVER2_HOST, SERVER2_PORT))
            s2.sendall(filename.encode('utf-8'))
            response = s2.recv(BUFFER_SIZE)
            print("Received response from SERVER 2.")
            return response
    except ConnectionRefusedError:
        print("[ERROR] Connection to SERVER 2 failed.")
        return b"ERROR:SERVER2_UNAVAILABLE"
    except Exception as e:
        print(f"[ERROR] An error occurred while communicating with SERVER 2: {e}")
        return b"ERROR:COMMUNICATION_ERROR"

def handle_client(conn, addr):
    """ Handles an incoming connection from a client. """
    print(f"Connected by {addr}")
    try:
        # Receive the filename request from the client
        filename = conn.recv(1024).decode('utf-8')
        if not filename:
            return
        
        print(f"Client requested file: {filename}")
        
        # --- LOGIC AS PER PROBLEM STATEMENT ---
        
        # 1. Check for the file locally on SERVER 1
        s1_filepath = os.path.join(FILE_DIR, filename)
        s1_content = None
        s1_file_exists = os.path.exists(s1_filepath)
        if s1_file_exists:
            with open(s1_filepath, 'r') as f:
                s1_content = f.read()
            print("File found locally on SERVER 1.")
        else:
            print("File not found locally on SERVER 1.")

        # 2. Send the same file request to SERVER 2
        s2_response_bytes = get_file_from_server2(filename)
        s2_content = None
        s2_file_exists = not s2_response_bytes.startswith(b"ERROR:")
        if s2_file_exists:
            s2_content = s2_response_bytes.decode('utf-8')
            print("File found on SERVER 2.")
        else:
            print("File not found on SERVER 2.")
        
        # 3. Compare contents and prepare the response for the client
        final_response = ""
        if s1_file_exists and s2_file_exists:
            if s1_content == s2_content:
                # Files are identical, send one copy
                final_response = s1_content
                print("Files are identical. Sending one copy to client.")
            else:
                # Files are different, send both
                final_response = f"DIFFERENCE:{s1_content}|||{s2_content}"
                print("Files differ. Sending both versions to client.")
        elif s1_file_exists:
            # File only on SERVER 1
            final_response = s1_content
            print("File only exists on SERVER 1. Sending to client.")
        elif s2_file_exists:
            # File only on SERVER 2
            final_response = s2_content
            print("File only exists on SERVER 2. Sending to client.")
        else:
            # File not found on either server
            final_response = "ERROR:FILE_NOT_FOUND: The requested file could not be found on any server."
            print("File not found on any server. Sending error to client.")
            
        # 4. Send the final response to the client
        conn.sendall(final_response.encode('utf-8'))

    except Exception as e:
        print(f"An error occurred with client {addr}: {e}")
    finally:
        print(f"Closing connection with {addr}")
        conn.close()

def start_server():
    """ Starts SERVER 1 to listen for client connections. """
    if not os.path.exists(FILE_DIR):
        os.makedirs(FILE_DIR)
        print(f"Created directory: {FILE_DIR}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"SERVER 1 is listening on {HOST}:{PORT}...")
        
        while True:
            conn, addr = s.accept()
            # Start a new thread for each client to handle requests concurrently
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    start_server()
