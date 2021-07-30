from portfoliosim import __version__
import portfoliosim as ps

def test_version():
    assert __version__ == '0.1.0'

def test_simulator_check_desired_income_type():
    """
    ensure that Simulator flags non float desired income correctly
    Only things castable to float should be accepted
    """
    try:
        income_data = {
            "desired_annual_income": 'a',
            "inflation": 1.027,
            "min_income_multiplier": 0.75
            }
        x = ps.Simulator(income_data=income_data)
        assert False, 'ValueError should be raised when desired_annual_income in income_data cannot be coerced to float'
    except ValueError as ve:
        assert str(ve) == "desired_annual_income should be castable to float. received 'a' of type <class 'str'>"

def test_simulator_check_inflation_type():
    """
    ensure that Simulator flags non float inflation correctly
    Only things castable to float should be accepted
    """
    try:
        income_data = {
            "desired_annual_income": 100000,
            "inflation": 'a',
            "min_income_multiplier": 0.75
            }
        x = ps.Simulator(income_data=income_data)
        assert False, 'ValueError should be raised when inflation in income_data cannot be coerced to float'
    except ValueError as ve:
        assert str(ve) == "inflation should be castable to float. received 'a' of type <class 'str'>"

def test_simulator_check_min_income_multiplier_type():
    """
    ensure that Simulator flags non float inflation correctly
    Only things castable to float should be accepted
    """
    try:
        income_data = {
            "desired_annual_income": 100000,
            "inflation": 1.026,
            "min_income_multiplier": 'a'
            }
        x = ps.Simulator(income_data=income_data)
        assert False, 'ValueError should be raised when min_income_multiplier in income_data cannot be coerced to float'
    except ValueError as ve:
        assert str(ve) == "min_income_multiplier should be castable to float. received 'a' of type <class 'str'>"
