import socket
import time

SERVER_ADDRESS = 'localhost'  # IP address of the Unity server
PORT = 55000                  # Port number matching Unity

def send_command(command):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SERVER_ADDRESS, PORT))
            client_socket.sendall(command.encode('utf-8'))
            print(f"Sent: {command}")
    except ConnectionRefusedError:
        print("Connection failed. Ensure that the Unity server is running.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Send 'right' command
    send_command("right")
    time.sleep(2)  # Wait for the turn to complete

    # Send 'forward' command (no command needed; it moves forward by default)
    time.sleep(3)  # Wait for a few seconds while moving forward

    # Send 'left' command
    send_command("left")
    time.sleep(2)  # Wait for the turn to complete

    # Send 'forward' command (no command needed)
    time.sleep(3)  # Continue moving forward
