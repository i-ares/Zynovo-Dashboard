from mftool import Mftool
from sklearn.ensemble import RandomForestClassifier
import streamlit as st, pandas as pd, numpy as np, plotly.express as px\


mf=Mftool()

st.title("ZYNOVO")
st.title('Your All-in-One Financial Advisor')

option=st.sidebar.selectbox(
    "Choose an option",
    ["View All schemes", "View scheme details", "Historical NAV", "Compare NAVs", 
     "Average Assets under Management", "Scheme Performance", "Risk and Volatility Analysis"]
)

scheme_names={v: k for k, v in mf.get_scheme_codes().items()}

if option=="View All schemes":
    st.header("All Mutual Fund Schemes")
    amc=st.sidebar.text_input("Enter AMC name")
    schemes=mf.get_available_schemes(amc)
    st.write(pd.DataFrame(schemes.items(), columns=["Scheme Name", "Scheme Code"])) if schemes else st.write("No schemes found") 


if option=="View scheme details":
    st.header("Scheme Details")
    scheme_code=scheme_names[st.sidebar.selectbox("Select Scheme", list(scheme_names.keys()))]
    details=pd.DataFrame(mf.get_scheme_details(scheme_code)).iloc[0]
    st.write(details)

if option=="Historical NAV":
    st.header("Historical NAV")
    scheme_code=scheme_names[st.sidebar.selectbox("Select Scheme", scheme_names.keys())]
    nav=mf.get_scheme_historical_nav(scheme_code, as_Dataframe=True)
    st.write(nav)

if option=="Compare NAVs":
    st.header("Compare NAVs")
    selected_schemes=st.sidebar.multiselect("Select Schemes to compare", options=list(scheme_names.keys()))
    if selected_schemes:
        comparison_df=pd.DataFrame()
        for scheme in selected_schemes:
            code= scheme_names[scheme]
            data=mf.get_scheme_historical_nav(code, as_Dataframe=True)
            data=data.reset_index().rename(columns={"Index":"Date"})
            data["date"]=pd.to_datetime(data["date"], dayfirst=True).sort_values()
            data["nav"]=data["nav"].replace(0,None).interpolate()
            comparison_df[scheme]=data.set_index("date")["nav"]

        fig=px.line(comparison_df, x=comparison_df.index, y=comparison_df.columns, title="NAV Comparison")
        st.plotly_chart(fig)
    else:
        st.write("Select atleast 2 schemes to compare")


#avg aum
if option=="Average Assets under Management":
    st.header("Average AUM")
    aum_data=mf.get_average_aum('July - September 2024', False)
    if aum_data:
        aum_df=pd.DataFrame(aum_data)
        aum_df["Total AUM"]=aum_df[["AAUM Overseas","AAUM Domestic"]].astype(float).sum(axis=1)
        st.write(aum_df[["Fund Name", "Total AUM"]])    
    else:
        st.write("No data found") 

elif option=="Scheme Performance":
    st.header("Scheme Performance")
    
    scheme_name=st.sidebar.selectbox("Select Scheme", scheme_names.keys())
    scheme_code=scheme_names[scheme_name]
    nav_data=mf.get_scheme_historical_nav(scheme_code, as_Dataframe=True)

    if not nav_data.empty:
        nav_data=nav_data.reset_index().rename(columns={"Index":"Date"})
        nav_data["month"]=pd.DatetimeIndex(nav_data['date']).month
        nav_data['nav']=nav_data['nav'].astype(float)
        heatmap_data=nav_data.groupby("month")["dayChange"].mean().reset_index()   
        heatmap_data["month"]=heatmap_data["month"].astype(str)
        fig=px.density_heatmap(heatmap_data, x="month", y="dayChange", title=f"NAV performance of {scheme_name}", color_continuous_scale="agsunset"
                               , labels={"day change":"Average Daily Change"})
        st.plotly_chart(fig)
    else:
        st.write("No data found for the selected scheme")


#Risk and Volatility Analysis

elif option=="Risk and Volatility Analysis":
    st.header("Risk and Volatility Analysis")
    scheme_name=st.sidebar.selectbox("Select Scheme", scheme_names.keys())
    scheme_code=scheme_names[scheme_name]
    nav_data=mf.get_scheme_historical_nav(scheme_code, as_Dataframe=True)

    if not nav_data.empty:

        nav_data=nav_data.reset_index().rename(columns={"Index":"Date"})
        nav_data["date"]=pd.to_datetime(nav_data["date"], dayfirst=True)

        nav_data["nav"]=pd.to_numeric(nav_data["nav"], errors="coerce")
        nav_data=nav_data.dropna(subset=["nav"])

        #calculate daily returns
        nav_data["returns"]=nav_data["nav"]/nav_data["nav"].shift(1)-1
        nav_data=nav_data.dropna(subset=["returns"])


        #Calculate metrics
        annualised_volatility = nav_data["returns"].std()*np.sqrt(252)
        annualised_return = ((1+nav_data["returns"].mean())**252)-1
        risk_free_rate=0.06
        sharpe_ratio=(annualised_return-risk_free_rate)/annualised_volatility

        st.write(f"### Metrics for {scheme_name}")
        st.metric("Annualised Volatility", f"{annualised_volatility:.2%}")
        st.metric("Annualised Return", f"{annualised_return:.2%}")
        st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")

        #Plot
        fig=px.scatter(
            nav_data, x="returns", y="returns", title=f"Risk Return Scatter for {scheme_name}",
            labels={"returns":"Daily Returns", "date":"Date"}
        )
        st.plotly_chart(fig)


        #Monte Carlo Simulation
        st.write("### Monte Carlo Simulation for future NAV projection")

        #parameters
        num_simulations=st.slider("Number of Simulations", 100, 5000, 1000)
        num_days=st.slider("Number of Days to simulate", 30, 365, 252)

        #Monte Carlo Simulation
        last_nav=nav_data["nav"].iloc[-1]
        daily_volatility=nav_data["returns"].std()
        daily_mean_return=nav_data["returns"].mean()

        simulation_results=[]
        for _ in range(num_simulations):
            prices=[last_nav]
            for _ in range(num_days):
                simulated_return=np.random.normal(daily_mean_return, daily_volatility)
                prices.append(prices[-1]*(1+simulated_return))
            simulation_results.append(prices)

        #dataframe visualisation
        simulation_df=pd.DataFrame(simulation_results).T
        simulation_df.index.name="Day"
        simulation_df.columns=[f"Simulation {i+1}" for i in range(num_simulations)]


        #plot
        fig_simulation=px.line(simulation_df, 
                               title=f"Monte Carlo Simulation for {scheme_name} future NAV projection",
                               labels={"value":"Projected NAV", "index":"Day"},
                               template="plotly_dark"
                            )
        st.plotly_chart(fig_simulation)


        #statistics
        final_prices=simulation_df.iloc[-1]
        st.write(f"### Simulation Statistics for {scheme_name}")
        st.metric("Expected Final NAV", f"{final_prices.mean():.2f}")
        st.metric("Minimum Final NAV", f"{final_prices.min():.2f}")
        st.metric("Maximum Final NAV", f"{final_prices.max():.2f}")
    
    else:
        st.write("No data found for the selected scheme")