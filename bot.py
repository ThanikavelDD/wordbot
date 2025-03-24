import tweepy
import pandas as pd
import os
from PIL import Image, ImageDraw, ImageFont

# Load API keys from GitHub Secrets
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# Authenticate with Twitter API v2 (for tweets)
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

# Authenticate with Twitter API v1.1 (for media uploads)
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Image settings
IMAGE_PATH = "ddd.jpg"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SIZE = 50
TEXT_POSITION = (50, 50)
TEXT_COLOR = "white"

# CSV File Path
CSV_FILE = "word_list.csv"

def post_word_of_the_day():
    # Read the word list
    df = pd.read_csv(CSV_FILE)
    
    if df.empty:
        print("Word list is empty. No words to post.")
        return
    
    # Get the first word entry
    word, meaning, example = df.iloc[0]
    
    # Create image with word overlay
    img = Image.open(IMAGE_PATH)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    draw.text(TEXT_POSITION, word, fill=TEXT_COLOR, font=font)
    
    # Save image
    word_image = "word_of_the_day.jpg"
    img.save(word_image)
    
    # Upload media using API v1.1
    media = api.media_upload(filename=word_image)

    # Post tweet using API v2
    status = f"Word of the Day: {word}\nMeaning: {meaning}\nExample: {example}"
    client.create_tweet(text=status, media_ids=[media.media_id])
    
    # Remove posted word from CSV
    df = df.iloc[1:]
    df.to_csv(CSV_FILE, index=False)
    
    print(f"Posted: {word}")

if __name__ == "__main__":
    post_word_of_the_day()
