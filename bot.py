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
FONT_SIZE = 50
TEXT_COLOR = "white"
TEXT_POSITION = (50, 50)

# CSV File Path
CSV_FILE = "word_list.csv"

def create_word_image(word, meaning, example):
    """Creates an image with the word, meaning, and example sentence overlayed."""
    img = Image.open(IMAGE_PATH).convert("RGB")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    
    # Prepare text
    text = f"Word: {word}\nMeaning: {meaning}\nExample: {example}"
    
    # Get text size
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Position text in the center
    img_width, img_height = img.size
    x = (img_width - text_width) // 2
    y = (img_height - text_height) // 2
    
    draw.text((x, y), text, fill=TEXT_COLOR, font=font, align="center")
    
    # Save image
    word_image = "word_of_the_day.jpg"
    img.save(word_image)
    return word_image

def post_word_of_the_day():
    """Reads a word from the CSV, creates an image, and posts it on Twitter."""
    df = pd.read_csv(CSV_FILE)
    
    if df.empty:
        print("Word list is empty. No words to post.")
        return
    
    # Get the first word entry
    word, meaning, example = df.iloc[0]
    
    # Create image with text
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
