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
        simulation_cofig = {
            'starting_portfolio_value': 1000000.0,
            "desired_annual_income": 'a',
            "inflation": 1.027,
            "min_income_multiplier": 0.75,
            "max_withdrawal_rate" : 0.02
            }
        x = ps.Simulator(**simulation_cofig)
        assert False, 'ValueError should be raised when desired_annual_income in simulation_cofig cannot be coerced to float'
    except ValueError as ve:
        assert str(ve) == "desired_annual_income should be castable to float. received 'a' of type <class 'str'>"

def test_simulator_check_inflation_type():
    """
    ensure that Simulator flags non float inflation correctly
    Only things castable to float should be accepted
    """
    try:
        simulation_cofig = {
            'starting_portfolio_value': 1000000.0,
            "desired_annual_income": 100000,
            "inflation": 'a',
            "min_income_multiplier": 0.75,
            "max_withdrawal_rate" : 0.02
            }
        x = ps.Simulator(**simulation_cofig)
        assert False, 'ValueError should be raised when inflation in simulation_cofig cannot be coerced to float'
    except ValueError as ve:
        assert str(ve) == "inflation should be castable to float. received 'a' of type <class 'str'>"

def test_simulator_check_min_income_multiplier_type():
    """
    ensure that Simulator flags non float inflation correctly
    Only things castable to float should be accepted
    """
    try:
        simulation_cofig = {
            'starting_portfolio_value': 1000000.0,
            "desired_annual_income": 100000,
            "inflation": 1.026,
            "min_income_multiplier": 'a',
            "max_withdrawal_rate" : 0.02
            }
        x = ps.Simulator(**simulation_cofig)
        assert False, 'ValueError should be raised when min_income_multiplier in simulation_cofig cannot be coerced to float'
    except ValueError as ve:
        assert str(ve) == "min_income_multiplier should be castable to float. received 'a' of type <class 'str'>"

def test_simulator_check_starting_portfolio_value_type():
    """
    ensure that Simulator flags non float starting portfolio value correctly
    Only things castable to float should be accepted
    """
    try:
        simulation_cofig = {
            'starting_portfolio_value': 'a',
            "desired_annual_income": 100000,
            "inflation": 1.027,
            "min_income_multiplier": 0.75,
            "max_withdrawal_rate" : 0.02
            }
        x = ps.Simulator(**simulation_cofig)
        assert False, 'ValueError should be raised when desired_annual_income in simulation_cofig cannot be coerced to float'
    except ValueError as ve:
        assert str(ve) == "starting_portfolio_value should be castable to float. received 'a' of type <class 'str'>"


def test_simulator_check_simulation_length_type():
    """
    ensure that Simulator flags non int length correctly
    Only things castable to int should be accepted
    """
    try:
        simulation_cofig = {
            'starting_portfolio_value': 1000000.0,
            "desired_annual_income": 100000,
            "inflation": 1.026,
            "min_income_multiplier": 0.75,
            "simulation_length_years" : 'a',
            "max_withdrawal_rate" : 0.02
            }
        x = ps.Simulator(**simulation_cofig)
        assert False, 'ValueError should be raised when simulation_length_years in simulation_cofig cannot be coerced to int'
    except ValueError as ve:
        assert str(ve) == "simulation_length_years should be castable to int. received 'a' of type <class 'str'>"

def test_simulator_generate_income_schedule():
    """
    ensure that Simulator income generator calculates income schedule correctly
    """
    expected_schedule = pd.DataFrame({
        'year': pd.Series([1,2,3],dtype='int'), 
        'desired_income': pd.Series([100000.0,101000.0,102010.0],dtype='float'),
        'min_income':pd.Series([50000.0,50500.0,51005.0],dtype='float')
        })
    simulation_cofig = {
        'starting_portfolio_value': 1000000.0,
        "desired_annual_income": 100000,
        "inflation": 1.01,
        "min_income_multiplier": 0.5,
        "simulation_length_years" : 3,
        "max_withdrawal_rate" : 0.02
        }
    x = ps.Simulator(**simulation_cofig)
    pd.testing.assert_frame_equal(expected_schedule,x._get_income_schedule())

