#!/usr/bin/env python

import csv
from datetime import datetime

# go to leagueline up and download all three leagues worth of
# schedules and save them into afc, nfc, and afl 
games = []

def strcomp(left, rite):
    if  left < rite:
        return -1

    if  left > rite:
        return 1

    return 0

def compare_dates(left, rite):
    if left['dt'] < rite['dt']:
        return -1
    elif left['dt'] > rite['dt']:
        return 1
    return 0

def compare(left, rite):
    # sort days together
    if left['day'] < rite['day']:
        return -1

    if left['day'] > rite['day']:
        return 1

    # then sort by location within the day
    val = strcomp(left['location'], rite['location'])

    if val == 0:
        # then sort by time within the location
        if left['dt'] < rite['dt']:
            val = -1
        elif left['dt'] > rite['dt']:
            val = 1

    return val

def readFile(fileName):

    with open(fileName) as csvfile:
        reader = csv.reader(csvfile, dialect='excel')

        for row in reader:

            if row[0] == 'Date':
                continue

            game = {
                'date': row[0],
                'time': row[1],
                'league': row[3],
                'away': row[4],
                'home': row[5],
                'location': row[6],
            }

            st = game['date'] + ' ' + game['time']
            game['dt'] = datetime.strptime(st, '%m/%d/%Y %I:%M%p')
            game['day'] = datetime.strptime(game['date'] + ' 12:00am', '%m/%d/%Y %I:%M%p')

            if game['location'] == 'Rec Center (Dale Blum Field)':
                game['location'] = 'Dale Blum Field'

            if game['league'] == 'AFL 11-14':
                game['league'] = 'AFL'
            elif game['league'] == 'NFC 5-7':
                game['league'] = 'NFC'
            elif game['league'] == 'AFC 8-10':
                game['league'] = 'AFC'

            games.append(game)

readFile('afc.csv')
readFile('nfc.csv')
readFile('afl.csv')

games.sort(cmp=compare_dates)
afc_count = 0
nfc_count = 0
afl_count = 0
game_count = 0

for game in games:
    game_count += 1
    game['count'] = game_count
    if game['league'] == 'AFL':
        afl_count += 1
        game['league_count'] = afl_count
    elif game['league'] == 'NFC':
        nfc_count += 1
        game['league_count'] = nfc_count
    elif game['league'] == 'AFC':
        afc_count += 1
        game['league_count'] = afc_count

games.sort(cmp=compare)

with open('sorted_games.csv', 'w') as out:
    out.write("Date,Time,,League,Visitor,Home,Location,LCount,GCount\n")
    for game in games:
        out.write("%s,%s,,%s,%s,%s,%s,%d,%d\n" % (
            game['date'],
            game['time'],
            game['league'],
            game['away'],
            game['home'],
            game['location'],
            game['league_count'],
            game['count']
        ))
