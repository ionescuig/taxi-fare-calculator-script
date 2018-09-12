#!/usr/bin/env python
# title           :taxi_calculator.py
# description     :A calculator for the fare for a Hackney Carriage (Black Cab) in Plymouth, UK.
# author          :Gabriel Ionescu
# date            :2018/06/11
# version         :1.0
# notes           :
# python_version  :3.6.3
# ==============================================================================

"""
work in progress...
A calculator for the fare for a Hackney Carriage (Black Cab) in Plymouth, UK.
The fare is not fixed, is affected by the traffic and tolls (ex: for Cornwall),
for 1-2 people (each extra passenger after the second passenger: 20p).

Tariff one: Monday to Saturday from 6am to 7pm
    For any distance up to one tenth of a mile:       £3.00
    The next one tenth of a mile:                     £0.30
    For each subsequent one fifth of a mile:          £0.30
    Each completed period of 90 seconds waiting time: £0.30

Tariff two: Monday to Saturday from 7pm to midnight,
            Sunday and Bank Holidays from 6am to 7pm
    For any distance up to one tenth of a mile:       £3.50
    The next one tenth of a mile:                     £0.30
    For each subsequent one fifth of a mile:          £0.30
    Each completed period of 60 seconds waiting time: £0.30

Tariff three:   Monday to Sunday from midnight to 6am
                Sunday and Bank Holidays from 7pm to midnight
    For any distance up to one tenth of a mile:       £4.00
    The next one tenth of a mile:                     £0.30
    For each subsequent one fifth of a mile:          £0.30
    Each completed period of 60 seconds waiting time: £0.30

Tariff four:    From 7pm on Christmas Eve to 7am on Christmas Day
                From 7am on Boxing Day to 7am on 27 December
                From 7pm to midnight on 31 December
                From 7am on 1 January to 7am on 2 January
    For any distance up to one tenth of a mile:       £4.50
    The next one tenth of a mile:                     £0.45
    For each subsequent one fifth of a mile:          £0.45
    Each completed period of 60 seconds waiting time: £0.45

Tariff five:    From 7am on Christmas Day to 7am on Boxing Day
                New Year's Day from midnight to 7am
    For any distance up to one tenth of a mile:       £6.00
    The next one tenth of a mile:                     £0.60
    For each subsequent one fifth of a mile:          £0.60
    Each completed period of 60 seconds waiting time: £0.60
"""

from time import strftime


def calculate(date, miles, no_of_people, toll):
    """
    calculates for a certain hour and certain miles
    """

    # fixed data
    tariff_1 = (3.0, 0.30, 0.30, 0.30)
    tariff_2 = (3.5, 0.30, 0.30, 0.30)
    tariff_3 = (4.0, 0.30, 0.30, 0.30)
    tariff_4 = (4.5, 0.45, 0.45, 0.45)
    tariff_5 = (6.0, 0.60, 0.60, 0.60)
    tariff_choice = ()
    # fare = 0
    bank_holidays = ('03/30/18', '04/02/18', '05/07/18', '05/28/18', '08/27/18',
                     '04/19/19', '04/22/19', '05/06/19', '05/27/19', '08/26/19',
                     '04/10/20', '04/13/20', '05/04/20', '05/25/20', '08/31/20', '12/28/20')

    # calculate the right tariff
    if date('%x') in bank_holidays or date('%A') == 'Sunday':
        if 6 <= int(date('%H')) < 19:
            tariff_choice = tariff_2
        elif int(date('%H')) >= 19:
            tariff_choice = tariff_3
    elif date('%m') == '01':
        if date('%d') == '01':
            if int(date('%H')) < 7:
                tariff_choice = tariff_5
            else:
                tariff_choice = tariff_4
        elif date('%d') == '02':
            if int(date('%H')) < 7:
                tariff_choice = tariff_4
    elif date('%m') == '12':
        if date('%d') == '24' and int(date('%H')) > 19:
            tariff_choice = tariff_4
        elif date('%d') == '25':
            if int(date('%H')) < 7:
                tariff_choice = tariff_4
            else:
                tariff_choice == tariff_5
        elif date('%d') == '26':
            if int(date('%H')) < 7:
                tariff_choice == tariff_5
            else:
                tariff_choice = tariff_4
        elif date('%d') == '27':
            if int(date('%H')) < 7:
                tariff_choice = tariff_4
        elif date('%d') == '31' and 19 <= int(date('%H')):
            tariff_choice = tariff_4
    elif 6 <= int(date('%H')) < 19:
        tariff_choice = tariff_1
    elif int(date('%H')) >= 19:
        tariff_choice = tariff_2
    else:
        tariff_choice = tariff_3

    # calculate the fare
    if miles < 0.1:
        fare = tariff_choice[0]
    elif miles == 0.1:
        fare = tariff_choice[0] + tariff_choice[1]
    else:
        multiplier = (miles - 0.2) // 0.2

        if miles < 5:
            waiting = miles
        else:
            waiting = 5
        waiting_time = ((waiting * tariff_choice[3]) // tariff_choice[3]) * tariff_choice[3]

        fare = tariff_choice[0] + tariff_choice[1] + tariff_choice[2] * multiplier + waiting_time
    if no_of_people > 2:
        fare += (no_of_people - 2) * 0.2
    if toll:
        fare += toll
        
    # print('tariff: ', tariff_choice)
    print('Fare: %.2f' % fare)

    
if __name__ == "__main__":
    """
    as a standalone:
    calculates the fare for this hour, for a selected number of miles
    """
    no_of_miles = float(input("Miles: "))
    no_of_people = input("Number of people: ")
    if no_of_people:
        no_of_people = int(no_of_people)
    else:
        no_of_people = 1
    toll = input("Toll: ")
    if toll:
        toll = float(toll)
    else:
        toll = 0
    calculate(strftime, no_of_miles, no_of_people, toll)
    input("\nPress any key to exit...")
