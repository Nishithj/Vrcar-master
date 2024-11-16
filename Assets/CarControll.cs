using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Collections.Concurrent;

public class CarController : MonoBehaviour
{
    public float speed = 10f;               // Speed of the car
    public float rotationSpeed = 100f;      // Rotation speed for turning
    public int port = 55000;                // Port number for the TCP server
    private TcpListener server;
    private Thread serverThread;
    private bool running = true;
    private ConcurrentQueue<string> commandQueue = new ConcurrentQueue<string>();

    private enum State { MovingForward, TurningRight, TurningLeft }
    private State currentState = State.MovingForward;

    private float turnDuration = 1f;        // Duration of a turn in seconds
    private float turnTimer = 0f;           // Timer to track turning

    void Start()
    {
        serverThread = new Thread(new ThreadStart(StartServer));
        serverThread.IsBackground = true;
        serverThread.Start();
    }

    void Update()
    {
        if (commandQueue.TryDequeue(out string command))
        {
            if (command.ToLower() == "right")
            {
                currentState = State.TurningRight;
                turnTimer = turnDuration;
            }
            else if (command.ToLower() == "left")
            {
                currentState = State.TurningLeft;
                turnTimer = turnDuration;
            }
        }

        switch (currentState)
        {
            case State.MovingForward:
                MoveForward();
                break;
            case State.TurningRight:
                Turn(Vector3.up);
                break;
            case State.TurningLeft:
                Turn(-Vector3.up);
                break;
        }
    }

    void MoveForward()
    {
        transform.Translate(Vector3.forward * speed * Time.deltaTime);
    }

    void Turn(Vector3 direction)
    {
        turnTimer -= Time.deltaTime;
        transform.Rotate(direction, rotationSpeed * Time.deltaTime);
        if (turnTimer <= 0)
        {
            currentState = State.MovingForward; // Return to moving forward after turning
        }
    }

    void StartServer()
    {
        server = new TcpListener(IPAddress.Any, port);
        server.Start();
        Debug.Log("Server started on port " + port);

        while (running)
        {
            try
            {
                TcpClient client = server.AcceptTcpClient();
                NetworkStream stream = client.GetStream();
                byte[] buffer = new byte[1024];
                int bytesRead = stream.Read(buffer, 0, buffer.Length);
                string data = Encoding.UTF8.GetString(buffer, 0, bytesRead);

                commandQueue.Enqueue(data.Trim().ToLower());

                client.Close();
            }
            catch (SocketException e)
            {
                Debug.LogError("Socket exception: " + e.Message);
            }
        }
    }

    void OnApplicationQuit()
    {
        running = false;
        if (server != null)
        {
            server.Stop();
        }
        if (serverThread != null)
        {
            serverThread.Abort();
        }
    }
}
