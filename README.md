Let's pick up where we left off, shall we?

Recall our previous disappointment - the mismatch between our dataset and the weather station data? That was a curveball, wasn't it? Half of our measurements were out of range, raising eyebrows and doubts alike. Our quest for data validation had hit a snag, but as any seasoned data scientist will tell you, every problem is a hidden opportunity waiting to be discovered.

I'm sure you have some ideas on how to solve this, so I'll share mine...

One thing that bugs me is the tolerance level I chose. Why 1.5%?

We saw that half of our means were not within that tolerance, but why would it be within 1.5% and not 5%?

Although we may think 1.5% is a good measurement of accuracy, there may be errors in each dataset, and more variation in one than the other, which could make the means differ by more than 1.5% even if the objective truth is that the means are the same. We need to be a little more scientific with our approach and account for the difference in the data. I am sure you know what I am about to say next, right?

**Hypothesis testing** takes into account both the means and the variances of the distributions being compared. The variance here is crucial because it gives us insight into the spread of the data points around the means for our two datasets. Two samples could have the same mean but very different variances, leading to different interpretations of their similarities or differences.

Our main goal is the same: Is the data in our `MD_agric_df` dataset representative of reality? To answer this, we use weather-related data from nearby stations to validate our results. If the weather data matches the data we have, we can be more confident that our dataset represents reality.

So what's the plan?
1. Create a null hypothesis.
1. Import the `MD_agric_df` dataset and clean it up.
1. Import the weather data.
1. Map the weather data to the field data.
1. Calculate the means of the weather station dataset and the means of the main dataset.
2. Calculate all the parameters we need to do a t-test.
3. Interpret our results.

Do you see a bit of repetition here? Steps 2-5 are a repeat of last time. The quick and dirty fix is to copy that code across to our notebook, but what about next time and the time after that? All of that code will also clutter this notebook and make our analysis harder to read.

You might also think of exporting the fixed and merged data from last time to a CSV, but what if there is new data in the database?

So, let's stop for a second and think about how we can make this simpler, more extendible and reusable in the future.