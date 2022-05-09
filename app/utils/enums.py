import enum


class BaseEnum(enum.Enum):

    @classmethod
    def values(cls):
        return [_.value for _ in cls]


class DepartmentEnum(BaseEnum):
    WEB = 'Web'
    MOBILE = 'Mobile'
    MARKETING = 'Marketing'
    ADMINISTRATION = 'Administration'
    HUMAN_RESOURCE = 'Human Resource'
    ACCOUNTING = 'Accounting'
    SALES = 'Sales'
    CUSTOMER_SUPPORT = 'Customer Support'
    SECURITY = 'Security'
    QUALITY_ASSURANCE = 'Quality Assurance'


class ErrorCodes(BaseEnum):
    department_id_not_found = 'The department id is invalid'
    email_not_found = 'Email not found'
    unauthorized = 'Unauthorized'
    email_already_exist = 'Email already exist'
    user_not_found = 'User not found'


class RequestsStateEnum(BaseEnum):
    PENDING_APPROVAL = 'pending_approval'
    APPROVED = 'approved'
    APPROVED_AND_REGISTERED = 'approved_and_registered'
    PENDING_CONFIRMATION = 'pending_confirmation'
    CANCELED = 'canceled'
    DECLINED = 'declined'


class RequestTypeEnum(BaseEnum):
    VACATION = 'vacation'
    OWN_EXPENSE_LEAVE = 'own_expense_leave'
    SICK_LEAVE = 'sick_leave'


class UserPicture(BaseEnum):
    women = 'https://sun9-79.userapi.com/s/v1/if2/WgKDJzQkrqrrEvEfzKZmy2CdO3q8qryCT1bnT7mVgedExmDD0AB6d-4A_0V_eyrl0oNDVx9A0jaARLri8tQ3HdjA.jpg?size=860x900&quality=95&type=album'
