import portfoliosim as ps
import pandas as pd


def test_simulation_get_current_prices():
    """
    ensure that get_current_prices retrieves prices correctly
    """

    simulation_config = {
        "starting_portfolio_value" : 1202,
        "max_withdrawal_rate" : 0.99,
        "income_schedule" : pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'desired_income':pd.Series([100,102,104], dtype='float'),
            'min_income':pd.Series([50,51,52], dtype='float')
            }),
        "historical_data_subset": pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'month':pd.Series([1,2,3], dtype='float'),
            'gold':pd.Series([5,10,20], dtype='float'),
            'stocks':pd.Series([10,20,40], dtype='float'),
            'bonds':pd.Series([50,100,200], dtype='float')
            }),
        "portfolio_allocation" : {
            'stocks' : 1,
            'gold' : 1,
            'bonds' : 1,
            'cash' : 1
            },
        "cash_buffer_years" : 2
        }
    
    expected_prices0 = pd.Series(data={
        'year': 1,
        'month': 1,
        'gold': 5.0,
        'stocks': 10.0,
        'bonds': 50.0
        })
    expected_prices2 = pd.Series(data={
        'year': 3,
        'month': 3,
        'gold': 20.0,
        'stocks': 40.0,
        'bonds': 200.0
        })

    x = ps.Simulation(**simulation_config)
    pd.testing.assert_series_equal(x.get_current_prices(),expected_prices0,check_names=False)
    x.run()
    pd.testing.assert_series_equal(x.get_current_prices(),expected_prices2,check_names=False)

def test_simulation_get_desired_allowance():
    """
    ensure that _get_desired_allowance retrieves desired_allowance correctly
    """       

    simulation_config = {
        "starting_portfolio_value" : 1202,
        "max_withdrawal_rate" : 0.99,
        "income_schedule" : pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'desired_income':pd.Series([100,102,104], dtype='float'),
            'min_income':pd.Series([50,51,52], dtype='float')
            }),
        "historical_data_subset": pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'month':pd.Series([1,2,3], dtype='float'),
            'gold':pd.Series([5,10,20], dtype='float'),
            'stocks':pd.Series([10,20,40], dtype='float'),
            'bonds':pd.Series([50,100,200], dtype='float')
            }),
        "portfolio_allocation" : {
            'stocks' : 1,
            'gold' : 1,
            'bonds' : 1,
            'cash' : 1
            },
        "cash_buffer_years" : 2
        }

    x = ps.Simulation(**simulation_config)
    assert x._get_desired_allowance(0) == 100
    assert x._get_desired_allowance(1) == 102

def test_simulation_get_min_income():
    """
    ensure that _get_desired_allowance retrieves desired_allowance correctly
    """       

    simulation_config = {
        "starting_portfolio_value" : 1202,
        "max_withdrawal_rate" : 0.99,
        "income_schedule" : pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'desired_income':pd.Series([100,102,104], dtype='float'),
            'min_income':pd.Series([50,51,52], dtype='float')
            }),
        "historical_data_subset": pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'month':pd.Series([1,2,3], dtype='float'),
            'gold':pd.Series([5,10,20], dtype='float'),
            'stocks':pd.Series([10,20,40], dtype='float'),
            'bonds':pd.Series([50,100,200], dtype='float')
            }),
        "portfolio_allocation" : {
            'stocks' : 1,
            'gold' : 1,
            'bonds' : 1,
            'cash' : 1
            },
        "cash_buffer_years" : 2
        }

    x = ps.Simulation(**simulation_config)
    assert x._get_min_income(0) == 50
    assert x._get_min_income(1) == 51

