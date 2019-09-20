from app import db
from models import BlogPost

# CREATE THE DATABASE AND THE DB TABLES
# import ipdb; ipdb.set_trace()
db.create_all()

# INSERT
db.session.add(BlogPost(title="Good", description="I am good"))
db.session.add(BlogPost(title="Happy", description="I am happy"))
db.session.add(BlogPost(title="Well", description="I am well"))
db.session.add(BlogPost(title="Postgres setup", description="I have setup postgres locally"))


# COMMIT THE CHANGES
db.session.commit()
