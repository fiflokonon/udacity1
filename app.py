# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
from crypt import methods
from itertools import count
import json
from site import venv
from datetime import datetime
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from models import Artist, db, Venue, Show

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
migrate = Migrate(app, db)
db.init_app(app)

# ----------------------------------------------------------------------------#
# filter_bys.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

#-----------------------Get Venues List-------------------#

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
  cities = []
  areas = []
  venues = Venue.query.all()
  for x in venues:
    cities.append(x.city)
    cities = list(set(cities))
  for city in cities:
    area = Venue.query.with_entities(Venue.id, Venue.name, Venue.state).filter_by(city=city).all()
    state = area[0].state
    donne = {
        'city': city, 
        'state': state, 
        'venues': area
        }
    areas.append(donne)  
  return render_template('pages/venues.html', data = areas)

#-------------Search Venue----------------#

@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    search_term = request.form.get('search_term', '')
    response = Venue.query.filter(Venue.name.ilike('%'+ search_term +'%')).all()
    count = Venue.query.filter(Venue.name.ilike('%'+ search_term +'%')).count()
    return render_template('pages/search_venues.html', results=response, count = count)

#------------------------------Get a Venue-------------------#

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    up_shows = []
    past_shows = []
    #---------Get past_shows and up_coming shows by Using JOIN------------#

    past = db.session.query(Show).join(Venue).filter(Show.venue_id == venue_id).filter(Show.start_time < datetime.now()).all()
    up = db.session.query(Show).join(Venue).filter(Show.venue_id == venue_id).filter(Show.start_time > datetime.now()).all()
    #---------Get Past show data-------------#

    for x in past:
        donne = {"artis_id": x.artist_id,
                 "artist_name": Artist.query.with_entities(Artist.name).filter_by(id = x.artist_id).first(),
                 "artist_image_link": Artist.query.with_entities(Artist.image_link).filter_by(id = x.artist_id).first(),
                 "start_time": str(x.start_time)
                }
        past_shows.append(donne)
    #--------Get Up coming shows data-------#

    for x in up:
        donnes = {
            "artist_id": x.artist_id,
            "artist_name": Artist.query.with_entities(Artist.name).filter_by(id = x.artist_id).first(),
            "artist_image_link": Venue.query.with_entities(Artist.image_link).filter_by(id = x.artist_id).first(),
            "start_time": str(x.start_time)
        }   
        up_shows.append(donnes)
    # TODO: replace with real venue data from the venues table, using venue_id
    venue = Venue.query.filter_by(id = venue_id).first()
    data = {
    "id": venue_id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": up_shows,
    "past_shows_count": len(past),
    "upcoming_shows_count": len(up),
    }
    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm()
    # TODO: insert form data as a new Venue record in the db, instead
    try:
    #------------Get User inputs-------------#    
        venue = Venue(name = form.name.data,
                    city = form.city.data,
                    state = form.state.data,
                    address = form.address.data,
                    phone = form.phone.data,
                    genres = form.genres.data,
                    facebook_link = form.facebook_link.data,
                    image_link = form.image_link.data,
                    website_link = form.website_link.data,
                    seeking_talent = form.seeking_talent.data,
                    seeking_description = form.seeking_description.data
        )
        # TODO: modify data to be the data object returned from db insertion
        db.session.add(venue)
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
        # TODO: on unsuccessful db insert, flash an error instead.
    except:
        db.session.rollback()
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    finally: 
        db.session.close()
    return render_template('pages/home.html')

#------------------DELETE A VENUE-----------#

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    try:
        venue = Venue.query.filter_by(id = venue_id).first()
        db.session.delete(venue)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    return render_template('pages/venues.html')


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    return render_template('pages/artists.html', artists = Artist.query.all())

#-----------Search Artist-------------#

@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term', '')
    response = Artist.query.filter(Artist.name.ilike('%'+ search_term +'%')).all()
    count = Artist.query.filter(Artist.name.ilike('%'+ search_term +'%')).count()
    return render_template('pages/search_artists.html', results = response, count = count, search_term = search_term)

