import chess.pgn
import os
import requests
from io import StringIO

def get_puzzle_position(pgn_text, ply_count):
    pgn = StringIO(pgn_text)
    game = chess.pgn.read_game(pgn)

    board = game.board()
    for move in game.mainline_moves():
        board.push(move)
        if board.fullmove_number * 2 - (2 if board.turn == chess.BLACK else 1) > ply_count:
            break

    return board.fen()

def save_position_image(fen, image_filename):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    image_directory = os.path.join(current_directory, 'puzzle_images')
    
    # Check if the directory exists, if not create it
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)
    
    image_path = os.path.join(image_directory, image_filename)
    url = f"https://fen2image.chessvision.ai/{fen}"
    response = requests.get(url)

    if response.status_code == 200:
        with open(image_path, "wb") as file:
            file.write(response.content)
        print(f"Image saved as {image_path}")
    else:
        print(f"Failed to retrieve the image. Status code: {response.status_code}")
