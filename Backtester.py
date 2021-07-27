import matplotlib.pyplot as plt
import math


class Backtester:
    """
    Class for backtesting various strategies and portfolio's, assumes all start balance will be invested (0 sum)

    note: Make sure data is compatible with model
    """

    def __init__(self, data, start_balance, price_data, start_portfolio):
        """

        :param start_portfolio: Format: {'ticker/asset id': % of portfolio (total of these should sum to 1), ...}
        :type start_portfolio: dictionary
        :param data: Data for use in model run, make sure columns reflect time (important for plotting)
        Note: columns should not be string but datetime objects:
        https://www.geeksforgeeks.org/convert-the-column-type-from-string-to-datetime-format-in-pandas-dataframe/
        :type data: pandas.DataFrame
        :param start_balance: Starting balance amount
        :type start_balance: float
        :param price_data: Data for running model purchases/sells and calculating final portfolio value, should have
        same number of columns as data DataFrame, with columns containing asset symbol
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

        :param model: Model used to generate portfolio positions, should take in current data and step_output boolean
        as parameters
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
        if sum(self.portfolio.values()) == 1:
            self.value = self.__calculate_value(date)
        data = self.data.loc[:date]
        out = self.model_fn(data, step_output)
        if out:
            checksum = sum(out.values())
            if (not math.isclose(checksum, 0, rel_tol=0, abs_tol=0.009) or
                    not math.isclose(checksum, 1, rel_tol=0, abs_tol=0.009)):
                raise ValueError('Invalid Model Portfolio output sum: ' + str(checksum))
            self.portfolio = out
            if step_output:
                print("Value: " + str(self.value))

    def __calculate_value(self, date):
        """

        :param date: Current column date value
        :type date: string
        :return: current value
        :rtype: float
        """
        value = 0
        for symbol in self.portfolio:
            position = self.portfolio[symbol]
            num = position * self.value
            price = self.data.loc[date][symbol]
            val = price * num
            value += val
        return value

    def run(self, start_index, plot=True, info=True, step_output=False):
        """

        :param start_index: Defines which data point (date) to start on, ie, 100 = start on 100th datapoint, this way
        model has 100 data points as input
        :type start_index: integer
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

            for i in self.data.index[start_index:]:
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
