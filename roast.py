#!/usr/bin/env python3

#   Copyright (c) 2016 Trey Boehm
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
#   TODO:
#       - Bagging input
#       - Optimal bagging of extra
#       - Blend calculations and output

import csv

# Columns:
#   0: ID-Tag
#   1: Profile
#   2: Date
#   3: Components
#   4: Start Weight
#   5: End Weight
#   6: Weight Loss

rawData = list(csv.reader(open('2016-07-19_90-day.csv')))
profiles = sorted(list(set([rawData[i][1] for i in range(len(rawData))])))
totals = []
for profile in profiles:
    lossPercentages = []
    greenWeight = 0
    roastWeight = 0
    zeroes = 0
    for roast in rawData:
        if roast[1] == profile:
            if roast[6] == '0':
                zeroes += 1
            else:
                lossPercentages.append(abs(float(roast[6])))
            greenWeight += float(roast[4])
            roastWeight += float(roast[5])
    dataPts = len(lossPercentages)
    average = sum(lossPercentages)/dataPts
    highest = max(lossPercentages)
    lowest  = min(lossPercentages)
    dataRange = highest-lowest
    print("%s %.2f%%" % (profile, average))
    #totals.append([profile, greenWeight, roastWeight, average, dataPts, dataRange, zeroes])

pickMeUp = {"Colombian Excelso EP":.34, "Peru ESP":.33, "Ethiopia 25":.33}
AMrescue = {"Guat ESP":.40, "Costa Rica 25":.60}
connection = {"Colombia 1":.60, "Sumatra 25":.40}
stimulate = {"Sumatra ESP":.45, "Guat ESP":.35, "Peru ESP":.10, "Ethiopian ESP":.10}
kickstart = {"Sumatra ESP":.50, "Guat ESP":.35, "Mexico ESP":.15}

blends = [pickMeUp, AMrescue, connection, stimulate, kickstart]

# All products in a dictionary as "Product Name":"Roast profile"
# TODO: Make blends happen
products = {"Bright Minds":"Colombia 1", "Burundi":"Burundi 10 kilo", "Connection Cold Brew":"blend", "Decaf":"Decaf Brazil", "Fresh Perspective":"Ethiopian 25", "Gedeb":"Gedeb 22", "Hill Country":"Brazil 25", "Huehuetenango":"Huehue", "Kenya":"Kenya 10kilo", "Kickstart":"blend", "Life Saver":"Guatemala 25 ", "Peru":"Peru ESP", "Pick-Me-Up":"Blend", "PNG":"PNG Korona 10 lbs", "Rainha":"Rainha", "Rainha Dark":"Rainha Dark", "Rise and Shine":"Sumatra ESP", "Solarte":"Solarte", "Spark":"Guat ESP", "Stimulate":"blend", "Take Me Home":"blend"}

# Columns:
#   0: Product
#   1: Amount needed (lbs)

#roastNeeds = list(csv.reader(open('roast.conf')))
#roastInput = []
#for product in roastNeeds:
#    if product[1] != "0":
#        avgLoss = float(totals[profiles.index(products[product[0]])][3])/100
#        print("Need %s lbs of %s. Average loss is %.2f%%" % (product[1], product[0], avgLoss*100))
#        print("To compensate, roast %.2f lbs." % (float(product[1])/(1-avgLoss)))
