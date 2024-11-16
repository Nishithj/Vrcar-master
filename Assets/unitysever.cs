using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class UnityServer : MonoBehaviour
{
    private TcpListener server;
    private Thread serverThread;
    private bool running = true;

    // Set the port number
    public int port = 55000; // You can choose any available port number

    void Start()
    {
        // Start the server thread
        serverThread = new Thread(new ThreadStart(StartServer));
        serverThread.IsBackground = true;
        serverThread.Start();
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
                // Wait for a client connection
                TcpClient client = server.AcceptTcpClient();
                NetworkStream stream = client.GetStream();
                byte[] buffer = new byte[1024];
                int bytesRead = stream.Read(buffer, 0, buffer.Length);
                string data = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                Debug.Log("Received: " + data);
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
        serverThread.Abort();
    }
}