def test_simulator_check_starting_portfolio_above_zero():
    """
    ensure that Simulator flags starting_portfolio_value not larger than 0
    Only starting_portfolio_value greater than 0 should be accepted
    """
    simulation_cofig = {
        "desired_annual_income": 100000,
        "inflation": 1.026,
        "min_income_multiplier": 0.75,
        "simulation_length_years" : 30,
        "max_withdrawal_rate" : 0.02
        }
    for i in [0,-1]:
        
        simulation_cofig['starting_portfolio_value'] = i   
        try:
            x = ps.Simulator(**simulation_cofig)
            assert False, 'ValueError should be raised when starting_portfolio_value is not greater than 0'
        except ValueError as ve:
            assert str(ve) == f"starting_portfolio_value should be greater than zero. received '{i}'"

def test_simulator_check_desired_annual_income_above_zero():
    """
    ensure that Simulator flags desired_annual_income not larger than 0
    Only desired_annual_income greater than 0 should be accepted
    """
    simulation_cofig = {
        "starting_portfolio_value": 1000000,
        "inflation": 1.026,
        "min_income_multiplier": 0.75,
        "simulation_length_years" : 30,
        "max_withdrawal_rate" : 0.02
        }
    for i in [0,-1]:
        
        simulation_cofig['desired_annual_income'] = i   
        try:
            x = ps.Simulator(**simulation_cofig)
            assert False, 'ValueError should be raised when desired_annual_income is not greater than 0'
        except ValueError as ve:
            assert str(ve) == f"desired_annual_income should be greater than zero. received '{i}'"

def test_simulator_check_inflation_above_zero():
    """
    ensure that Simulator flags inflation not above zero
    Only inflation above zero
    """
    simulation_cofig = {
        "starting_portfolio_value": 1000000,
        "desired_annual_income": 100000,
        "min_income_multiplier": 0.75,
        "simulation_length_years" : 30,
        "max_withdrawal_rate" : 0.02
        }
    for i in [0,-1]:
        
        simulation_cofig['inflation'] = i   
        try:
            x = ps.Simulator(**simulation_cofig)
            assert False, 'ValueError should be raised when inflation is not greater than 0'
        except ValueError as ve:
            assert str(ve) == f"inflation should be greater than zero. received '{i}'"

def test_simulator_check_min_income_between_zero_and_one_inclusive():
    """
    ensure that Simulator flags min_income_multiplier not between 0 and 1 inclusive
    Only min_income_multiplier between 0 and 1 inclusive should be accepted
    """
    simulation_cofig = {
        "starting_portfolio_value": 1000000,
        "desired_annual_income": 100000,
        "inflation": 1.026,
        "simulation_length_years" : 30,
        "max_withdrawal_rate" : 0.02
        }
    for i in [-0.4,1.1]:
        
        simulation_cofig['min_income_multiplier'] = i   
        try:
            x = ps.Simulator(**simulation_cofig)
            assert False, 'ValueError should be raised when min_income_multiplier is not between 0 and 1 inclusive'
        except ValueError as ve:
            assert str(ve) == f"min_income_multiplier should be between 0 and 1 inclusive. received '{i}'"

def test_simulator_check_max_withdrawal_more_than_zero_and_smaller_or_equals_one():
    """
    ensure that Simulator flags max_withdrawal greater than zero, and less than or equal to one
    Only max_withdrawal 0 < x <= 1  should be accepted
    """
    simulation_cofig = {
        "starting_portfolio_value": 1000000,
        "desired_annual_income": 100000,
        "inflation": 1.026,
        "simulation_length_years" : 30,
        "min_income_multiplier" : 0.5
        }
    for i in [-0.1,0,1.1]:
        
        simulation_cofig['max_withdrawal_rate'] = i   
        try:
            x = ps.Simulator(**simulation_cofig)
            assert False, 'ValueError should be raised when max_withdrawal_rate is not 0 < x <= 1'
        except ValueError as ve:
            assert str(ve) == f"max_withdrawal_rate should be greater than zero and less than or equal to one. received '{i}'"


