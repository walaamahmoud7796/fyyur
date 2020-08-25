import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL

#dialect : postgres
#username : zbbokoqcvgzgvx
#password : 8f7d0622dac83921b8beefcd2ba9f48f7b1f8487747067fa837eee2f6f750ea0
#host : ec2-34-192-122-0.compute-1.amazonaws.com
#port : 5432
#database : d4vmj1k4k2ejvm
SQLALCHEMY_DATABASE_URI = 'postgres://zbbokoqcvgzgvx:8f7d0622dac83921b8beefcd2ba9f48f7b1f8487747067fa837eee2f6f750ea0@ec2-34-192-122-0.compute-1.amazonaws.com:5432/d4vmj1k4k2ejvm'
