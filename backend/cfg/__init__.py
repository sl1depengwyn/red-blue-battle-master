import os
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, 'cfg', 'config.yml')

MAIN_CFG = yaml.load(open(CONFIG_PATH), Loader=yaml.FullLoader)

def db_cfg():
    return MAIN_CFG['db']

def game_cfg():
    return MAIN_CFG['game']

def celery_cfg():
    return MAIN_CFG['celery']

def team_cfg():
    return MAIN_CFG['team']

def task_cfg():
    return MAIN_CFG['tasks']
