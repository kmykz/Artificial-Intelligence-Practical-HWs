import gym
import gym_cityflow
import numpy as np
import matplotlib.pyplot as plt

EPISODES = 1000
EPSILON = 0.4
ALPHA = 0.99
GAMMA = 0.9
Q = {}
optimal_policy = {}


def bool_with_prob(prob):
    return np.random.rand() < prob


def best_action(state):
    if state not in Q:
        Q[state] = np.full(9, -50)
    return np.argmax(Q[state])


def update_Q(state, action, reward, new_state):
    if new_state not in Q:
        Q[new_state] = np.full(9, -50)
    Q[state][action] += ALPHA * (reward + GAMMA * np.max(Q[new_state]) - Q[state][action])


def simulate(env):
    obs = env.reset()
    done = False
    total_reward = 0
    turns = 0
    while not done:
        action = best_action(str(obs))
        obs, reward, done, info = env.step(action)
        total_reward += (GAMMA ** turns) * reward
        turns += 1
    return total_reward

if __name__ == "__main__":
    env = gym.make('gym_cityflow:CityFlow-1x1-LowTraffic-v0')

    rewards = []
    for _ in range(EPISODES):
        if _ % 150 == 0:
            EPSILON/=2
        obs = env.reset()
        done = False
        total_reward = 0
        action_rewards = []
        states = [obs]
        actions = []
        turns = 0
        while not done:
            if str(obs) not in Q:
                Q[str(obs)] = np.full(9, -50)
            if bool_with_prob(EPSILON):
                action = np.random.randint(0, 9)
            else:
                action = best_action(str(obs))
            actions.append(action)
            next_obs, reward, done, info = env.step(action)
            update_Q(str(obs), action, reward, str(next_obs))
            obs = next_obs
            states.append(obs)
            action_rewards.append(reward)
            total_reward += reward
            turns += 1
        rewards.append(simulate(env))
        if _ % 10 == 0:
            ALPHA *= 0.95

    plt.plot(rewards)
    plt.savefig("plot.png")
