from stable_baselines3 import PPO
from alien_env import AlienEnv

env = AlienEnv()

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100000)  # تعداد فریم‌های آموزش
model.save("/home/am/Documents/AI/anaconda3/envs/ML/AI_Game/alien_ai_model")
