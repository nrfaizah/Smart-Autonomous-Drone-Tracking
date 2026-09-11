import time
from djitellopy import Tello
import cv2

# Initialize Tello
tello = Tello()
tello.connect()
print("Battery:", tello.get_battery())

# Start video stream
tello.streamon()

# Video writer setup
frame_read = tello.get_frame_read()
height, width, _ = frame_read.frame.shape
video_writer = cv2.VideoWriter('tello_recording.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

# Takeoff
tello.takeoff()
time.sleep(2)

try:
    while True:
        # Get frame from Tello
        img = frame_read.frame

        # Check if the frame is valid before writing
        if img is not None:
            # Resize the frame for display (optional)
            img = cv2.resize(img, (width, height))

            # Display the frame in RGB
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cv2.imshow("Tello Video Stream", img_rgb)

            # Convert the frame to BGR for writing
            img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
            video_writer.write(img_bgr)

        # Wait for the 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            tello.land()
            break

except KeyboardInterrupt:
    # Land the drone if the script is interrupted
    tello.land()

# Cleanup
video_writer.release()
cv2.destroyAllWindows()
tello.streamoff()
