# sg-http

## Install
This is just a django site, ensure that you have python (3.6 preferred) installed, along with django.
If you dont, you can just run `pip install django`. That should get it.

Other dependencies:

1. django-dotenv
2. shotgun_api3

## Running
To run it, just cd into the main directory, and run `run.sh`.
If on Windows (which is untested) run `run.bat`.

Once its running, you can connect to it through http, through whatever ajax library or language you like.
Right now there aren't many language specific bindings, but I do intend on creating bindings for Rust, and possibly Javascript.

## Why?
Shotgun Currently doesnt support using pure http for their api. It does however support python.
Whilst you could make calls to shotgun directly, by reworking their python api,
they still consistently make breaking changes to the way their HTTP calls work.
In order to fix this, I have begun the development of a translation layer of sorts for the shotgun api.
It runs a local server, and listens for your html requests, and does all the hard work for you, in python.

## How It Works
Basically, the Django web server gets run, and listens for a request. 
On a request, it queries the python shotgun api for your information, and relays it to you in json, through http.
