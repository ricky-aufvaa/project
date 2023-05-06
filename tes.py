import cv2
import pytesseract

# Load the image
img = cv2.imread('image.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply thresholding to binarize the image
thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Apply some morphological operations to clean up the image
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
cleaned = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, kernel)

# Use pytesseract to extract th
# Use pytesseract to extract the text from the image
title = pytesseract.image_to_string(cleaned)

# Print the extracted title
print(title)
