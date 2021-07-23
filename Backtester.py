class Backtester:
    """
    Class for backtesting various strategies and portfolio's, assumes all start balance will be invested (0 sum)

    note: Make sure data is compatible with model
    """
    def __init__(self, data, start_balance, start_portfolio, price_data):
        """

        :param data: Data for use in model run, make sure columns reflect time (important for plotting)
        :type data: pandas.DataFrame
        :param start_balance: Starting balance amount
        :type start_balance: float
        :param start_portfolio: starting portfolio, should include all assets that model considers trade options on,
        dictionary reflects percentage, sum of all assets in portfolio is 1
        note: if start_portfolio is not empty, consider balance fully invested at start (no cash buying power)
        :type start_portfolio: dictionary
        :param price_data: Data for running model purchases/sells and calculating final portfolio value, should have
        same number of columns as data DataFrame, with rows containing asset symbol
        :type price_data: pandas.DataFrame
        """
        self.portfolio = start_portfolio
        self.data = data
        self.start_balance = start_balance
        self.price_data = price_data
        self.model_fn = None

    def set_model(self, model):
        """

        :param model: Model used to generate portfolio positions, should take in current date, and data as parameters
        :type model: function
        """
        self.model_fn = model

    def __model_step(self, date):
        """

        :param date: Current column date value
        :type date: string
        :return: returns output of model
        :rtype: dictionary
        """

    def run(self, plot=True, info=False, delta=False):
        """

        :param delta: If True, model should output dictionary of change in portfolio positions, otherwise should output
        new portfolio positions summing to 1
        :type delta: bool
        :param info: True, prints summary of run, False, remains quiet
        :type info: bool
        :param plot: True to plot, False to not plot
        :type plot: bool
        :return: Returns end_balance and model outputs in list
        :rtype: list
        """

