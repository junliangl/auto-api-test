def pytest_addoption(parser):
    """
    pytest --environment=local
    available environment : local, docker
    """
    parser.addoption("--environment", action="store", default="local", help="Custom parameter")
