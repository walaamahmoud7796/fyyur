#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from ansi import color
import os
import sys
from datetime import datetime 

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config['SQLALCHEMY_DATABASE_URI']  = 'postgres://zbbokoqcvgzgvx:8f7d0622dac83921b8beefcd2ba9f48f7b1f8487747067fa837eee2f6f750ea0@ec2-34-192-122-0.compute-1.amazonaws.com:5432/d4vmj1k4k2ejvm'
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)
migrate = Migrate(app,db)


# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


  
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
   
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.String(120),nullable=False,default= "All")
    # artists = relationship("Artist",secondary=show)
    shows = relationship("Show",back_populates="venue")
class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
   
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    shows = relationship('Show',back_populates ="artist" )
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


class Show(db.Model):
  __tablename__ = "Show"
  id = db.Column(db.Integer,primary_key=True)
  artist_id = db.Column(db.Integer,db.ForeignKey("Artist.id"))
  venue_id = db.Column(db.Integer,db.ForeignKey("Venue.id"))
  start_time = db.Column(db.DateTime,nullable =False)
  venue = relationship("Venue",back_populates="shows")
  artist = relationship("Artist",back_populates="shows")







#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  # date = dateutil.parser.isoparse(value)
  # print(date)
  # if format == 'full':
  #     format="EEEE MMMM, d, y 'at' h:mma"
  # elif format == 'medium':
  #     format="EE MM, dd, y h:mma"
  print(color['Blue'],datetime.now())
  date = datetime.now()
  # date =datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%Z")
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  ------------------------------------------------------------------
#  Venues CRUD
#  ----------------------------------------------------------------


  
@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  venues = Venue.query.all()
  data =[]
  city_map={}
  for index in range(len(venues)):
    map_ = venues[index].__dict__

    city_object ={}
    venue_object={"name":map_['name'],"id":map_['id']}
    
    if map_['city'] not in city_map:
      city_object={"city":map_['city'],'state':map_['state'],'venues':[venue_object]}
      city_map[map_['city']] = True
    else:
      for object_ in data:
        if object_['city']==map_['city']:
          object_['venues'].append(venue_object)
    data.append(city_object)
  print(data)
    # venues = []
    # city_info = {}
    # venue_info = {"name":map_['name'],"id":map_['id']}
    # venues.append(venue_info)
    # if map_['city'] in city_map:
    #    city_info['venues'].append(venue_info)

    # else:
    #   city_map[map_['city']] = True
    #   city_info = {"city":map_['city'],"state":map_['state'],"venues":venues}
    # data.append(city_info)  
  # data=[{
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "venues": [{
  #     "id": 1,
  #     "name": "The Musical Hop",
  #     "num_upcoming_shows": 0,
  #   }, {
  #     "id": 3,
  #     "name": "Park Square Live Music & Coffee",
  #     "num_upcoming_shows": 1,
  #   }]
  # }, {
  #   "city": "New York",
  #   "state": "NY",
  #   "venues": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }]
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  print('---------------------',request.form.get('search_term'))
  search_key = request.form.get('search_term')
  venues = Venue.query.filter(Venue.name.contains(search_key)).all()
  print(venues)
  response ={"count":len(venues),"data":[]}
  for index in range(len(venues)):
    data_object = {"id":venues[index].id,"name":venues[index].name}
    response["data"].append(data_object)
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id


  venue_data = Venue.query.filter(Venue.id==venue_id).first()
  past_shows = db.session.query(Show.artist_id
                                ,Artist.name.label("artist_name")
                                ,Artist.image_link.label("artist_image_link")
                                ,Show.start_time)\
                                .join(Artist,Show.artist_id== Artist.id)\
                                .join(Venue,Show.venue_id==Venue.id)\
                                .filter(Venue.id== venue_id,Show.start_time<datetime.now())\
                                .all()
  upcoming_shows = db.session.query(Show.artist_id
                                ,Artist.name.label("artist_name")
                                ,Artist.image_link.label("artist_image_link")
                                ,Show.start_time)\
                                .join(Artist,Show.artist_id== Artist.id)\
                                .join(Venue,Show.venue_id==Venue.id)\
                                .filter(Venue.id== venue_id,Show.start_time>datetime.now())\
                                .all()
  past_shows_list = []
  upcoming_shows_list =[]
  for past_show in past_shows:
    past_shows_list.append(past_show._asdict())


  for upcoming_show in upcoming_shows:
    upcoming_shows_list.append(upcoming_show._asdict())
  
  data = venue_data.__dict__
  data['past_shows']= past_shows_list  
  data['upcoming_shows']= upcoming_shows_list
  data['past_shows_count']= len(past_shows_list)
  data['upcoming_shows_count']=len(upcoming_shows_list)
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()

  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  try:
    new_venue = Venue(name = request.form['name']
                      ,city = request.form['city']
                      ,state = request.form['state']
                      ,address = request.form['address']
                      ,phone = request.form['phone']
                      ,genres = request.form['genres']
                      ,facebook_link = request.form['facebook_link']
                      ,image_link = request.form['image_link'])
    db.session.add(new_venue)
    db.session.commit()
    print(color['Green'],"NEW VENUE IS ADDED")
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    error = True 
    db.session.rollback()
    print(color['Red'],sys.exc_info())
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')

  # on successful db insert, flash success
  
  return render_template('pages/home.html')

  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue_data = Venue.query.filter(Venue.id==venue_id).first()

  venue = venue_data.__dict__
  
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)
@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  # print(color['Cyan'],request.form['name'])
  # print(**request.form.dict())
  try:
    db.session.query(Venue).filter(Venue.id== venue_id).update({Venue.name : request.form['name']
                        ,Venue.city : request.form['city']
                        ,Venue.state : request.form['state']
                        ,Venue.address : request.form['address']
                        ,Venue.phone : request.form['phone']
                        ,Venue.genres : request.form['genres']
                        ,Venue.facebook_link : request.form['facebook_link']
                        ,Venue.image_link: request.form['image_link']})
    db.session.commit()
  except Exception as e:
    print(color['Red'],e)
    db.session.rollback()
  return redirect(url_for('show_venue', venue_id=venue_id))


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  flash('Venue ' + venue_id + ' was successfully deleted!')

  return render_template('pages/venues.html', areas=data)




#  ----------------------------------------------------------------
#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database


  artists = Artist.query.all()
  data = []
  for artist in artists :
    artist_object = {"id":artist.id,"name":artist.name}
    data.append(artist_object)
  
  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search_key = request.form.get('search_term')
  artists = Artist.query.filter(Artist.name.contains(search_key)).all()
  print(color['Blue'],artists)
  data = []
  response ={}
  response['count']= len(artists)
  for artist in artists:
    artist_object = {"id":artist.id,"name":artist.name}
    data.append(artist_object)
  response["data"] = data
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # print(color['Blue'],artist_id)
  artist_data = Artist.query.filter(Artist.id==artist_id).first()

  
  past_shows = db.session.query(Show.artist_id
                                ,Show.venue_id
                                ,Venue.name.label("venue_name")
                                ,Venue.image_link.label("venue_image_link")
                                ,Show.start_time)\
                                .join(Artist,Show.artist_id== Artist.id)\
                                .join(Venue,Show.venue_id==Venue.id)\
                                .filter(Artist.id== artist_id,Show.start_time<datetime.now())\
                                .all()
  upcoming_shows = db.session.query(Show.artist_id
                                ,Show.venue_id
                                ,Venue.name.label("venue_name")
                                ,Venue.image_link.label("venue_image_link")
                                ,Show.start_time)\
                                .join(Artist,Show.artist_id== Artist.id)\
                                .join(Venue,Show.venue_id==Venue.id)\
                                .filter(Artist.id== artist_id,Show.start_time>datetime.now())\
                                .all()
  past_shows_list = []
  upcoming_shows_list =[]
  for past_show in past_shows:
    past_shows_list.append(past_show._asdict())


  for upcoming_show in upcoming_shows:
    upcoming_shows_list.append(upcoming_show._asdict())
  
  data = artist_data.__dict__
  data['past_shows']= past_shows_list
  data['upcoming_shows']= upcoming_shows_list
  data['past_shows_count']= len(past_shows_list)
  data['upcoming_shows_count']=len(upcoming_shows_list)
  print(color['Blue'],data)

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist_data = Artist.query.filter(Artist.id==artist_id).first()

  artist = artist_data.__dict__  
 
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  try:
    db.session.query(Artist).filter(Artist.id==artist_id).update({Artist.name : request.form['name']
                                                              , Artist.city : request.form['city']
                                                              , Artist.state : request.form['state']
                                                              , Artist.phone : request.form['phone']
                                                              , Artist.genres : request.form['genres']
                                                              , Artist.facebook_link : request.form['facebook_link']
                                                              , Artist.image_link:request.form['image_link']})
    db.session.commit()
  except Exception as e:
    print(color['Red'],e)
    db.session.rollback()
  return redirect(url_for('show_artist', artist_id=artist_id))



#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  try:
    new_artist = Artist(name = request.form['name']
                      , city = request.form['city']
                      , state = request.form['state']
                      , phone = request.form['phone']
                      , genres = request.form['genres']
                      , facebook_link = request.form['facebook_link']
                      , image_link = request.form['image_link'])
    db.session.add(new_artist)
    db.session.commit()
    print(color['Green'],"NEW VENUE IS ADDED")
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    error = True 
    db.session.rollback()
    print(color['Red'],sys.exc_info())
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')

#  ----------------------------------------------------------------
#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[]
  
  show_list = db.session.query(Show.artist_id,Show.venue_id,Show.start_time,
                              Artist.name.label("artist_name"),
                              Artist.image_link.label("artist_image_link"),
                              Venue.name.label("venue_name"))\
                  .join(Artist, Show.artist_id == Artist.id)\
                  .join(Venue, Show.venue_id == Venue.id)\
                  .all()
  for show in show_list:
      data.append(show._asdict())
      # data.append(show._asdict())  
      print(color['Cyan'],data)

  # data=[{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 4,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 5,
  #   "artist_name": "Matt Quevedo",
  #   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "start_time": "2019-06-15T23:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-01T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-08T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-15T20:00:00.000Z"
  # }]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  try:
    show = Show(artist_id=request.form['artist_id'],
                venue_id = request.form['venue_id'],
                start_time = request.form['start_time'])
  # on successful db insert, flash success
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except Exception as e:
    print(color['Red'],e)
    db.session.rollback()
    flash('Show was failed to be listed!')


  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
