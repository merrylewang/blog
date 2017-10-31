from py2neo import Graph, Node, Relationship
from passlib.hash import bcrypt
from datetime import datetime
import uuid


graph = Graph()



class User:

    def __init__(self,username):
        self.username = username

    def find(self):
        user = graph.find_one("User","username",self.username)
        return user

    def register(self,password):
        if not self.find():
            user = Node("User",username=self.username,password=bcrypt.encrypt(password))
            graph.create(user)
            return True

        return False

    def verify_password(self,password):
        user = self.find()

        if not user:
            return False

        return bcrypt.verify(password,user["password"])

    def add_post(self, title,tags, text):
        user = self.find()

        post = Node("Post",id=str(uuid.uuid4()),title=title,text=text,timestamp=int(datetime.now().stfttime("%s"),date=datetime.now().strf("%F")))

        tags = [x.strip() for x in tags.lower().split(",")]
        for tag in tags:
            t = graph.merge_one("Tag","name",tag)
            rel = Relationship(t, "TAGGED", post)
            graph.create(rel)


def todays_recent_posts(n):
    query = """
    MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag)
    WHERE post.date = {today}
    RETURN user.username, post, COLLECT(tag.name) AS tags
    ORDER BY post.timestamp DESC LIMIT {n}
    """

    today = datetime.now().strftime("%F")
    return graph.cypher.execute(query,today=today,n=n)