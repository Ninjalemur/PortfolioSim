import portfoliosim as ps
import pandas as pd


def test_log_results():
    """
    test log_results during simulation run
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

    expected_timestep_data = pd.DataFrame({
            'timestep':pd.Series([1], dtype='int'),
            'year':pd.Series([1], dtype='int'),
            'month':pd.Series([1], dtype='int'),
            'cash_buffer':pd.Series([0.0], dtype='float'),
            'bonds_qty':pd.Series([24.75], dtype='float'),
            'stocks_qty':pd.Series([24.75], dtype='float'),
            'gold_qty':pd.Series([24.75], dtype='float'),
            'bonds_value':pd.Series([24.75], dtype='float'),
            'stocks_value':pd.Series([24.75], dtype='float'),
            'gold_value':pd.Series([24.75], dtype='float'),
            'cash_notional':pd.Series([24.75], dtype='float'),
            'allowance':pd.Series([1], dtype='float'),
            })

    x = ps.Simulation(**simulation_config)
    x._run_timestep(0)
    pd.testing.assert_frame_equal(x.get_timestep_data(),expected_timestep_data)
