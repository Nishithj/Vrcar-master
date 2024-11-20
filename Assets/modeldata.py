import socket
import time
import pandas as pd
from keras.models import load_model

# Load the saved model
try:
    model = load_model("D:\\Nishith\\Python\\try.h5")
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")

# Load the test data from CSV
try:
    X_test = pd.read_csv("E:\\BCI\\X_test.csv")
    print("Test data loaded successfully.")
    print("Test data shape:", X_test.shape)
except Exception as e:
    print(f"Error loading test data: {e}")

# Ensure the data matches the model's input format (e.g., normalization, reshaping)
try:
    # Example preprocessing (adjust as needed)
    # X_test = X_test / 255.0  # Normalize if needed
    y_pred_probs = model.predict(X_test)
    print("Predictions made successfully.")
except Exception as e:
    print(f"Error during prediction: {e}")

# Threshold and map predictions to commands
try:
    y_pred = (y_pred_probs > 0.5).astype(int)
    inverse_label_mapping = {0: 'left', 1: 'right'}
    y_pred_labels = [inverse_label_mapping[pred] for pred in y_pred.flatten()]
    print("Predicted labels:", y_pred_labels[:10])  # Print first 10 labels for verification
except Exception as e:
    print(f"Error mapping predictions: {e}")

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
    try:
        for i in range(min(10, len(y_pred_labels))):  # Ensure we don't exceed available predictions
            print(f"Sending command to Unity: {y_pred_labels[i]}")
            send_command(y_pred_labels[i])
            time.sleep(2)  # Wait before sending the next command
        send_command("stop")
    except Exception as e:
        print(f"Error in sending commands: {e}")
