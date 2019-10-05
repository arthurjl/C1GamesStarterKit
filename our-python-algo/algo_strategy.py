import gamelib
import random
import math
import warnings
from sys import maxsize
import json


"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips: 

  - You can analyze action frames by modifying on_action_frame function

  - The GameState.map object can be manually manipulated to create hypothetical 
  board states. Though, we recommended making a copy of the map to preserve 
  the actual current map state.
"""

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        seed = random.randrange(maxsize)
        random.seed(seed)
        gamelib.debug_write('Random seed: {}'.format(seed))

    def on_game_start(self, config):
        """ 
        Read in config and perform any initial setup here 
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER
        FILTER = config["unitInformation"][0]["shorthand"]
        ENCRYPTOR = config["unitInformation"][1]["shorthand"]
        DESTRUCTOR = config["unitInformation"][2]["shorthand"]
        PING = config["unitInformation"][3]["shorthand"]
        EMP = config["unitInformation"][4]["shorthand"]
        SCRAMBLER = config["unitInformation"][5]["shorthand"]
        # This is a good place to do initial setup
        self.scored_on_locations = []

    
        

    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        game_state.enable_warnings = False

        self.static_defense(game_state)

        game_state.submit_turn()


    """
    NOTE: All the methods after this point are part of the sample starter-algo
    strategy and can safely be replaced for your custom algo.
    """

    def static_defense(self, game_state):
        filter_points = [[1, 13], [26, 13], [6, 13], [21, 13], [11, 13], [16, 13]]

        destructor_points = [[1, 12], [26, 12], [6, 12], [21, 12], [11, 12], [16, 12]]

        if game_state.turn_number > 1:
            filter_points.extend([[0, 13], [27, 13], [2, 13], [25, 13], [8, 13], [19, 13], [17, 13], [10, 13]])
            destructor_points.extend([[3, 13], [24, 13], [3, 12], [24, 12], [7, 12], [20, 12], [22, 12], [10, 12], [5, 12], [17, 1]])

        
        game_state.attempt_spawn(FILTER, filter_points)
                                  
        game_state.attempt_spawn(DESTRUCTOR, destructor_points)


        mid_filter_points = []
        for y in range(16, 10, -1):
            mid_filter_points.extend([[12, y], [15, y]])
        gamelib.debug_write(mid_filter_points)
        game_state.attempt_spawn(FILTER, mid_filter_points)

        # y - 11 to 16 x 11
        mid_destructor_points = []
        for y in range(16, 10, -1):
            mid_destructor_points.extend([[11, y], [16, y]])
        gamelib.debug_write(mid_destructor_points)
        game_state.attempt_spawn(DESTRUCTOR, mid_destructor_points)



if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
