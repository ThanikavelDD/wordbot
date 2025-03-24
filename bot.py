import tweepy
import pandas as pd
import os
import schedule
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Twitter API authentication
client = tweepy.Client(
    consumer_key=os.getenv("TWITTER_CONSUMER_KEY"),
    consumer_secret=os.getenv("TWITTER_CONSUMER_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
)

def create_word_image(word, meaning, example):
    """Creates an image with the word, meaning, and example sentence."""
    img = Image.open("background.png")
    draw = ImageDraw.Draw(img)
    
    font_word = ImageFont.truetype("arial.ttf", 80)
    font_text = ImageFont.truetype("arial.ttf", 40)
    
    # Positioning
    img_width, img_height = img.size
    padding = 50
    
    # Prepare text content
    text = f"{word}\n\nMeaning: {meaning}\n\nExample: {example}"
    
    # Calculate text size
    text_width, text_height = draw.multiline_textbbox((0, 0), text, font=font_text)[2:]
    x = (img_width - text_width) // 2
    y = (img_height - text_height) // 2
    
    # Draw text
    draw.multiline_text((x, y), text, font=font_text, fill="white", align="center")
    
    output_path = "word_of_the_day.png"
    img.save(output_path)
    return output_path

def post_word_of_the_day():
    """Reads the next word from the CSV and posts it to Twitter."""
    df = pd.read_csv("word_list.csv")
    if df.empty:
        print("No words left in the list.")
        return
    
    word, meaning, example = df.iloc[0]
    word_image = create_word_image(word, meaning, example)
    
    media = client.media_upload(filename=word_image)
    tweet_text = ""
    client.create_tweet(text=tweet_text, media_ids=[media.media_id])
    
    df = df.iloc[1:]  # Remove the posted word
    df.to_csv("word_list.csv", index=False)
    print(f"Posted: {word}")

def schedule_jobs():
    """Schedules the bot to run daily at 11:00 AM IST."""
    schedule.every().day.at("05:30").do(post_word_of_the_day)  # 11:00 AM IST
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    post_word_of_the_day()
