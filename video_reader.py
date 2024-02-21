# python code that reads video frame by frame and read the text in certain area (for all frames)

# use easyocr instead of pytesseract

import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Path to the video file C:\Users\ahyil\Videos\Captures\flight.mp4
video_path = 'C:\\Users\\ahyil\\Videos\\Captures\\flight.mp4'

# Path to the output CSV file
output_csv_path = 'C:\\Users\\ahyil\\PycharmProjects\\Tekno_telem_to_csv\\video_data.csv'

# Create a VideoCapture object
cap = cv2.VideoCapture(video_path)

# Create an empty list to store the data
data = []
prev_text = ''

# skip to the 16th minute 40th second
cap.set(cv2.CAP_PROP_POS_MSEC, 1000000)

# Loop through the video frames
while True:

    # Read the next frame
    ret, frame = cap.read()
    # print the current second of the video
    print(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)


    # If the frame was not successfully read then break the loop
    if not ret:
        break

    # Crop the frame to the area containing the text
    cropped_frame = frame[963:978, 110:750]

    # Display the cropped frame
    cv2.imshow('Cropped Frame', cropped_frame)

    # Convert the cropped frame to grayscale
    gray_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to the grayscale frame
    _, threshold_frame = cv2.threshold(gray_frame, 150, 255, cv2.THRESH_BINARY)

    # Convert the thresholded frame to a string
    text = pytesseract.image_to_string(threshold_frame)

    if text and text != prev_text:
        prev_text = text
        # convert all C's and D's to 0's
        text = text.replace('C', '0')
        text = text.replace('D', '0')
        text = text.replace('R', '0')
        text = text.replace('G', '0')
        text = text.replace('B', '0')
        text = text.replace('§', '$')

        # convert all SAT to $AT
        text = text.replace('SAT', '$AT')
        text = text.replace('5AT', '$AT')
        text = text.replace('$A7', '$AT')
        text = text.replace('Sst', '$ST')
        text = text.replace('5AT', '$AT')
        text = text.replace('5A7', '$AT')
        text = text.replace('$sT', '$ST')
        text = text.replace('ssT', '$ST')

        text = text.replace('SST', '$ST')
        text = text.replace('SAT', '$AT')
        text = text.replace('SFY', '$FY')

        text = text.replace('8ST', '$ST')
        text = text.replace('8AT', '$AT')
        text = text.replace('8FY', '$FY')

        text = text.replace('$ST-', '$ST;')
        text = text.replace('$AT-', '$AT;')
        text = text.replace('$FY-', '$FY;')

        text = text.replace('$ST:', '$ST;')
        text = text.replace('$AT:', '$AT;')
        text = text.replace('$FY:', '$FY;')

        text = text.replace('$ST.', '$ST;1,0')

        # delete all spaces
        text = text.replace(' ', '')

        # Append the text to the data list
        data.append(text)
        print(text)

    # If the 'q' key is pressed then break the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close the window
cap.release()
cv2.destroyAllWindows()

# Write the data to a CSV file
with open(output_csv_path, 'w') as file:
    for line in data:
        file.write(line + '\n')
