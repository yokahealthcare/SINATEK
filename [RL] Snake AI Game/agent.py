import gameAI
import pygame
import numpy as np
import os

env = gameAI.SnakeGameAI()
# GAME CONFIGURATION
BLOCK_SIZE = 20

# CREATING Q-TABLE
q_table = np.zeros((2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3))

# DEFINE IMPORTANT VARIABLES
num_episodes = 10000
max_steps_per_episode = 100

learning_rate = 0.1
discount_rate = 0.99

# EPSILON
exploration_rate = 1
max_exploration_rate = 1
min_exploration_rate = 0.01
exploration_decay_rate = 0.001

# Q-TRAINING
rewards_all_episodes = list()
print("TRAINING...")
for episode in range(num_episodes):
  state = env.reset()
  done = False
  rewards_current_episode = 0

  for step in range(max_steps_per_episode):
    # Exploration - Exploitation Trade Off
    exploration_rate_threshold = np.random.uniform(0, 1)
    if exploration_rate_threshold > exploration_rate:
      action = np.argmax(q_table[state, :])
    else:
      action = np.random.randint(0, 3)

    new_state, reward, done, info = env.play_step(action)
  
    # Q-LEARNING ALGORITHM
    q_table[state, action] =  (1 - learning_rate) * q_table[state, action] + learning_rate * (reward + discount_rate * np.max(q_table[new_state, :]))

    state = new_state
    rewards_current_episode += reward

    if done == True:
      break
  
  # PLOT AVG
  if episode % 1000 == 0 and episode != 0:
    success_ratio = np.around(np.average(rewards_all_episodes), 3)
    success_percentage = np.around(success_ratio*100, 3)
    print("\n\nEpisodes {}:\n{} \t({}% Success Rate)".format(episode, success_ratio, success_percentage))
    time.sleep(5)

  # EXPLORATION DECAY
  exploration_rate = min_exploration_rate + (max_exploration_rate-min_exploration_rate) * np.exp(-exploration_decay_rate*episode)

  rewards_all_episodes.append(rewards_current_episode)

print("TRAINING FINISHED!")
print("Number of Episodes \t: {}".format(num_episodes))
print("Max Steps Per Episode \t: {}".format(max_steps_per_episode))
success_ratio = np.around(np.average(rewards_all_episodes), 3)
success_percentage = np.around(success_ratio*100, 3)
print("\nSuccess Rate \t: {}%".format(success_percentage))


