import json
import os
import numpy as np
import random
from collections import OrderedDict

import rlohhell
from rlohhell.envs import Env
from rlohhell.games.ohhell import Game
from rlohhell.games.base import Card
from rlohhell.games.ohhell.utils import ACTION_SPACE, ACTION_LIST, cards2list

DEFAULT_GAME_CONFIG = {
        'game_num_players': 4,
        }

class OhHellEnv(Env):
    ''' OhHell Environment
    '''

    def __init__(self, config):
        ''' Initialize the Limitholdem environment
        '''
        self.name = 'ohhell'
        self.default_game_config = DEFAULT_GAME_CONFIG
        self.game = Game()
        super().__init__(config)
        self.state_shape = [[111] for _ in range(self.num_players)]
        self.action_shape = [None for _ in range(self.num_players)]

        with open(os.path.join(rlohhell.__path__[0], 'games/ohhell/card2index.json'), 'r') as file:
            self.card2index = json.load(file)


    def _extract_state(self, state):
        # obs = np.zeros((4, 4, 15), dtype=int)
        # encode_hand(obs[:3], state['hand'])
        # encode_trump_card(obs[3], state['trump_card'])
        # played_cards = state['played_cards']
        # hand = state['hand']
        # trump_card = state['trump_card']
        # tricks_won = state['tricks_won']
        # proposed_tricks = state['proposed_tricks']
        # players_tricks_won = state['players_tricks_won']
        
        # idx1 = [self.card2index[card] for card in played_cards]
        # idx2 = list(np.array([self.card2index[card] for card in hand]) + 51)
        
        # obs = np.zeros(111)
        # obs[idx1] = 1
        # obs[idx2] = 1
        # obs[104] = self.card2index[trump_card] 
        # obs[105] = tricks_won
        # obs[106] = proposed_tricks
        # obs[107:] = players_tricks_won

        
        # legal_action_id = self._get_legal_actions()
        # extracted_state = {'obs': obs, 'legal_actions': legal_action_id}


        # extracted_state['raw_obs'] = state
        # extracted_state['raw_legal_actions'] = [a for a in state['legal_actions']]
        # extracted_state['action_record'] = self.action_recorder
        # return extracted_state

        ''' get_state(player_id) is called on game and returns a dictonary with

        state['hand'] = [c.get_index() for c in players[player_id].hand]
        state['played_cards'] = [c.get_index() for c in self.played_cards]
        state['proposed_tricks'] = players[player_id].proposed_tricks
        state['tricks_won'] = players[player_id].tricks_won
        state['players_tricks_won'] = [player.tricks_won for player in players]
        state['legal_actions'] = self.get_legal_actions(players, player_id) 
        state['current_player'] = self.round.current_player
        state['trump_card'] = self.trump_card.get_index()
        state['previous_cards_played'] = [c.get_index() for c in self.previous_cards_played]


        get_index returns suit+rank for the card for instance S2 or SA 

        we can encode the information from this and return an extracted state, the previous version is above for tips.
        '''



    def _get_legal_actions(self):
        ''' Get all legal actions

        Returns:
            encoded_action_list (list): return encoded legal action list (from str to int)
        '''
        legal_actions = self.game.get_legal_actions()
        if self.game.round.players_proposed == self.game.num_players:
            legal_ids = {ACTION_SPACE[action.get_index()]: None for action in legal_actions}
        else:
            legal_ids = {ACTION_SPACE[str(action)]: None for action in legal_actions}
        return OrderedDict(legal_ids)

    def get_payoffs(self):
        ''' Get the payoff of a game

        Returns:
           payoffs (list): list of payoffs
        '''
        return self.game.get_payoffs()

    def _decode_action(self, action_id):
        legal_ids = self._get_legal_actions()
        if self.game.round.players_proposed == self.game.num_players:
            if action_id in list(legal_ids):
                return Card(ACTION_LIST[action_id][0], ACTION_LIST[action_id][1])
            else:
                random_card = ACTION_LIST[random.choice(list(legal_ids))]
                return Card(random_card[0], random_card[1])
        else:
            if action_id in list(legal_ids):
                return int(ACTION_LIST[action_id])
            else:
                return int(ACTION_LIST[random.choice(list(legal_ids))])

    def get_perfect_information(self):
        ''' Get the perfect information of the current state

        Returns:
            (dict): A dictionary of all the perfect information of the current state
        '''
        state = {}
        state['tricks_won'] = [self.game.players[i].tricks_won for i in range(self.num_players)]
        state['trump_card'] = self.game.trump_card
        state['played_cards'] = cards2list(self.game.round.played_cards)
        state['hand_cards'] = [[c.get_index() for c in self.game.players[i].hand] for i in range(self.num_players)]
        state['current_player'] = self.game.current_player
        state['legal_actions'] = self.game.get_legal_actions()
        return state



