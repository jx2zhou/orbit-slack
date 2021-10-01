# slackboss

## installation

Dependencies:

- slackclient
- flask

## setup

To run the server:

    $ python3 -m flask run

in the same directory as `app.py`. It will default to running on localhost on port 5000.

Interactivity requires a URL endpoint to make HTTP requests to. Consequently I used [ngrok](https://ngrok.com) to open a tunnel to localhost.
(This combined with the flask dev server makes it hella insecure i guess. But who cares)

Set up ngrok and open a tunnel:

    $ ngrok http 5000
    
Note the generated domain (e.g. http://fcb7-107-3-141-83.ngrok.io).

Copy the interactivity endpoint into the Request URL field (e.g. http://fcb7-107-3-141-83.ngrok.io/interact).

Copy the options load endpoint into the Options Load URL field (e.g. http://fcb7-107-3-141-83.ngrok.io/options-load)

now u shud b gud 2 go :^)