def test_check_desired_less_than_max_withdrawal():
    """
    ensure that _check_desired_less_than_max_withdrawal correctly checks
    whether desired allowance is less than max_withdrawal
    """       

    simulation_config = {
        "starting_portfolio_value" : 1202,
        "max_withdrawal_rate" : 0.99,
        "income_schedule" : pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'desired_income':pd.Series([100,102,104], dtype='float'),
            'min_income':pd.Series([50,51,52], dtype='float')
            }),
        "historical_data_subset": pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'month':pd.Series([1,1,1], dtype='float'),
            'gold':pd.Series([5,10,20], dtype='float'),
            'stocks':pd.Series([10,20,40], dtype='float'),
            'bonds':pd.Series([50,100,200], dtype='float')
            }),
        "portfolio_allocation" : {
            'stocks' : 1,
            'gold' : 1,
            'bonds' : 1,
            'cash' : 1
            },
        "cash_buffer_years" : 2
        }

    x = ps.Simulation(**simulation_config)
    assert x._check_desired_less_than_max_withdrawal(2,1) == False
    assert x._check_desired_less_than_max_withdrawal(1,2) == True

def test_check_remaining_withdrawal_amount_can_refill_buffer():
    """
    ensure that _check_remaining_withdrawal_amount_can_refill_buffer
    correctly assesses whether remaining withdrawal amount is sufficient
    to fill empty cash buffer
    """       

    simulation_config = {
        "starting_portfolio_value" : 1202,
        "max_withdrawal_rate" : 0.99,
        "income_schedule" : pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'desired_income':pd.Series([100,102,104], dtype='float'),
            'min_income':pd.Series([50,51,52], dtype='float')
            }),
        "historical_data_subset": pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'month':pd.Series([1,1,1], dtype='float'),
            'gold':pd.Series([5,10,20], dtype='float'),
            'stocks':pd.Series([10,20,40], dtype='float'),
            'bonds':pd.Series([50,100,200], dtype='float')
            }),
        "portfolio_allocation" : {
            'stocks' : 1,
            'gold' : 1,
            'bonds' : 1,
            'cash' : 1
            },
        "cash_buffer_years" : 2
        }

    x = ps.Simulation(**simulation_config)
    assert x._check_remaining_withdrawal_amount_can_refill_buffer(4,3,2,1) == True
    assert x._check_remaining_withdrawal_amount_can_refill_buffer(4,3,2,0) == True
    assert x._check_remaining_withdrawal_amount_can_refill_buffer(4,3,2,2) == False

def test_check_cash_buffer_enough_funds_for_allowance():
    """
    ensure that _check_cash_buffer_enough_funds_for_allowance
    correctly assesses whether cash buffer has enough funds for 
    to supply desired_allowance
    """       

    simulation_config = {
        "starting_portfolio_value" : 1202,
        "max_withdrawal_rate" : 0.99,
        "income_schedule" : pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'desired_income':pd.Series([100,102,104], dtype='float'),
            'min_income':pd.Series([50,51,52], dtype='float')
            }),
        "historical_data_subset": pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'month':pd.Series([1,1,1], dtype='float'),
            'gold':pd.Series([5,10,20], dtype='float'),
            'stocks':pd.Series([10,20,40], dtype='float'),
            'bonds':pd.Series([50,100,200], dtype='float')
            }),
        "portfolio_allocation" : {
            'stocks' : 1,
            'gold' : 1,
            'bonds' : 1,
            'cash' : 1
            },
        "cash_buffer_years" : 2
        }

    x = ps.Simulation(**simulation_config)
    assert x._check_cash_buffer_enough_funds_for_allowance(4,3) == True
    assert x._check_cash_buffer_enough_funds_for_allowance(4,4) == True
    assert x._check_cash_buffer_enough_funds_for_allowance(3,4) == False

def test_check_max_withdrawal_allow_top_up_to_target_income():
    """
    ensure that _check_max_withdrawal_allow_top_up_to_target_income
    correctly assesses whether withdrawal limit has enough funds for 
    to supply target allowance
    """       

    simulation_config = {
        "starting_portfolio_value" : 1202,
        "max_withdrawal_rate" : 0.99,
        "income_schedule" : pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'desired_income':pd.Series([100,102,104], dtype='float'),
            'min_income':pd.Series([50,51,52], dtype='float')
            }),
        "historical_data_subset": pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'month':pd.Series([1,1,1], dtype='float'),
            'gold':pd.Series([5,10,20], dtype='float'),
            'stocks':pd.Series([10,20,40], dtype='float'),
            'bonds':pd.Series([50,100,200], dtype='float')
            }),
        "portfolio_allocation" : {
            'stocks' : 1,
            'gold' : 1,
            'bonds' : 1,
            'cash' : 1
            },
        "cash_buffer_years" : 2
        }

    x = ps.Simulation(**simulation_config)
    assert x._check_max_withdrawal_allow_top_up_to_target_income(2,2,1) == True
    assert x._check_max_withdrawal_allow_top_up_to_target_income(2,3,1) == True
    assert x._check_max_withdrawal_allow_top_up_to_target_income(2,4,1) == False

