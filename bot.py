import tweepy
import pandas as pd
import os
from PIL import Image, ImageDraw, ImageFont

# Load API keys from GitHub Secrets
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# Authenticate with Twitter API v2
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

# Image settings
IMAGE_PATH = "ddd.jpg"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SIZE = 50  # Default size
TEXT_COLOR = "white"

# CSV File Path
CSV_FILE = "word_list.csv"

def create_word_image(word, meaning, example):
    """Creates an image with the word, meaning, and example text."""
    img = Image.open(IMAGE_PATH)
    draw = ImageDraw.Draw(img)
    
    # Load font
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    # Define text content
    text = f"{word}\n\nMeaning: {meaning}\n\nExample: {example}"
    
    # Get image dimensions
    img_width, img_height = img.size
    text_width, text_height = draw.multiline_textsize(text, font=font)
    
    # Position text at the center
    x = (img_width - text_width) // 2
    y = (img_height - text_height) // 2
    
    # Draw text
    draw.multiline_text((x, y), text, font=font, fill=TEXT_COLOR, align="center")

    # Save the image
    word_image = "word_of_the_day.jpg"
    img.save(word_image)
    return word_image

def post_word_of_the_day():
    """Reads a word from CSV, generates an image, and tweets it."""
    df = pd.read_csv(CSV_FILE)
    
    if df.empty:
        print("Word list is empty. No words to post.")
        return
    
    # Get the first word entry
    word, meaning, example = df.iloc[0]

    # Create image with full text
    word_image = create_word_image(word, meaning, example)
    
    # Post to Twitter
    media = client.media_upload(filename=word_image)
    status = f"Word of the Day: {word}\nMeaning: {meaning}\nExample: {example}"
    client.create_tweet(text=status, media_ids=[media.media_id])
    
    # Remove posted word from CSV
    df = df.iloc[1:]
    df.to_csv(CSV_FILE, index=False)
    
    print(f"Posted: {word}")

if __name__ == "__main__":
    post_word_of_the_day()
