#A Better Maze: Q-Learning - Environment file

import numpy as np
import pygame as pg
import sys

class Environment():
    
    def __init__(self):
        
        self.cellWidth = 100
        self.cellHeight = 100
        self.nRows = 3
        self.nColumns = 3
        self.rewards = [-3, -10, 1000, -20000, -20]
        
        for reward in self.rewards:
            if reward == 0:
                sys.exit('Reward can not be equal to 0!')
                
        self.width = self.nColumns * self.cellWidth
        self.height = self.nRows * self.cellHeight
        
        self.nObjects = len(self.rewards)
        
        self.screen = pg.display.set_mode((self.width, self.height))
        
        
        self.rewardBoard = np.zeros((self.nRows*self.nColumns, self.nRows*self.nColumns))
        self.maze = np.zeros((self.nRows, self.nColumns))
        
        self.sprites = list()
        
        #Required Sprites
        self.loadSprite('Player.png')
        self.loadSprite('Wall.png')
        self.loadSprite('Finish.png')
        
        #Additional Sprites
        self.loadSprite('Fire.png')
        self.loadSprite('Water.png')
        
        
        
        self.startingPos = -1
        self.playerPos = -1
        self.place = np.zeros((self.nObjects))
        
        self.edit()
        
        
    
    def loadSprite(self, path):
        sprite = pg.image.load(path)
        sprite = pg.transform.smoothscale(sprite, (self.cellWidth, self.cellHeight))
        self.sprites.append(sprite)
        
    def edit(self):
        print('You have entered edit mode')
        playerPlaced = False
        finishPlaced = 0
        while True:
            #1 = Player
            #2 = Wall
            #3 = Finish
            #4 = Fire
            #5 = Water
            position = pg.mouse.get_pos()
            posx = int(position[0] / self.cellWidth)
            posy = int(position[1] / self.cellHeight)
            inxToDraw = -1
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN and finishPlaced > 0 and playerPlaced:
                        self.fillRBoard()
                        print('You have exited edit mode')
                        return
                    elif event.key == pg.K_d:
                        self.place = np.zeros((self.nObjects))
                        inxToDraw = -1
                        if self.maze[posy][posx] == 1:
                            playerPlaced = False
                            self.playerPos = -1
                        elif self.maze[posy][posx] == 3:
                            finishPlaced -= 1
                        self.maze[posy][posx] = 0
                    elif event.key == pg.K_1 and not playerPlaced:
                        self.place = np.zeros((self.nObjects))
                        self.place[0] = 1
                    elif event.key == pg.K_2:
                        self.place = np.zeros((self.nObjects))
                        self.place[1] = 1
                    elif event.key == pg.K_3:
                        self.place = np.zeros((self.nObjects))
                        self.place[2] = 1
                    elif event.key == pg.K_4:
                        self.place = np.zeros((self.nObjects))
                        self.place[3] = 1
                    elif event.key == pg.K_5:
                        self.place = np.zeros((self.nObjects))
                        self.place[4] = 1
                elif event.type == pg.MOUSEBUTTONDOWN:
                    for i in range(len(self.place)):
                        b = self.place[i]
                        if b:
                            self.maze[posy][posx] = i + 1
                            if i == 0:
                                playerPlaced = True
                                self.startingPos = posy*self.nColumns + posx
                                self.playerPos = self.startingPos
                            elif i == 2:
                                finishPlaced += 1
            
            for i in range(len(self.place)):
                if self.place[i]:
                    inxToDraw = i        
                    
            if playerPlaced and inxToDraw == 0:
                inxToDraw = -1
                self.place[0] = 0
                
            self.drawScreen(inxToDraw, position)
    
    def fillRBoard(self):
        for i in range(self.nRows):
            for j in range(self.nColumns):
                state = i*self.nColumns + j
                if i > 0: #UP
                    k = int(self.maze[i - 1][j])
                    if k == 0:
                        self.rewardBoard[state][state - self.nColumns] = self.rewards[0]
                    elif k == 2:
                        if self.maze[i][j] == 0 or self.maze[i][j] == 2 or self.maze[i][j] == 1:
                            self.rewardBoard[state][state] = self.rewards[1]
                        elif self.maze[i][j] != 1:
                            self.rewardBoard[state][state] = self.rewards[int(self.maze[i][j]) - 1]
                    elif k != 1:
                        self.rewardBoard[state][state - self.nColumns] = self.rewards[k - 1]
                else:
                    if self.maze[i][j] == 0 or self.maze[i][j] == 2 or self.maze[i][j] == 1:
                        self.rewardBoard[state][state] = self.rewards[1]
                    elif self.maze[i][j] != 1:
                        self.rewardBoard[state][state] = self.rewards[int(self.maze[i][j]) - 1]
                    
                    
                
                if i < self.nRows - 1:
                    k = int(self.maze[i + 1][j])
                    if k == 0:
                        self.rewardBoard[state][state + self.nColumns] = self.rewards[0]
                    elif k == 2:
                        if self.maze[i][j] == 0 or self.maze[i][j] == 2 or self.maze[i][j] == 1:
                            self.rewardBoard[state][state] = self.rewards[1]
                        elif self.maze[i][j] != 1:
                            self.rewardBoard[state][state] = self.rewards[int(self.maze[i][j]) - 1]
                    elif k != 1:
                        self.rewardBoard[state][state + self.nColumns] = self.rewards[k - 1]
                else:
                    if self.maze[i][j] == 0 or self.maze[i][j] == 2 or self.maze[i][j] == 1:
                        self.rewardBoard[state][state] = self.rewards[1]
                    elif self.maze[i][j] != 1:
                        self.rewardBoard[state][state] = self.rewards[int(self.maze[i][j]) - 1]
                
                if j > 0:
                    k = int(self.maze[i][j - 1])
                    if k == 0:
                        self.rewardBoard[state][state - 1] = self.rewards[0]
                    elif k == 2:
                        if self.maze[i][j] == 0 or self.maze[i][j] == 2 or self.maze[i][j] == 1:
                            self.rewardBoard[state][state] = self.rewards[1]
                        elif self.maze[i][j] != 1:
                            self.rewardBoard[state][state] = self.rewards[int(self.maze[i][j]) - 1]
                    elif k != 1:
                        self.rewardBoard[state][state - 1] = self.rewards[k - 1]
                else:
                    if self.maze[i][j] == 0 or self.maze[i][j] == 2 or self.maze[i][j] == 1:
                        self.rewardBoard[state][state] = self.rewards[1]
                    elif self.maze[i][j] != 1:
                        self.rewardBoard[state][state] = self.rewards[int(self.maze[i][j]) - 1]
                
                if j < self.nColumns - 1:
                    k = int(self.maze[i][j + 1])
                    if k == 0:
                        self.rewardBoard[state][state + 1] = self.rewards[0]
                    elif k == 2:
                        if self.maze[i][j] == 0 or self.maze[i][j] == 2 or self.maze[i][j] == 1:
                            self.rewardBoard[state][state] = self.rewards[1]
                        elif self.maze[i][j] != 1:
                            self.rewardBoard[state][state] = self.rewards[int(self.maze[i][j]) - 1]
                    elif k != 1:
                        self.rewardBoard[state][state + 1] = self.rewards[k - 1]
                else:
                    if self.maze[i][j] == 0 or self.maze[i][j] == 2 or self.maze[i][j] == 1:
                        self.rewardBoard[state][state] = self.rewards[1]
                    elif self.maze[i][j] != 1:
                        self.rewardBoard[state][state] = self.rewards[int(self.maze[i][j]) - 1]
        
        for i in range(self.nRows):
            for j in range(self.nColumns):
                if self.maze[i][j] == 2:
                    self.rewardBoard[i*self.nColumns + j] = np.zeros((self.nRows * self.nColumns))
        
        self.drawScreen(-1, (0,0))
    
    def movePlayer(self, nextPos):
        self.playerPos = nextPos
        self.drawScreen(-1, (0,0))
        
        for event in pg.event.get():
           if event.type == pg.QUIT:
               exit()
                    
        pg.time.wait(400)
    
    def drawScreen(self, inx, pos):
        self.screen.fill((255,255,255))
        
        for i in range(self.nRows):
            for j in range(self.nColumns):
                if self.maze[i][j] > 0 and self.maze[i][j] != 1:
                    self.screen.blit(self.sprites[int(self.maze[i][j]) - 1], (j*self.cellWidth, i*self.cellHeight))
                    
        if self.playerPos != -1:        
            self.screen.blit(self.sprites[0], ((self.playerPos % self.nColumns) * self.cellWidth, int(self.playerPos / self.nColumns) * self.cellHeight))
            
        for i in range(1, self.nRows):
            pg.draw.line(self.screen, (0,0,0), (0, i*self.cellHeight), (self.width, i*self.cellHeight))
        
        for i in range(1, self.nColumns):
            pg.draw.line(self.screen, (0,0,0), (i*self.cellWidth, 0), (i*self.cellWidth, self.height))
        
        if inx >= 0:
            self.screen.blit(self.sprites[inx], (pos[0] - self.cellWidth/2, pos[1] - self.cellHeight/2))
        
        pg.display.flip()
                               
                    
        
if __name__ == '__main__':
    env = Environment()