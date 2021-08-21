import portfoliosim as ps
import pandas as pd
import time

def main():
    ## define a set of parameters for simulations
    simulation_cofig = {
        "starting_portfolio_value": 1000000,
        "desired_annual_income": 50000,
        "min_income_multiplier": 0.75,
        "inflation": 1.027,
        "simulation_length_years" : 50,
        "max_withdrawal_rate" : 0.025,
        "cash_buffer_years" : 3,
        "portfolio_allocation":{
            'stocks' : 0.6,
            'bonds' : 0.4,
            'gold' : 0.0,
            'cash' : 0.0
            }
        }

    ## run simulator and log results
    x = ps.Simulator(**simulation_cofig)
    print('running basic simulation')
    x.run_simulations()
    x.write_results('../results/basic/')

    ## run simulations of varying simulation durations
    for i in range(10,51,10):
        print('running simulation for simulation length {i} years')
        simulation_cofig["simulation_length_years"] = i 
        x = ps.Simulator(**simulation_cofig)
        x.run_simulations()
        x.write_results('../results/vary_simulation_years/')

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f'time taken: {end - start:3f} seconds')