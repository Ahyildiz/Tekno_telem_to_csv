import pandas as pd

# Define a dictionary with the variables and their corresponding symbols and meanings
probability_statistics_variables = {
    "Variable Name": [
        "Variance",
        "Mean",
        "Standard Deviation",
        "Sample Size",
        "Probability of Success",
        "Population Mean",
        "Population Proportion",
        "Sample Mean",
        "Sample Proportion",
        "Z-Score",
        "T-Score",
        "Chi-Square Statistic",
        "P-Value",
        "Degree of Freedom",
        "Expected Frequency",
        "Observed Frequency",
        "Error Term",
        "Regression Coefficient",
        "Correlation Coefficient",
        "Covariance"
    ],
    "Symbols": [
        r"\(\sigma^2\), \(s^2\)",
        r"\(\mu\)",
        r"\(\sigma\), \(s\)",
        r"\(n\)",
        r"\(p\)",
        r"\(\mu_{population}\)",
        r"\(\pi\)",
        r"\(\bar{x}\)",
        r"\(\hat{p}\)",
        r"\(z\)",
        r"\(t\)",
        r"\(\chi^2\)",
        r"\(p-value\)",
        r"\(df\)",
        r"\(E_i\)",
        r"\(O_i\)",
        r"\(e\)",
        r"\(\beta\)",
        r"\(r\)",
        r"\(cov(X,Y)\)"
    ],
    "Meaning": [
        "Measure of dispersion in a dataset",
        "Average value of a dataset",
        "Measure of the amount of variation or dispersion of a set of values",
        "Number of observations in a sample",
        "Likelihood of a success in a Bernoulli trial",
        "Average value of a population",
        "True proportion in a population",
        "Average value of a sample",
        "Proportion in a sample",
        "Standard deviation units from the mean in a normal distribution",
        "Scaled version of the Z-score accounting for sample size",
        "Statistic used to test the statistical significance of observed versus expected data",
        "Probability of obtaining test results at least as extreme as the results actually observed, under the assumption that the null hypothesis is correct",
        "Number of values in a final calculation of a statistic that are free to vary",
        "Frequency expected in a category in a statistical test",
        "Frequency observed in a category in a statistical test",
        "Difference between observed and estimated values",
        "Indicator of the amount of change in the dependent variable that is due to the independent variable",
        "Measure of the strength and direction of association between two variables",
        "Measure of the joint variability of two random variables"
    ]
}

# Convert the dictionary into a DataFrame
variables_df = pd.DataFrame(probability_statistics_variables)

# Convert the DataFrame into a CSV file
variables_csv = variables_df.to_csv(index=False)
variables_csv_path = "probability_statistics_variables.csv"

variables_df.to_csv(variables_csv_path, index=False)

variables_csv_path
