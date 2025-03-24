import tweepy
import pandas as pd
import os
from PIL import Image, ImageDraw, ImageFont

# Load API keys from GitHub Secrets
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# Authenticate with Twitter API v2 (for posting tweets)
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

# Authenticate with Twitter API v1.1 (for media upload)
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Image settings
IMAGE_PATH = "ddd.jpg"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SIZE = 50
TEXT_COLOR = "white"
TEXT_POSITION = (50, 50)

# CSV File Path
CSV_FILE = "word_list.csv"

def create_word_image(word, meaning, example):
    """Creates an image with the word, meaning, and example sentence."""
    img = Image.open(IMAGE_PATH)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    # Positioning text
    text = f"{word}\n\nMeaning: {meaning}\nExample: {example}"
    text_x, text_y, text_w, text_h = draw.textbbox((0, 0), text, font=font)
    img_width, img_height = img.size
    x = (img_width - text_w) // 2
    y = (img_height - text_h) // 2

    # Draw text on image
    draw.text((x, y), text, font=font, fill=TEXT_COLOR)

    # Save image
    output_path = "word_of_the_day.jpg"
    img.save(output_path)
    return output_path

def post_word_of_the_day():
    """Reads the CSV, creates an image, and posts it to Twitter."""
    df = pd.read_csv(CSV_FILE)

    if df.empty:
        print("Word list is empty. No words to post.")
        return

    # Get the first word entry
    word, meaning, example = df.iloc[0]

    # Create image with text
    word_image = create_word_image(word, meaning, example)

    # Upload media using Tweepy API v1.1
    media = api.media_upload(filename=word_image)

    # Post tweet with image using Tweepy API v2
    status = f"Word of the Day: {word}\nMeaning: {meaning}\nExample: {example}"
    client.create_tweet(text=status, media_ids=[media.media_id_string])

    # Remove the posted word from CSV
    df = df.iloc[1:]
    df.to_csv(CSV_FILE, index=False)

    print(f"Posted: {word}")

if __name__ == "__main__":
    post_word_of_the_day()
