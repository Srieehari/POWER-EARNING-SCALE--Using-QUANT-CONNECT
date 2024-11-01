# region imports
from AlgorithmImports import *
# endregion

class POWEREARNINGSCALE(QCAlgorithm):

    def initialize(self):
        #intitializs the start and end of the test
        self.set_start_date(2023, 4, 30)
        self.set_end_date(2023, 9, 2)
        #cash is currently 100000
        self.set_cash(100000)


        
        self.SPY = self.AddEquity("SPY", Resolution.Minute).Symbol

        self.AddUniverse(self.CoarseFilter, self.FineFilter)
        
        #starts the equity at SPY and will traverse through all the other symbols
        self.SPY = self.AddEquity("SPY").Symbol
        #check every day and buy stock 
        self.Schedule.On(self.DateRules.EveryDay("SPY"), self.TimeRules.AfterMarketOpen("SPY",1), self.AfterMarketOpen)

        
    def AfterMarketOpen(self): 
        self.Debug("Running AfterMarketOpen")

        #loops through the entire thing
        for security in self.ActiveSecurities.Values:

            #SKIPS OVER SPY
            symbol = security.Symbol

            if symbol == self.SPY:
                continue
            
            #Requests History for the symbol 
            historyData = self.History(symbol, 7, Resolution.Daily)

            try:
                #Accesss the close and OPen columns
                openDayAfterEarnings = historyData['open'][-1]
                closeDayAfterEarnings = historyData['close'][-1]
                highDayAfterEarnings = historyData['high'][-1]
                closeDayBeforeEarnings = historyData['close'][-2]
            except:
                self.Debug(f"History data unavailable for {symbol.Value}")
                continue


            #Compares the two earnings and calulates the price gap between the two earnings.
            priceGap = openDayAfterEarnings - closeDayBeforeEarnings
            #percent
            percentGap = priceGap / closeDayBeforeEarnings
            #Make sure that it doesnt fade away
            closeStrength = (closeDayAfterEarnings - openDayAfterEarnings) / (highDayAfterEarnings - openDayAfterEarnings)

            if percentGap > 0.05:
                self.Debug(f"{symbol.Value} gapped up by {percentGap} - {closeDayBeforeEarnings} {openDayAfterEarnings}")

                if closeDayAfterEarnings > closeDayBeforeEarnings and closeStrength > 0.5:
                    self.Debug(f"{symbol.Value} closed strong!")
                else:
                    self.Debug(f"{symbol.Value} faded after earnings")


    #Filter through the stock symbols
    def CoarseFilter(self, universe):
                universe = [asset for asset in universe if asset.DollarVolume > 1000000 and asset.Price > 10 and asset.HasFundamentalData]

                sortedByDollarVolume = sorted(universe, key = lambda asset: asset.DollarVolume, reverse = True)

                topSortedByDollarVolume = sortedByDollarVolume[:500]
                #sorts the objects by symbol to seee
                symbolObjects = [asset.Symbol for asset in topSortedByDollarVolume]
                #Creates only one with ticker
                tickerSymbolValuesOnly = [symbol.Value for symbol in symbolObjects]

                return symbolObjects


        #Filters even more 
    def FineFilter(self, coarseUniverse):
        yesterday = self.Time - timedelta(days=1)

        # Filter symbols based on the availability of basic earnings data and market cap
        FineUniverse = [
            asset.Symbol 
            for asset in coarseUniverse 
            if hasattr(asset, 'EarningReports') and hasattr(asset.EarningReports, 'BasicEPS') and asset.MarketCap > 1e9
        ]
        
    


        

        return FineUniverse    
    
    def on_data(self, data: Slice):
        if not self.portfolio.invested:
            self.set_holdings("SPY", 0.33)
            self.set_holdings("BND", 0.33)
            self.set_holdings("AAPL", 0.33)