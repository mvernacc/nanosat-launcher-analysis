''' Analyze the (cost per mass) versus (production rate) relationship for launch vehicles.

I heard that for many engineered systems, the cost per kilogram is correlated with
the number of units produced per year. The correlation is expected to be positive,
lower-production-rate systems cost more because fixed costs (engineering time, tooling
etc.) are amortized over fewer vehicles. I fit a regression model to this correlation
for space launch vehicles. Then, I use the regression model to make a rough prediction
of the cost of a nanosat launcher, given its mass and number of launches per year.
'''

from __future__ import division
import numpy as np
from matplotlib import pyplot as plt
from sklearn import linear_model


# name, mass [kilogram], cost [USD], units/year
vehicles = [
('747', 240e3, 350e6, 1500/(2015-1968)),
('Delta IV H', 730e3, 400e6, 8/10),
('Atlas V', 334.5e3, 173e6, 58/(2015-2002)),
('Falcon 9', 505.8e3, 61e6, 19/5),
('Falcon 1', 38e3, 7.9e6, 5/3),
('Electron', 6e3, 5e6, 1),
('Minotaur I', 36e3, 28.8e6, 11/15),
('Minotaur IV', 86.3e3, 50e6, 5/5),
('Proton M', 712.8e3, 83e6, 117/14),
('Vega', 137e3, 23e6, 5/3),
('Ariane 5', 777e3, 220e6, 82/(2015-1996)),
('Dnepr', 211e3, 14e6, 22/16),
('Shavit', 50e3, 15e6, 9/(2015-1988)),
('Delta II', 200e3, 107e6, 153/(2015 - 1989)),
('Energia', 2400e3, 240e6, 2),
('Shuttle', 2030e3, 1e9, 135/(2011-1981)),
('Titan IV', 943e3, 432e6, 39/(2005 - 1989))
]

# Scatter plot the launch vehicle names on (cost/mass) versus (years/unit).
cost_per_mass = []
prod_period = []
for v in vehicles:
    cost_per_mass.append(v[2] / v[1])
    prod_period.append(1 / v[3])
    plt.annotate(v[0], xy=(prod_period[-1], cost_per_mass[-1]), xytext=(-10,10),
        textcoords = 'offset points')

# Use the Random Sample Consensus algorithm to fit a linear regression model.
# USe RANSAC because it is robust to outliers.
prod_period = np.array(prod_period).reshape((len(vehicles), 1))
cost_per_mass = np.array(cost_per_mass).reshape((len(vehicles), 1))
model_ransac = linear_model.RANSACRegressor(linear_model.LinearRegression())
model_ransac.fit(prod_period, cost_per_mass)
inlier_mask = model_ransac.inlier_mask_
outlier_mask = np.logical_not(inlier_mask)

# Plot the regression model
line_X = np.arange(0, 2)
line_y_ransac = model_ransac.predict(line_X[:, np.newaxis])
plt.plot(prod_period[inlier_mask], cost_per_mass[inlier_mask], '.g', label='Inliers')
plt.plot(prod_period[outlier_mask], cost_per_mass[outlier_mask], '.r', label='Outliers')
plt.plot(line_X, line_y_ransac, '-b', label='RANSAC regressor')


a = model_ransac.predict(0)
b = model_ransac.predict(1)
print 'RANSAC trend: cost_per_mass = %.2f prod_period + %.0f' % ((b - a), a)
# Nanosat launcher mass [kilogram]
m_nano = 3300
# Nanosat launcher production period [years unit**-1]
T_nano = 1 / 6
# Nanosat launcher cost per mass prediction [USD kilogram**-1]
c = (b - a) *  T_nano + a
# Nanosat launcher cost prediction [USD]
cost_predict = c * m_nano
print 'Predicted cost for a %.0f kg launch vehicle, with %.1f launches per year:' \
    % (m_nano, 1/T_nano)
print ' = %.1f kUSD' % (cost_predict / 1e3)


plt.xlabel('Production period [years / unit]')
plt.ylabel('Cost per liftoff mass [USD / kg]')
plt.legend()
plt.xlim([0, 3.2])
plt.ylim([0, 1000])
plt.show()
