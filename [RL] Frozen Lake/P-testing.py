import numpy as np
import gym
import time
import os

env = gym.make("FrozenLake-v1", is_slippery=False)
# CREATING Q-TABLE
q_table = np.loadtxt("q_table.csv", delimiter=",", dtype=float)

# DEFINE IMPORTANT VARIABLES
max_steps_per_episode = 100

for episode in range(3):
  state = env.reset()
  done = False
  time.sleep(1)

  for step in range(max_steps_per_episode):
    os.system("cls")
    env.render()
    time.sleep(0.1)
    
    action = np.argmax(q_table[state, :])
    new_state, reward, done, info = env.step(action)

    if done:
      os.system("cls")
      env.render()

      if reward == 1:
        print("###### YOU REACHED YOUR GOAL ######")
        time.sleep(3)
      else:
        print("###### YOU FALLEN TO A HOLE ######")
        time.sleep(3)
      
      os.system("cls")
      break
    
    state = new_state

env.close()