def test_execute_logic_01():
    """
    test exucute logic to execute logic outcome 01
        - desired allowance is less than max withdrawal
        - full amount withdrawn from portfolio
        - amount from max withdrawal not utilised by allowance 
            tops up cash buffer fully
    """       

    simulation_config = {
        "starting_portfolio_value" : 100,
        "max_withdrawal_rate" : 0.1,
        "income_schedule" : pd.DataFrame(data={
            'year':pd.Series([1], dtype='int'),
            'desired_income':pd.Series([1], dtype='float'),
            'min_income':pd.Series([1], dtype='float')
            }),
        "historical_data_subset": pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'month':pd.Series([1,1,1], dtype='float'),
            'gold':pd.Series([1,1,1], dtype='float'),
            'stocks':pd.Series([1,1,1], dtype='float'),
            'bonds':pd.Series([1,1,1], dtype='float')
            }),
        "portfolio_allocation" : {
            'stocks' : 1,
            'gold' : 1,
            'bonds' : 1,
            'cash' : 1
            },
        "cash_buffer_years" : 0
        }

    x = ps.Simulation(**simulation_config)
    x._run_timestep(0)
    assert round(x._get_portfolio_value(),3) == 99
    assert x.get_cash_buffer() == 0
    assert x.get_allowance() == 1

def test_execute_logic_02():
    """
    test exucute logic to execute logic outcome 02
        - desired allowance is less than max withdrawal
        - full amount withdrawn from portfolio
        - amount from max withdrawal not utilised by allowance 
            tops up cash buffer partially
    """       

    simulation_config = {
        "starting_portfolio_value" : 104,
        "max_withdrawal_rate" : 0.01,
        "income_schedule" : pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'desired_income':pd.Series([3,1,1], dtype='float'),
            'min_income':pd.Series([3,1,1], dtype='float')
            }),
        "historical_data_subset": pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'month':pd.Series([1,1,1], dtype='float'),
            'gold':pd.Series([1,4,4], dtype='float'),
            'stocks':pd.Series([1,4,4], dtype='float'),
            'bonds':pd.Series([1,4,4], dtype='float')
            }),
        "portfolio_allocation" : {
            'stocks' : 1,
            'gold' : 1,
            'bonds' : 1,
            'cash' : 0
            },
        "cash_buffer_years" : 2
        }

    x = ps.Simulation(**simulation_config)
    x._run_timestep(0)
    x._run_timestep(1)
    assert round(x._get_portfolio_value(),3) == 398
    assert x.get_cash_buffer() == 2
    assert x.get_allowance() == 1

def test_execute_logic_03():
    """
    test exucute logic to execute logic outcome 03
        - desired allowance is more than max withdrawal
        - desired allowance entirely withdrawn from cash buffer
    """       

    simulation_config = {
        "starting_portfolio_value" : 104,
        "max_withdrawal_rate" : 0.01,
        "income_schedule" : pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'desired_income':pd.Series([3,1,1], dtype='float'),
            'min_income':pd.Series([3,1,1], dtype='float')
            }),
        "historical_data_subset": pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'month':pd.Series([1,1,1], dtype='float'),
            'gold':pd.Series([1,1,1], dtype='float'),
            'stocks':pd.Series([1,1,1], dtype='float'),
            'bonds':pd.Series([1,1,1], dtype='float')
            }),
        "portfolio_allocation" : {
            'stocks' : 1,
            'gold' : 1,
            'bonds' : 1,
            'cash' : 1
            },
        "cash_buffer_years" : 2
        }

    x = ps.Simulation(**simulation_config)
    x._run_timestep(0)
    assert round(x._get_portfolio_value(),3) == 100
    assert x.get_cash_buffer() == 1
    assert x.get_allowance() == 3

