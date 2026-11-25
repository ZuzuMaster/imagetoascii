import os
import sys
import cv2
import tkinter as tk
from tkinter import filedialog
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Hide the main tkinter window so only the file dialog shows
root = tk.Tk()
root.withdraw()

# Ask the user to pick an image
image_path = filedialog.askopenfilename(
    title="Select an Image for Translating",
    filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.webp")]
)
root.destroy()

# Exit if the dialog was cancelled
if not image_path:
    sys.exit("No file selected.")

# Load the image (imdecode handles non-ASCII paths on Windows)
image = cv2.imdecode(np.fromfile(image_path, np.uint8), cv2.IMREAD_COLOR)
if image is None:
    sys.exit(f"Could not load {image_path}")
    
# Inspect and change image for dimensions and processing
aspect_r = image.shape[0] / image.shape[1]
n_width = 100
n_height = int(n_width * aspect_r * 0.55)
image = cv2.resize(image, (n_width, n_height))
img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
height, width = img.shape

# Find brightness of each pixel and store it
brights = []
for i in range(height):
    for j in range(width):
        brights.append(img[i, j])
    brights.append(4)

brights = [4 if x == 4 else round((x / 255) * 3) for x in brights]

# Create ASCII art using brightnesses for each char
characters = ['░', '▒', '▓', '█']
lines = []
line = ""
for k in brights:
    if k == 4:
        lines.append(line)
        line = ""
    else:
        line += characters[k]

# --- RENDER AS AN IMAGE INSTEAD OF PRINTING ---

# Combine all lines into a single text block
text_content = "\n".join(lines)

# Set font size (you can adjust this if needed)
font_size = 14
try:
    # Try to load a clean monospaced font
    font = ImageFont.truetype("consola.ttf", font_size)
except IOError:
    font = ImageFont.load_default()

# Calculate text block dimensions
dummy_img = Image.new("RGB", (1, 1))
draw = ImageDraw.Draw(dummy_img)
bbox = draw.multiline_textbbox((0, 0), text_content, font=font)
img_width = bbox[2] + 30
img_height = bbox[3] + 30

# Create the final output image with a dark background
output_image = Image.new("RGB", (img_width, img_height), color=(15, 15, 15))
draw = ImageDraw.Draw(output_image)

# Draw the ASCII text onto the image (white text)
draw.text((15, 15), text_content, fill=(240, 240, 240), font=font)

# Save and display the resulting image
output_path = "ascii_art_output.png"
output_image.save(output_path)
print(f"Success! Image saved as '{output_path}'")
output_image.show()
