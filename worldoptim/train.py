import sys
sys.path.append('../')
from worldoptim.environments.models import get_model
from worldoptim.environments.cost_functions import get_cost_function
from worldoptim.environments.gym_envs import get_env
from worldoptim.optimization import get_algorithm
from worldoptim.configs.get_params import get_params
from worldoptim.utils import get_logdir, set_seeds
import argparse

CONFIG =  'nsga_ii_world2'  # 'nsga_ii', 'dqn', 'goal_dqn', 'goal_dqn_constraints'

def train(config, expe_name, trial_id, beta_default):
    """
    Main training script. Defines the cost function and epidemiological model to form the environment model.

    Parameters
    ----------
    config: str
        Identifier of the configuration parameters.
    expe_name: str
        String to describe your experiment, will be used for the logging directory.
    trial_id: int
        Trial identifier for logging path.
    beta_default: float
        Additional parameter for our experiments.

    """
    # Get the configuration
    params = get_params(config_id=config, expe_name=expe_name)
    params.update(trial_id=trial_id)
    params['cost_params']['beta_default'] = beta_default

    # Set seeds
    set_seeds(params['seed'])

    # Get the epidemiological model
    model = get_model(model_id=params['model_id'],
                        params=params['model_params'])

    # Update cost function params
    # here we have cost function parametres that depend on model variables.
    params['cost_params']['drn'] = model.initial_internal_params['DRN']

    # Get cost function
    cost_function = get_cost_function(cost_function_id=params['cost_id'],
                                      params=params['cost_params'])

    # Create the optimization problem as a Gym-like environment
    env = get_env(env_id=params['env_id'],
                  cost_function=cost_function,
                  model=model,
                  simulation_horizon=params['simulation_horizon'],
                  seed=params['seed'],
                  **params['env_params'])


    # Setup logdir
    params = get_logdir(params=params)

    # Get DQN algorithm parameterized by beta
    algorithm = get_algorithm(algo_id=params['algo_id'],
                              env=env,
                              params=params)

    # Run the training loop
    algorithm.learn(num_train_steps=params['num_train_steps'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    add = parser.add_argument
    add('--config', type=str, default=CONFIG, help='config id')
    add('--expe-name', type=str, default='', help='name of the experiment')
    add('--trial_id', type=int, default=1, help='trial identifier')
    add('--beta-default', type=float, default=0.5, help='default mixing param')
    kwargs = vars(parser.parse_args())
    train(**kwargs)
