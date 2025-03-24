import tweepy
import pandas as pd
import os

# Load Twitter API keys from GitHub Secrets
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Function to post a tweet
def post_word_of_the_day():
    file_path = "word_list.csv"

    # Read the CSV file
    df = pd.read_csv(file_path)

    if df.empty:
        print("No words left! Please update the list.")
        return
    
    # Get the first word from the list
    word_entry = df.iloc[0]
    word, meaning, example = word_entry["Word"], word_entry["Meaning"], word_entry["Example"]

    # Create tweet text
    tweet_text = f"📖 Word of the Day: {word}\n\n📝 Meaning: {meaning}\n💬 Example: {example}\n\n#WordOfTheDay #Vocabulary"

    # Post tweet
    api.update_status(tweet_text)
    print(f"Tweet posted: {word}")

    # Remove the used word and update the CSV
    df = df.iloc[1:]  # Remove first row
    df.to_csv(file_path, index=False)

# Run the function
if __name__ == "__main__":
    post_word_of_the_day()
