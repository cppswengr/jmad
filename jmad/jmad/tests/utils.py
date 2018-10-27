from albums.models import Album, Track

from solos.models import Solo

def create_test_data():
    album1 = Album.objects.create(
        name='My Favorite Things', slug='my-favorite-things'
    )
    track1 = Track.objects.create(
        name='My Favorite Things', slug='my-favorite-things',
        album=album1
    )
    solo1 = Solo.objects.create(
        instrument='saxophone', artist='John Coltrane',
        track=track1, slug='john-coltrane'
    )

    album2 = Album.objects.create(
        name='Kind of Blue', slug='kind-of-blue'
    )
    track2 = Track.objects.create(
        name='All Blues', slug='all-blues',
        album=album2, track_number=4
    )
    track4 = Track.objects.create(
        name='Freddie Freeloader',
        album=album2,
        track_number=2
    )
    track5 = Track.objects.create(
        name='Blue in Green',
        album=album2,
        track_number=3
    )
    solo2 = Solo.objects.create(
        instrument='saxophone', artist='Cannonball Adderley',
        track=track2, start_time='4:05', end_time='6:04',
        slug='cannonball-adderley'
    )

    solo4 = Solo.objects.create(
        instrument='trumpet', artist='Miles Davis',
        track=track2, slug='miles-davis',
        start_time='1:46', end_time='4:04'
    )

    album3 = Album.objects.create(
        name='Know What I Mean?', slug='know-what-i-mean'
    )
    track3 = Track.objects.create(
        name='Waltz for Debby', slug='waltz-for-debby',
        album=album3
    )
    solo3 = Solo.objects.create(
        instrument='saxophone', artist='Cannonball Adderley',
        track=track3, slug='cannonball-adderley'
    )

