'''
Simple example pokerbot, written in Python.
'''
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from skeleton.states import GameState, TerminalState, RoundState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot

import random
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

import p0, p1, p2
BOT_NAMES = ['Strong', 'Monte-Carlo', 'ABC']
BOT_LIST = [p0.Player, p1.Player, p2.Player]

class Player(Bot):
    '''
    A pokerbot.
    '''

    def __init__(self):
        '''
        Called when a new game starts. Called exactly once.

        Arguments:
        Nothing.

        Returns:
        Nothing.
        '''

        self.botnames = BOT_NAMES
        self.botlist = BOT_LIST
        self.n_bots = len(BOT_LIST)

        self.history = [] # array of delta histories for each bot
        self.score = [] # array of historical average deltas for each bot

        for i in range(self.n_bots):
            self.history.append([]) # initialize each history with empty list
            self.score.append(0) # initialize each score at 0

        self.current_bot = None
        self.current_bot_index = None

        self.chosen_bots = []# history of chosen bot over time for plotting

    def handle_new_round(self, game_state, round_state, active):
        '''
        Called when a new round starts. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        # if game_state.round_num <= 0.2 * NUM_ROUNDS: # biphasic approach
        if random.random() <= 0.2:      # epsilon greedy

            current_bot_index = np.random.randint(self.n_bots) # random bot
        else:
            current_bot_index = np.argmax(self.score) # empirically best bot

        self.current_bot_index = current_bot_index
        self.chosen_bots.append(current_bot_index)

        self.current_bot = self.botlist[current_bot_index]()
        self.current_bot.handle_new_round(game_state, round_state, active)

    def handle_round_over(self, game_state, terminal_state, active):
        '''
        Called when a round ends. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        terminal_state: the TerminalState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        
        my_delta = terminal_state.deltas[active]
        current_bot_history = self.history[self.current_bot_index]
        # update history and stats
        current_bot_history.append(my_delta)
        self.score[self.current_bot_index] = np.mean(current_bot_history)

        # visualize actions at end of match
        if game_state.round_num == NUM_ROUNDS:
            pass
            plt.figure(figsize=(10, 3))
            plt.scatter(range(NUM_ROUNDS), self.chosen_bots, marker="|", alpha=0.4)
            plt.xlabel("Step")
            plt.ylabel("Chosen Bot")
            plt.title("Bandit Bot: Chosen Bots Over Time")
            plt.yticks(range(self.n_bots), labels=[f"{self.botnames[i]}" for i in range(self.n_bots)])
            plt.savefig("../epsilon_greedy.png")

    def get_action(self, game_state, round_state, active):
        '''
        Where the magic happens - your code should implement this function.
        Called any time the engine needs an action from your bot.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Your action.
        '''
        return self.current_bot.get_action(game_state, round_state, active)

if __name__ == '__main__':
    run_bot(Player(), parse_args())