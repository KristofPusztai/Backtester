# Python Backtester "Engine" for strategy testing

### Usage:

    from Backtester import Backtester
    
    # Data is for strategy, price_data is for calculating value
    bt = Backtester(data, start_balance, price_data, start_portfolio)
    
    # Model function, used to generate portfolio positions, 
    # should take in current data and step_output boolean
    # as parameters
    bt.set_model(model)
    
    start_index = 0
    
    # Runs strategy with given output parameters for plotting/info
    time, history, returns = bt.run(start_index, name=None, plot=True, info=True, step_output=False, show_trade_points=True)

#### For plotting/running benchmark:
    # Data is for strategy, price_data is for calculating value
    bt = Backtester(data, start_balance, price_data, start_portfolio)
    
    # NOTE: start_portfolio when benchmark 
    # is arbitrary and will be set later by method call
    
    symbol = 'SPY'
    start_index = 0
    
    bt.benchmark(self, start_index, symbol, plot=True, info=True)
