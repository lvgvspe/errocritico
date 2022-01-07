from deta import Deta
import main

deta = Deta('b09y7hmi_AFEApMypWh31wYJdM9JbkvjMMrvm5RKk')
db = deta.Base('simple_db')


def create_post(name, content):
    db.put({'name':name, 'post': content})

def get_post():
    item = db.fetch(query=None)
    global posts
    posts = item.items

def delete_post(key):
    res = db.delete(key)

if __name__ == '__main__':
    # delete_post(key)
    get_post()
    print (posts)