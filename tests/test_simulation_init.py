import portfoliosim as ps
import pandas as pd


def test_simulation_portfolio_cash_buffer_initialisation():
    """
    ensure that simulation initialises portfolio correctly
    """

    simulation_config = {
        "starting_portfolio_value" : 1202,
        "max_withdrawal_rate" : 0.99,
        "income_schedule" : pd.DataFrame(data={
            'year':pd.Series([1,2,3], dtype='int'),
            'desired_income':pd.Series([98,100,102], dtype='float'),
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
    
    expected_portfolio = {
        'stocks' : 25.0,
        'gold' : 50.0,
        'bonds' : 5.0,
        'cash' : 250.0
        }
    expected_cash_buffer = 202

    assert x.get_portfolio() == expected_portfolio
    assert x.get_cash_buffer() == expected_cash_buffer
        