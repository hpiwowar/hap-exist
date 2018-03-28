import os
import datetime
from dateutil import parser
from exist import Exist

### this is super ugly, pulled together one afternoon in a coffee shop.
## not going to spend any time cleaning or documenting
## but if it helps you, then here you go world!  :)


exist = Exist(os.getenv("EXIST_CLIENT_ID"), os.getenv("EXIST_CLIENT_SECRET"), os.getenv("EXIST_ACCESS_TOKEN"))
# print (exist.user())
# print (exist.attributes())
# print(exist.correlations())

# typo "arquire" is in the library
exist.arquire_attributes([{"name":"instagram_likes", "active":True}])
exist.arquire_attributes([{"name":"instagram_comments", "active":True}])
exist.arquire_attributes([{"name":"instagram_posts", "active":True}])

print [a.label for a in exist.owned_attributes()]
[str(a) for a in exist.owned_attributes()]

# Data is from "Hormonal characteristics of the human menstrual cycle throughout reproductive life." J Clin Invest. 1975;55(4):699-706. doi:10.1172/JCI107979
# Figure 3: "The mean and range of serum LH, FSH, E., and P in five women, age 40-41, are compared to the mean +2 SEM in 10 cycles in women aged 18-30."
# testosterone from a variety of sources, estimated
# ovulation is right after the high day
# assumes 27 day cycle

hormone_levels_by_day = [
#    {"estrogen": 40, "progesterone": 0, "testosterone": 0},  # day 0, first day of bleeding
    {"estrogen": 45, "progesterone": 0, "testosterone": 0},
    {"estrogen": 50, "progesterone": 0, "testosterone": 0},
    {"estrogen": 70, "progesterone": 0, "testosterone": 0},
    {"estrogen": 90, "progesterone": 0, "testosterone": 0},
    {"estrogen": 110, "progesterone": 0, "testosterone": 0},
    {"estrogen": 130, "progesterone": 0, "testosterone": 0},
    {"estrogen": 150, "progesterone": 0, "testosterone": 0},
    {"estrogen": 190, "progesterone": 1, "testosterone": 0},
    {"estrogen": 210, "progesterone": 1, "testosterone": 2},
    {"estrogen": 210, "progesterone": 1, "testosterone": 6},
    {"estrogen": 300, "progesterone": 2, "testosterone": 9},
    {"estrogen": 400, "progesterone": 3, "testosterone": 10}, # estrogen peak
    {"estrogen": 120, "progesterone": 4, "testosterone": 9},  #ovulation, the day after the peak; period normally lasts for standard 14 days after this
    {"estrogen": 100, "progesterone": 10, "testosterone": 6},
    {"estrogen": 100, "progesterone": 22, "testosterone": 2},
    {"estrogen": 110, "progesterone": 26, "testosterone": 0},
    {"estrogen": 110, "progesterone": 30, "testosterone": 0},
    {"estrogen": 120, "progesterone": 28, "testosterone": 0},
    {"estrogen": 130, "progesterone": 25, "testosterone": 0},
    {"estrogen": 170, "progesterone": 22, "testosterone": 0},
    {"estrogen": 160, "progesterone": 25, "testosterone": 0},
    {"estrogen": 120, "progesterone": 23, "testosterone": 0},
    {"estrogen": 100, "progesterone": 17, "testosterone": 0},
    {"estrogen": 80, "progesterone": 13, "testosterone": 0},
    {"estrogen": 60, "progesterone": 8, "testosterone": 0},
    {"estrogen": 60, "progesterone": 8, "testosterone": 0},
    {"estrogen": 60, "progesterone": 8, "testosterone": 0},
    {"estrogen": 60, "progesterone": 8, "testosterone": 0},
    {"estrogen": 60, "progesterone": 8, "testosterone": 0},
    {"estrogen": 60, "progesterone": 8, "testosterone": 0}
    ]

period_start_date_strings = [
    "2017-11-23",
    "2017-12-20",
    "2018-01-17",
    "2018-02-14",
    "2018-03-14"
]
start_dates = [parser.parse(x) for x in period_start_date_strings]

def update_exist(my_day, levels):
    my_day_str = my_day.isoformat()[0:10]
    print "saving {} for {}".format(levels, my_day_str)
    response = exist.update_attributes([
        {"name": "instagram_likes", "date": my_day_str, "value":levels["estrogen"]},
        {"name": "instagram_comments", "date": my_day_str, "value":levels["progesterone"]},
        {"name": "instagram_posts", "date": my_day_str, "value":levels["testosterone"]}
    ])

def run():
    my_day = parser.parse("2017-11-24")
    previous_period_start = None
    while my_day <= datetime.datetime.now():
        for start_date in sorted(start_dates):
            if start_date <= my_day:
                previous_period_start = start_date
        days_into_period = (my_day - previous_period_start).days
        print "days_into_period", days_into_period
        levels = hormone_levels_by_day[days_into_period]
        update_exist(my_day, levels)
        my_day = my_day + datetime.timedelta(days=1)


run()
