from gtts import gTTS
import os
import pytesseract
from PIL import Image
from PIL import ImageEnhance

# Open the image file
# image = Image.open('uo0v00/i8c8g8a.png')
image = Image.open('uo0v00/title.png')

# Apply image enhancement
enhancer = ImageEnhance.Contrast(image)
enhanced_image = enhancer.enhance(2.0)  # Adjust the enhancement factor as needed

# Convert the enhanced image to grayscale
enhanced_image = enhanced_image.convert('L')

# Use pytesseract to extract text from the image
text = pytesseract.image_to_string(enhanced_image, lang='eng')

# Print the extracted text
print(text)

# Text to be converted into speech
# text = "This is the text to be converted into speech."

# Create gTTS object
tts = gTTS(text)

# Save the speech as an audio file
tts.save("output.mp3")

# Play the audio file
os.system("output.mp3")
