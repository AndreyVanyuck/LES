# import os

# from configs.development import DevelopmentConfig
# from configs.staging import StagingConfig
# from configs.production import ProductionConfig
from configs.test import TestConfig
# from configs.base import BaseConfig


# if os.environ.get('ENVIRONMENT') == 'development':
#     config = DevelopmentConfig()
# elif os.environ.get('ENVIRONMENT') == 'staging':
#     config = StagingConfig()
# elif os.environ.get('ENVIRONMENT') == 'production':
#     config = ProductionConfig()
# elif os.environ.get('ENVIRONMENT') == 'test':
#     config = TestConfig()
# else:
#     config = BaseConfig()

CONFIG = TestConfig()
