def save_game(player):
    with open("saves/savefile.txt", "w") as file:
        file.write(f"{player.rect.x},{player.rect.y}")

def load_game(player):
    try:
        with open("saves/savefile.txt", "r") as file:
            x, y = map(int, file.read().split(","))
            player.rect.x = x
            player.rect.y = y
    except FileNotFoundError:
        pass
 