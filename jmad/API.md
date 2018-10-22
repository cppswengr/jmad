# Get a Track with Solos
    * URL: /api/tracks/\<pk\>/
    * HTTP Method: GET
## Example Response
    {
        "name": "All Blues",
        "slug": "all-blues",
        "album": {
        "name": "Kind of Blue",
        "url": "http://jmad.us/api/albums/2/"
    },
    "solos": [
        {
            "artist": "Cannonball Adderley",
            "instrument": "saxophone",
            "start_time": "4:05",
            "end_time": "6:04",
            "slug": "cannonball-adderley",
            "url": "http://jmad.us/api/solos/281/"
        },
...
    ]
}
# Add a Solo to a Track
    * URL: /api/solos/
    * HTTP Method: POST
    
## Example Request
    {
        "track": "/api/tracks/83/",
        "artist": "Don Cherry",
        "instrument": "cornet",
        "start_time": "2:13",
        "end_time": "3:54"
    }
    
## Example Response
    {
        "url": "http://jmad.us/api/solos/64/",
        "artist": "Don Cherry",
        "slug": "don-cherry",
        "instrument": "cornet",
        "start_time": "2:13",
        "end_time": "3:54",
        "track": "http://jmad.us/api/tracks/83/"
    }
