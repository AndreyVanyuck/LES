import os

from configs.base import BaseConfig


class TestConfig(BaseConfig):
    def __init__(self, *args, **kwargs):
        super(TestConfig, self).__init__()