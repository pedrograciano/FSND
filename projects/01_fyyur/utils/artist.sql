INSERT INTO "Artist" (
    name,
    genres,
    city,
    state,
    phone,
    website,
    facebook_link,
    seeking_venue,
    seeking_description,
    image_link
) VALUES (
    'Guns N Petals',
    ARRAY ['Rock n Roll'],
    'San Francisco',
    'CA',
    '326-123-5000',
    'https://www.gunsnpetalsband.com',
    'https://www.facebook.com/GunsNPetals',
    True,
    'Looking for shows to perform at in the San Francisco Bay Area!',
    'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80'   
);

INSERT INTO "Artist" (
    name,
    genres,
    city,
    state,
    phone,
    facebook_link,
    seeking_venue,
    image_link
) VALUES (
    'Matt Quevedo',
    ARRAY ['Jazz'],
    'New York',
    'NY',
    '300-400-5000',
    'https://www.facebook.com/mattquevedo923251523',
    False,
    'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80'   
);


INSERT INTO "Artist" (
    name,
    genres,
    city,
    state,
    phone,
    seeking_venue,
    image_link
) VALUES (
    'The Wild Sax Band',
    ARRAY ['Jazz', 'Classical'],
    'San Francisco',
    'CA',
    '3432-325-5432',
    False,
    'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80'   
);

INSERT INTO "Artist" (
    name,
    genres,
    city,
    state,
    phone,
    seeking_venue,
    image_link
) VALUES (
    'Test Artist',
    ARRAY ['Jazz', 'Classical'],
    'Test City',
    'AL',
    '3432-325-5432',
    False,
    'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80'   
);


data1={
    "past_shows": [{
      "venue_id": 1,
      "venue_name": "The Musical Hop",
      "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }