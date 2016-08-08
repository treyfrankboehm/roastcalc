#!/usr/bin/env python3

# This file is part of roastcalc
# 
# roastcalc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more detail.
# <http://www.gnu.org/licenses/>
#
# You should have received a copy of the GNU General Public License
# along with roastcalc.  If not, see <http://www.gnu.org/licenses/>.

### Define magic numbers ###
safetyBuffer = 0.005        # Add this percent to roast input weight
cupQuantity = 0.2           # Add to roast for production cupping
emailBool = False           # Email report or no?
emails = ["trey.frank.boehm@gmail.com",
          "tcobb775@gmail.com",
          "trey@ggroasting.com"]

### Import data from CSV files ###
import scrape   # Download the spreadsheet as CSV files
import csv      # Parse the CSV files
import os       # Run the email command

# Download the files 
scrape.main()

# Column indices for history.csv:
# ID-Tag, Profile, Date, Component, Start Weight, End Weight, % Loss
# 0,      1,       2,    3,         4,            5,          6
historyCSV = list(csv.reader(open("history.csv")))

# Column indices for products.csv:
# Product, Component, Component #, Roast profile, % of blend
# 1,       2,         3,           4,             5
productsCSV = list(csv.reader(open("products.csv")))
# List of available products
uniqueProducts = set([product[0] for product in productsCSV])

# Column indices for totals.csv:
# Product, 3oz, 12oz, 2lb, 5lb, total lbs, roast/don't roast [1/0]
# 0,       1,   2,    3,   4,   5,         6
totalsCSV = list(csv.reader(open("totals.csv")))
# Dict formatted for easier access
totals = {p[0]:p[1:] for p in totalsCSV}

# Column indices for subscriptions.csv:
subsCSV = list(csv.reader(open("subscriptions.csv")))
# Remove products that aren't shipping today
subscriptions = [p for p in subsCSV if p[-2] == '0']

### Percent loss calculation ###
# Return the average percent loss for a given component/profile combo
def percentLoss(component, profile):
    losses = []
    for roast in historyCSV:
        if component in roast[3] and profile in roast[1]:
            loss = float(roast[6])
            # Sometimes the loss is entered as 0.00 by mistake
            if loss != 0:
                losses.append(float(roast[6]))
    # Average the losses across all available roasts
    return sum(losses)/len(losses)

# Print the percent loss for all component/profile combos (this isn't
# actually called by the script, but it can be helpful for debugging)
def allPercentLoss():
    percents = []
    for i in range(len(products)):
        percents.append("Component %s (Profile %s): %.2f%% loss." %
                (products[i][1],
                 products[i][3],
                 percentLoss(products[i][1],
                 products[i][3])))
    for percent in sorted(list(set(percents))):
        print(percent)
    return 0

### Product information ###
# Add all of the products to the "productInfo" dict.
# (Note that single-origin and blends are treated the same way, using
# 1.00 as the percent of total for the component. This eliminates the
# need for redundant code.)
# productInfo is an associative array with each element formatted as
#   "Product Name":[
#       ["Component 1", "Roast Profile 1", "Percent 1"],
#       ["Component 2", "Roast Profile 2", "Percent 2"],
#       [...]
#   ]
productInfo = {}
for product in uniqueProducts:
    roastInfo = []
    for i in range(len(productsCSV)):
        if productsCSV[i][0] == product:
            roastInfo.append([productsCSV[i][1],
                              productsCSV[i][3],
                              productsCSV[i][4]])
    productInfo[product] = roastInfo

### Subscription handler ###
# Add subscriptions into totals, if applicable
for sub in subscriptions:
    if sub[-2] == "0": # We need to ship
        product =       sub[1]
        pounds  = float(sub[2])
        # Adjust the amount we have in the 'totals' dict
        totals[product][-2] = str(float(totals[product][-2]) + pounds)
        if float(totals[product][-2]) > 0: # If we don't have enough:
            totals[product][-1] = "1" # Set 'roast' cell to 1 so we will

### Sum roast quantities ###
# roastNeeds is an associative array with each element formatted as
#   ("Component", "Profile"):pounds
roastNeeds = {}
for product in totals:
    pounds = float(totals[product][-2])
    if pounds < 0 or totals[product][-1] == '1':
        for part in productInfo[product]:
            component =       part[0]
            profile   =       part[1]
            percent   = float(part[2])
            # Deal with an uninitialized key
            if not (component, profile) in roastNeeds:
                roastNeeds[(component, profile)] = pounds*percent
            else:
                roastNeeds[(component, profile)] += pounds*percent



### Main ###
if __name__ == "__main__":
    # Print everything to the console and write to a file (for email)
    outFile = open("report.txt", "w")
    header = ("Safety buffer percentage for roasting: %.2f%%\n"
            "Amount to add for cupping: %.2f lbs\n" %
            (100*safetyBuffer, cupQuantity))
    print("\n%s" % header)
    outFile.write("%s\n" % header)
    # Actually tell us how much to roast
    for (component, profile) in roastNeeds:
        loss   = percentLoss(component, profile)
        needed = roastNeeds[(component, profile)]+cupQuantity
        roast  = needed+needed*abs(loss/100+safetyBuffer)
        r = ("Roast %.2f lbs of %s on the %s profile to yield %.2f lbs "
              "(avg. %.2f%% loss)" %
              (roast, component, profile, needed, loss))
        if roast > 0:
            print(r)
            outFile.write("%s\n" % r)
    print("")
    outFile.write("\n")
    for p in totals:
        if totals[p][-1] == '1':
            pack = ("%s: Bag %sx3oz, %sx12oz, %sx2lb, and %sx5lb" %
                    (p, totals[p][0], totals[p][1],
                        totals[p][2], totals[p][3]))
            print(pack)
            outFile.write("%s\n" % pack)
    for p in subscriptions:
        s = ("\nSend a %s lb bag of %s to \n\t%s" %
                (p[2], p[1], p[0].replace('\\', '\n\t')))
        print(s)
        outFile.write("%s\n" % s)
    outFile.close()
    # Send emails, if applicable
    if emailBool:
        for e in emails:
            emailCommand = ("mailx %s < outFile.txt" % e)
            os.system(emailCommand)
