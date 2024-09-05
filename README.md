Attendance Bot
The Attendance Bot is a Discord bot that allows for an easy and quick way to take attendance in meetings by tracking who was present in a specific voice channel. The bot records attendance in a Google Sheet using the Google Sheets API.

Features
-Automatically logs the names of members present in a specified Discord voice channel.
-Records attendance in a Google Sheet with customizable dates.
-Avoids duplicate entries for both names and dates.
-Marks attendance with a light green background.

Prerequisites
-Python 3.7 or higher
-A Discord bot token
-A Google Cloud service account with access to Google Sheets API
-Google Sheets API credentials file (JSON format)
-A Google Spreadsheet where you want to log attendance

Installation

Clone the repository:
Run git clone https://github.com/your-username/attendance-bot.git and navigate into the directory using cd attendance-bot.

Create a virtual environment:
Set up a virtual environment using python -m venv venv. Activate it with source venv/bin/activate on Unix systems or venv\Scripts\activate on Windows.

Install dependencies:
Install the necessary Python packages by running pip install -r requirements.txt.

Set up environment variables:
Create a .env file in the project root directory. Add your Discord bot token and Google Sheets spreadsheet ID in the format:
DISCORD_BOT_TOKEN=your_discord_bot_token
SPREADSHEET_TOKEN=your_google_spreadsheet_id

Google Sheets API Setup:
Enable the Google Sheets API in your Google Cloud project. Create a service account, download the credentials JSON file, and save it in the project directory (e.g., credentials.json). Share your Google Spreadsheet with the service account email found in the credentials JSON with edit permissions.

Configuration
Update the path to the Google Sheets credentials JSON file in the bot script to match the location of your credentials file. Ensure that the Google Spreadsheet ID in your .env file corresponds to the correct spreadsheet you wish to use.

Usage

Run the bot by executing python bot.py in your terminal.
Use the bot command !mark_attendance in Discord to log attendance for members in the "meetings" voice channel.

How It Works
The bot listens for the !mark_attendance command. When invoked, it checks the specified voice channel for members, logs their names in a Google Sheet starting from column B2, and marks attendance under the appropriate date column. If the current date does not exist, it adds the date to the next available column starting from column C, ensuring no duplicate dates or names.

Contributing
Contributions are welcome! Please open an issue or submit a pull request with any enhancements or bug fixes.

Contact
For further questions or suggestions, please contact codingpower101@gmail.com