def test_simulator_check_simulation_length_years_above_zero():
    """
    ensure that Simulator flags simulation_length_years not above zero
    Only simulation_length_years above zero allowed
    """
    simulation_cofig = {
        "starting_portfolio_value": 1000000,
        "desired_annual_income": 100000,
        "min_income_multiplier": 0.75,
        "inflation" : 1.025,
        "max_withdrawal_rate" : 0.02
        }
    for i in [0,-1]:
        
        simulation_cofig['simulation_length_years'] = i   
        try:
            x = ps.Simulator(**simulation_cofig)
            assert False, 'ValueError should be raised when simulation_length_years is not greater than 0'
        except ValueError as ve:
            assert str(ve) == f"simulation_length_years should be greater than zero. received '{i}'"

def test_simulator_check_for_valid_assets_in_portfolio():
    """
    ensure that Simulator flags portfolio asset classes other than stocks, bonds, cash, gold
    Only asset classes stocks, bonds, cash, gold allowed
    """
    simulation_cofig = {
        "starting_portfolio_value": 1000000,
        "desired_annual_income": 100000,
        "min_income_multiplier": 0.75,
        "inflation" : 1.025,
        "max_withdrawal_rate" : 0.02,
        "portfolio_allocation" : {
            'cats' : 0.6,
            'gold' : 0.4
            }
        }
    
    try:
        x = ps.Simulator(**simulation_cofig)
        assert False, 'ValueError should be raised when portfolio_allocation contains keys other than stocks, bonds, cash, gold'
    except TypeError as ve:
        assert str(ve) == f"portfolio assets should only be stocks, bonds, cash, gold. received 'cats'"

def test_simulator_check_for_portfolio_allocation_type():
    """
    ensure that Simulator flags portfolio allocations that cannot be converted to float
    Only values that can be converted to float are allowed
    """
    simulation_cofig = {
        'starting_portfolio_value': 1000000.0,
        "desired_annual_income": 10000,
        "inflation": 1.027,
        "min_income_multiplier": 0.75,
        "max_withdrawal_rate" : 0.02,
        "portfolio_allocation" : {
            'stocks' : 'a',
            'gold' : 0.4
            }
        }
    try:
        x = ps.Simulator(**simulation_cofig)
        assert False, 'ValueError should be raised when protfolio_allocation value in simulation_cofig cannot be coerced to float'
    except ValueError as ve:
        assert str(ve) == "portfolio_allocation for stocks should be castable to float. received 'a' of type <class 'str'>"

def test_simulator_check_for_portfolio_allocation_type():
    """
    ensure that Simulator flags portfolio allocations are below zero
    Only values that are above 1 are allowed
    """
    simulation_cofig = {
        'starting_portfolio_value': 1000000.0,
        "desired_annual_income": 10000,
        "inflation": 1.027,
        "min_income_multiplier": 0.75,
        "max_withdrawal_rate" : 0.02,
        "portfolio_allocation" : {
            'stocks' : -0.5,
            'gold' : 0.4
            }
        }
    try:
        x = ps.Simulator(**simulation_cofig)
        assert False, 'ValueError should be raised when protfolio_allocation value in simulation_cofig are at least zero'
    except ValueError as ve:
        assert str(ve) == "portfolio_allocation for stocks should be at least zero. received '-0.5'"

def test_simulator_check_cash_buffer_years_at_least_zero():
    """
    ensure that Simulator flags cash_buffer_years not at least 0
    Only cash_buffer_years at least 0 should be accepted
    """
    simulation_cofig = {
        "starting_portfolio_value": 1000000,
        "desired_annual_income": 100000,
        "inflation": 1.026,
        "min_income_multiplier": 0.75,
        "simulation_length_years" : 30,
        "max_withdrawal_rate" : 0.02,
        'cash_buffer_years': -1
        }

    try:
        x = ps.Simulator(**simulation_cofig)
        assert False, 'ValueError should be raised when cash_buffer_years is not at least 0'
    except ValueError as ve:
        assert str(ve) == "cash_buffer_years should be at least zero. received '-1'"
