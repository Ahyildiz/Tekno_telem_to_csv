import cv2
import numpy as np

# Load the video
input_file = 'C:\\Users\\ahyil\\Videos\\Captures\\2023-08-19 22-14-49.mp4'
cap = cv2.VideoCapture(input_file)

# Check if the video file opened successfully
if not cap.isOpened():
    print("Error opening video file")
    exit()

# Create VideoWriter object to save the output
output_file = 'filtered_video.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = cap.get(cv2.CAP_PROP_FPS)
frame_size = (int(cap.get(3)), int(cap.get(4)))
out = cv2.VideoWriter(output_file, fourcc, fps, frame_size)

# Function to apply noise filtering
def filter_noise(frame):
    # Apply a median filter to reduce noise
    filtered_frame = cv2.medianBlur(frame, 5)
    return filtered_frame

# Process each frame in the video
while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Apply noise filtering
    filtered_frame = filter_noise(frame)

    # Display the original and filtered frames
    cv2.imshow('Original Frame', frame)
    cv2.imshow('Filtered Frame', filtered_frame)

    # Write the filtered frame to the output video file
    out.write(filtered_frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and writer objects
cap.release()
out.release()

# Destroy all OpenCV windows
cv2.destroyAllWindows()