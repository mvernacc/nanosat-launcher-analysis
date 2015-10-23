Nanosat Launcher Analysis
=========================

This is an analysis of the economic viability of a cubesat launcher.


Launcher Perofrmance
--------------------
See dv.py.

A delta-v of approximately 9 km/s is required to reach Low Earth Orbit. Using current propulsion technology, a 4-stage launcher capable of providing 9.5 km/s dv to a 10 kg payload will have a mass of the pad of about 3300 kg.


Launcher Cost
-------------
See cost.py.

In order to estimate the cost of the nanosat launcher, I fit a regression model to (cost per mass) versus (production rate) data for existing space launch vehicles. Using this model, I can estimate the cost of the nanosat launcher from its mass and production rate. The mass was estimated in the above section. Now I estimate the production rate:

In 2013, 14 and 15 there were an average of 88 cubsats laucnhed per year. Assuming that the new launcher captures 20% of the existing market, it will launch 18 cubesats per year. A rocket with a 10 kg payload capacity can carry 7U, or approximately 3 cubesats. Therefore the nanosat launcher will be produced and launched at a rate of about 6 rockets per year.

Depending on how the regression is fit (there are not enough data points for a highly consistent RANSAC result), the predicted cost is 400 to 1200 kUSD. Assuming a best-case cost of 400 kUSD, the launch cost is 60 kUSD per 1U.

Cube sat launch costs are typically 65 to 80 kUSD / 1U  as a secondary payload (https://en.wikipedia.org/wiki/CubeSat#Costs). Therefore, the dedicated nanosat launcher is likely not cost competative with launching cubesats as a secondary payload on existing, large launch vehicles.
