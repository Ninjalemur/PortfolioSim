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
        