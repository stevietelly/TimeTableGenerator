from Logic.DateTime.Day import Day
from Logic.DateTime.Time import Time
from Logic.DateTime.DayTime import DayTime
from Logic.DateTime.Week import Week
from Assets.Functions.Functions import get_data_list

def test_days():
    # create some sample days, times, and daytimes
    nine_am = Time("9:00am")
    ten_am = Time("10:00am")
    eleven_am = Time("11:00am")
    twelve_pm = Time("12:00pm")
    one_pm = Time("1:00pm")
    two_pm = Time("2:00pm")
    three_pm = Time("3:00pm")
    four_pm = Time("4:00pm")
    five_pm = Time("5:00pm")

    all_times = [nine_am, ten_am, eleven_am, twelve_pm, one_pm, two_pm, three_pm, four_pm, five_pm]

    monday = Day("Monday", ten_am, five_pm)
    tuesday = Day("Tuesday", ten_am, five_pm)
    wednesday = Day("Wednesday", ten_am, five_pm)
    thursday = Day("Thursday", ten_am, five_pm)
    friday = Day("Friday", ten_am, five_pm)

    dt1 = DayTime(monday, nine_am)
    dt2 = DayTime(monday, ten_am)
    dt3 = DayTime(tuesday, nine_am)
    dt4 = DayTime(tuesday, ten_am)
    dt5 = DayTime(wednesday, nine_am)
    dt6 = DayTime(wednesday, ten_am)

    all_daytimes = [dt1, dt2, dt3, dt4, dt5, dt6]

    # create a sample week
    week = [monday, tuesday, wednesday, thursday, friday]

    # test the traverse function
    days = get_data_list(week, 3, monday, "after")
    assert str(days) == "[Day:->Tuesday, Day:->Wednesday, Day:->Thursday]"

    times = get_data_list(all_times, 2, nine_am, "after")
   
    assert str(times) == "[10:00am, 11:00am]"

    daytimes = get_data_list(all_daytimes, 3, dt1, "after")
    assert str(daytimes) == "[DayTime:->Monday at 10:00am, DayTime:->Tuesday at 9:00am, DayTime:->Tuesday at 10:00am]"

    days2 = get_data_list(week, 0, monday, "after")
    assert str(days2) == "[Day:->Tuesday, Day:->Wednesday, Day:->Thursday, Day:->Friday]"

    # test the traverse function using before
    days = get_data_list(week, 3, thursday, "before")
    assert str(days) == "[Day:->Wednesday, Day:->Tuesday, Day:->Monday]"



    times2 = get_data_list(all_times, 2, three_pm, "before")

    assert str(times2)  == "[12:00pm, 11:00am]"

    daytimes3 = get_data_list(all_daytimes, 3, dt6, "before")
    assert str(daytimes3)  == f'[DayTime:->Wednesday at 9:00am, DayTime:->Tuesday at 10:00am, DayTime:->Tuesday at 9:00am]'

    days2 = get_data_list(week, 0, friday, "before")
    assert str(days2)  == "[Day:->Thursday, Day:->Wednesday, Day:->Tuesday, Day:->Monday]"

test_days()




  