# config = {'game_num_players': 4, 'allow_step_back':False, 'seed':1}
# env = OhHellEnv(config)
# env.reset()
# env.game.round.players_proposed = 4
# env.game.players[0].has_proposed = True
# env.game.players[1].has_proposed = True
# env.game.players[2].has_proposed = True
# env.game.players[3].has_proposed = True

# print(env._get_legal_actions())
# env.game.current_player = 0

# print(env._get_legal_actions())
# print(type(env._decode_action(16)))

import gym
from gym.utils import seeding

class OhHellEnv2(gym.Env):


    def __init__(self):
        self.game = Game()
        self.game.init_game()
        self.seed()
        self.action_recorder = []
        self.timestep = 0

        self.observation_space = None
        self.action_space = ACTION_SPACE

        
        with open(os.path.join(rlohhell.__path__[0], 'games/ohhell/card2index.json'), 'r') as file:
            self.card2index = json.load(file)
    
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    
    def _extract_state(self, state):
        # obs = np.zeros((4, 4, 15), dtype=int)
        # encode_hand(obs[:3], state['hand'])
        # encode_trump_card(obs[3], state['trump_card'])
        # played_cards = state['played_cards']
        # hand = state['hand']
        # trump_card = state['trump_card']
        # tricks_won = state['tricks_won']
        # proposed_tricks = state['proposed_tricks']
        # players_tricks_won = state['players_tricks_won']
        
        # idx1 = [self.card2index[card] for card in played_cards]
        # idx2 = list(np.array([self.card2index[card] for card in hand]) + 51)
        
        # obs = np.zeros(111)
        # obs[idx1] = 1
        # obs[idx2] = 1
        # obs[104] = self.card2index[trump_card] 
        # obs[105] = tricks_won
        # obs[106] = proposed_tricks
        # obs[107:] = players_tricks_won

        
        # legal_action_id = self._get_legal_actions()
        # extracted_state = {'obs': obs, 'legal_actions': legal_action_id}


        # extracted_state['raw_obs'] = state
        # extracted_state['raw_legal_actions'] = [a for a in state['legal_actions']]
        # extracted_state['action_record'] = self.action_recorder
        # return extracted_state

        ''' get_state(player_id) is called on game and returns a dictonary with

        state['hand'] = [c.get_index() for c in players[player_id].hand]
        state['played_cards'] = [c.get_index() for c in self.played_cards]
        state['proposed_tricks'] = players[player_id].proposed_tricks
        state['tricks_won'] = players[player_id].tricks_won
        state['players_tricks_won'] = [player.tricks_won for player in players]
        state['legal_actions'] = self.get_legal_actions(players, player_id) 
        state['current_player'] = self.round.current_player
        state['trump_card'] = self.trump_card.get_index()
        state['previous_cards_played'] = [c.get_index() for c in self.previous_cards_played]


        get_index returns suit+rank for the card for instance S2 or SA 

        we can encode the information from this and return an extracted state, the previous version is above for tips.
        '''

    
    def reset(self):
        ''' Start a new game

        Returns:
            (tuple): Tuple containing:

                (numpy.array): The begining state of the game
                (int): The begining player
        '''
        state, player_id = self.game.init_game()
        self.action_recorder = []
        return self._extract_state(state), player_id


    def _decode_action(self, action_id):
        legal_ids = self._get_legal_actions()
        if self.game.round.players_proposed == self.game.num_players:
            if action_id in list(legal_ids):
                return Card(ACTION_LIST[action_id][0], ACTION_LIST[action_id][1])
            else:
                random_card = ACTION_LIST[random.choice(list(legal_ids))]
                return Card(random_card[0], random_card[1])
        else:
            if action_id in list(legal_ids):
                return int(ACTION_LIST[action_id])
            else:
                return int(ACTION_LIST[random.choice(list(legal_ids))])

    
    def step(self, action, raw_action=False):
        ''' Step forward

        Args:
            action (int): The action taken by the current player
            raw_action (boolean): True if the action is a raw action

        Returns:
            (tuple): Tuple containing:

                (dict): The next state
                (int): The ID of the next player
        '''
        if not raw_action:
            action = self._decode_action(action)

        self.timestep += 1
        # Record the action for human interface
        self.action_recorder.append((self.get_player_id(), action))
        next_state, player_id = self.game.step(action)

        return self._extract_state(next_state), player_id


    def _get_legal_actions(self):
        ''' Get all legal actions

        Returns:
            encoded_action_list (list): return encoded legal action list (from str to int)
        '''
        legal_actions = self.game.get_legal_actions()
        if self.game.round.players_proposed == self.game.num_players:
            legal_ids = {ACTION_SPACE[action.get_index()]: None for action in legal_actions}
        else:
            legal_ids = {ACTION_SPACE[str(action)]: None for action in legal_actions}
        return OrderedDict(legal_ids)
