#!/usr/bin/env python

import csv
import re
import sys

# reads a csv as exported from excel and checks for teams with coaches that are coaching two teams
# to see if they have any conflicts where their two teams have back to back games

teamSchedule = dict()
games = []
teams = dict()

def fixgame(game):
    if game['loc'] == 'Century Park2':
        game['loc'] = 'Century Park 2'

    if game['loc'] == 'Century Park1':
        game['loc'] = 'Century Park 1'

    if game['loc'] == 'Rec Center':
        game['loc'] = 'Rec Center (Dale Blum Field)'

    game['mmddyy'] = game['day'].split(' ')[1] + '/17'

    iTime = getTime(game['time'])
    game['hhmm'] = hhmm(iTime)

def create_day_dict(schdule):

    dayDict = dict()

    for evt in schdule:
        day = evt['day']

        if not day in dayDict:
            dayDict[day] = evt

    return dayDict

def hhmm(time):
    if time == 10:
        return '10:00 am'
    if time == 11:
        return '11:00 am'
    if time == 12:
        return '12:00 pm'
    if time == 13:
        return '1:00 pm'
    if time == 14:
        return '2:00 pm'
    if time == 15:
        return '3:00 pm'
    if time == 16:
        return '4:00 pm'
    if time == 17:
        return '5:00 pm'
    if time == 18:
        return '6:00 pm'
    if time == 19:
        return '7:00 pm'
    if time == 20:
        return '8:00 pm'

    if time == 13.5:
        return '1:30 pm'
    if time == 14.5:
        return '2:30 pm'
    if time == 15.5:
        return '3:30 pm'
    if time == 16.5:
        return '4:30 pm'
    if time == 17.5:
        return '5:30 pm'

    print time
    raise 'shit'

def getTime(time):

    if time == '10am':
        return 10
    if time == '11am':
        return 11
    if time == '12pm':
        return 12
    if time == '1pm':
        return 13
    if time == '2pm':
        return 14
    if time == '3pm':
        return 15
    if time == '4pm':
        return 16
    if time == '5pm':
        return 17
    if time == '6pm':
        return 18
    if time == '7pm':
        return 19
    if time == '8pm':
        return 20

    if time == '1:30pm':
        return 13.5
    if time == '2:30pm':
        return 14.5
    if time == '3:30pm':
        return 15.5
    if time == '4:30pm':
        return 16.5
    if time == '5:30pm':
        return 17.5

    print time
    raise 'shit'

def check_two(t1Name, t2Name, backToBackOkay=False):
    t1 = teamSchedule[t1Name]
    t2 = teamSchedule[t2Name]

    t1DayDict = create_day_dict(t1)
    t2DayDict = create_day_dict(t2)

    days = set(t1DayDict.keys() + t2DayDict.keys())

    print "########################################"
    print t1Name, t2Name
    print "########################################"
    first = True
    for day in days:
        first = False
        # print day
        try:
            d1 = t1DayDict[day]
            d2 = t2DayDict[day]

            time1 = getTime(d1['time'])
            time2 = getTime(d2['time'])

            if abs(time1 - time2) < 2:
                if not backToBackOkay:
                    print day
                    print t1Name, "at", d1['loc'], d1['time']
                    print t2Name, "at", d2['loc'], d2['time']
                else:
                    if d1['loc'] != d2['loc']:
                        print day
                        print t1Name, "at", d1['loc'], d1['time']
                        print t2Name, "at", d2['loc'], d2['time']

        except KeyError as e:
            pass
            # print 'One game for', day

def addSchedule(team, schedule):
    teamSchedule[team].append(schedule)

def addTeam(team):
    if not team in teamSchedule:
        teamSchedule[team] = list()

with open('/vagrant/orig.csv') as csvfile:
    reader = csv.reader(csvfile, dialect='excel')

    for row in reader:
        home = row[6]
        away = row[7]
        loc = row[2]
        day = row[3]
        time = row[4]
        division = row[5]

        schedule = {
            'time': time,
            'day': day,
            'loc': loc
        }

        addTeam(home);
        addTeam(away);

        addSchedule(home, schedule)
        addSchedule(away, schedule)

        # populate game and teams
        if loc == 'Field' or ' ' in home or time == 'Varies' or time == '??':
            continue

        game = {
            'time': time,
            'day': day,
            'loc': loc,
            'division': division,
            'home': home,
            'away': away
        }

        if game['loc'] != '':
            fixgame(game)
            games.append(game)

            if not division in teams:
                teams[division] = dict()

            teams[division][home] = True
            teams[division][away] = True

check_two("Dolphins", "Storm")
check_two("Bears", "Jaguars")
check_two("Bears", "Thunder")
check_two("Steelers", "Fury")

# these teams are assistants for at least one of the team so they don't necessarily need
# the one hour gap, but they do need to be on the same field
check_two("Jets", "Storm", True)
check_two("Texans", "Outlaws", True)
check_two("Buccaneers", "Ravens", True)
check_two("Ravens", "Blaze", True)

check_two("Broncos", "Rush", True)

# these are spectators so it isn't as important to have the hour gap
# however it would be nice if they could be at the same field back to back
# thus the True
check_two("Falcons", "Steelers", True)
check_two("Steelers", "Rattlers", True)

with open('/vagrant/teams.csv', 'w') as outFile:
    for div in teams:
        sys.stderr.write('Division ' + div + ' team count: ' + str(len(teams[div])) + '\n')
        for team in teams[div]:
            outFile.write(div + ',' + team + '\n')

with open('/vagrant/schedule.csv', 'w') as outFile:
    for game in games:
        outFile.write(game['mmddyy'] + ','
                    + game['hhmm'] + ','
                    + game['loc'] + ','
                    + game['away'] + ','
                    + game['home'] + ','
                    + game['division']
                    + '\n'
        )