#-------------Get Artist by using ID--------------#

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # TODO: replace with real artist data from the artist table, using artist_id
    past_shows = []
    up_shows = []
    artist = Artist.query.filter_by(id=artist_id).first()
    past = db.session.query(Show).join(Venue).filter(Show.artist_id == artist_id).filter(Show.start_time < datetime.now()).all()
    up = db.session.query(Show).join(Venue).filter(Show.artist_id == artist_id).filter(Show.start_time > datetime.now()).all()
    for x in past:
        donne = {"venue_id": x.venue_id,
                 "venue_name": Venue.query.with_entities(Venue.name).filter_by(id = x.venue_id).first(),
                 "venue_image_link": Venue.query.with_entities(Venue.image_link).filter_by(id = x.venue_id).first(),
                 "start_time": str(x.start_time)
                }
        past_shows.append(donne)
    for x in up:
        donnes = {
            "venue_id": x.venue_id,
            "venue_name": Venue.query.with_entities(Venue.name).filter_by(id = x.venue_id).first(),
            "venue_image_link": Venue.query.with_entities(Venue.image_link).filter_by(id = x.venue_id).first(),
            "start_time": str(x.start_time)
        }   
        up_shows.append(donnes)   

    data = {
            "id": artist_id,
            "name": artist.name,
            "genres": artist.genres,
            "city": artist.city,
            "state": artist.state,
            "phone": artist.phone,
            "website": artist.website_link,
            "facebook_link": artist.facebook_link,
            "seeking_venue": artist.seeking_venue,
            "seeking_description": artist.seeking_description,
            "image_link": artist.image_link,
            "past_shows": past_shows,
            "upcoming_shows": up_shows,
            "past_shows_count": len(past),
            "upcoming_shows_count": len(up)      
            }
    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.filter_by(id = artist_id).first()
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm()
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    try:
        artist = Artist.query.filter_by(id = artist_id).first()
        artist.name = form.name.data
        artist.city = form.city.data,
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.genres = form.genres.data
        artist.facebook_link = form.facebook_link.data
        artist.image_link = form.image_link.data
        artist.website_link = form.website_link.data
        artist.seeking_venue = form.seeking_venue.data
        artist.seeking_description = form.seeking_description.data
        db.session.commit()
    except:
        db.session.rollback()
        flash('An error occurred. Artist ' + artist.name + ' could not be updated.')
    finally:
        db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.filter_by(id = venue_id).first()
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form = form, venue = venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    form = VenueForm()
    venue = Venue.query.filter_by(id = venue_id).first()
    venue.name = form.name.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.address = form.address.data
    venue.phone = form.phone.data
    venue.genres = form.genres.data
    venue.facebook_link = form.facebook_link.data
    venue.image_link = form.image_link.data
    venue.website_link = form.website_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data
    db.session.commit()
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm()
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    try:
        #-----Get User Input---------#
        artist = Artist(
            name = form.name.data,
            city = form.city.data,
            state = form.state.data,
            phone = form.phone.data,
            genres = form.genres.data,
            facebook_link = form.facebook_link.data,
            image_link = form.image_link.data,
            website_link = form.website_link.data,
            seeking_venue = form.seeking_venue.data,
            seeking_description = form.seeking_description.data
        )
        # TODO: modify data to be the data object returned from db insertion
        db.session.add(artist)
        db.session.commit()
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    except:
        db.session.rollback()
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    shows = []
    datas = Show.query.all()
    for show in datas:
        data = {
            "venue_id": show.venue_id,
            "venue_name": Venue.query.with_entities(Venue.name).filter_by(id = show.venue_id).first(),
            "artist_id": show.artist_id,
            "artist_image_link": Artist.query.with_entities(Artist.image_link).filter_by(id = show.artist_id).first(),
            "start_time": str(show.start_time)
        }
        shows.append(data)
    return render_template('pages/shows.html', shows=shows)

#----------------Create Show---------------#
@app.route('/shows/create')
def create_shows():
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm()
    # called to create new shows in the db, upon submitting new show listing form
    try:
        #--------------Get User input--------#
        show = Show(
            venue_id = form.venue_id.data,
            artist_id = form.artist_id.data,
            start_time = form.start_time.data
        )
        db.session.add(show)
        # TODO: insert form data as a new Show record in the db, instead
        db.session.commit()
        # on successful db insert, flash success
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    finally:
        db.session.close()
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

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
