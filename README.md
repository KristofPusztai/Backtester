# Python Backtester "Engine" for strategy testing

### Usage:

    from Backtester import Backtester
    
    # Data is for strategy, price_data is for calculating value
    bt = Backtester(data, start_balance, price_data, start_portfolio)
    
    # Model function, used to generate portfolio positions, 
    # should take in current data and step_output boolean
    # as parameters
    bt.set_model(model)
    
    # Runs strategy with given output parameters for plotting/info
    time, history, returns = bt.run(start_index, name=None, plot=True, info=True, step_output=False, show_trade_points=True)

#### For plotting/running benchmark:
    # Data is for strategy, price_data is for calculating value
    bt = Backtester(data, start_balance, price_data, start_portfolio)
    
    # NOTE: start_portfolio when benchmarking
    # is arbitrary and will be set later by method call
    
    bt.benchmark(self, start_index, symbol, plot=True, info=True)
#### Example Output:
    ROI: 88.131%
    Final Value: 5643.92
    Final Portfolio: {'AMD': 0.0325, 'JBLU': 0.0, 'V': 0.0, 'MSFT': 0.38045, 'PFE': 0.41758, 'NOK': 0.02001, 'T': 0.14946}
    Biggest Loss: -240.56
    ROI: 86.703%
    Final Value: 5601.08
    Final Portfolio: {'SPY': 1}
    Biggest Loss: -244.47
    ROI: 184.53%
    Final Value: 8535.89
    Final Portfolio: {'AMD': 0.0545, 'JBLU': 0.0401, 'V': 0.4375, 'MSFT': 0.2022, 'PFE': 0.0755, 'NOK': 0.1068, 'T': 0.09}
    Biggest Loss: -345.0
 ![alt text](https://github.com/KristofPusztai/Backtester/blob/master/example_output.png)
