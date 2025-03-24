import tweepy
import pandas as pd
import os
from PIL import Image, ImageDraw, ImageFont

# Twitter API keys (Use GitHub Secrets for security)
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# Authenticate with Twitter API
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# File paths
csv_file = "word_list.csv"
image_path = "ddd.jpg"  # Updated to match your uploaded JPG file

def post_word_of_the_day():
    # Read CSV
    df = pd.read_csv(csv_file)
    if df.empty:
        print("Word list is empty!")
        return

    # Get first word and remove it from list
    word, meaning, example = df.iloc[0]
    df = df.iloc[1:]
    df.to_csv(csv_file, index=False)

    # Create image with text
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 50)  # Adjust font if needed
    except IOError:
        font = ImageFont.load_default()

    text = f"{word}\n\n{meaning}\n\nExample: {example}"
    
    # Center text dynamically
    text_x, text_y = 50, 50  # Adjust position as needed
    draw.text((text_x, text_y), text, font=font, fill="black")  

    # Save the image
    output_image = "word_of_the_day.jpg"  # Keep it JPG format
    img.save(output_image)

    # Post to Twitter
    status = f"📖 Word of the Day: {word}\n\n🔹 Meaning: {meaning}\n🔹 Example: {example}"
    media = api.media_upload(output_image)
    api.update_status(status=status, media_ids=[media.media_id])

    print(f"Posted: {word}")

# Run the bot
if __name__ == "__main__":
    post_word_of_the_day()
