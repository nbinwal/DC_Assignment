# Distributed Computing - Client/Server File System

This project is an implementation of a simple distributed file system as part of the Distributed Computing (CCZG 526) assignment for BITS Pilani. It demonstrates the client-server paradigm with file replication and synchronization checks.

The system consists of three main components:
* **CLIENT**: A command-line program that requests a file from the primary server.
* **SERVER 1**: The primary server that receives client requests, checks its local file system, and coordinates with a replica server.
* **SERVER 2**: A replica file server that holds a backup copy of the files.

---

### ## ✨ Key Features

-   **File Replication**: `SERVER 2` acts as a replica of `SERVER 1`, holding the same set of files.
-   **Synchronization Check**: When a file is requested, `SERVER 1` compares its version with the version on `SERVER 2`.
-   **Differential Response**:
    -   If file versions are identical, the client receives one copy.
    -   If file versions differ, the client receives both versions.
-   **Fault Tolerance**: If a file is available on only one of the servers, it is still successfully delivered to the client.
-   **Error Handling**: The client receives a clear "File Not Found" message if the file doesn't exist on either server.

---

### ## 🚀 How to Run

This system was designed for a 3-node setup but can be run on a single machine using `localhost` to bypass potential firewall restrictions in cloud lab environments.

#### **Prerequisites**
- Python 3

#### **Single-Node `localhost` Setup**

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/nbinwal/DC_Assignment.git](https://github.com/nbinwal/DC_Assignment.git)
    cd DC_Assignment
    ```

2.  **Set up the file directories:**
    Create the necessary files for testing within the `server1_files` and `server2_files` directories.

3.  **Run the servers and client:**
    Open **three separate terminals** in the `DC_Assignment` directory.

    * **In Terminal 1, start Server 2:**
        ```bash
        python server2.py
        ```
    * **In Terminal 2, start Server 1:**
        ```bash
        python server1.py
        ```
    * **In Terminal 3, run the Client:**
        ```bash
        # Request a file that exists on both servers
        python client.py hello.txt

        # Request a file that does not exist
        python client.py non_existent_file.txt
        ```
---

### ## 📂 Code Structure

* `client.py`: The client application. It takes a filename as a command-line argument, connects to SERVER 1, and prints the response.
* `server1.py`: The primary server. It listens for client connections, manages the logic of checking for local files, and communicates with SERVER 2 for file comparison.
* `server2.py`: The replica server. It listens for requests from SERVER 1 and returns the content of the requested file if it exists.
