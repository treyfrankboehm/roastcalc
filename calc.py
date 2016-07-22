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
del(single[0]) # Spreadsheet header
del(blends[0])

# Columns:
#   0: Product
#   1: num. 3 oz bags
#   2: num. 12 oz bags
#   3: num. 2 lb bags
#   4: num. 5 lb bags
orders = list(csv.reader(open('orders.csv')))
stock  = list(csv.reader(open('stock.csv')))
### }}}

### Past Roast Data {{{
def percentLoss(component, profile):
    losses = []
    for roast in history:
        if component in roast[3] and profile in roast[1]:
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
#roastInput = []
#for product in roastNeeds:
#    if product[1] != "0":
#        print(products[product[0]])
        #avgLoss = float(totals[profiles.index(products[product[0]])][3])/100
        #print("Need %s lbs of %s. Average loss is %.2f%%" % (product[1], product[0], avgLoss*100))
        #print("To compensate, roast %.2f lbs." % (float(product[1])/(1-avgLoss)))
### }}}

print(single)
print(blends)
print(products)
print(history)
print(stock)
print(orders)
# vim: set foldmethod=marker foldlevel=0:
