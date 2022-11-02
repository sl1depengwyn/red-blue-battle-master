import yaml
import sys
import os
import shutil
import subprocess
import virtualenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def setup_db(config):
    postgres_env_path = os.path.join(
        BASE_DIR,
        'docker_cfg',
        'postgres',
        'postgres_env.env',
    )
    db_config = config['db']['postgres']
    postgres_host = db_config['host']
    postgres_port = db_config['port']
    postgres_user = db_config['user']
    postgres_password = db_config['password']
    postgres_db = db_config['name']

    postgres_config = [
        'POSTGRES_HOST={postgres_host}'.format(postgres_host=postgres_host),
        'POSTGRES_PORT={postgres_port}'.format(postgres_port=postgres_port),
        'POSTGRES_USER={postgres_user}'.format(postgres_user=postgres_user),
        'POSTGRES_PASSWORD={postgres_password}'.format(postgres_password=postgres_password),
        'POSTGRES_DB={postgres_db}'.format(postgres_db=postgres_db),
    ]

    with open(postgres_env_path, 'w') as f:
        f.write('\n'.join(postgres_config))

def setup_flower(config):
    flower_env_path = os.path.join(
        BASE_DIR,
        'docker_cfg',
        'flower',
        'flower_env.env',
    )

    flower_username = config['flower']['username']
    flower_password = config['flower']['password']
    flower_config = [
        'FLOWER_BASIC_AUTH={flower_username}:{flower_password}'.format(
            flower_username=flower_username,
            flower_password=flower_password,
        ),
    ]

    with open(flower_env_path, 'w') as f:
        f.write('\n'.join(flower_config))

def create_env(config):
    conf_path = os.path.join(BASE_DIR, 'config.yml')
    config = yaml.load(open(conf_path), Loader=yaml.FullLoader)
    env_path = os.path.join(BASE_DIR, 'checkers/', 'checker_venv/')
    if not os.path.exists(env_path):
        virtualenv.create_environment(env_path)
    if os.path.exists(os.path.join(BASE_DIR, 'checkers/', 'requirements.txt')):
        cmd = f"source {env_path}/bin/activate && pip install -r {os.path.join(BASE_DIR, 'checkers/', 'requirements.txt')}"
        os.system(cmd)

def setup_config():
    conf_path = os.path.join(BASE_DIR, 'config.yml')
    config = yaml.load(open(conf_path), Loader=yaml.FullLoader)
    setup_db(config)
    setup_flower(config)
    create_env(config)

def clear_db():
    data_path = os.path.join(BASE_DIR, 'docker_volumes/postgres')
    shutil.rmtree(data_path)

    subprocess.check_output(
        ['docker-compose', 'down', '-v', '--remove-orphans'],
        cwd=BASE_DIR,
    )

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'setup':
            setup_config()
        elif sys.argv[1] == 'clear':
            clear_db()
        else:
            exit(1)
    else:
        exit(1)
