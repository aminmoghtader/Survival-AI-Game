import time
from alien_env import AlienEnv

env = AlienEnv(render_mode="human")

obs, info = env.reset()

done = False
while not done:
    action = env.action_space.sample()  # حرکت تصادفی
    obs, reward, terminated, truncated, info = env.step(action)
    env.render()  # صفحه را رندر می‌کنیم
    time.sleep(0.03)  # FPS حدود 30
    done = terminated or truncated

env.close()
