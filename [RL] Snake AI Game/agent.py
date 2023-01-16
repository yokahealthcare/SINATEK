import gameAI
import pygame
import numpy as np
import os
import time
import pickle

# DEFINE IMPORTANT VARIABLES
num_episodes = 10000
max_steps_per_episode = 100000

learning_rate = 0.01
discount_rate = 0.999

# EPSILON
exploration_rate = 1
max_exploration_rate = 1
min_exploration_rate = 0.002
exploration_decay_rate = 0.005

# REWARDS
rewards_all_episodes = list()
scores_all_episodes = list()

# PROGRAM START HERE
menu = [
  "Use Latest Saved Model",
  "Train New One",
  "Exit"
]

os.system("cls")
print("====== SNAKE AI AGENT ======")
for n, i in enumerate(menu): print("[{}] {}".format(n+1, i))
inpt = int(input("\n>> "))

if inpt == 1:
  env = gameAI.SnakeGameAI(w=640, h=360, isDisplayed=True)
  filename = f"pickle/model.pickle"
  with open(filename, 'rb') as file:
    q_table = pickle.load(file)

  total_score = 0
  while True:
    state = env.get_state()
    action = np.argmax(q_table[state])
    new_state, reward, done, score = env.play_step(action)

    if done:
      print("\nGAME FINISHED!")
      print("Your score \t: {}".format(score))
      break


elif inpt == 2:
  num_episodes = int(input("\nNumber of Episodes to Train : "))
  env = gameAI.SnakeGameAI(w=640, h=360, isDisplayed=True)

  os.system("pause")
  # CREATING Q-TABLE
  q_table = np.zeros((2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3))

  # Q-LEARNING
  # SETTING FOR "PLOT AVG"
  elapsed = 0
  batch_size = 1000
  print("TRAINING...")
  for episode in range(num_episodes):
    env.gen = episode+1
    env.reset()
    state = env.get_state()

    print("\rEPISODE : {}".format(episode+1), end='')

    done = False
    rewards_current_episode = 0
    score_current_episode = 0


    for step in range(max_steps_per_episode):
      # Exploration - Exploitation Trade Off
      exploration_rate_threshold = np.random.uniform(0, 1)
      if exploration_rate_threshold > exploration_rate:
        # print("THINK ACTION")
        action = np.argmax(q_table[state])
      else:
        # print("RANDOM ACTION")
        action = np.random.randint(0, 3)

      new_state, reward, done, score = env.play_step(action)
    
      # Q-LEARNING ALGORITHM
      a = (1 - learning_rate) * q_table[state][action]
      b = learning_rate * (reward + discount_rate * np.max(q_table[new_state]))
      q_table[state][action] = a + b

      state = new_state
      rewards_current_episode += reward
      score_current_episode = score

      if done == True:
        break

    # EXPLORATION DECAY
    exploration_rate = min_exploration_rate + (max_exploration_rate-min_exploration_rate) * np.exp(-exploration_decay_rate*episode)
    rewards_all_episodes.append(rewards_current_episode)
    scores_all_episodes.append(score_current_episode)

    # PLOT AVG
    if episode % batch_size == 0 and episode != 0:
      success_ratio = np.around(sum(rewards_all_episodes[elapsed*batch_size:episode])/len(rewards_all_episodes), 3)
      print("\t({}% Success Rate)".format(success_ratio))
      time.sleep(0.5)
      elapsed += 1

    

  print("\n\nTRAINING FINISHED!")
  print("Number of Episodes \t: {}".format(num_episodes))
  print("Max Steps Per Episode \t: {}".format(max_steps_per_episode))
  success_ratio = np.around(sum(rewards_all_episodes[elapsed*batch_size:episode])/len(rewards_all_episodes), 3)
  print("\nFinal Success Rate \t: {}%".format(success_ratio))

  # Save The Model
  with open(f'pickle/model.pickle', 'wb') as file:
    pickle.dump(q_table, file)

  print("Model Has Been Saved!\n")
  os.system("pause")

elif inpt == 3:
  exit()

