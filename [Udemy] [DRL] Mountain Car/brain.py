#Mountain Car: Deep Q-Learning: Brain file

#Importing the libraries
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

#Building the Brain class
class Brain():
     
     def __init__(self, numInputs, numOutputs, lr):
          self.numInputs = numInputs
          self.numOutputs = numOutputs
          self.learningRate = lr
          
          #Creating the neural network
          self.model = Sequential()
          
          self.model.add(Dense(units = 32, activation = 'relu', input_shape = (self.numInputs, )))
          
          self.model.add(Dense(units = 16, activation = 'relu'))
          
          self.model.add(Dense(units = self.numOutputs))
          
          self.model.compile(optimizer = Adam(lr = self.learningRate), loss = 'mean_squared_error')

     



        
    