BlooGraph
=========

Background
----------
Bloocoin was a toy implementation of a cryptocurrency, written by some people on the internet. It lacked the benefits of BitCoin - it was centralised, and relied on you trusting the server, so wasn't really much good. However, it was a good way to get an idea of how Bitcoing Mining worked, and for some reason became quite popular for a few weeks.

This tool queried the BlooCoin API to acquire and plot mining-rate statistics, and market-cap stats.

I don't think BlooCoin is around any more (at least not in its previous form), so this tool isn't of much use - here for Archive purposes. 


Installation
------------

Install Django, run syncdb, run: "screen python manage.py getdata" to run the data acquisition loop. Not a nice way of doing it, will use celery or similar in future release.


