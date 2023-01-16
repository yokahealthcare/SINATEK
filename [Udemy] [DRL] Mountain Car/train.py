#Mountain Car: Deep Q-Learning - Training 

# PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

#Importing the libraries
from dqn import Dqn
from brain import Brain
import gym
import numpy as np
import matplotlib.pyplot as plt

#Setting the parameters
learningRate = 0.001
maxMemory = 50000
gamma = 0.9
batchSize = 32
epsilon = 1.
epsilonDecayRate = 0.995

#Initializing the Environment, the Brain and the Experience Replay Memory
env = gym.make('MountainCar-v0')
brain = Brain(2, 3, learningRate)
model = brain.model
DQN = Dqn(maxMemory, gamma)

#Starting the main loop
epoch = 0
currentState = np.zeros((1, 2))
nextState = currentState
totReward = 0
rewards = list()
while True:
     epoch += 1
     
     #Starting to play the game
     env.reset()
     currentState = np.zeros((1, 2))
     nextState = currentState
     gameOver = False
     while not gameOver:
          
          #Taking an action
          if np.random.rand() <= epsilon:
               action = np.random.randint(0, 3)
          else:
               qvalues = model.predict(currentState)[0]
               action = np.argmax(qvalues)
          
          #Updating the Environment
          nextState[0], reward, gameOver, _ = env.step(action)
          env.render()
          
          totReward += reward
          
          #Remembering new experience, training the AI and updating current state
          DQN.remember([currentState, action, reward, nextState], gameOver)
          inputs, targets = DQN.getBatch(model, batchSize)
          model.train_on_batch(inputs, targets)
          
          currentState = nextState
     
     #Lowering epsilon and displaying the results
     epsilon *= epsilonDecayRate
     
     print('Epoch: ' + str(epoch) + ' Epsilon: {:.5f}'.format(epsilon) + ' Total Reward: {:.2f}'.format(totReward))
     
     rewards.append(totReward)
     totReward = 0
     """
     plt.plot(rewards)
     plt.xlabel('Epoch')
     plt.ylabel('Rewards')
     plt.show()
     """

env.close()
