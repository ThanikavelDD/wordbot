# wordbot



📌 Project: Automated Twitter Bot – Word of the Day
🔹 Overview
Designed and implemented a fully automated Twitter bot that posts a "Word of the Day" daily at 11:00 AM IST. The bot fetches words from a CSV file, overlays them on an image, and tweets them along with their meanings and example sentences. The entire process is automated using GitHub Actions, eliminating the need for manual execution.

🛠️ Technologies & Tools Used
💻 Programming & Scripting
Python – Core programming language used for automation, data handling, and API interactions.

⏳ Automation & Deployment
GitHub Actions

Automates script execution using a cron job in a YAML workflow.

Runs the bot daily at 11:00 AM IST.

Ensures fully autonomous execution without user intervention.

Cron Scheduling

Used within GitHub Actions to execute the bot at a predefined time.

Format used: cron: "30 5 * * *" (Executes at 5:30 AM UTC = 11:00 AM IST).

🐦 Twitter API Integration
Twitter API v2 (tweepy.Client)

Responsible for posting tweets with the word, meaning, and example.

Uses OAuth 2.0 Bearer Token authentication to ensure secure API access.

Twitter API v1.1 (tweepy.API)

Required for media uploads (Twitter API v2 doesn’t support direct media uploads).

Uses OAuth 1.0a authentication to allow image posting.

OAuth Authentication (API Keys & Tokens)

Securely manages authentication using API_KEY, API_SECRET, ACCESS_TOKEN, and ACCESS_SECRET.

API credentials are stored as GitHub Secrets to enhance security.

📂 Data Handling & Storage
Pandas (Data Analysis Library)

Reads and processes the word_list.csv file.

Extracts the first word from the list to be posted.

Removes the posted word from the CSV file to avoid repetition.

Saves the updated list back to word_list.csv.

CSV File (word_list.csv)

Stores the words along with their meanings and example sentences.

Example format:

Word	Meaning	Example Sentence
Serendipity	Unexpected good fortune	She found the book by pure serendipity.
The bot ensures that no duplicate words are posted by removing them after posting.

🖼️ Image Processing (Text Overlay on Image)
Pillow (PIL - Python Imaging Library)

Opens the background image (ddd.png).

Overlays the word of the day in a stylish font.

Uses ImageDraw to draw text on the image.

Uses ImageFont.truetype() to specify font style and size.

Image Settings

Background Image: ddd.png (Pre-selected image for all posts).

Font: DejaVuSans-Bold.ttf (Ensures high-quality text rendering).

Font Size: 350 (Increased for better readability).

Text Position: (50, 50) (Ensures proper alignment).

Text Color: "darkgreen" (Selected for aesthetic appeal).

Final Image Processing

Saves the modified image as word_of_the_day.jpg.

The image is then uploaded to Twitter before posting.

📁 File & Repository Structure
bash
Copy
Edit
📂 Twitter-Bot-Word-of-the-Day
│── 📜 bot.py               # Main script for tweet automation
│── 📜 requirements.txt      # Dependencies (tweepy, pandas, pillow)
│── 📜 word_list.csv         # Word database with meanings & examples
│── 🖼️ ddd.png              # Background image for word overlay
│── 📂 .github/
│   ├── 📂 workflows/
│   │   ├── post_word.yml   # GitHub Actions workflow (automation)
🔒 Security & Secrets Management
GitHub Secrets

API credentials (API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET) are stored securely.

Prevents hardcoding sensitive information in the script.

Environment Variables (os.getenv)

Loads API keys at runtime to enhance security.

Avoids exposing credentials in the repository.

🚀 Workflow Execution
1️⃣ Scheduled Execution
GitHub Actions triggers the bot every day at 11:00 AM IST.

2️⃣ Data Extraction
Reads the next word from word_list.csv.

3️⃣ Image Processing
Opens ddd.png, overlays the word, and saves word_of_the_day.jpg.

4️⃣ Posting to Twitter
Uploads the image to Twitter (API v1.1).

Posts the tweet with word, meaning, and example (API v2).

5️⃣ Word List Update
Removes the posted word from word_list.csv to prevent duplicates.

6️⃣ Completion & Logging
Logs the posted word to console.

Execution completes automatically.

📜 Skills & Keywords for CV
🖥️ Technical Skills
✔ Python (Automation, API Integration, Data Handling)
✔ GitHub Actions (CI/CD Automation)
✔ Twitter API v2 & v1.1 (OAuth, Tweepy)
✔ Pandas (CSV Data Processing)
✔ Pillow (Image Processing, Text Overlay)
✔ YAML (Workflow Automation)

🛠️ Tools & Technologies
✔ Git & GitHub
✔ Environment Variables (os.getenv)
✔ OAuth Authentication
✔ Cron Jobs (Task Scheduling)

🚀 Project Impact
✅ Fully automated, zero manual intervention required
✅ Secure authentication using GitHub Secrets
✅ Ensures unique daily posts by managing CSV dynamically
✅ Uses efficient API handling to optimize tweet & media upload
✅ Enhances engagement on Twitter through interactive daily posts
