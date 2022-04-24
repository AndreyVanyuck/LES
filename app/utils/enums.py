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