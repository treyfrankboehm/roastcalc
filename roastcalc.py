#!/usr/bin/env python3

### Disclaimer ### {{{
# This file is part of roastcalc
# 
# roastcalc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more detail.
# <http://www.gnu.org/licenses/>

# You should have received a copy of the GNU General Public License
# along with roastcalc.  If not, see <http://www.gnu.org/licenses/>.
### }}}

### Magic numbers ### {{{
# Add this percent to roast input weight
safetyBuffer = 0.005
# Roast this many extra pounds for production cupping
cupQuantity = 0.2
# Whether to email the roast report or not (set to False when testing)
emailBool = False
# The emails to send the report to
#emails = ["trey.frank.boehm@gmail.com", "tcobb775@gmail.com", "trey@ggroasting.com"]
emails = []
### }}}

### Import data from CSV files ### {{{
import csv
import os

# Download the files 
print("Running scrape.py")
os.system("./scrape.py")
print("scrape.py completed\n")

# Column indices for history.csv:
# ID-Tag, Profile, Date, Component, Start Weight, End Weight, % Loss
# 0,      1,       2,    3,         4,            5,          6
history = list(csv.reader(open("history.csv")))

# Column indices for products.csv:
# Product, Component, Component #, Roast profile, % of blend
# 1,       2,         3,           4,             5
products = list(csv.reader(open("products.csv")))

# Column indices for totals.csv:
# Product, 3oz, 12oz, 2lb, 5lb, total lbs, roast/don't roast [1/0]
# 0,       1,   2,    3,   4,   5,         6
raw_totals = list(csv.reader(open("totals.csv")))
# Remove products that don't need to be roasted (no orders)
totals = [p for p in raw_totals if p[-1] == '1']

# Column indices for subscriptions.csv:
raw_subs = list(csv.reader(open("subscriptions.csv")))
# Remove products that aren't shipping today
subscriptions = [p for p in raw_subs if p[-2] == '0']
### }}}

### Percent loss calculation ### {{{
# Return the average percent loss for a given component/profile combo
def percentLoss(component, profile):
    losses = []
    for roast in history:
        if component in roast[3] and profile in roast[1]:
            loss = float(roast[6])
            # Sometimes the loss is entered as 0.00 by mistake
            if loss != 0:
                losses.append(float(roast[6]))
    # Average the losses across all available roasts
    return sum(losses)/len(losses)

# Print the percent loss for all component/profile combos
def allPercentLoss():
    percents = []
    for i in range(len(products)):
        percents.append("Component %s (Profile %s): %.2f%% loss." %
                (products[i][1], products[i][3], percentLoss(products[i][1], products[i][3])))
    for percent in sorted(list(set(percents))):
        print(percent)
    return 0
### }}}

### Product information ### {{{
# First we need a unique list of all the available products (names are
# repeated so in the spreadsheet so each component/profile/percent
# can be shown).
unique = set([product[0] for product in products])

# Dictionary (associative array) of all the products, taken from the spreadsheet
productInfo = {}

# Add all of the products to the "productInfo" dict.
# "Product Name":[["Component 1","Roast Profile 1","Percent 1"],
#       ["Component 2", "Roast Profile 2", "Percent 2"], [etc]]
# Note that single-origin and blends are treated the same way, using
# 1.00 as the percent of total for the component. This eliminates the
# need for redundant code.
for product in unique:
    roastInfo = []
    for i in range(len(products)):
        if products[i][0] == product:
            roastInfo.append([products[i][1], products[i][3], products[i][4]])
    productInfo[product] = roastInfo
### }}}

### Calculate roast quantities ### {{{
# Another associative array formatted as
#   {("Component 1", "Profile 1"):pounds,
#    ("Component 2", "Profile 2"):pounds, etc}
roastNeeds = {}

# Populate the dict
for i in range(len(totals)):
    pounds = float(totals[i][5])
    if pounds != 0:
        product = totals[i][0]
        for i in range(len(productInfo[product])):
            component =       productInfo[product][i][0]
            profile   =       productInfo[product][i][1]
            percent   = float(productInfo[product][i][2])
            # If the key:value pair has not been initialized yet, it
            # returns an error. Try to add weight, otherwise initialize.
            try:
                roastNeeds[(component, profile)] += pounds*percent
            except KeyError:
                roastNeeds[(component, profile)] = pounds*percent
for i in range(len(subscriptions)):
    pounds = float(subscriptions[i][2])
    product = subscriptions[i][1]
    for i in range(len(productInfo[product])):
        component =       productInfo[product][i][0]
        profile   =       productInfo[product][i][1]
        percent   = float(productInfo[product][i][2])
        # If the key:value pair has not been initialized yet, it
        # returns an error. Try to add weight, otherwise initialize.
        try:
            roastNeeds[(component, profile)] += pounds*percent
        except KeyError:
            roastNeeds[(component, profile)] = pounds*percent
# }}}

### Main ### {{{
if __name__ == "__main__":
    outFile = open("outFile.txt", "w")
    header = ("Safety buffer percentage: %.2f%%\n"
            "Amount for cupping: %.2f lbs\n" %
            (100*safetyBuffer, cupQuantity))
    print(header)
    outFile.write("%s\n" % header)
    for (component, profile) in roastNeeds:
        loss   = percentLoss(component, profile)
        needed = roastNeeds[(component, profile)]+cupQuantity
        roast  = needed+needed*abs(loss/100+safetyBuffer)
        r = ("Roast %.2f lbs of %s on the %s profile to yield %.2f lbs "
              "(avg. %.2f%% loss)" %
              (roast, component, profile, needed, loss))
        print(r)
        outFile.write("%s\n" % r)
    for p in subscriptions:
        s = ("\nSend a %s lb bag of %s to \n\t%s" %
                (p[2], p[1], p[0].replace('\\', '\n\t')))
        print(s)
        outFile.write("%s\n" % s)
    outFile.close()
    if emailBool:
        for e in emails:
            emailCommand = ("mailx %s < outFile.txt" % e)
            os.system(emailCommand)
### }}}

# vim: set foldmethod=marker foldlevel=0:
