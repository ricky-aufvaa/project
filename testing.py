import cv2
import requests
from bs4 import BeautifulSoup
import numpy as np

# Define the path to the EAST text detection model
model_path = 'path/to/east/model/frozen_east_text_detection.pb'

# Load the EAST model
net = cv2.dnn.readNet(model_path)

# Define the minimum confidence score for text detection
min_confidence = 0.5

# Define the maximum width and height of the input image
max_width = 800
max_height = 800

# Define the URL of the website to scrape
url = 'https://www.example.com'

# Define the search terms to use when scraping the website
search_terms = ['genre', 'about the author', 'summary', 'recent reviews']

# Load the input image or video
image = cv2.imread('path/to/image')

# Resize the input image
height, width, _ = image.shape
if width > height:
    new_width = max_width
    new_height = int(height * (max_width / width))
else:
    new_height = max_height
    new_width = int(width * (max_height / height))
image = cv2.resize(image, (new_width, new_height))

# Convert the input image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply bilateral filtering to smooth the image and reduce noise
gray = cv2.bilateralFilter(gray, 11, 17, 17)

# Detect edges in the input image using the Canny edge detection algorithm
edges = cv2.Canny(gray, 30, 200)

# Construct a blob from the input image to use as input to the EAST model
blob = cv2.dnn.blobFromImage(image, 1.0, (new_width, new_height), (123.68, 116.78, 103.94), True, False)

# Set the input to the EAST model and perform text detection
net.setInput(blob)
(scores, geometry) = net.forward(['feature_fusion/Conv_7/Sigmoid', 'feature_fusion/concat_3'])

# Decode the predictions and apply non-maxima suppression to remove overlapping bounding boxes
rectangles, confidences = cv2.dnn.NMSBoxesRotated(
    geometry[0, 0], scores[0, 0], min_confidence, min_distance=4 * (new_width / 500))

# Loop over the bounding boxes and recognize the text
for i in range(len(rectangles)):
    box = rectangles[i]
    confidence = confidences[i]
    if confidence > min_confidence:
        # Extract the coordinates of the bounding box
        box = cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        box = cv2.orderPoints(box)
        # Extract the region of interest from the input image
        roi = image[int(box[1, 1]):int(box[0, 1]), int(box[1, 0]):int(box[2, 0])]
        # Convert the ROI to grayscale
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        # Apply adaptive thresholding to binarize the ROI and make it easier to recognize the text
        thresh_roi = cv2.adaptiveThreshold(gray_roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        # Perform OCR to recognize the text in the ROI using Pytesseract
try:
    import pytesseract
except ImportError:
    print('Please install Pytesseract to perform OCR.')
    exit()

# Set the configuration options for Pytesseract
config = ('-l eng --oem 1 --psm 3')

# Perform OCR on the ROI
text = pytesseract.image_to_string(thresh_roi, config=config)

# Print the recognized text
print('Recognized text:', text)

# Search the website for the search terms and scrape the information
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
for term in search_terms:
    # Search for the term in the HTML of the website
    results = soup.findAll(text=lambda text: text and term.lower() in text.lower())
    if results:
        # Print the search term and the corresponding information
        print(term.capitalize() + ':', results[0])
    else:
        # If the term is not found, print a message
        print(term.capitalize() + ': Not found on website.')