def test_execute_logic_04():
    """
    test exucute logic to execute logic outcome 04
        - desired allowance is more than max withdrawal
        - deplete cash buffer to withdraw allowance
        - portfolio withdrawal tops up allowance to desired
    """       

    simulation_config = {
        "starting_portfolio_value" : 105,
        "max_withdrawal_rate" : 0.01,
        "income_schedule" : pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'desired_income':pd.Series([5,1,1], dtype='float'),
            'min_income':pd.Series([2.5,0.5,0.5], dtype='float')
            }),
        "historical_data_subset": pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'month':pd.Series([1,1,1], dtype='float'),
            'gold':pd.Series([1,1,1], dtype='float'),
            'stocks':pd.Series([1,1,1], dtype='float'),
            'bonds':pd.Series([1,1,1], dtype='float')
            }),
        "portfolio_allocation" : {
            'stocks' : 1,
            'gold' : 1,
            'bonds' : 1,
            'cash' : 1
            },
        "cash_buffer_years" : 1
        }

    x = ps.Simulation(**simulation_config)
    x._run_timestep(0)
    x._run_timestep(1)
    assert round(x._get_portfolio_value(),3) == 99
    assert x.get_cash_buffer() == 0
    assert x.get_allowance() == 1

def test_execute_logic_05():
    """
    test exucute logic to execute logic outcome 05
        - desired allowance is more than max withdrawal
        - deplete cash buffer to withdraw allowance
        - portfolio withdrawal up to max withdrawal results in reduced income
            that is between desired and minimum income
    """       

    simulation_config = {
        "starting_portfolio_value" : 105,
        "max_withdrawal_rate" : 0.01,
        "income_schedule" : pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'desired_income':pd.Series([5,1.1,1.1], dtype='float'),
            'min_income':pd.Series([2.5,0.55,0.55], dtype='float')
            }),
        "historical_data_subset": pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'month':pd.Series([1,1,1], dtype='float'),
            'gold':pd.Series([1,1,1], dtype='float'),
            'stocks':pd.Series([1,1,1], dtype='float'),
            'bonds':pd.Series([1,1,1], dtype='float')
            }),
        "portfolio_allocation" : {
            'stocks' : 1,
            'gold' : 1,
            'bonds' : 1,
            'cash' : 1
            },
        "cash_buffer_years" : 1
        }

    x = ps.Simulation(**simulation_config)
    x._run_timestep(0)
    x._run_timestep(1)
    assert round(x._get_portfolio_value(),3) == 99
    assert x.get_cash_buffer() == 0
    assert x.get_allowance() == 1

def test_execute_logic_06():
    """
    test exucute logic to execute logic outcome 06
        - desired allowance is more than max withdrawal
        - deplete cash buffer to withdraw allowance
        - withdraw from portfolio to hit minimum income
        - withdrawal from portfolio exceeds max withdrawal
    """       

    simulation_config = {
        "starting_portfolio_value" : 105,
        "max_withdrawal_rate" : 0.009,
        "income_schedule" : pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'desired_income':pd.Series([5,2,2], dtype='float'),
            'min_income':pd.Series([2.5,1,1], dtype='float')
            }),
        "historical_data_subset": pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'month':pd.Series([1,1,1], dtype='float'),
            'gold':pd.Series([1,1,1], dtype='float'),
            'stocks':pd.Series([1,1,1], dtype='float'),
            'bonds':pd.Series([1,1,1], dtype='float')
            }),
        "portfolio_allocation" : {
            'stocks' : 1,
            'gold' : 1,
            'bonds' : 1,
            'cash' : 1
            },
        "cash_buffer_years" : 1
        }

    x = ps.Simulation(**simulation_config)
    x._run_timestep(0)
    x._run_timestep(1)
    assert round(x._get_portfolio_value(),3) == 99
    assert x.get_cash_buffer() == 0
    assert x.get_allowance() == 1