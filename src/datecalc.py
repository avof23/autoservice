import datetime

from sqlalchemy.orm import Session
from sqlalchemy import func

from db import engine, Masters, Orders
from constants import WORK_TIME, WEEKEND_DAYS


def get_masters_db(qu: str) -> list:
    """
    The function get information about masters from database
        :param qu: string master qualification width filter in query
        :return List information about masters
       """
    with Session(engine) as session:
        q_result = session.query(Masters).filter(Masters.qualification == qu).all()
    return q_result


def get_orders_db(master_id: int, start_date: datetime.datetime, end_date: datetime.datetime | bool = False) -> list:
    """
    The function get information about orders from database by specific master ID
        :param master_id: Integer for width filter in query
        :param start_date: Datetime for width filter in query
        :param end_date: Datetime for width filter in query
        :return: List information about orders
       """
    with Session(engine) as session:
        m_result = session.query(Orders)\
            .filter(Orders.master_id == master_id) \
            .filter(Orders.status_id < 4) \
            .filter(Orders.start_date >= start_date)

        if end_date:
            m_result.filter(Orders.start_date <= end_date)
        m_result.all()
    return m_result


def check_free_master_in_date(master_id: int, work_date: datetime.datetime) -> bool:
    """
    The function checks the database for whether a master is occupied on a specific date
    :param master_id: checked master ID
    :param work_date: checked datetime
    :return: bool False if master is busy, True if master free
    """
    with Session(engine) as session:
        m_result = session.query(Orders) \
            .filter(Orders.master_id == master_id) \
            .filter(Orders.status_id < 4) \
            .filter(Orders.start_date <= work_date) \
            .filter(Orders.end_date > work_date)
        m_result.first()
    return m_result.count() == 0


def get_statistic_masters_db(qu: str) -> list:
    """
    The function calculates the number of active orders on each of the masters
    :param qu: Str of master qualification
    :return: List statistic for all masters {masterID:ordersCount}
    """
    with Session(engine) as session:
        stat_result = session.query(Orders.master_id,
                      func.count(Orders.id)).group_by(Orders.master_id).join(Masters)\
            .filter(Orders.status_id < 4, Masters.qualification == qu).all()
    return stat_result


def get_free_master_db(qu: str, work_date: datetime.datetime) -> int:
    """
    The function calculates all available masters for a specific time
    and returns the master ID for assigning an order, taking into account workload statistics
    :param qu: Str of master qualification
    :param work_date: Date for which the order must be created
    :return: Integer Master ID
    """
    free_masters = dict()
    for master in get_masters_db(qu):
        if check_free_master_in_date(master.id, work_date):
            free_masters[master.id] = 0
    if len(free_masters) > 1:
        statistic = get_statistic_masters_db(qu)
        free_masters.update(statistic)
    elif len(free_masters) == 0:
        return 0
    return min(free_masters, key=lambda unit: free_masters[unit])


def get_daystime() -> list:
    """
    The function calculates all available days in the current time interval
    :return: List of sets have all available days in current time period
    """
    now = datetime.datetime.now()
    start_day = now.day
    days_for_reg = []
    while len(days_for_reg) < 7 - len(WEEKEND_DAYS):
        if int(now.strftime('%w')) in WEEKEND_DAYS:
            now += datetime.timedelta(days=1)
            continue
        days_for_reg.append(
            set(datetime.datetime.strptime(f'{now.date()} {i}:00', '%Y-%m-%d %H:%M') for i in WORK_TIME
                if not (i < now.hour + 2 and now.day == start_day))
        )
        now += datetime.timedelta(days=1)
    return days_for_reg


def parse_ord(order: Orders) -> set:
    """
    Helper function for converting a time period into a datetime set with an interval of 1 hour
    :param order: One order that contains a time interval
    :return: set of all datetime element in time period
    """
    d = set()
    while order.start_date < order.end_date:
        d.add(order.start_date)
        order.start_date += datetime.timedelta(hours=1)
    return d


def calculate_free_days(work_type: str) -> list:
    """
    The function calculates free days based on orders from the database
    :param work_type: String type of work user selected
    :return: List of free days for show in keyboard
    """
    available = set()
    for s in get_daystime():
        available = available.union(s)

    matrix_busy_datetime = dict()
    for master in get_masters_db(work_type):
        master_orders = get_orders_db(master.id, datetime.datetime.now())
        matrix_busy_datetime[master.id] = [parse_ord(order) for order in master_orders]

    result_union = set()
    matrix_union_by_master = dict()
    for ms in matrix_busy_datetime:
        for s in matrix_busy_datetime[ms]:
            result_union = result_union.union(s)
        matrix_union_by_master[ms] = result_union

    result_diff = set()
    for master_set in matrix_union_by_master.values():
        result_diff = result_diff.union(available.difference(master_set))

    date_button = set()
    for item in result_diff:
        date_button.add(datetime.datetime.strftime(item, '%d.%m.%Y'))
    return sorted(date_button)


def calculate_free_times(work_type: str, start_date: str) -> list:
    """
    The function calculates free time based on orders from the database
    :param work_type: String type of work user selected
    :param start_date: String data %d.%m.%Y format
    :return: List of free hours for show in keyboard
    """
    query_date = datetime.datetime.strptime(start_date, '%d.%m.%Y')
    now = datetime.datetime.now()
    master_hours = dict()
    for master in get_masters_db(work_type):
        master_hours[master.id] = set()
        master_orders = get_orders_db(master.id, query_date, query_date)
        for hour in WORK_TIME:
            hour_is_free = True
            if query_date == now.date() and hour < now.hour + 1:
                continue
            for order in master_orders:
                if order.start_date <= datetime.datetime.strptime(f'{start_date} {hour}:00', '%d.%m.%Y %H:%M') < order.end_date:
                    hour_is_free = False
                    break
            if hour_is_free:
                master_hours[master.id].add(hour)
    free_hours = set()
    for master_set in master_hours.values():
        free_hours = free_hours.union(master_set)
    return sorted(free_hours)


if __name__ == '__main__':
    print(get_statistic_masters_db('gen'))
