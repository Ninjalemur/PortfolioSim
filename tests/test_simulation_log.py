import portfoliosim as ps
import pandas as pd


def test_timestep_log_results():
    """
    test log_results after each timestep during simulation run
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
            'failed':pd.Series([False], dtype='boolean')
            })

    x = ps.Simulation(**simulation_config)
    x._run_timestep(0)
    pd.testing.assert_frame_equal(x.get_timestep_data(),expected_timestep_data)

def test_get_survival_duration():
    """
    test get_survival_duration returns correct survival duration
    """       

    simulation_config = {
        "starting_portfolio_value" : 100,
        "max_withdrawal_rate" : 0.1,
        "income_schedule" : pd.DataFrame(data={
            'year':pd.Series([1,2], dtype='int'),
            'desired_income':pd.Series([99,99], dtype='float'),
            'min_income':pd.Series([99,99], dtype='float')
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
    x.run()
    assert x.get_survival_duration() == 1

    simulation_config2 = {
        "starting_portfolio_value" : 100,
        "max_withdrawal_rate" : 0.1,
        "income_schedule" : pd.DataFrame(data={
            'year':pd.Series([1,2], dtype='int'),
            'desired_income':pd.Series([1,1], dtype='float'),
            'min_income':pd.Series([1,1], dtype='float')
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

    y = ps.Simulation(**simulation_config2)
    y.run()
    assert y.get_survival_duration() == 2

def test_run_results_generation():
    """
    test log_results during simulation run
    """       

    simulation_config = {
        "starting_portfolio_value" : 100,
        "max_withdrawal_rate" : 0.1,
        "income_schedule" : pd.DataFrame(data={
            'year':pd.Series([1,2], dtype='int'),
            'desired_income':pd.Series([1,1], dtype='float'),
            'min_income':pd.Series([1,1], dtype='float')
            }),
        "historical_data_subset": pd.DataFrame(data={
            'year':pd.Series([1,2], dtype='int'),
            'month':pd.Series([1,1], dtype='float'),
            'gold':pd.Series([1,1], dtype='float'),
            'stocks':pd.Series([1,1], dtype='float'),
            'bonds':pd.Series([1,1], dtype='float')
            }),
        "portfolio_allocation" : {
            'stocks' : 1,
            'gold' : 1,
            'bonds' : 1,
            'cash' : 1
            },
        "cash_buffer_years" : 0
        }

    expected_run_data = pd.DataFrame({
            'start_ref_year':pd.Series([1], dtype='int'),
            'start_ref_month':pd.Series([1], dtype='int'),
            'end_ref_year':pd.Series([2], dtype='int'),
            'end_ref_month':pd.Series([1], dtype='int'),
            'final_value':pd.Series([98.0], dtype='float'),
            'survival_duration':pd.Series([2], dtype='int')
            })

    x = ps.Simulation(**simulation_config)
    run_data, timestep_data = x.run()
    pd.testing.assert_frame_equal(run_data,expected_run_data)