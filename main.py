import os
import json
import datetime as dt
import statistics
import calendar
import math
import dateutil.relativedelta
from colors import color

os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    # dic = json.load(open(os.getcwd()+'/stats.json'))
    sett = json.load(open(os.getcwd()+'/config.toml'))
    stepno = sett["stepno"]
except:
    stepno = 4

step_to4 = [ [0, 4], [0, 2, 4], [0, 1, 3, 4] ]

def vcol(dic, y):
    if y[0] == "#":
        y = y[1:]
    hex = False
    if len(y) == 3 or len(y) == 6:
        hex = True
        for x in y:
            if x.lower() not in "0123456789abcdef":
                hex = False

    if hex:
        return "#" + y
    else:
        found = False
        for x in dic:
            if x[0] == y:
                found = True
                return vcol(dic, x[1])
        bit34 = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
        if y in bit34 or y[7:] in bit34:
            found = True
            return y 
        if not found:
            print(f"invalid color {y}.")
            exit()

def ccol(dic, col):
    lis = []
    for y in col:
        lis.append(vcol(dic, y))
    return lis

def cday(day):
    try:
        day = dt.date.fromisoformat(day)
    except:
        match day:
            case "tdy":
                return dt.date.today()
            case "yst":
                return dt.date.today() - dt.timedelta(days=1)
            case "sun" | "mon" | "tue" | "wed" | "thu" | "fri" | "sat":
                ds = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
                wd = dt.date.today().weekday()

                if dt.date.today().weekday() < 5:
                    sat = dt.date.today() + dt.timedelta(days=5-wd)
                elif dt.date.today().weekday() == 6:
                    sat = dt.date.today() + dt.timedelta(days=6)
                else:
                    sat = dt.date.today()

                return sat - dt.timedelta(days=6-ds.index(day))
            case _:
                if isinstance(day, dt.date):
                    return day
                else:
                    exit()
    else:
        return day

def rearr(dic, habit1, habit2):
    lis = []

    for habit in dic:
        lis.append(habit)

    lis.remove(habit1)
    ind = lis.index(habit2)
    lis.insert(ind + 1, habit1)

    return {habit : dic[habit] for habit in lis}

def newyear(json, habit, year):
    nmth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    lmth = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    json[habit] = {
        str(year) : []
    }

    for x in range(12):
        json[habit][str(year)].append([])
        if int(year) % 4 == 0:
            for x in range(lmth[x]):
                json[habit][str(year)][-1].append(0)
        else:
            for x in range(nmth[x]):
                json[habit][str(year)][-1].append(0) 

def add(json, habit):
    if habit in json:
        print(f"    habit '{habit}' already exists.")
    else:
        tyr = dt.date.today().year
        newyear(json, habit, tyr)
        json[habit]["stepno"] = 4
        print(f"    habit '{habit}' added.")

def track(json, day, habit, ono):
    ono = int(ono)
    if habit in json:
        try:
            stepno = json[habit]["stepno"]
        except:
            json[habit]["stepno"] = 4
            stepno = 4
        if ono <= stepno and ono >= 0:
            date = ()
            
            day = cday(day)
            date = (day.year, day.month, day.day)
            
            if str(date[0]) not in json[habit]:
                newyear(json, habit, date[0])
           
            if stepno != 4:
                no = step_to4[stepno-1][ono]
                json[habit][str(date[0])][date[1]-1][date[2]-1] = no
            else:
                json[habit][str(date[0])][date[1]-1][date[2]-1] = ono

def multitrack(json, day):
    lis = []
    max = 0

    for habit in json:
        if len(habit) > max:
            max = len(habit)
        lis.append(habit)

    for habit in lis:
        sn = json[habit]["stepno"]
        spaces = (max-len(habit))*" "
        ono = input(f"    {spaces}{habit}? ({sn}) ")
        track(json, day, habit, ono)
    

