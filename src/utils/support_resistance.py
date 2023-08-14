import numpy as np

from utils.extras import format_float


class SupportResistance:
    """With methods to help in detecting Support Resistance."""

    def is_support(self, df, i):
        """Helper function to validate the support zone."""
        return df['low'][i] < df['low'][i - 1] < df['low'][i - 2] and \
        df['low'][i] < df['low'][i + 1] < df['low'][i + 2]


    def is_resistance(self, df, i):
        """Helper function to validate the resistance zone."""
        return df['high'][i] > df['high'][i - 1] and \
        df['high'][i] > df['high'][i + 1] > df['high'][i + 2] and \
        df['high'][i - 1] > df['high'][i - 2]


    def is_far_from_level(self, l, s, levels):
        """Helper function to validate detected level from sr zone."""
        return np.sum([abs(l - x) < s for x in levels]) == 0


    def sr_levels(self, data):
        """Helper function to find the support resistance levels."""
        levels = []
        s = np.mean(data['high'] - data['low'])
        for i in range(2, data.shape[0] - 2):
            if self.is_support(data, i):
                l = data['low'][i]
                if self.is_far_from_level(l, s, levels):
                    levels.append(format_float(l))
            elif self.is_resistance(data, i):
                l = data['high'][i]
                if self.is_far_from_level(l, s, levels):
                    levels.append(format_float(l))
        return sorted(levels)
