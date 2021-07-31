from portfoliosim import __version__
import portfoliosim as ps
import pandas as pd

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

def test_simulator_generate_income_schedule():
    """
    ensure that Simulator income generator calculates income schedule correctly
    """
    expected_schedule = pd.DataFrame({
        'year': pd.Series([1,2,3],dtype='int'), 
        'desired_income': pd.Series([100000.0,101000.0,102010.0],dtype='float'),
        'min_income':pd.Series([50000.0,50500.0,51005.0],dtype='float')
        })
    income_data = {
        "desired_annual_income": 100000,
        "inflation": 1.01,
        "min_income_multiplier": 0.5
        }
    x = ps.Simulator(income_data=income_data,simulation_length_years=3)
    pd.testing.assert_frame_equal(expected_schedule,x._get_income_schedule())