from celery import shared_task, chain
from celery.signals import worker_ready
from celery.utils.log import get_task_logger
from .checker import run_check, run_get, run_put, task_status
import requests
import db
import cfg
import secrets
import random

@shared_task
def check_action(task_id, round):
    team = db.models.Team.select().where(db.models.Team.type == 'blue').first()
    task = db.models.Task.select().where(db.models.Task.id == task_id).first()

    tmp_verdict = db.models.Check.create(
        status=task_status('CHECKER_ERROR'),
        task=task,
        error='Check pending',
        message='',
        command='check',
        round=round
    )

    checker_verdict = run_check(checker_path=task.checker,host=team.ip,timeout=task.timeout, round=round)

    tmp_verdict.status = checker_verdict.status
    task.status = checker_verdict.status
    tmp_verdict.save()
    task.save()
    game = db.models.Game.select().first()
    if task.status == task_status('UP'):
        game.score += 20
    elif task.status == task_status('CORRUPT') or task.status == task_status('MUMBLE'):
        game.score += 5
    else:
        game.score -= 5
    game.save()

    return checker_verdict.status == task_status('UP')


@shared_task
def put_action(check_ok, task_id, round):

    if not check_ok:
        return False

    team = db.models.Team.select().where(db.models.Team.type == 'blue').first()
    task = db.models.Task.select().where(db.models.Task.id == task_id).first()

    ok = True
    for i in range(task.puts):
        flag = 'CTF'+secrets.token_hex(20)
        vuln = secrets.choice(range(1, task.vulns + 1))
        checker_verdict, flag_id = run_put(
            checker_path=task.checker,
            host=team.ip,
            vuln=task.vulns,
            flag=flag,
            timeout=task.timeout,
            round=round,
        )

        if checker_verdict.status == task_status('UP'):
            flag = db.models.Flag.create(flag=flag, flag_id=flag_id, vuln=vuln, task=task, round=round)
        else:
            task.status = checker_verdict.status
            task.save()
            game = db.models.Game.select().first()
            if task.status == task_status('UP'):
                game.score += 20
            elif task.status == task_status('CORRUPT') or task.status == task_status('MUMBLE'):
                game.score += 5
            else:
                game.score -= 5
            db.models.Check.create(status=checker_verdict.status, task=task, command='put', message=checker_verdict.message, error=checker_verdict.error, round=round)
            ok = False
            break

    return ok


@shared_task
def get_action(put_ok, task_id, round):
    if not put_ok:
        return False

    team = db.models.Team.select().where(db.models.Team.type == 'blue').first()
    task = db.models.Task.select().where(db.models.Task.id == task_id).first()

    rounds_to_check = list(x for x in range(round-task.gets,round) if x >= 1)

    checker_verdict = db.models.Check.create(
        status=task_status('UP'),
        message='',
        error='',
        command='get',
        task=task,
        round=round
    )

    for get_round in rounds_to_check:
        flag = random.choice(db.models.Flag.select().where(
            task=task,
            round=get_round,
        ))

        if not flag:
            checker_verdict.status = task_status('CORRUPT')
            checker_verdict.error = f'No flags from round {get_round}'
            checker_verdict.message = f'Could not get flag from round {get_round}'
            checker_verdict.save()
        else:
            checker_verdict = run_get(
                checker_path=task.checker,
                host=team.ip,
                flag=flag,
                timeout=task.checker_timeout,
                round=round
            )

        if checker_verdict.status != task_status('UP'):
            break
    task.status = checker_verdict.status
    task.save()

    game = db.models.Game.select().first()
    if task.status == task_status('UP'):
        game.score += 20
    elif task.status == task_status('CORRUPT') or task.status == task_status('MUMBLE'):
        game.score += 5
    else:
        game.score -= 5

    return checker_verdict.status == task_status('UP')

@worker_ready.connect
def startup(**_kwargs):
    db.models.db.create_tables([db.models.Check, db.models.Flag, db.models.Game, db.models.Submit, db.models.Task, db.models.Team])
    if db.models.Game.select().count() == 0:
        db.models.Game.create(running=False, score=0, round=0)
    if db.models.Team.select().count() == 0:
        teams = cfg.team_cfg()
        for team in teams:
            db.models.Team.create(name=team['name'], type=team['type'], ip=team['ip'])
    if db.models.Task.select().count() == 0:
        tasks = cfg.task_cfg()
        for task in tasks:
            db.models.Task.create(name=task['name'], checker=task['checker'], gets=task['gets'], puts=task['puts'], vulns=task['vulns'], timeout=task['timeout'], status=104)
        
    start_game.apply_async(eta=cfg.game_cfg()['start_time'])

@shared_task
def start_game():
    game = db.models.Game.select().first()

    if game:
        game.running = True
        game.save()

@shared_task
def process_round():
    game = db.models.Game.select().first()
    
    if not game.running:
        return 
    
    tasks = db.models.Task.select()

    for task in tasks:
        c = chain(check_action.s(task.id, game.round), put_action.s(task.id, game.round), get_action.s(task.id, game.round)).apply_async()
    
    game.round += 1
    game.save()