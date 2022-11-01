from celery import Celery
import os
import yaml
import cfg

app = Celery(
    __name__,
    include=[
        'background_tasks.tasks',
    ],
)

app.conf.beat_schedule = {
    'process_round': {
        'task': 'background_tasks.tasks.process_round',
        'schedule': cfg.game_cfg()['round_time'],
    },
}

app.conf.update(cfg.celery_cfg())