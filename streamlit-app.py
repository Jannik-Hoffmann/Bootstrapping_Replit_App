import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

def generate_data(n, correlation):
    mean = [0, 0]
    cov = [[1, correlation], [correlation, 1]]
    return np.random.multivariate_normal(mean, cov, n)

def bootstrap_correlation(data, n_iterations):
    correlations = []
    for _ in range(n_iterations):
        sample = resample(data)
        correlations.append(np.corrcoef(sample.T)[0, 1])
    return correlations

def resample(data):
    return data[np.random.randint(len(data), size=len(data))]

# Streamlit UI
st.title("WTF is Bootstrapping?!?: An Interactive Demonstration")

st.write("""
Ever found bootstrapping in statistics a bit elusive? You're not alone! This app is designed to turn that complexity into clarity with hands-on visualizations and simulations. Whether you’re new to the concept or looking to solidify your understanding, I am sure you will find this app to be interesting for you.

**What’s Bootstrapping All About?**
         
Bootstrapping is a key technique for most quantitative research projects. By resampling your data with replacement, you can get insights about your population even when you don’t know its underlying distribution. It’s perfect for when:

- The actual distribution of the data from which the sample is drawn is a mystery 👻
- You’re working with a small sample size
- You need to calculate confidence intervals for complex statistics

**Why Give Bootstrapping a Try?**
         
With bootstrapping, you can:

- Get better information about the sampling distribution of almost any statistic
- Build confidence intervals without relying on normality of the data
- Test hypotheses when traditional methods fall short due to the problems described above

Dive into my interactive demo and see bootstrapping in action! Adjust the parameters and watch how the bootstrap distribution and confidence intervals shift.
""")

# Sidebar inputs
st.sidebar.header("Data Generation Parameters")
n_samples = st.sidebar.slider("Sample Size", 10, 500, 100)
correlation = st.sidebar.slider("True Correlation", -1.0, 1.0, 0.5, 0.1)
n_bootstrap = st.sidebar.slider("Number of Bootstrap Samples", 100, 5000, 1000)

# Sidebar Quick Guide
with st.sidebar.expander("Quick Guide", expanded=True ):
    st.write("""
    - **Sample Size**: The number of data points in the generated dataset. Smaller sample sizes may show more variability.
    - **True Correlation**: The correlation parameter used to generate the data. Adjust this to see how different correlations affect the results.
    - **Number of Bootstrap Samples**: The number of resamples used in bootstrapping. More samples usually lead to more stable estimates.
    """)

# Sidebar References and GitHub Link
import streamlit as st

# Sidebar with GitHub link and star button
with st.sidebar.expander("GitHub", expanded=True):
    st.markdown("""
    - This app is open-sourced on GitHub. Feel free to check out the code and contribute:
    - ⭐ Star the project on GitHub
      <iframe src="https://ghbtns.com/github-btn.html?user=Jannik-Hoffmann&repo=Bootstrapping-Streamlit-App&type=star&count=true" width="150" height="30" title="GitHub"></iframe>
    """, unsafe_allow_html=True)


# Generate data
data = generate_data(n_samples, correlation)

# Plot original data with regression line
fig, ax = plt.subplots()
ax.scatter(data[:, 0], data[:, 1], alpha=0.5, label='Data Points')
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title(f"Original Data (n={n_samples}, r={correlation:.2f})")

# Fit a linear regression model
slope, intercept = np.polyfit(data[:, 0], data[:, 1], 1)
x_fit = np.linspace(data[:, 0].min(), data[:, 0].max(), 100)
y_fit = slope * x_fit + intercept

# Plot regression line
ax.plot(x_fit, y_fit, 'k--', label='Regression Line')
ax.legend()
st.pyplot(fig)

# Perform bootstrapping
bootstrap_correlations = bootstrap_correlation(data, n_bootstrap)

# Create histogram data
hist_data = np.histogram(bootstrap_correlations, bins=30, density=True)

# Plot bootstrap distribution with Plotly for interactivity
fig = go.Figure()

# Add histogram
fig.add_trace(go.Histogram(
    x=bootstrap_correlations,
    histnorm='probability',  # This scales the histogram to display probability density
    name='Bootstrap Distribution',
    nbinsx=20  # Number of bins for the histogram
))

# Add true correlation line
fig.add_trace(go.Scatter(
    x=[correlation, correlation],  # X values for the line
    y=[0, 1],  # Initial y values; Plotly will adjust this range based on histogram
    mode='lines',
    line=dict(color='red', width=2, dash='dash'),
    name='True Correlation'
))

# Add mean of bootstrap samples line
fig.add_trace(go.Scatter(
    x=[np.mean(bootstrap_correlations), np.mean(bootstrap_correlations)],  # X values for the line
    y=[0, 1],  # Initial y values; Plotly will adjust this range based on histogram
    mode='lines',
    line=dict(color='green', width=2, dash='dash'),
    name='Bootstrap Mean'
))

# Update layout
fig.update_layout(
    title=f"Bootstrap Distribution (n_iterations={n_bootstrap})",
    xaxis_title="Correlation", # X-axis title
    yaxis_title="Density", # Y-axis title
    barmode='overlay',  # Ensures the histogram and lines are overlaid correctly
    yaxis= dict(title_text='Density', range=[0, 0.3]),  # Set y-axis range to 0-1.1
    showlegend=True
)

# Display the plot
st.plotly_chart(fig)

# Calculate and display confidence interval
confidence_interval = np.percentile(bootstrap_correlations, [2.5, 97.5])
st.write(f"95% Confidence Interval for Correlation: ({confidence_interval[0]:.3f}, {confidence_interval[1]:.3f})")

st.write("""
## Interpretation
The histogram above shows the distribution of correlations obtained through bootstrapping. 
The red dashed line represents the true correlation we set, while the green dashed line shows the mean of our bootstrap samples.
The 95% confidence interval gives us a range where we can be 95% confident that the true correlation lies.

Try adjusting the parameters in the sidebar to see how they affect the bootstrap distribution and confidence interval!
""")
st.write("""
## References
- Wright, D. B., London, K., & Field, A. P. (2018). Using Bootstrap Estimation and the Plug-in Principle for Clinical Psychology Data. *Journal of Experimental Psychopathology, 2*(2).

- Kmiecik, M. J., & Pongpipat, E. E. (2018). [Bootstrapping and Permutation Testing: A Shiny App](https://mattkmiecik.com/post-Bootstrapping-and-Permutation-Testing-Shiny-App.html). Retrieved from https://mattkmiecik.com/post-Bootstrapping-and-Permutation-Testing-Shiny-App.html
""")
