import logging

from gym_http_client import Client

class RandomDiscreteAgent(object):
    def __init__(self, n):
        self.n = n

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)

    # Set up client
    remote_base = 'http://127.0.0.1:5000'
    client = Client(remote_base)

    # Set up environment
    env_id = 'CartPole-v0'
    instance_id = client.env_create(env_id, 0)

    # Set up agent
    action_space_info = client.env_action_space_info(instance_id)
    agent = RandomDiscreteAgent(action_space_info['n'])

    # Run experiment, with monitor
    outdir = '/tmp/random-agent-results'
    client.env_monitor_start(instance_id, outdir, force=True, resume=False, video_callable=False)
    
    episode_count = 100
    max_steps = 200
    reward = 0
    done = False

    for i in range(episode_count):
        ob = client.env_reset(instance_id)

        for j in range(max_steps):
            action = client.env_action_space_sample(instance_id)
            ob, reward, done, _ = client.env_step(instance_id, action, render=True)
            if done:
                break

    # Dump result info to disk
    client.env_monitor_close(instance_id)
