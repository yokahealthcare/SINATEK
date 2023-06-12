import torch
from p_brain_pytorch import Linear_QNet
from p_snake_ai import SnakeGameAI
import os

model = Linear_QNet(15, 256, 3)

model.load_state_dict(torch.load("C:\\Users\\User\\Documents\\SINATEK\\[DRL] Snake AI Game\\model\\model.pth"))

model.eval()

game = SnakeGameAI(w=640, h=480, isDisplayed=True)

while True:

	current_state = torch.tensor(game.get_state(), dtype=torch.float)

	action = [0, 0, 0]
	move = torch.argmax(model(current_state)).item()
	action[move] = 1

	next_state, reward, game_over, score = game.play_step(action)

	if game_over:
		break

print("Final Score : {}".format(score))
