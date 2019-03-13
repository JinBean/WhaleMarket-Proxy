# WhaleMarket-Proxy

### About the Proxy

The proxy is created on a Django framework and exposes the whalemarket API.

The home page has endpoints to both the GET and POST request services of the API.

The GET request takes in a numerical input and finds a key-value pair of whale information using the input as the key.

Leaving the input blank will return all key-value pairs in the whalemarket.

The GET request is cached.


The POST request takes in a whale name and a location and adds that to the whalemarket.

Both fields in the POST request have to be filled in for the request to work.

Both requests are set to rate-throttle at 100 requests/day by default. This value can be changed if necessary.

There is also an endpoint to purge the cache completely. If the cache has been purged successfully, a message will appear notifiying you so.


### Setting Up Server

Create a python file with the directory "whaleapi/whaleapi/settings_secret.py"

This file stores both the server secret key and the whalemarket API key in the form:

  APIKey = "fill-in-secret"
  
  secretKey = "fill-in-secret"
  
Run the command "python manage.py runserver" to start the server. (I used Python 3.6)

### Changing throttle rates

Navigate to "whaleapi/whaleapi/settings.py"

Under REST_FRAMEWORK, DEFAULT_THROTTLE_RATES, change the value of 'anon'.

