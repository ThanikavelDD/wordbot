import os
import tweepy
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

# Twitter API authentication
client = tweepy.Client(
    consumer_key=os.getenv("API_KEY"),
    consumer_secret=os.getenv("API_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_SECRET")
)

# Image and font settings
IMAGE_PATH = "ddd.jpg"  # Background image
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SIZE = 50
TEXT_COLOR = "white"
TEXT_POSITION = (50, 50)  # Adjust this to center text properly

# CSV File Path
CSV_FILE = "word_list.csv"

def create_word_image(word, meaning, example, output_path="word_of_the_day.png"):
    """Creates an image with the word, meaning, and example sentence."""
    img = Image.open(IMAGE_PATH)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    # Format text
    text = f"{word}\n\nMeaning: {meaning}\n\nExample: {example}"

    # Calculate text positioning
    image_width, image_height = img.size
    text_width, text_height = draw.multiline_textbbox((0, 0), text, font=font)[2:]
    x = (image_width - text_width) // 2
    y = (image_height - text_height) // 2

    draw.multiline_text((x, y), text, font=font, fill=TEXT_COLOR, align="center")
    
    img.save(output_path)
    return output_path

def post_word_of_the_day():
    """Reads the next word from CSV, creates an image, and posts to Twitter."""
    df = pd.read_csv(CSV_FILE)
    if df.empty:
        print("No more words in the list.")
        return
    
    word, meaning, example = df.iloc[0]  # Get first word

    # Generate image
    word_image = create_word_image(word, meaning, example)

    # Upload media and tweet
    media = client.media_upload(filename=word_image)  # Twitter API v1.1 function
    client.create_tweet(text="", media_ids=[media.media_id])  # Post tweet with image

    # Remove posted word from CSV
    df = df.iloc[1:]
    df.to_csv(CSV_FILE, index=False)
    print(f"Posted: {word}")

if __name__ == "__main__":
    post_word_of_the_day()  # Runs once and exits
