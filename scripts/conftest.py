import pytest, os

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # we only look at actual failing test calls, not setup/teardown
    if rep.when == "call":
        mode = "a" if os.path.exists("pytest_line_log") else "w"
        with open("pytest_line_log", mode) as f:
            tag = {True:'OK', False:'ERROR'}[not rep.failed]
            # let's also access a fixture for the fun of it
            if rep.failed:
                targ = 'line_log_fail'
            else:
                targ = 'line_log_pass'
            if targ in item.fixturenames:
                extra = item.funcargs[targ]
            elif 'return' in item.function.__annotations__.keys():
                extra = item.function.__annotations__['return'] % tag
            else:
                extra = tag + ' ' + item.function.__name__

            f.write( '%s\n' %  extra )
