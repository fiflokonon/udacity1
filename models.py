from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

#-------------------------------------------------------#
#               Models                                  #
# ------------------------------------------------------#

#------------------------------------------------------#
#           Show Model                                 #
#------------------------------------------------------#
class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer(), primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    start_time = db.Column(db.DateTime, nullable=False)
    #----------------Link to Artist and Venue Models--------------------#
    venues = db.relationship('Venue', backref=db.backref('venues', lazy=True))
    artists = db.relationship('Artist', backref=db.backref('artists', lazy=True))
    
    def __repr__(self):
        return f'<Show: id: {self.id} venue_id: {self.venue_id} artist_id: {self.artist_id} start {self.start_time}>'
        
#----------------------------------------------#
#       Venue - Model                          #
#----------------------------------------------#
class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.PickleType())
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String())
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String())
    #------------Link to Artist----------------#
    artists = db.relationship('Artist', secondary = 'shows', lazy = 'joined')

    def __repr__(self):
        return f'<Venue {self.id} {self.name} {self.state} {self.address} {self.phone} {self.genres} {self.facebook_link} {self.image_link} {self.image_link} {self.seeking_talent} {self.seeking_description}>'

#--------------------------------------------------------#
#               Artist - Model                           #
#--------------------------------------------------------#
class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.PickleType())
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String())
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String())

    #----------Link to Venue--------------#
    venues = db.relationship('Venue', secondary = 'shows', lazy = 'joined')
    def __repr__(self):
        return f'<Artist {self.id} {self.name} {self.city} {self.state} {self.phone} {self.genres} {self.image_link} {self.facebook_link} {self.website_link} {self.seeking_venue} {self.seeking_description}>'
