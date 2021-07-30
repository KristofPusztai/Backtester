import matplotlib.pyplot as plt
import numpy as np
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
        checksum = sum(self.portfolio.values())
        # Invalid input check
        if (not math.isclose(checksum, 0, rel_tol=0, abs_tol=0.009) and
                not math.isclose(checksum, 1, rel_tol=0, abs_tol=0.009)):
            raise ValueError('Invalid Input Portfolio, output sum: ' + str(checksum))
        self.data = data
        self.value = start_balance
        self.price_data = price_data

        self.model_fn = None
        self.portfolio_num = None
        self.trade_points = [[], []]

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
        # If sum is 0, all cash no  change in value
        if math.isclose(sum(self.portfolio.values()), 1, rel_tol=0, abs_tol=0.009):
            self.value = self.__calculate_value(date)

        data = self.data.loc[:date]
        out = self.model_fn(data, step_output)
        if out:
            # For plotting trade_points if plot=True
            self.trade_points[0].append(date)
            self.trade_points[1].append(self.value)
            checksum = sum(out.values())
            # Invalid output check
            if (not math.isclose(checksum, 0, rel_tol=0, abs_tol=0.009) and
                    not math.isclose(checksum, 1, rel_tol=0, abs_tol=0.009)):
                raise ValueError('Invalid Model Portfolio output sum: ' + str(checksum))
            self.portfolio = out
            self.portfolio_num = self.__calculate_portfolio_num(date)
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
        for symbol in self.portfolio_num:
            num = self.portfolio_num[symbol]
            price = self.data.loc[date][symbol]
            val = price * num
            value += val
        return value

    def __calculate_portfolio_num(self, date):
        p = {}
        for symbol in self.portfolio:
            position = self.portfolio[symbol]
            val = position * self.value
            price = self.data.loc[date][symbol]
            num = val / price
            p[symbol] = num
        return p

    def run(self, start_index, name=None, plot=True, info=True, step_output=False, show_trade_points=True):
        """

        :param show_trade_points: Plots points of trade if plot = True
        :type show_trade_points: bool
        :param name: for legend if plot=True
        :type name: string
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
        :return: Returns datetime, history and returns of portfolio value (for comparison plots of different models)
        :rtype: list
        """
        if self.model_fn:
            history = []
            if info:
                biggest_loss = 0.0

            for i in self.data.index[start_index:]:
                if info:
                    prev_val = self.value
                if self.portfolio_num is None:
                    self.portfolio_num = self.__calculate_portfolio_num(i)
                self.__model_step(i, step_output)
                history.append(self.value)
                if info:
                    diff = self.value - prev_val
                    if diff < biggest_loss:
                        biggest_loss = diff
            time = self.data.index[start_index:]
            if plot:
                plt.plot(time, history, label=name)
                plt.xlabel('Date')
                plt.ylabel('Portfolio Value ($)')
                if show_trade_points:
                    plt.plot(self.trade_points[0], self.trade_points[1], "*")
                if name:
                    plt.legend()
            returns = []
            for i in range(1, len(history)):
                returns.append((history[i - 1] - history[i]) / history[i - 1])
            if info:
                roi = 100.0 * (self.value - self.start_val) / self.start_val
                print("ROI: " + str(round(roi, 3)) + "%")
                print("Final Value: " + str(round(self.value, 2)))
                print('Standard Deviation of Returns: ' + str(np.sqrt(np.var(returns))))
                print("Final Portfolio: " + str(self.portfolio))
                print("Biggest Loss: " + str(round(biggest_loss, 2)))
            return time, history, returns
        else:
            print("Model Function cannot be None, please set via set_model")
