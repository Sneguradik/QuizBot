import sqlite3 as sq

def on_start():
    global db , cur
    db = sq.connect('database_db.db')
    cur =db.cursor()
    if db:
        print('DB connected')
    
async def add_User(state):
    
    async with state.proxy() as data:
        dt = list(data.values())
        tuple(dt)
        cur.execute(f'INSERT INTO Users (telegram_id, Name, Surname, Email) VALUES(?,?,?,?)',dt)
        db.commit()

def get_inf(table_name, param_name=None, param=None):
    if param_name == None:
        res = cur.execute(f'SELECT * FROM {table_name}').fetchall()
    else:
        res = cur.execute(f'SELECT * FROM {table_name} WHERE {param_name}=?',(param,)).fetchall()
    return res

async def add_Question(state):
    
    async with state.proxy() as data:
        dt = list(data.values())
        tuple(dt)
        cur.execute(f'INSERT INTO Questions (Question, RightAnswer, Answer1, Answer2, Answer3, Score, file_id) VALUES(?,?,?,?,?,?,?)',dt)
        db.commit()

async def update_score(user_id, score):
    cur.execute(f'UPDATE Users SET Score = ? WHERE telegram_id = ?',(score, user_id))
    db.commit()

async def set_used(id):
    cur.execute(f'UPDATE Questions SET Used = ? WHERE id = ?', (True, id))
    db.commit()

async def delete_question(id):
    cur.execute('DELETE FROM Questions WHERE id = ?', (id))
    db.commit()