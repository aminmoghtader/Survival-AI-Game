import gymnasium as gym
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from alien_env import AlienEnv  # محیط خودت

# محیط را در VecEnv قرار بده
env = DummyVecEnv([lambda: AlienEnv()])

# مدل ذخیره شده را بارگذاری کن
model = PPO.load("/home/am/Documents/AI/anaconda3/envs/ML/AI_Game/alien_ai_model.zip"
                 , env=env)

obs = env.reset()

done = False
while not done:
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)  # فقط ۴ مقدار unpack

    env.render()


env.close()