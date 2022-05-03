from datetime import datetime
from dateutil.relativedelta import relativedelta

from app.utils.enums import RequestTypeEnum, RequestsStateEnum


class VacationDayCalculationService:
    VACATION_NORM = 29

    def __init__(self, user_service, request_service):
        self.user_service = user_service
        self.request_service = request_service

    def get_remained_days(self, user_id):
        user = self.user_service.fetch(id=user_id)

        periods = self._get_periods(user.hire_date, user_id)

        return {
            'periods': periods,
            'available_vacation_days': self._get_days_left(periods),
            'vacation_norm': self.VACATION_NORM,
            'sick_leave_days': self._get_total_sick_leave_days(periods),
            'own_expense_days': self._get_total_own_expense_days(periods)
        }

    def _get_periods(self, hire_date, user_id):
        today = datetime.today().date()

        periods = []
        start_date = hire_date.date()

        days_spent = self._get_days_spent(user_id)

        while True:
            end_date = start_date + relativedelta(days=364)

            days_earned = self._get_days_earned(start_date, end_date)
            days_left = days_earned

            if days_spent > 0:
                if days_spent - days_left > 0:
                    days_left = 0
                    days_spent_in_current_period = days_earned
                else:
                    days_spent_in_current_period = days_spent
                    days_left = days_earned - days_spent
            else:
                days_spent_in_current_period = 0

            days_spent -= days_spent_in_current_period

            periods.append({
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'vacation_norm': self.VACATION_NORM,
                'days_earned': days_earned,
                'days_left': days_left,
                'days_spent': days_spent_in_current_period,
                'sick_leave_days': self._get_sick_leave_days(user_id, start_date, end_date),
                'own_expense_days': self._get_own_expense_leave_days(user_id, start_date, end_date)
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

        return int((delta.days + 1) * self.VACATION_NORM / 365)

    @staticmethod
    def _get_days_left(periods):
        return sum([_['days_left'] for _ in periods])

    @staticmethod
    def _get_total_sick_leave_days(periods):
        return sum([_['sick_leave_days'] for _ in periods])

    @staticmethod
    def _get_total_own_expense_days(periods):
        return sum([_['own_expense_days'] for _ in periods])

    def _get_days_spent(self, user_id):
        requests = self.request_service.fetch_all(
            request_type=RequestTypeEnum.VACATION.value, user_id=user_id
        )

        return self.__calculate_days_sum(requests)

    def _get_sick_leave_days(self, user_id, start_date, end_date):
        requests = self.request_service.fetch_all(
            request_type=RequestTypeEnum.SICK_LEAVE.value, user_id=user_id,
            lte_={'end_date': end_date}, gt_={'start_date': start_date}
        )

        return self.__calculate_days_sum(requests)

    def _get_own_expense_leave_days(self, user_id, start_date, end_date):
        requests = self.request_service.fetch_all(
            request_type=RequestTypeEnum.OWN_EXPENSE_LEAVE.value, user_id=user_id,
            lte_={'end_date': end_date}, gt_={'start_date': start_date}
        )

        return self.__calculate_days_sum(requests)

    @staticmethod
    def __calculate_days_sum(requests):
        return sum(
            [
                (_.end_date - _.start_date).days + 1
                if _.state['state'] not in [RequestsStateEnum.CANCELED.value, RequestsStateEnum.DECLINED.value] else 0
                for _ in requests
            ]
        )
