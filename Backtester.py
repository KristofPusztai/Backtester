class Backtester:
    """
    Class for backtesting various strategies and portfolio's

    note: Make sure data is compatible with model
    """
    def __init__(self, data, start_balance):
        """

        :param data: Data for use in model run, make sure columns reflect time (important for plotting)
        :type data: pandas.DataFrame
        :param start_balance: Starting monetary balance amount
        :type start_balance: float
        """
        self.data = data
        self.start_balance = start_balance
        self.portfolio = {}

    def run(self, model, plot=True, info=False):
        """

        :param info: True, prints summary of run, False, remains quiet
        :type info: bool
        :param model: Model used to generate portfolio positions
        :type model: function
        :param plot: True to plot, False to not plot
        :type plot: bool
        :return: Returns end_balance and model outputs in list
        :rtype: list
        """
