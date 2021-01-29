import Enviorment as ENV
import random
import numpy as np
from sklearn.neural_network import MLPClassifier
env = ENV.Enviorment(render=True)
r = 0
def relu(x):
    return (x > 0) * x
def sig(x):
     return 1/(1 + np.exp(-x))
def dimensionred(arr):
    lenarr = len(arr) ** 2
    arr = arr.reshape(lenarr)
    return arr 
class NN():
    def __init__(self, input_size, alpha):
        self.weights_0_1 = 2*np.random.random((input_size, 1500))
        self.weights_1_2 = 2*np.random.random((1500, 100))
        self.weights_2_3 = 2*np.random.random((100, 4))
        self.alpha = alpha
    def train(self,X,y,iterations):
        for i in range(iterations):
            layer_0 = X
            layer_1 = relu(np.dot(layer_0, self.weights_0_1))
            layer_2 = sig(np.dot(layer_1, self.weights_1_2))
            layer_3 = np.dot(layer_2, self.weights_2_3)
        print(layer_3)

clf = MLPClassifier(solver='lbfgs', alpha=0.001, hidden_layer_sizes=(20,10), random_state=1,max_iter=30000)
Y = []
X = []
X_train = []
Y_train = []
run = 0
rewards = []
while True:
    for i in range(500000):
        y = np.array([0,0,0,0])
        reward = env.get_reward()
        if reward == 1:
            X_train.extend(X)
            Y_train.extend(Y)
            print(i)
            r +=1
            X = []
            Y = []
        if reward == -1:
            X = []
            Y = []
        x = dimensionred(env.get_game_field())
        direction = random.randint(0,3)
        y[direction] = 1
        Y.append(y)
        X.append(x)
        env.move_snake(direction)
        env.kill_snake_after(22)

    total = 0
    clf.fit(X_train,Y_train)
    for i in range(500):
        
        x = dimensionred(env.get_game_field())
        y = clf.predict_proba([x])[0]
        direction = y.argmax()
        env.move_snake(direction)
        env.kill_snake_after(60)
        rew = env.get_reward()
        #env.render()
        if  rew == -1:
            env.create_apple()
        total += rew
    rewards.append(total)
    run += 1
    print("total_frames:", len(Y_train))
    print("total_reward:", rewards)
    print("Runs:", run)