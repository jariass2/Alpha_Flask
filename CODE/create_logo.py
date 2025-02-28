from PIL import Image, ImageDraw, ImageFont
import os

# Create a new image with a white background
width = 400
height = 150
background_color = (255, 255, 255)
img = Image.new('RGB', (width, height), background_color)

# Get a drawing context
draw = ImageDraw.Draw(img)

# Draw a blue rectangle as background
draw.rectangle([(0, 0), (width, height)], fill=(30, 64, 175))

# Add text
text = "ALPHA ESPAI"
text_color = (255, 255, 255)  # White color

# Calculate text position for center alignment
text_bbox = draw.textbbox((0, 0), text, font=None, font_size=60)
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]
x = (width - text_width) // 2
y = (height - text_height) // 2

# Draw the text
draw.text((x, y), text, fill=text_color, font_size=60)

# Save the image
img.save('alpha_espai_logo.jpg', 'JPEG', quality=95)
