import os
import tweepy
import schedule
import time
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from datetime import datetime

# Twitter API authentication (v2 for tweets, v1.1 for media upload)
client = tweepy.Client(
    consumer_key=os.getenv("TWITTER_CONSUMER_KEY"),
    consumer_secret=os.getenv("TWITTER_CONSUMER_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
)

auth = tweepy.OAuth1UserHandler(
    os.getenv("TWITTER_CONSUMER_KEY"),
    os.getenv("TWITTER_CONSUMER_SECRET"),
    os.getenv("TWITTER_ACCESS_TOKEN"),
    os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
)
api = tweepy.API(auth, wait_on_rate_limit=True)  # API v1.1 for media upload

def create_word_image(word, meaning, example, output_path="word_of_the_day.png"):
    """Creates an image with the word, meaning, and example sentence."""
    bg_image = Image.open("ddd.jpg")  # Fixed file name
    draw = ImageDraw.Draw(bg_image)
    font = ImageFont.truetype("arial.ttf", 50)
    
    text = f"{word}\n\nMeaning: {meaning}\n\nExample: {example}"
    
    image_width, image_height = bg_image.size
    text_width, text_height = draw.multiline_textbbox((0, 0), text, font=font)[2:]
    
    x = (image_width - text_width) // 2
    y = (image_height - text_height) // 2
    
    draw.multiline_text((x, y), text, font=font, fill="white", align="center")
    
    bg_image.save(output_path)
    return output_path

def post_word_of_the_day():
    """Reads the next word from CSV, creates an image, and posts to Twitter."""
    df = pd.read_csv("word_list.csv")
    if df.empty:
        print("No more words in the list.")
        return
    
    word, meaning, example = df.iloc[0]
    word_image = create_word_image(word, meaning, example)
    
    # Upload media using API v1.1
    media = api.media_upload(filename=word_image)
    
    # Post tweet with media using API v2
    client.create_tweet(text="", media_ids=[media.media_id])
    
    # Remove posted word from CSV
    df = df.iloc[1:]
    df.to_csv("word_list.csv", index=False)
    print(f"Posted: {word}")

def job():
    """Schedules the Word of the Day post."""
    post_word_of_the_day()

schedule.every().day.at("05:30").do(job)  # 05:30 UTC = 11:00 AM IST

while True:
    schedule.run_pending()
    time.sleep(60)
