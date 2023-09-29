# lib/helpers.py
import os

from models import Player, Score

def initialize():
    Player.create_table()
    Player.get_all()
    Score.create_table()
    Score.get_all()

def create_player():
    os.system('clear')
    print("Enter your name:")
    player_name = input("> ")
    while not player_name:
        print("Error: Name cannot be blank!")
        print("Enter your name:")
        player_name = input("> ")
    new_player = Player.create(player_name)
    print("Player successfully added!")
    print(new_player)
    keyboard_input = input("* Press any key and then press 'return' to continue *\n")
    return new_player

def get_all_players():
    os.system('clear')
    if len(Player.all) == 0:
        print("Error: There are no players in the database!")
        keyboard_input = input("* Press any key and then press 'return' to continue *\n")
    else:
        for player in Player.all:
            print(player)
        print("Successfully retrieved all player data!")
        keyboard_input = input("* Press any key and then press 'return' to continue *\n")

def get_player_by_id():
    os.system('clear')
    if len(Player.all) == 0:
        print("Error: There are no players in the database!")
        keyboard_input = input("* Press any key and then press 'return' to continue *\n")
    else:
        player = search_by_id('find')
        print()
        print(player)
        print()
        if len(player.scores) > 0:
            print("Here are the scores for this player:")
            for score in player.scores:
                print(score)
        else:
            print("This player has no scores.")
            keyboard_input = input("* Press any key and then press 'return' to continue *\n")
        print()
        print("Successfully retrieved player data!")
        keyboard_input = input("* Press any key and then press 'return' to continue *\n")


def delete_player():
    os.system('clear')
    if len(Player.all) == 0:
        print("Error: There are no players in the database!")
        keyboard_input = input("* Press any key and then press 'return' to continue *\n")
    else:
        player = search_by_id('delete')
        player.delete()
        print(f"Successfully deleted player!")
        keyboard_input = input("* Press any key and then press 'return' to continue *\n")

def search_by_id(word):
    os.system('clear')
    print(f"Enter the id for the player you want to {word}:")
    id = input("> ")
    
    if id.isdigit():
        player = Player.find_by_id(int(id))
    else:
        player = None
    
    while not player:
        print("Error: Player not found!")
        print(f"Enter the id for the player you want to {word}:")
        id = input("> ")

        if id.isdigit():
            player = Player.find_by_id(int(id))
        else:
            player = None

    return player

def exit_program():
    print("Goodbye!")
    exit()