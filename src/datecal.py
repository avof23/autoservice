import datetime

from sqlalchemy.orm import Session

from db import engine, Masters, Orders

from keyboards import get_days
from constants import WORK_TIME, WEEKEND_DAYS

def get_masters_db(qu: str) -> list:
    """Function get information about masters from database
       Returns:
           List: Information about masters in list
       """
    with Session(engine) as session:
        q_result = session.query(Masters).filter(Masters.qualification == qu).all()
    return q_result


def get_orders_db(master_id: int, start_date: datetime):
    with Session(engine) as session:
        m_result = session.query(Orders).filter(
            Orders.master_id == master_id).filter(
            Orders.start_date >= start_date
        ).filter(Orders.status_id < 4 ).all()
    return m_result

def get_daystime() -> list:
    now = datetime.datetime.now()
    start_day = now.day
    days_for_reg = []
    while len(days_for_reg) < 7 - len(WEEKEND_DAYS):
        if int(now.strftime('%w')) in WEEKEND_DAYS:
            now += datetime.timedelta(days=1)
            continue
        days_for_reg.append(
            tuple(datetime.datetime.strptime(f'{now.date()} {i}:00', '%Y-%m-%d %H:%M') for i in WORK_TIME
                  if not (i < now.hour + 1 and now.day == start_day))
        )
        now += datetime.timedelta(days=1)
    return days_for_reg

work_type = 'gen'
checking_days = get_days()


matrix_free_datetime = dict()
for master in get_masters_db(work_type):
    #print(f'{master.qualification}_{master.id}')
    matrix_free_datetime[master.id] = list()
    master_orders = get_orders_db(master.id, datetime.datetime.strptime(checking_days[0], '%d.%m.%Y'))
    for day in checking_days:
        for hour in WORK_TIME:
            daytime = True
            for order in master_orders:
                # print(f"ID:{order.id} {order.start_date} {order.end_date}")
                if order.start_date <= datetime.datetime.strptime(f'{day} {hour}:00', '%d.%m.%Y %H:%M') < order.end_date:
                    #print(f'{day} {hour}:00 is busy! in master {master.qualification}_{master.id}')
                    daytime = False
                    break
            if daytime:
                matrix_free_datetime[master.id].append(datetime.datetime.strptime(f'{day} {hour}:00', '%d.%m.%Y %H:%M'))

print(matrix_free_datetime)

unique_matrix = set()
for free_range in matrix_free_datetime.values():
    unique_matrix = unique_matrix.union(free_range)
print(unique_matrix)
if datetime.datetime.strptime('2023-09-25 09:00', '%Y-%m-%d %H:%M') in unique_matrix:
    print('date is free')
else:
    print('date busy')
