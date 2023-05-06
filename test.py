import cv2
import pytesseract

# Load the image
img = cv2.imread('image.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply thresholding to preprocess the image
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Apply dilation to make the text more visible
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
dilated = cv2.dilate(thresh, kernel, iterations=5)

# Find contours in the image
contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Loop over the contours and extract the text
for contour in contours:
    # Get the bounding rectangle of the contour
    x, y, w, h = cv2.boundingRect(contour)

    # Crop the region of interest from the image
    roi = img[y:y+h, x:x+w]

    # Use pytesseract to extract the text from the ROI
    text = pytesseract.image_to_string(roi, lang='eng', config='--psm 11')
    
    # Print the extracted text
    print(text)

