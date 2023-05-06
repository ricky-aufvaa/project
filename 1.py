import pyocr
import pyocr.builders
from PIL import Image

# Set up the OCR engine
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    exit(1)
ocr_tool = tools[0]

# Open the image file using Pillow
with Image.open('image.jpg') as img:
    # Use the OCR engine to extract text from the image
    text = ocr_tool.image_to_string(
        img,
        builder=pyocr.builders.TextBuilder()
    )

# Print the extracted text
print(text)

