#!/usr/bin/env python
import asyncio
import uvicorn
import socketio
import random
import psycopg2

connection=''
# try:

# except (Exception, psycopg2.Error) as error :
#     print ("Error while connecting to PostgreSQL", error)
# finally:
#     if connection:
#         connection.close()
#         print("PostgreSQL connection is closed")

sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio, static_files={
    '/': 'app.html',
})
background_task_started = False

game_types={
    '1':{
        'max_player':'2',
    },
    '2':{
        'max_player':'8',
    },
}
online_user_ids={}
joined_room_player_ids=[]
room_detail={}

def generate_room_id():
    existing_room_ids = room_detail.keys()
    generated_room_id = ''
    while True:
        generated_room_id = random.randint(0, 1000000)
        if generated_room_id not in existing_room_ids:
            break
    return generated_room_id
def create_or_join_room(game_id,room_id,sid):
    if room_id in room_detail and sid in room_detail[room_id]['players']:
        pass
    elif room_id in room_detail and sid not in room_detail[room_id]['players']:
        room_detail[room_id]['players'].append(sid)
    else:
        room_detail[room_id]={
            'game_id':game_id,
            'players':[sid],
            'is_busy':False,
        }
def get_room_members(room_id):
    members = []
    member_uids = []
    if room_id in room_detail.keys():
        members=room_detail[room_id]['players']
    if members:
        for m in members:
            member_uids.append(get_uid(m))
    return member_uids
def get_uid(sid):
    return online_user_ids[sid] if sid in online_user_ids.keys() else ''
def update_online_status(uid,fun):
    connection = psycopg2.connect(
        user = "dbuser",
        password = "pass",
        host = "localhost",
        port = "",
        database = "db"
    )
    print ( connection.get_dsn_parameters(),"\n")

    cursor=connection.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")

    try:
        if fun:
            query="""Update accounts_user is_online=1 where id = %s """
        else:
            query="""Update accounts_user is_online=0 where id = %s """
        cursor.execute(query, uid)
        connection.commit()
    except (Exception, psycopg2.Error) as error :
        print ("Error while getting data from PostgreSQL", error)
    finally:
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


async def background_task():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        await sio.sleep(10)
        count += 1
        active_user_list=list(online_user_ids.values())
        await sio.emit('my_response', {'data': active_user_list})

@sio.on('my_event')
async def test_message(sid, message):
    uid = message['uid']
    online_user_ids[str(sid)]=str(uid)
    active_user_list=list(online_user_ids.values())
    update_online_status(uid,1)
    await sio.emit('my_response', {'data': active_user_list}, room=sid)

@sio.on('broadcast_all')
async def test_broadcast_message(sid, message):
    await sio.emit('my_response', {'data': message['data']})

@sio.on('broadcast_room')
async def send_room_message(sid, message):
    await sio.emit('my_response', {'data': message['data']},
                   room=message['room'])

@sio.on('create_room')
async def create_room(sid, message):
    game_type = message['game_type']
    generated_room_id = generate_room_id()
    room_id = str(generated_room_id)
    sio.enter_room(sid, room_id)
    joined_room_player_ids.append(online_user_ids[str(sid)])
    create_or_join_room(game_type,room_id,sid)
    room_players = get_room_members(room_id)
    data = {'room_id': room_id, 'players': room_players}
    await sio.emit('my_response', {'data': data}, room=room_id)

@sio.on('join')
async def join(sid, message):
    room_id=message['room']
    sio.enter_room(sid, room_id)
    joined_room_player_ids.append(online_user_ids[str(sid)])
    create_or_join_room(None,room_id,sid)
    room_detail[room_id]['is_busy']=True
    room_players = get_room_members(room_id)
    data = {'room_id': room_id, 'players': room_players}
    await sio.emit('my_response', {'data': data}, room=room_id)

@sio.on('random_join')
async def random_join(sid, message):
    game_id = message['gid']
    room_id = ''
    max_player = int(game_types[game_id]['max_player'])
    entered_room_id=''
    for i in room_detail.keys():
        if room_detail[i]['game_id'] == game_id:
            if not room_detail[i]['is_busy']:
                if max_player > len(room_detail[i]['players']):
                    room_id = i
                    sio.enter_room(sid, room_id)
                    joined_room_player_ids.append(online_user_ids[str(sid)])
                    create_or_join_room(None,room_id,sid)
                    entered_room_id = sio.rooms(sid,None)
    
    if entered_room_id=='':
        generated_room_id = generate_room_id()
        room_id = str(generated_room_id)
        sio.enter_room(sid, room_id)
        joined_room_player_ids.append(online_user_ids[str(sid)])
        create_or_join_room(game_id,room_id,sid)
    room_players = get_room_members(room_id)

    data = {'room_id': room_id, 'players': room_players}
    await sio.emit('my_response', {'data': data}, room=room_id)

@sio.on('update_room')
async def update_room(sid,message):
    room_detail[message['room']]['is_busy']=True
    await sio.emit('my_response', {'data': 'Room is busy now'}, room=message['room'])

@sio.on('close_room')
async def close_room(sid, message):
    await sio.emit('my_response',{'data': 'Room ' + message['room'] + ' is closing.'},room=message['room'])
    await sio.close_room(message['room'])
    room_players = get_room_members(message['room'])
    for p in room_players:
        if p in joined_room_player_ids:
            joined_room_player_ids.remove(p)
    del room_detail[message['room']]

@sio.on('disconnect_request')
async def disconnect_request(sid):
    await sio.sleep(10)
    await sio.disconnect(sid)

@sio.on('connect')
async def test_connect(sid, environ):
    global background_task_started
    if not background_task_started:
        sio.start_background_task(background_task)
        background_task_started = True
    await sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)

@sio.on('disconnect')
def test_disconnect(sid):
    room_id=''
    other_player=''
    room_players=''
    if str(sid) in online_user_ids:
        del online_user_ids[str(sid)]
    for r in room_detail:
        if sid in r['players']:
            room_players=r['players']
            room_id=r
            del room_detail[r]
    for p in room_players:
        if p!=sid:
            other_player=get_uid(p)
        joined_room_player_ids.remove(get_uid(p))
    print('Client disconnected')

    if room_id and other_player:
        connection = psycopg2.connect(
            user = "dbuser",
            password = "pass",
            host = "localhost",
            port = "",
            database = "db"
        )
        print ( connection.get_dsn_parameters(),"\n")

        cursor=connection.cursor()
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")

        try:
            query="""select status from game_game where room_id = %s"""
            cursor.execute(query, (int(room_id),))
            res = cursor.fetchone()
            if res != "finished":
                query="""Update game_game status=%s, winner=%s where room_id = %s """
                cursor.execute(query, ('finished',other_player,int(room_id)))
                connection.commit()
        except (Exception, psycopg2.Error) as error :
            print ("Error while getting data from db", error)
        finally:
            if(connection):
                cursor.close()
                connection.close()
                print("db connection is closed")

    update_online_status(sid,0)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
