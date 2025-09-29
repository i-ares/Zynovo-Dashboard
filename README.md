# ZYNOVO: Your All-in-One Financial Advisor

ZYNOVO is a Streamlit-based dashboard that provides comprehensive analytics and visualizations for Indian mutual funds. It leverages the `mftool` library and other data science tools to help users analyze schemes, compare NAVs, assess risk, and simulate future performance.

## Features

- **View All Schemes:** List all mutual fund schemes by AMC.
- **Scheme Details:** Get detailed information about any scheme.
- **Historical NAV:** Visualize the historical Net Asset Value of a scheme.
- **Compare NAVs:** Compare NAV trends across multiple schemes.
- **Average Assets Under Management:** View average AUM for a selected period.
- **Scheme Performance:** Analyze monthly NAV performance with heatmaps.
- **Risk and Volatility Analysis:** Calculate and visualize risk metrics, including annualized volatility, returns, Sharpe ratio, and run Monte Carlo simulations for future NAV projections.

## Getting Started

### Prerequisites

- Python 3.12+
- pip

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/i-ares/Zynovo-Dashboard.git
   cd MF-dashboard
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv mfenv
   source mfenv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the dashboard:**
   ```bash
   streamlit run dashboard.py
   ```

## Usage

- Use the sidebar to select different analytics options.
- Enter AMC names, select schemes, or adjust simulation parameters as needed.
- Visualizations and metrics will update based on your selections.

## Project Structure

```
Zynovo-Dashboard/
├── dashboard.py         # Main Streamlit app
├── mfenv/              # Python virtual environment (not needed in repo)
```

> **Tip:** Do not commit the `mfenv/` folder to your repository. Add it to `.gitignore`.

## Dependencies

- [streamlit](https://streamlit.io/)
- [pandas](https://pandas.pydata.org/)
- [numpy](https://numpy.org/)
- [plotly](https://plotly.com/python/)
- [mftool](https://pypi.org/project/mftool/)
- [scikit-learn](https://scikit-learn.org/)

## Contributing

Contributions are welcome! Please open issues or submit pull requests for new features, bug fixes, or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Data and APIs provided by [mftool](https://pypi.org/project/mftool/)
- Built with [Streamlit](https://streamlit.io/)
