# Python Backtester "Engine" for strategy testing

### Docs:

    from Backtester import Backtester
    
    # Data is for strategy, price_data is for calculating value
    bt = Backtester(data, start_balance, price_data, start_portfolio)
    
    # Model function, used to generate portfolio positions, 
    # should take in current data and step_output boolean
    # as parameters
    bt.set_model(model)
    
    # Runs strategy with given output parameters for plotting/info
    bt.run(start_index, name=None, plot=True, info=True, step_output=False, show_trade_points=True)