from peewee import Model, CharField, ForeignKeyField, IntegerField, BooleanField, IPField, DateTimeField, PostgresqlDatabase, TextField
import datetime
import cfg

db_data = cfg.db_cfg()['postgres']
db = PostgresqlDatabase(db_data['name'], user=db_data['user'], password=db_data['password'], host=db_data['host'], port=db_data['port'])

class BaseModel(Model):
    class Meta:
        database = db

class Game(BaseModel):
    running = BooleanField(default=False)
    score = IntegerField(default=0)
    round = IntegerField(default=0)

class Team(BaseModel):
    name = CharField(max_length=255)
    type = CharField(max_length=4)
    ip = CharField(max_length=255, null=True)

class Task(BaseModel):
    name = CharField(max_length=255)
    checker = CharField(max_length=255)
    gets = IntegerField(default=1)
    puts = IntegerField(default=1)
    vulns = IntegerField()
    status = IntegerField(default=104)
    timeout = IntegerField()

class Flag(BaseModel):
    flag = CharField(max_length=255)
    flag_id = CharField(max_length=255)
    vuln = IntegerField()
    task = ForeignKeyField(Task, on_delete='CASCADE')
    round = IntegerField()

class Check(BaseModel):
    status = IntegerField()
    task = ForeignKeyField(Task, on_delete='CASCADE')
    command = CharField(max_length=5)
    message = TextField(null=True)
    error = TextField(null=True)
    round = IntegerField()

class Submit(BaseModel):
    flag = ForeignKeyField(Flag, on_delete='CASCADE')
    time = DateTimeField(default=datetime.datetime.now)