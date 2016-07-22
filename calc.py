#!/usr/bin/env python3

#   Copyright (c) Greater Goods Roasting
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more detail.
#   <http://www.gnu.org/licenses/>

import csv

### Import Data from CSV Files {{{
# Columns:
#   0: ID-Tag
#   1: Profile
#   2: Date
#   3: Component
#   4: Start Weight
#   5: End Weight
#   6: Percent Loss
history = list(csv.reader(open('history.csv')))

# Columns:
#   0: Product Name
#   1: Component Name
#   2: Component Number
#   3: Roast Profile
#   4: Percent of blend (blend.csv only)
single = list(csv.reader(open('single.csv')))
blends = list(csv.reader(open('blends.csv')))

# Columns:
#   0: Product
#   1: num. 3 oz bags
#   2: num. 12 oz bags
#   3: num. 2 lb bags
#   4: num. 5 lb bags
#   5: total lbs (totals.csv only)
orders = list(csv.reader(open('orders.csv')))
stock  = list(csv.reader(open('stock.csv')))
totals = list(csv.reader(open('totals.csv')))
### }}}

### Past Roast Data {{{
def percentLoss(component, profile):
    losses = []
    for roast in history:
        if component in roast[3] and profile in roast[1]:
            loss = float(roast[6])
            if loss != 0:
                losses.append(float(roast[6]))
    return sum(losses)/len(losses)

def allPercentLoss():
    percents = []
    for i in range(len(single)):
        percents.append("Component %s (Profile %s): %.2f%% loss." % (single[i][1], single[i][3], percentLoss(single[i][1], single[i][3])))
    for i in range(len(blends)):
        percents.append("Component %s (Profile %s): %.2f%% loss." % (blends[i][1], blends[i][3], percentLoss(blends[i][1], blends[i][3])))
    for p in sorted(list(set(percents))):
        print(p)
    return 0
### }}}

### Product Information {{{
# Dictionary (associative array) of all the products, taken from the spreadsheet
products = {}

# Add all of the single-origin products to the "products" dict.
# "Product Name":["Component Name", "Roast Profile"]
for i in range(len(single)):
    products[single[i][0]] = [single[i][1],single[i][3]]

# Add all of the blends to the "products" dict:
# "Blend Name":[["Component 1","Roast Profile 1","Percent 1"],
#       ["Component 2", "Roast Profile 2", "Percent 2"], [etc]]
# Get a unique list of all the available blends
uniqueBlends = set([blend[0] for blend in blends])
for blend in uniqueBlends:
    components = []
    for i in range(len(blends)):
        if blends[i][0] == blend:
            components.append([blends[i][1], blends[i][3], blends[i][4]])
    products[blend] = components
### }}}

### Roast Needs Calculation {{{
roastNeeds = {}
safetyBuffer = 0.5

# This code is disgusting. My condolences to whomever reads it.
for i in range(len(totals)):
    pounds = float(totals[i][5])
    if pounds != 0:
        product = totals[i][0]
        if product in uniqueBlends:
            for i in range(len(products[product])):
                component =       products[product][i][0]
                profile   =       products[product][i][1]
                percent   = float(products[product][i][2])
                try:
                    roastNeeds[(component, profile)] += pounds*percent
                except KeyError:
                    roastNeeds[(component, profile)] = pounds*percent
        else:
            component = products[product][0]
            profile   = products[product][1]
            try:
                roastNeeds[(component, profile)] += pounds
            except KeyError:
                roastNeeds[(component, profile)] = pounds

for (component, profile) in roastNeeds:
    loss   = percentLoss(component, profile)
    needed = roastNeeds[(component, profile)]
    roast  = needed+needed*abs(loss/100)+safetyBuffer
    print("Roast %.2f lbs of %s on the %s profile to yield %.2f lbs (avg. %.2f%% loss plus %.2f lbs safety buffer)."
            % (roast, component, profile, needed, loss, safetyBuffer))

#print("%.2f pounds of %s needed. Roast %.2f pounds (historic %.2f%% loss plus %.2f lb buffer) on the %s profile."
#        % (pounds, component, pounds+pounds*abs(loss/100)+safetyBuffer, loss, safetyBuffer, profile))
# vim: set foldmethod=marker foldlevel=1:
