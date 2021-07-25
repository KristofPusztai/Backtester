import matplotlib.pyplot as plt


class Backtester:
    """
    Class for backtesting various strategies and portfolio's, assumes all start balance will be invested (0 sum)

    note: Make sure data is compatible with model
    """

    def __init__(self, data, start_balance, start_portfolio, price_data):
        """

        :param data: Data for use in model run, make sure columns reflect time (important for plotting)
        Note: columns should not be string but datetime objects:
        https://www.geeksforgeeks.org/convert-the-column-type-from-string-to-datetime-format-in-pandas-dataframe/
        :type data: pandas.DataFrame
        :param start_balance: Starting balance amount
        :type start_balance: float
        :param start_portfolio: starting portfolio, should include all assets that model considers trade options on,
        dictionary reflects percentage, sum of all assets in portfolio is 1 with keys being asset symbols
        (should correspond to price_data rows)
        note: if values in start_portfolio are not all 0, consider balance fully invested at start, i.e no cash B.P.
        :type start_portfolio: dictionary
        :param price_data: Data for running model purchases/sells and calculating final portfolio value, should have
        same number of columns as data DataFrame, with rows containing asset symbol
        :type price_data: pandas.DataFrame
        """
        self.start_val = start_balance  # For use if roi info is wanted during run

        self.portfolio = start_portfolio
        self.data = data
        self.value = start_balance
        self.price_data = price_data
        self.model_fn = None

    def set_model(self, model):
        """

        :param model: Model used to generate portfolio positions, should take in current date, and data as parameters
        :type model: function
        """
        self.model_fn = model

    def __model_step(self, date, step_output):
        """
        Takes a trading "step" according to model for specified data point(s), updates portfolio and value

        :param date: Current column date value
        :type date: string
        :return: nothing
        :rtype: None
        """
        self.value = self.__calculate_value(date)
        data = self.data.loc[:, :date]
        self.portfolio = self.model_fn(data)
        # TODO: step_output is true

    def __calculate_value(self, date):
        """

        :param date: Current column date value
        :type date: string
        :return: current value
        :rtype: float
        """
        value = 0
        for symbol, position in self.portfolio.iteritems():
            num = position * self.value
            price = self.data[date][symbol]
            val = price * num
            value += val
        return value

    def run(self, plot=True, info=True, step_output=False):
        """

        :param step_output: True, prints each step output and portfolio value, False, remains quiet
        :type step_output: bool
        :param info: True, prints summary of run including biggest loss, percentage gain, final value, final portfolio,
        False, remains quiet and only returns end_balance
        :type info: bool
        :param plot: True to plot, False to not plot
        :type plot: bool
        :return: Returns history of portfolio value
        :rtype: list
        """
        if self.model_fn:
            history = []
            if info:
                biggest_loss = 0.0
            if plot:
                time = []

            for i in self.data:
                if info:
                    prev_val = self.value
                self.__model_step(i, step_output)
                history.append(self.value)
                if plot:
                    time.append(i)
                if info:
                    diff = self.value - prev_val
                    if diff < biggest_loss:
                        biggest_loss = diff

            if plot:
                plt.plot(time, history)
                plt.xlabel('Date')
                plt.ylabel('Portfolio Value ($)')
            if info:
                roi = 100.0 * (self.value - self.start_val) / self.start_val
                print("ROI: " + str(roi) + "%")
                print("Final Value: " + str(self.value))
                print("Final Portfolio: " + str(self.portfolio))
                print("Biggest Loss: " + str(biggest_loss))
            return history
        else:
            print("Model Function cannot be None, please set via set_model")
