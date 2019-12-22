def pytest_addoption(parser):
    group = parser.getgroup('general')
    group.addoption('--force_run', action='store_true', dest='force_run',
                    default=False, help='force run ahAPICore case.')
