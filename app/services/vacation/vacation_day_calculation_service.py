from datetime import datetime, date
from dateutil.relativedelta import relativedelta


class VacationDayCalculationService:
    VACATION_NORM = 29

    def __init__(self, user_service):
        self.user_service = user_service

    def get_remained_days(self, user_id):
        user = self.user_service.fetch(id=user_id)

        periods = self._get_periods(user.hire_date)
        days_left = self._get_days_left(periods)

        return {'periods': periods, 'days_left': days_left}

    def _get_periods(self, hire_date):
        today = datetime.today().date()

        periods = []
        start_date = hire_date.date()

        while True:
            end_date = start_date + relativedelta(days=364)

            periods.append({
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'vacation_norm': self.VACATION_NORM,
                'days_earned': self._get_days_earned(start_date, end_date),
                'days_left': 11,
                'days_spent': 0
            })

            if today <= end_date:
                break

            start_date = end_date + relativedelta(days=1)

        return periods

    def _get_days_earned(self, start_date, end_date):
        today = datetime.today().date()

        if today <= end_date:
            delta = today - start_date
        else:
            delta = end_date - start_date

        return int(delta.days * self.VACATION_NORM / 365)

    @staticmethod
    def _get_days_left(periods):
        return sum([_['days_left'] for _ in periods])
