# server2.py
import socket
import os
import threading

# --- CONFIGURATION ---
HOST = '0.0.0.0'         # Listen on all available network interfaces
PORT = 65002             # Port for SERVER 2
FILE_DIR = "server2_files" # Directory to store files for this server

def handle_request(conn, addr):
    """ Handles a file request from SERVER 1. """
    print(f"Request received from {addr}")
    try:
        # Receive the filename from SERVER 1
        filename = conn.recv(1024).decode('utf-8')
        if not filename:
            return
            
        print(f"Searching for file: {filename}")
        filepath = os.path.join(FILE_DIR, filename)

        # Check if file exists and send it or send an error
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                file_data = f.read()
            conn.sendall(file_data)
            print(f"File '{filename}' found and sent.")
        else:
            conn.sendall(b"ERROR:FILE_NOT_FOUND")
            print(f"File '{filename}' not found.")

    except Exception as e:
        print(f"An error occurred with {addr}: {e}")
    finally:
        print(f"Closing connection with {addr}")
        conn.close()

def start_server():
    """ Starts SERVER 2 and listens for connections. """
    if not os.path.exists(FILE_DIR):
        os.makedirs(FILE_DIR)
        print(f"Created directory: {FILE_DIR}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"SERVER 2 is listening on {HOST}:{PORT}...")

        while True:
            conn, addr = s.accept()
            # Handle each request in a new thread
            thread = threading.Thread(target=handle_request, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    start_server()
