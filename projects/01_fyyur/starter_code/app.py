#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import json
import dateutil.parser
import babel
import sys
from flask import (Flask, render_template, request, Response, flash, redirect, url_for,jsonify)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from sqlalchemy import func, and_
from datetime import datetime

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
# models.py
from models import *


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    regions = Venue.query.with_entities(
        Venue.city, Venue.state).distinct().all()
    data = []

    for r in regions:
        venues_city = Venue.query.filter_by(city=r.city).all()
        venues = []
        for venue in venues_city:
            venues.append({
                'id': venue.id,
                'name': venue.name,
            })

        obj = {
            'city': r.city,
            'state': r.state,
            'venues': venues
        }
        data.append(obj)

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = '%{}%'.format(request.form.get('search_term', ''))
    venues = Venue.query.filter(
        Venue.name.ilike("%" + search_term + "%")).all()
    venuesList = []

    for v in venues:
        venuesList.append(v)

    response = {
        'count': len(venues),
        'data': venuesList
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    current_time = datetime.now()
    result = Venue.query.get(venue_id)

    upcoming_shows = db.session.query(Show).join(Venue).join(Artist).filter(Show.start_time > current_time).filter(venue_id==Show.venue_id)
    upcoming_show = []
    for up_show in upcoming_shows:
        obj = {
            'artist_id' : up_show.artist_id,
            'artist_name': Artist.query.get(up_show.artist_id).name,
            'artist_image_link': Artist.query.get(up_show.artist_id).image_link,
            'start_time': str(up_show.start_time)
        }
        upcoming_show.append(obj)

    upcoming_show_count = len(upcoming_show)

    past_shows = db.session.query(Show).join(Venue).join(Artist).filter(Show.start_time < current_time).filter(venue_id==Show.venue_id)
    past_show = []
    for pst_show in past_shows:
        obj = {
            'artist_id' : pst_show.artist_id,
            'artist_name': Artist.query.get(pst_show.artist_id).name,
            'artist_image_link': Artist.query.get(pst_show.artist_id).image_link,
            'start_time': str(pst_show.start_time)
        }
        past_show.append(obj)

    past_show_count = len(past_show)

    data = {
        'id' : result.id,
        'name' : result.name,
        'city' : result.city,
        'state' : result.state,
        'address' : result.address,
        'phone' : result.phone,
        'genres' : result.genres,
        'facebook_link' : result.facebook_link,
        'image_link' : result.image_link,
        'website': result.website,
        'upcoming_shows': upcoming_show,
        'upcoming_shows_count' : upcoming_show_count,
        'past_shows': past_show,
        'past_shows_count' : past_show_count,
        'seeking_talent': result.seeking_talent,
        'seeking_description': result.seeking_description,
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
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    try:
        venue = Venue(
            name=request.form.get('name'),
            city=request.form.get('city'),
            state=request.form.get('state'),
            address=request.form.get('address'),
            phone=request.form.get('phone'),
            genres=request.form.getlist('genres'),
            facebook_link=request.form.get('facebook_link')
        )
        db.session.add(venue)
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash('Venue ' + request.form['name'] + ' could not be listed!')
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
        flash('Venue deleted!')
    except:
        db.session.rollback()
        flash('Venue could not be deleted!')
    finally:
        db.session.close()
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    artists = Artist.query.all()
    data = []
    for a in artists:
        obj = {
            'id': a.id,
            'name': a.name
        }
        data.append(obj)
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = '%{}%'.format(request.form.get('search_term', ''))
    artists = Artist.query.filter(
        Artist.name.ilike("%" + search_term + "%")).all()
    data = []
    for a in artists:
        obj = {
            'id': a.id,
            'name': a.name
        }
        data.append(obj)

    response = {
        'count': len(artists),
        'data': data
    }

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    #data = Artist.query.get(artist_id)
    current_time = datetime.now()
    result = Artist.query.get(artist_id)

    upcoming_shows = db.session.query(Show).join(Venue).join(Artist).filter(Show.start_time > current_time).filter(artist_id==Show.artist_id)
    upcoming_show = []
    for up_show in upcoming_shows:
        obj = {
            'venue_id' : up_show.venue_id,
            'venue_name': Venue.query.get(up_show.venue_id).name,
            'venue_image_link': Venue.query.get(up_show.venue_id).image_link,
            'start_time': str(up_show.start_time)
        }
        upcoming_show.append(obj)

    upcoming_show_count = len(upcoming_show)

    past_shows = db.session.query(Show).filter(artist_id == Show.artist_id).filter(Show.start_time < current_time).all()
    past_show = []
    for pst_show in past_shows:
        obj = {
            'venue_id' : pst_show.venue_id,
            'venue_name': Venue.query.get(pst_show.venue_id).name,
            'venue_image_link': Venue.query.get(pst_show.venue_id).image_link,
            'start_time': str(pst_show.start_time)
        }
        past_show.append(obj)

    past_show_count = len(past_show)

    data = {
        'id' : result.id,
        'name' : result.name,
        'city' : result.city,
        'state' : result.state,
        'phone' : result.phone,
        'genres' : result.genres,
        'facebook_link' : result.facebook_link,
        'image_link' : result.image_link,
        'website': result.website,
        'upcoming_shows': upcoming_show,
        'upcoming_shows_count' : upcoming_show_count,
        'past_shows': past_show,
        'past_shows_count' : past_show_count,
        'seeking_venue': result.seeking_venue,
        'seeking_description': result.seeking_description,
    }
    
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(obj=artist)

    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    try:
        artist = Artist.query.get(artist_id)
        artist.name = request.form.get('name'),
        artist.city = request.form.get('city'),
        artist.state = request.form.get('state'),
        artist.address = request.form.get('address'),
        artist.phone = request.form.get('phone'),
        artist.genres = request.form.get('genres'),
        artist.facebook_link = request.form.get('facebook_link')

        db.session.add(artist)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(obj=venue)
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    try:
        venue = Venue.query.get(venue_id)
        venue.name = request.form.get('name'),
        venue.city = request.form.get('city'),
        venue.state = request.form.get('state'),
        venue.address = request.form.get('address'),
        venue.phone = request.form.get('phone'),
        venue.genres = request.form.get('genres'),
        venue.facebook_link = request.form.get('facebook_link')

        db.session.add(venue)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    try:
        artist = Artist(
            name=request.form.get('name'),
            city=request.form.get('city'),
            state=request.form.get('state'),
            phone=request.form.get('phone'),
            genres=request.form.getlist('genres'),
            facebook_link=request.form.get('facebook_link')
        )
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('Artist ' + request.form['name'] + ' could not be listed!')
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    try:
        Artist.query.filter_by(id=artist_id).delete()
        db.session.commit()
        flash('Artist deleted!')
    except:
        db.session.rollback()
        flash('Artist could not be deleted!')
    finally:
        db.session.close()
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------


@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    shows = Show.query.all()
    data = []
    for s in shows:
        obj = {
            'venue_id': s.venue_id,
            'venue_name': Venue.query.get(s.venue_id).name,
            'artist_id': s.artist_id,
            'artist_name': Artist.query.get(s.artist_id).name,
            'artist_image_link': Artist.query.get(s.artist_id).image_link,
            'start_time': str(s.start_time)
        }
        data.append(obj)
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    try:
        artist_id = request.form.get('artist_id')
        venue_id = request.form.get('venue_id')

        show = Show(
            venue_id=venue_id,
            artist_id=artist_id,
            start_time=request.form.get('start_time')
        )
        db.session.add(show)
        db.session.commit()
        # on successful db insert, flash success
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash('Show could not be listed!')
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    #return render_template('errors/404.html'), 404
    return jsonify({
        'success':False,
        'error': 404,
        'message':"deu ruim",
    }),404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
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
