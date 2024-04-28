import requests
import random
import pandas as pd
from .generate_image import get_puzzle_position, save_position_image

def get_random_puzzle_id(csv_path):
    df = pd.read_csv(csv_path)
    return random.choice(df['PuzzleId'].tolist())

def puzzle_parser(puzzle_id):
    lichess_puzzle_url = f"https://lichess.org/api/puzzle/{puzzle_id}"
    response = requests.get(lichess_puzzle_url)
    if response.status_code == 200:
        puzzle_data = response.json()
        pgn = puzzle_data['game']['pgn']
        ply_moves = puzzle_data['puzzle']['initialPly']
        
        # Generate the FEN from the PGN and ply moves
        fen = get_puzzle_position(pgn, ply_moves)
        # Save the position as an image
        image_path = save_position_image(fen, f"chess_puzzle_{puzzle_id}.png")
        return image_path, puzzle_data
    else:
        print('Failed to retrieve the puzzle. Status code:', response.status_code)
        return None, None

# This part can remain if you want to be able to run puzzle_parser.py directly for testing
if __name__ == "__main__":
    puzzle_id = get_random_puzzle_id('chess_logic/puzzles/puzzles.csv')
    image_path, puzzle_data = puzzle_parser(puzzle_id)
    if image_path and puzzle_data:
        print('Puzzle image saved at:', image_path)
