import arcade
import logging

from mqttclient import MQTTClient
from blinker import signal
import json

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = 'BoxingBet'

# Comment for production
logging.getLogger().setLevel(logging.INFO)

class Player:
    def __init__(self, sprite, pos_x, is_player):
        self.id = 0
        self.is_player = is_player
        self.name = 0
        self.scale = 0.5
        self.pos_x = pos_x
        self.player_sprite = arcade.Sprite(f'Assets/{sprite}.png', self.scale, flipped_horizontally=not is_player)
    
    def setup(self):
        self.player_sprite.center_x = self.pos_x
        self.player_sprite.center_y = 128

    def addToList(self, sprite_list):
        sprite_list.append(self.player_sprite)
    
    def update(self):
        self.player_sprite.center_x = self.pos_x


class Game(arcade.Window):
    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.player_list = []
        self.player_list.append(Player('Skin1/Idle1', 48, True))
        self.player_list.append(Player('Skin2/Idle1', 500, False))

    def setup(self):
        for player in self.player_list:
            player.setup()

    def on_draw(self):
        arcade.start_render()
        sprites = arcade.SpriteList()
        for player in self.player_list:
            player.addToList(sprites)
        sprites.draw()
        # Code to draw the screen goes here

    def on_key_press(self, key, modifiers):
        packet = {'topic': 'player/0', 'body': {'control': 'L'}}
        if key == arcade.key.LEFT or key == arcade.key.A:
            packet['body']['control'] = 'L'
            signal('message').send(packet)
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            packet['body']['control'] = 'R'
            signal('message').send(packet)
        elif key == arcade.key.C:
            # Connect, move within an input text menu
            connect_packet = {'topic': 'player/connection', 'body': {'name': 'Oreo'}}
            signal('message').send(connect_packet)

def main():
    # ---------------------------------
    # Initializing MQTT
    mqtt_client = MQTTClient(['debug/player'])
    mqtt_client.setup()
    mqtt_client.run()

    # ---------------------------------
    # Running game
    window = Game()
    window.setup()
    arcade.run()

    # ---------------------------------
    # Closing connection
    mqtt_client.stop()

if __name__ == "__main__":
    main()