import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_formatting import CellFormat, Color, format_cell_range
from datetime import datetime
import pytz

# Load environment variables from a .env file
load_dotenv('token.env')

# Get import information from the env file
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
SPREADSHEET_TOKEN = os.getenv('SPREADSHEET_TOKEN')

# Define the intents the bot will use
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True 
intents.members = True 

# Bot's prefix for commands
bot = commands.Bot(command_prefix="!", intents=intents)

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("coding-power-bot-50115a993ad0.json", scope)
client = gspread.authorize(creds)

# Open the Google Spreadsheet in the correct section
spreadsheet_id = SPREADSHEET_TOKEN
spreadsheet = client.open_by_key(spreadsheet_id)
sheet = spreadsheet.worksheet('Fall 2024')  # MAKE SURE TO UPDATE THIS TO THE SHEET YOU WANT TO UPDATE

# When bot is run
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.command(name='mark_attendance')
async def mark_attendance(ctx):
    
    # Find the correct channel where the voice chat is occuring
    channel = discord.utils.get(ctx.guild.voice_channels, name="meetings")
    
    # Get the current time in PST
    pst_timezone = pytz.timezone('America/Los_Angeles')
    current_time_pst = datetime.now(pst_timezone)
    today_day = current_time_pst.strftime("%m/%d") 
    today_date = current_time_pst.strftime("%m/%d %I:%M %p")

    #Check if the channel exists
    if not channel:
        await ctx.send("Voice channel 'meetings' not found.")
        return

    # Get the names of all members in the voice channel
    members = channel.members
    if not members:
        await ctx.send(f"No members found in the voice channel 'meetings'.")
        return

    member_names = [member.display_name for member in members]

    # Get all values in the sheet
    sheet_values = sheet.get_all_values()
    header_row = sheet_values[0]  # Get the first row
    name_column = [row[1] for row in sheet_values]  # Gets the second column which has the names of all the members or will be added here
    
    today_date_without_zero = today_day.lstrip('0') # Google sheets does weird things so makes sure that the correct dates are being compared
    
    date_col_index = None
    
    for i, cell_value in enumerate(header_row[2:], start=3):  # Start checking for the date if it exists and if it doesn't create a new column 

        if cell_value.lstrip('0') == today_date_without_zero:
            date_col_index = i
            break
        elif cell_value == "":
            date_col_index = i
            sheet.update_cell(1, date_col_index, today_date_without_zero)
            break
    
    if date_col_index is None:
        date_col_index = len(header_row) + 1
        sheet.update_cell(1, date_col_index, today_day)

    # For members who are present, they get this color
    light_green = CellFormat(backgroundColor=Color(224/255, 236/255, 212/255))

    # Mark attendance for each member
    for member_name in member_names:
        row_index = None
        for i in range(2, len(sheet_values) + 2): 
            cell_value = sheet.cell(i, 2).value
            if cell_value is None or cell_value == "":
                row_index = i
                break
            elif cell_value.lower() == str(member_name).lower():
                row_index = i
                break

        if row_index is None:
            # Add the member if they are not yet there
            row_index = len(sheet_values) + 1
            sheet.update_cell(row_index, 2, member_name)
        elif sheet.cell(row_index, 2).value != member_name:
            # If an empty cell was found but doesn't have the name, add the name
            sheet.update_cell(row_index, 2, member_name)

        # Update the attendance cell with the light green color
        cell_range = f"{gspread.utils.rowcol_to_a1(row_index, date_col_index)}"
        format_cell_range(sheet, cell_range, light_green)

    await ctx.send(f"Attendance marked and recorded for Coding Power members on {today_date}")





# Run the bot
bot.run(TOKEN)
