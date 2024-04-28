from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response, generate_chess_puzzle
from discord.ext import tasks
from discord import File

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

@tasks.loop(minutes=60)  # Adjust the time to be less frequent to avoid spam
async def post_chess_puzzle():
    channel_id = 1211867222645940247 # Replace with your channel ID
    channel = client.get_channel(channel_id)
    if channel:
        puzzle_image_path, puzzle_text = generate_chess_puzzle()
        if puzzle_image_path and puzzle_text:
            # Send the image and the puzzle text in an embed or as a simple message
            with open(puzzle_image_path, 'rb') as puzzle_image:
                await channel.send(puzzle_text, file=File(puzzle_image, 'puzzle.png'))


@client.event 
async def on_ready() -> None:
    print(f'{client.user} is now running!')
    post_chess_puzzle.start()

@client.event 
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    user_message: str = message.content

    # Check if the message is a command for the bot
    if user_message.startswith('!'):
        command = user_message[1:].lower().strip()
        if command == 'generate me a puzzle':
            puzzle_image_path, puzzle_text = generate_chess_puzzle()
            if puzzle_image_path:
                await message.channel.send(puzzle_text, file=File(puzzle_image_path, 'puzzle.png'))
            return
        elif command == 'hello bot':
            response = "Hello! How can I assist you?"
            await message.channel.send(response)
            return
        # Handle other commands or ignore

    # Ignore all other messages
    return

def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()