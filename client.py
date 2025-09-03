# client.py
import socket
import sys

# --- CONFIGURATION ---
SERVER1_HOST = '127.0.0.1'  # IP address of SERVER 1
SERVER1_PORT = 65001        # Port for SERVER 1
BUFFER_SIZE = 4096

def request_file(filename):
    """ Connects to SERVER 1 and requests a file. """
    
    # Create a socket and connect to SERVER 1
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Connecting to SERVER 1 at {SERVER1_HOST}:{SERVER1_PORT}...")
        try:
            s.connect((SERVER1_HOST, SERVER1_PORT))
            print("Connected.")
            
            # Send the filename to SERVER 1
            s.sendall(filename.encode('utf-8'))
            print(f"Requested file: {filename}")

            # Receive the response from SERVER 1
            response = s.recv(BUFFER_SIZE).decode('utf-8')

            # Process the response
            if response.startswith("DIFFERENCE:"):
                print("[INFO] Received two different versions of the file.\n")
                parts = response.split("|||")
                print(f"--- Version from SERVER 1 ---\n{parts[0][11:]}\n")
                print(f"--- Version from SERVER 2 ---\n{parts[1]}")
            elif response.startswith("ERROR:"):
                print(f"[ERROR] Received message from server: {response[6:]}")
            else:
                print("[SUCCESS] Received file from SERVER1.")
                print("Content:\n--------------------")
                print(response)
                print("--------------------")

        except ConnectionRefusedError:
            print("[FATAL] Connection to SERVER 1 failed. Is the server running?")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python client.py <filename>")
        sys.exit(1)
        
    file_to_request = sys.argv[1]
    request_file(file_to_request)
