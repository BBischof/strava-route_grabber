# Route Grabber

This app replaces a bunch of bash/python hackery that we did to build a prototype. Find the main project [here](https://github.com/lgoerl/stravapp).

I started with a [germ](https://github.com/BBischof/docker_flask_germ).

We're using:
- [reverse-geocoder](https://github.com/thampiman/reverse-geocoder) to find City/State/Country data.
- [vincenty](https://github.com/maurycyp/vincenty/blob/master/vincenty/__init__.py) to compute Vincenty distance.
- [lxml](http://lxml.de/) for all the html parsing.

## How to run locally

Build the container:
```
docker-compose build
```

Start the container:
```
docker-compose up
```

Make a request:
```
curl -X GET 'localhost:3000/get_routes/3&10'
```
