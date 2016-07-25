#!/usr/bin/env python3

### Import data from CSV files ### {{{
import csv

# Column indices for history.csv:
# ID-Tag, Profile, Date, Component, Start Weight, End Weight, % Loss
# 0,      1,       2,    3,         4,            5,          6
history = list(csv.reader(open('history.csv')))

# Column indices for products.csv:
# Product, Component, Component #, Roast profile, % of blend
# 1,       2,         3,           4,             5
products = list(csv.reader(open('products.csv')))

# Column indices for totals.csv:
# Product, 3oz, 12oz, 2lb, 5lb, total lbs, roast/don't roast [1/0]
# 0,       1,   2,    3,   4,   5,         6
raw_totals = list(csv.reader(open('totals.csv')))
# Remove products that don't need to be roasted (no orders)
totals = [p for p in raw_totals if p[-1] == '1']

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
# Add $safetyBuffer$ pounds to each roast input weight
safetyBuffer = 0.5

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
# }}}

### Main ### {{{
if __name__ == "__main__":
    for (component, profile) in roastNeeds:
        loss   = percentLoss(component, profile)
        needed = roastNeeds[(component, profile)]
        roast  = needed+needed*abs(loss/100)+safetyBuffer
        print("Roast %.2f lbs of %s on the %s profile to yield %.2f lbs"
              "(avg. %.2f%% loss plus %.2f lbs as a safety buffer)."
              % (roast, component, profile, needed, loss, safetyBuffer))
### }}}

# vim: set foldmethod=marker foldlevel=0:
