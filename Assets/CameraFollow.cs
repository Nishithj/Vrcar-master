using UnityEngine;

public class CameraFollow : MonoBehaviour
{
    public Transform target;         // Reference to the car's transform
    public Vector3 offset;           // Offset position from the car
    public float smoothSpeed = 0.125f; // Smoothing factor for the camera movement

    void LateUpdate()
    {
        // Calculate the desired position based on the target's position and the offset
        Vector3 desiredPosition = target.position + offset;
        
        // Smoothly interpolate the camera's position towards the desired position
        Vector3 smoothedPosition = Vector3.Lerp(transform.position, desiredPosition, smoothSpeed);
        transform.position = smoothedPosition;

        // Ensure the camera looks at the target (optional)
        transform.LookAt(target);
    }
}
