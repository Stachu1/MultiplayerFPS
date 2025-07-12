import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from Game.Game import Game


class Client:
    def __init__(self):
        self.game = Game()
    
    def run(self):
        self.game.run()


if __name__ == "__main__":
    client = Client()
    client.run()