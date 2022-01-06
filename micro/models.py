from deta import Deta
deta = Deta('b09y7hmi_AFEApMypWh31wYJdM9JbkvjMMrvm5RKk')
db = deta.Base('simple_db')


def create_post(name, content):
    db.put(name, content)

def get_posts():
    res = db.fetch()
    posts = res.items
    while res.last:
        res = db.fetch(last=res.last)
        posts += res.items
    return posts
