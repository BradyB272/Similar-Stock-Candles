
import matplotlib.dates as mdates
from matplotlib import style
import pandas as pd
import re
import statistics
import numpy as np
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

style.use('ggplot')


df = pd.read_csv('nee.csv', parse_dates = True, index_col=0)
df = df.drop(columns="Volume")


opencol = df.iloc[0:,2] #this selects and prints all the open columns
closecol = df.iloc[0:,3]
highcol = df.iloc[0:,0]
lowcol = df.iloc[0:,1]
rn = 0.125
relclose = ((closecol-opencol)/opencol) * 100
relclose.rename("relclose", inplace = True)
rchigh = relclose + rn
rclow = relclose - rn
relhigh = ((highcol-opencol)/opencol) * 100
relhigh.rename("relhigh", inplace = True)
rhhigh = relhigh + rn
rhlow = relhigh - rn
rellow = ((lowcol-opencol)/opencol) * 100
rellow.rename("rellow", inplace = True)
rlhigh = rellow + rn
rllow = rellow - rn
opencollist = list(opencol)
closecollist = list(closecol)
highcollist = list(highcol)
lowcollist = list(lowcol)
df['relclose'] = relclose #adds relative close to df
df['relhigh'] = relhigh
df['rellow'] = rellow
rchigh = list(rchigh)
rclow = list(rclow)
relclosediff = list(zip(rchigh, rclow))
relhighdiff = list(zip(rhhigh,rhlow))
rellowdiff = list(zip(rlhigh, rllow))
listall = list(zip(relclosediff, relhighdiff, rellowdiff))
df = df.round(6)

#LOOP THROUGH THE RELATIVE CLOSING PRICES#
listofrelclose = list()
for x in relclosediff:
    if relclose[0] <= x[0] and relclose[0] >= x[1]:
        listofrelclose.append(x)
lorclist = list(zip(*listofrelclose)) #this unzips the list of tuples and makes two lists
lorclist1 = list(lorclist[0])
relclosematch = list()
for l in lorclist1:
    l = l - rn
    l = "%.6f" % l #note this makes the value only a certain amount of decimal points
    relclosematch.append(l)
####

#LOOP THROUGH THE RELATIVE HIGH PRICES#
listofrelhigh = list()
for j in relhighdiff:
    if relhigh[0] <= j[0] and relhigh[0] >= j[1]:
        listofrelhigh.append(j)
lorhlist = list(zip(*listofrelhigh))
lorhlist1 = list(lorhlist[0])
relhighmatch = list()
for k in lorhlist1:
    k = k - rn
    k = "%.6f" % k
    relhighmatch.append(k)
####

#LOOP THROUGH THE RELATIVE LOW PRICES#
listofrellow = list()
for q in rellowdiff:
    if rellow[0] <= q[0] and rellow[0] >= q[1]:
        listofrellow.append(q)
lorllist = list(zip(*listofrellow))
lorllist1 = list(lorllist[0])
rellowmatch = list()
for w in lorllist1:
    w = w - rn
    w = "%.6f" % w
    rellowmatch.append(w)
####

#COMPARE THE MATCHES WITH THE ORIGINAL DATA TO PULL THE DATES#
compareclose = df['relclose'].isin(relclosematch)
df['Bool'] = compareclose

comparehigh = df['relhigh'].isin(relhighmatch)
df['Bool2'] = comparehigh

comparelow = df['rellow'].isin(rellowmatch)
df['Bool3'] = comparelow
####

# SELECTS ALL ROWS THAT FALL IN RANGE #
allrowslist = df.index[(df['Bool'] == True) & (df['Bool2'] == True) & (df['Bool3'] == True)].tolist()
finalrows = df.loc[allrowslist] #this locates all rows that meet range condidtion
print(finalrows)
####
