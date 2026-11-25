import os
import sys
import cv2
import tkinter as tk
from tkinter import filedialog

# Hide the main tkinter window so only the file dialog shows
root = tk.Tk()
root.withdraw()

# Ask the user to pick an image
image_path = filedialog.askopenfilename(
    title="Select an Image for Head Counting",
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
    brights.append(10)

brights = [10 if x == 10 else round((x / 255) * 9) for x in brights]

# Create ASCII art using brightnesses for each char
characters = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@']
lines = []
line = ""
for k in brights:
    if k == 10:
        lines.append(line)
        line = ""
    else:
        line += characters[k]

# Finally, print full image
for l in lines:
    print(l)