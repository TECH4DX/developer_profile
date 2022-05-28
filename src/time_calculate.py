import datetime
import chinese_calendar

## Time format: 2022-05-18T17:37:38+08:00

def overlap_calculate(start, end, interval_begin, interval_end):

    left = max(start, interval_begin)
    right = min(end, interval_end)
    overlap = int((right - left).total_seconds()/60)

    return max(overlap, 0)

def time_calculate_in_one_day(start_time, end_time):
    signal = 1
    if start_time > end_time:
        signal = -1
        start_time, end_time = end_time, start_time

    interval_begin = start_time.replace(hour=9)
    interval_begin = interval_begin.replace(minute=0)
    interval_begin = interval_begin.replace(second=0)
    interval_end = end_time.replace(hour=12)
    interval_end = interval_end.replace(minute=0)
    interval_end = interval_end.replace(second=0)

    time_count = overlap_calculate(start_time, end_time, interval_begin, interval_end)

    interval_begin = interval_begin.replace(hour=14)
    interval_end = interval_end.replace(hour=18)
    time_count += overlap_calculate(start_time, end_time, interval_begin, interval_end)

    return time_count * signal

def time_calculate(start_date, end_date):
    
    start = datetime.datetime.strptime(start_date, r"%Y-%m-%dT%H:%M:%S+08:00")
    end = datetime.datetime.strptime(end_date, r"%Y-%m-%dT%H:%M:%S+08:00")

    if start_date > end_date:
        start_date, end_date = end_date, start_date

    time_all = 0

    while(start < end or start.day == end.day):
        if start.day == end.day and start.month == end.month and start.year == end.year:
            time_all += time_calculate_in_one_day(start, end)
            break
        else:
            if chinese_calendar.is_workday(start):
                time_all += (7*60)
                start += datetime.timedelta(days=1)
            else:
                start = start.replace(hour=8)
                start = start.replace(minute=0)
                start = start.replace(second=0)
                start += datetime.timedelta(days=1)
    print(datetime.datetime.strftime(start, r"%Y-%m-%dT%H:%M:%S+08:00"))
    print(datetime.datetime.strftime(end, r"%Y-%m-%dT%H:%M:%S+08:00"))

    return time_all

if __name__ == "__main__":
    time_diff = time_calculate("2022-05-18T17:37:38+08:00", "2022-05-20T17:37:38+08:00")
    print(time_diff)