import socket
import time
from keras.models import load_model

# Load the saved model
model = load_model("E:\\BCI\\final67.h5")

# Make predictions on the test set
y_pred_probs = model.predict(X_test)  
y_pred = (y_pred_probs > 0.5).astype(int)  # Thresholding the probabilities to 0 or 1

# Map the predicted labels back to 'left' or 'right'
inverse_label_mapping = {0: 'left', 1: 'right'}
y_pred_labels = [inverse_label_mapping[pred] for pred in y_pred.flatten()]

# Send prediction results to Unity
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
    # Send predictions (left or right) to Unity sequentially
    for i in range(10):  # Sending the first 10 predictions
        print(f"Sending command to Unity: {y_pred_labels[i]}")
        send_command(y_pred_labels[i])
        time.sleep(2)  # Wait for a few seconds before sending the next prediction

    # Optional: Send a stop or reset command if needed after the predictions
    send_command("stop")  # This can be a custom command in Unity for stopping or resetting the car
