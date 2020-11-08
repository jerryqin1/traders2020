import unittest
from mock_trader import Trader

symbols = ['A', 'B', 'C', 'D']
hedge_costs = {sym: 2e2 for sym in symbols}
stock_prices = [
    [93.83138183287349, 90.40920734584516, 130.14747704063825, 146.74217440110132],
    [91.90641358612055, 91.61527708820573, 131.2179882841117, 146.6598423495824],
    [92.19921550525827, 93.6062902705898, 132.99267034479632, 147.12942096536167],
    [93.0087865976987, 93.25718395171889, 131.93322897222262, 147.83490295330947],
    [93.15043761434687, 93.88566447046506, 130.46458971087452, 148.2974750571442],
    [93.19654593541122, 94.17622380335452, 133.04988642983565, 148.43256474872905],
    [93.30478871982389, 94.11303677571362, 132.59408009391979, 147.91289857092139],
    [96.14212026187184, 94.57182163891729, 131.93559356881102, 148.82522743691],
    [93.57746644751492, 95.00501610400183, 132.6604805306392, 148.74738217725942],
    [94.2974045922658, 96.40334842382431, 132.8732292694804, 149.52881555170902]
]

hedge_data = [
    [-14815.654904502811, 146446.06795925464, 71117.7290397539, 78625.71133106675],
    [121171.93502246532, 186351.90437511363, 26880.83255884215, 176995.4658136546],
    [89905.09411786823, 128131.80272031928, -73158.08138155665, 195672.95674455466],
    [17049.184249462847, 101919.69144501531, -147437.24258216232, 127049.0814138057],
    [63980.432380939004, 31910.843249607493, -12113.693736285344, -12203.204343300402],
    [22727.703430993482, -20311.735515716246, 77475.57530979965, -45558.866734620744],
    [-4384.310172092854, 38685.128194534125, -79651.15041968464, -53527.20926231197],
    [47496.134129289894, 48063.1291135798, -36483.539425611336, 137663.52422417066],
    [67462.67569004811, 73799.39004774735, 89471.48454175732, 228649.70538196032],
    [58903.83225167323, 127507.0557065113, 158375.78150992747, 129515.9920523488]
]

assert len(stock_prices) == len(hedge_data), 'Price and Info lists of different length'
assert len(symbols) == len(stock_prices[0]) and len(symbols) == len(hedge_data[0]), 'Not all symbols present'


class Test_1_Lose_All_Auctions(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Test_1_Lose_All_Auctions, self).__init__(*args, **kwargs)
        self.t = Trader()
        self.profit = 0

    def test_bid_results(self):
        bid = self.t.WonAuctions({sym: False for sym in ['A', 'B', 'C', 'D']})

    def test_trading(self):
        for timestep in range(len(stock_prices) - 1):
            stock_prices_now = dict(zip(symbols, stock_prices[timestep]))
            hedge_data_now = dict(zip(symbols, hedge_data[timestep]))

            # test BuyInfo()
            info_order = self.t.BuyInfo(timestep, stock_prices_now, hedge_costs)
            self.assertIsInstance(info_order, dict, f'Make your info_order a dict. Round {timestep}.')
            self.assertTrue(set(symbols).issubset(set(info_order)),
                f'Include all symbols in your info_order. Missing {set(symbols) - set(info_order)}. Round {timestep}.')
            for sym in symbols:
                self.assertIsInstance(info_order[sym], bool, f'Your info_order must be boolean. Round {timestep}.')
            info_they_get = {sym : hedge_data_now[sym] for sym in symbols if info_order.get(sym, False)}
            self.profit -= sum([hedge_costs[sym] for sym in symbols if info_order.get(sym, False)])
            trades = self.t.MakeTrades(timestep, info_they_get, stock_prices_now)

            # test MakeTrades()
            self.assertIsInstance(trades, dict, f'Make your trades a dict. Round {timestep}.')
            self.assertTrue(set(symbols).issubset(set(trades)),
                f'Include all symbols in your trades. Missing {set(symbols) - set(trades)}. Round {timestep}.')
            total_pos = 0
            for sym in symbols:
                self.assertTrue(abs(trades[sym]) < 6e5, 
                    f'Your trade for {sym} is {trades[sym]}: not within limits. Round {timestep}.')
                total_pos += abs(trades[sym])
            self.assertTrue(total_pos < 1e6, f'Your total trade costs exceed $1M. Round {timestep}.')

            stock_prices_next = dict(zip(symbols, stock_prices[timestep + 1]))
            self.profit += sum(
                [(stock_prices_next[sym] - stock_prices_now[sym]) * trades[sym] for sym in symbols])
        print(f'Finished with total profits {self.profit}.')


class Test_2_Win_All_Auctions(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Test_2_Win_All_Auctions, self).__init__(*args, **kwargs)
        self.t = Trader()
        self.profit = 0

    def test_bid_results(self):
        bid = self.t.WonAuctions({sym: True for sym in ['A', 'B', 'C', 'D']})

    def test_trading(self):
        for timestep in range(len(stock_prices) - 1):
            stock_prices_now = dict(zip(symbols, stock_prices[timestep]))
            hedge_data_now = dict(zip(symbols, hedge_data[timestep + 1]))

            # test BuyInfo()
            info_order = self.t.BuyInfo(timestep, stock_prices_now, hedge_costs)
            self.assertIsInstance(info_order, dict, f'Make your info_order a dict. Round {timestep}.')
            self.assertTrue(set(symbols).issubset(set(info_order)),
                f'Include all symbols in your info_order. Missing {set(symbols) - set(info_order)}. Round {timestep}.')
            for sym in symbols:
                self.assertIsInstance(info_order[sym], bool, f'Your info_order must be boolean. Round {timestep}.')
            info_they_get = {sym : hedge_data_now[sym] for sym in symbols if info_order.get(sym, False)}
            self.profit -= sum([hedge_costs[sym] for sym in symbols if info_order.get(sym, False)])
            trades = self.t.MakeTrades(timestep, info_they_get, stock_prices_now)

            # test MakeTrades()
            self.assertIsInstance(trades, dict, f'Make your trades a dict. Round {timestep}.')
            self.assertTrue(set(symbols).issubset(set(trades)),
                f'Include all symbols in your trades. Missing {set(symbols) - set(trades)}. Round {timestep}.')
            total_pos = 0
            for sym in symbols:
                self.assertTrue(abs(trades[sym]) < 6e5, 
                    f'Your trade for {sym} is {trades[sym]}: not within limits. Round {timestep}.')
                total_pos += abs(trades[sym])
            self.assertTrue(total_pos < 1e6, f'Your total trade costs exceed $1M. Round {timestep}.')

            stock_prices_next = dict(zip(symbols, stock_prices[timestep + 1]))
            self.profit += sum(
                [(stock_prices_next[sym] - stock_prices_now[sym]) * trades[sym] for sym in symbols])
        print(f'Finished with total profits {self.profit}.')


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
    