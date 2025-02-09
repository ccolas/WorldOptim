from gym.envs.registration import register
from worldoptim.environments.gym_envs.get_env import get_env

register(id='EpidemicDiscrete-v0',
         entry_point='worldoptim.environments.gym_envs.epidemic_discrete:EpidemicDiscrete')

register(id='World2Discrete-v0',
         entry_point='worldoptim.environments.gym_envs.world2_discrete:World2Discrete')