def daymap(begin, end, col, json, bydur):
    col = ccol([], col)
    if col == []:
        col = ["#FFFFFF"]

    begin = str(begin)
    end = str(end)

    match len(begin):
        case 10:
            begin = dt.date.fromisoformat(begin)
        case 7:
            begin = dt.date.fromisoformat(begin + "-01")
        case 4:
            begin = dt.date.fromisoformat(begin + "-01-01")

    match len(end):
        case 10:
            end = dt.date.fromisoformat(end)
        case 7:
            end = dt.date.fromisoformat(end + "-" + str(calendar.monthrange(int(end[0:4]), int(end[5:7]))[1]))
        case 4:
            end = dt.date.fromisoformat(end + "-12-31")

    st = cday(begin)
    end = cday(end)

    max = 2
    lis = ["yy", "mm", "dd"]
    
    for habit in list(json.keys()) + ["overall", ""]:
        habit = habit.strip()
        if len(habit) > max:
            max = len(habit)
        lis.append(habit)

    if len(lis) <= 4:
        print("    you have no habits. please add a habit and try again.")
        exit()

    strings = {}

    start = st
    ps = st
        # start += dt.timedelta(days=1) 
    colno = 0

    while start <= end:
        match bydur:
            case "day":
                ns = start + dateutil.relativedelta.relativedelta(days=+1)
            case "week":
                if start.weekday() != 6:
                    ns = start
                    while ns.weekday() != 6:
                        ns += dateutil.relativedelta.relativedelta(days=+1)
                else:
                    ns = start + dateutil.relativedelta.relativedelta(days=+7)
            case "month":
                if start.day != 1:
                    ns = start
                    while ns.day != 1:
                        ns += dateutil.relativedelta.relativedelta(days=+1)
                else:
                    ns = start + dateutil.relativedelta.relativedelta(months=+1)
            case "year":
                if start.day != 1 and start.month != 1:
                    ns = start
                    while ns.day != 1 and ns.month != 1:
                        ns += dateutil.relativedelta.relativedelta(days=+1)
                else:
                    ns = start + dateutil.relativedelta.relativedelta(years=+1)
            case _:
                print("    invalid bydur.")
                exit()

        date = (start.year, start.month, start.day)
        nums = []
        for habit in lis:
            try:
                string = strings[habit]
            except:
                string = habit
                while len(string) < max:
                    string = " " + string
                string = "    " + string + " "

            if habit == "overall":
                num = math.floor(statistics.mean(nums))
                match num:
                    case 0:
                        string += "  "
                    case 1:
                        string += "░░"
                    case 2:
                        string += "▒▒"
                    case 3:
                        string += "▓▓"
                    case 4:
                        string += "██"
            elif habit == "":
                num = int(round(statistics.mean(nums)/4, 2)*100)
                if num < 10:
                    num = "0" + str(num)
                elif num == 100:
                    num = "!!"
                string += str(num)
            elif habit in ["yy", "mm", "dd"]:
                match habit:
                    case "yy":
                        if ps.year != start.year or start == st or start == end or ns > end:
                            if start.year < 10:
                                string += "0" + str(start.year)
                            else:
                                string += str(start.year)[-2:]
                        else:
                            string += "  "
                    case "mm":
                        if bydur == "year":
                            string += "  "
                        elif ps.month != start.month or start == st or start == end or ns > end:
                            if start.month < 10:
                                string += "0" + str(start.month)
                            else:
                                string += str(start.month)
                        else:
                            string += "  "
                    case "dd":
                        if bydur == "month" or bydur == "year":
                            string += "  "
                        elif bydur == "week" or ns > end:
                            if start.day < 10:
                                string += "0" + str(start.day)
                            else:
                                string += str(start.day)
                        elif start.day == 1:
                            string += "01"
                        elif start.day == 5:
                            string += "05"
                        elif start.day == 30 and calendar.monthrange(start.year, start.month)[1] in [30, 31] and start != st and start != end:
                            string += "  "
                        elif start.day % 5 == 0 or start == st or start == end or start.day - ps.day != 1:
                            if start.day < 10:
                                string += "0" + str(start.day)
                            else:
                                string += str(start.day)
                        else:
                            string += "  "
            else:
                snums = []
                sta = start
                while sta < ns:
                    try:
                        num = json[habit][str(sta.year)][sta.month-1][sta.day-1]
                    except:
                        newyear(json, habit, date[0])
                        num = 0
                    nums.append(num)
                    snums.append(num)
                    sta += dateutil.relativedelta.relativedelta(days=+1)
                
                num = math.floor(statistics.mean(snums))
                match num:
                    case 0:
                        string += "  "
                    case 1:
                        string += "░░"
                    case 2:
                        string += "▒▒"
                    case 3:
                        string += "▓▓"
                    case 4:
                        string += "██" 
            strings[habit] = string

        ps = start
        start = ns
        colno += 1
    
    output = ""

    for x in strings:
        output += strings[x] + "\n"
        
    return output


def monthmap(begin, end, col, json):
    begin = dt.date.isoformat(dt.datetime.combine(dt.date(int(begin[0:4]), int(begin[5:7]), 1), dt.datetime.min.time()))
    end = dt.date.isoformat(dt.datetime.combine(dt.date(int(end[0:4]), int(end[5:7]), [1]), dt.datetime.min.time()))
    return daymap(begin, end, col, json, "day")

def yearmap(year, habit, col, json):
    try:
        stat = json[habit][str(year)]
    except:
        newyear(json, habit, year)
        stat = json[habit][str(year)]
    yearindow = [[], [], [], [], [], [], []]
    strings = []
    months = [0]
    weekcount = 0
    def twkd(date):
        if date.weekday() == 6:
            return 0
        else:
            return date.weekday() + 1
    for x in range(twkd(dt.date(dt.date.today().year,1,1))):
        yearindow[x].append(0)
    for x in range(12):
        for y in range(len(stat[x])):
            yearindow[twkd(dt.date(int(year),x+1,y+1))].append(int(stat[x][y]))
            if twkd(dt.date(int(year),x+1,y+1)) == 6:
                weekcount += 1
        months.append(weekcount)

    months = months[:-1]
    monstr = "        "
    colno = 0
    for x in range(len(months)):
        while len(monstr) < months[x] * 2 + 8:
            monstr = monstr + ("  ")
        if x+1 < 10:
            monstr = monstr + "0" + str(x+1)
        else:
            monstr = monstr + str(x+1)
        colno += 1
    strings.append(monstr)

    colno = 0
    for x in range(len(yearindow)):
        days = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
        string = "    " + days[x] + " "
        co = col[colno % len(col)]
        for y in yearindow[x]:
            try:
                int(y) 
            except:
                string += "  "
            else:
                match y:
                    case 0:
                        string += "  "
                    case 1:
                        string += "░░"
                    case 2:
                        string += "▒▒"
                    case 3:
                        string += "▓▓"
                    case 4:
                        string += "██"
        strings.append(string)
        colno += 1

    output = ""
    for x in strings:
        output += x + "\n"
    return output
