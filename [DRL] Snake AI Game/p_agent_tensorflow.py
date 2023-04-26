import numpy as np
from p_brain_tensorflow import Brain
from p_dqn_tensorflow import Dqn
from p_snake_ai import SnakeGameAI
import tensorflow as tf
import random

tf.keras.utils.disable_interactive_logging()

# DEFINE IMPORTANT VARIABLES
max_memory = 100_000

learning_rate = 0.01
discount_rate = 0.999
batch_size = 1000

# EPSILON
epsilon = 0

game = SnakeGameAI(w=640, h=480, isDisplayed=True)
model = Brain(11, 3, learning_rate).model()
dqn = Dqn(max_memory, discount_rate)

def show_debug_information(current_state, action, reward, next_state, game_over, score):
    print("---------- Game Debug Information ----------")
    print("Score \t\t: {}".format(score))
    print("Epsilon \t: {}".format(epsilon))

    print("---------- State Debug Information ----------")
    print("Current State \t: {}".format(current_state))
    print("Action \t\t: {}".format(action))
    print("Reward \t\t: {}".format(reward))
    print("Next State \t: {}".format(next_state))
    print("Game Over \t: {}".format(game_over))

    print("---------- Memory Debug Information ----------") 
    print("Memory Length : {}".format(len(dqn.memory)))
    # print("Memory Content:")
    # print(self.memory)

    print()

n_games = 0
while True:
    game.gen = n_games
    current_state = game.get_state()
    next_state = current_state           
    
    # ACTION TAKER
    action = [0, 0, 0]
    epsilon = 80 - n_games

    if random.randint(0, 200) > epsilon:
        # MACHINE IS THINKING
        action_prediction = model.predict(current_state)[0]
        move = np.argmax(action_prediction).item()
        action[move] = 1
    else:
        # MACHINE IS RANDOM
        move = np.random.randint(0, 3)
        action[move] = 1

    # PLAY
    next_state, reward, game_over, score = game.play_step(action)

    dqn.remember([current_state, action, reward, next_state], game_over)
    
    # UPDATE THE current_state
    current_state = next_state

    if game_over:
        game.reset()
        n_games += 1

        # AI
        inputs, targets = dqn.getBatches(model, batch_size)
        model.train_on_batch(inputs, targets)
        show_debug_information(current_state, action, reward, next_state, game_over, score)
