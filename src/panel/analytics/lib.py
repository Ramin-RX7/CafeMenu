import datetime
from orders.models import Order



def dict_to_list(data:dict, value_item:str=None,thisweek=False,lastweek=False,last7days=False,thismonth=False,lastmonth=False,last30days=False ,hour=False):
    all_orders = Order.objects.all()
    today_date = datetime.datetime.today()
    week_day = today_date.weekday()
    to_day = today_date.day

    last_day = today_date - datetime.timedelta(1)

    this_week = today_date - datetime.timedelta(week_day)
    last_week = today_date - datetime.timedelta(week_day+7)

    this_month = today_date - datetime.timedelta(to_day)
    last_month = today_date - datetime.timedelta(to_day + 30)

    last_7_days = datetime.datetime.today() - datetime.timedelta(7)
    last_30_days = datetime.datetime.today() - datetime.timedelta(30)


    list_data = []
    # if hour:
    #     for i in range(0,24):
    #         for item in data:
    #             if int(item['hour']) == i:
    #                 list_data.append(item[value_item])
    #                 break
    #         else:
    #             list_data.append(0)

    if thisweek:
        for i in range(int((today_date - this_week).days)+1):
            date = str((this_week + datetime.timedelta(i)).date())
            # print("this",date)
            for item in data:
                if str(item['day']) == date:
                    list_data.append(item[value_item])
                    break
            else:
                list_data.append(0)

    if lastweek:
        for i in range(int((this_week - last_week).days)):
            date = str((last_week + datetime.timedelta(i)).date())
            # print("last",date)
            for item in data:
                if str(item['day']) == date:
                    list_data.append(item[value_item])
                    break
            else:
                list_data.append(0)

    if last7days:
        for i in range(int((today_date - last_7_days).days)):
            date = str((last_7_days+ datetime.timedelta(i)).date())
            for item in data:
                if str(item['day']) == date:
                    list_data.append(item[value_item])
                    break
            else:
                list_data.append(0)

    if thismonth:
        for i in range(int((today_date - this_month).days)+1):
            date = str((this_month + datetime.timedelta(i)).date())
            for item in data:
                if str(item['day']) == date:
                    list_data.append(item[value_item])
                    break
            else:
                list_data.append(0)

    if lastmonth:
        for i in range(int((this_month - last_month).days)+1):
            date = str((last_month + datetime.timedelta(i)).date())
            for item in data:
                if str(item['day']) == date:
                    list_data.append(item[value_item])
                    break
            else:
                list_data.append(0)

    if last30days:
        for i in range(int((today_date - last_30_days).days)+1):
            date = str((last_30_days+ datetime.timedelta(i)).date())
            for item in data:
                if str(item['day']) == date:
                    list_data.append(item[value_item])
                    break
            else:
                list_data.append(0)
    return list_data
