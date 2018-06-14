
import matplotlib.pyplot as plt


class Logger:
    def __init__(self, Chain, interval=None):
        """
            Logger is a wrapper for the MarkovChain class that tracks
            statistics as we move through the states of the chain. Uses
            regular Python lists for performance (as it's faster to append
            to a linked list than it is to merge to NumPy arrays).

            :Chain: Instance of the MarkovChain class.
            :interval: Sets the interval at which statistics are binned;
                        default is 1% of the total number of iterations.
        """
        self.Chain = Chain

        # Assign the binning interval; if there's no interval provided as
        # an argument to Logger, then we bin every 1% of the steps.
        self.interval = max(1, int(Chain.total_steps * 0.01)) if interval is None else interval
        
        # Find the total number of districts.
        stats = self.Chain.state
        first_key = next(iter(stats.keys()))
        self.num_districts = len(stats[first_key])
        
        # Initialize histogram, generating lists at each key.
        self.histograms = {stat: list(cds.values()) for stat, cds in stats.items()}

        # Run the chain.
        self._run_chain()


    def _run_chain(self):
        """
            Class-private method that runs automagically. Runs the chain
            and, at the specified intervals, bins the current statistics
            of the partition. This can be augmented to log stats to the
            console at the same rate, but we can add that as a flag later.

            Futhermore, this should be modified to control for interval
            size, as small intervals with a large number of iterations will
            stress the memory of the machine. We should consider writing
            to a file (every n intervals) or using another caching method.
        """
        step = 0

        # Loop for running the chain. *This method needs to be augmented.*
        for state in self.Chain:
            # If we encounter an interval step, get the current statistics
            # and add their values to the existing histograms.
            if step % self.interval == 0:

                # Add current state's stats to the histogram.
                for stat in self.histograms:
                    self.histograms[stat] += list(state[stat].values())

            step += 1

        # Generate graphical histograms.
        self._generate_histograms()
    

    def _generate_histograms(self):
        """
            Generates graphical histograms (for each statistic) using matplotlib.
        """
        for stat in self.histograms:
            # Calculating the number of histogram bins. Assuming we want each bin
            # to represent ~10 values, we can calculate bins by:
            #
            #   bins = (number of collections) / (number of districts * values per bin)
            bins = int(len(self.histograms[stat]) / (self.num_districts * 10))

            # Plot histogram for this statistic.
            plt.hist(self.histograms[stat], bins=bins)
            plt.show()