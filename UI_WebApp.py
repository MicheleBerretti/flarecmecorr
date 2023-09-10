import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import scipy.stats as spst
import seaborn as sns

# Set page title
st.title('Flare and CME Correlation')
pw = st.text_input("Insert password")

if pw == st.secrets["PASSWORD"]

    matched_events = pd.read_csv('matched_events.csv')
    matched_events["time_delta"] = matched_events["time_delta"].astype('timedelta64[s]')
    matched_events["time_delta"] = matched_events["time_delta"].astype('int64')
    matched_events["time_delta"] = matched_events["time_delta"]/60
    
    st.write('This is a webapp to show the correlation between the flare and CME parameters.')
    
    tab1, tab2, tab3 = st.tabs(["Catalog", "Correlation", "Plots"])
    
    with tab1:
        st.write('This is the catalog of the matched events.')
        st.write(matched_events)
        st.write('The catalog is composed by the following parameters:')
        st.write('Work In Progress')
    
    
    with tab2:
    
        time_delta = np.array(matched_events["time_delta"])
    
        value_1 = st.selectbox('Select the first parameter', matched_events.columns)
        value_2 = st.selectbox('Select the second parameter', matched_events.columns)
    
        filter = st.checkbox('Do you want to use any filters?', key="filter_corr")
        if filter:
    
            time_smaller = st.number_input('Select T0 (in minutes) for flare start (can be negative if cme is before flare)')
            time_greater = st.number_input('Select T1 (in minutes) for flare start (can be negative if cme is before flare) WARNING: T1 > T0')
    
            st.write("Minimum T: ", np.min(time_delta))
            st.write("Maximum T: ", np.max(time_delta))
            st.write("Use min and max to not use a time filter")
    
    
            cycle = st.select_slider("Select the period of the solar cycle:", options=["Min", "Max"])
            if cycle == "Min":
                cycle_num = 0
            elif cycle == "Max":
                cycle_num = 1
    
            matched_events_temp = matched_events[(matched_events["time_delta"] < time_greater) & (matched_events["cycle"] == cycle_num) & (matched_events["time_delta"] > time_smaller)]
    
            P_corr = spst.pearsonr(matched_events_temp[value_1], matched_events_temp[value_2])
            st.write("Pearson Correlation Coefficient: ", P_corr[0])
            st.write("p-value: ", P_corr[1])
        
        else:
            P_corr = spst.pearsonr(matched_events[value_1], matched_events[value_2])
            st.write("Pearson Correlation Coefficient: ", P_corr[0])
            st.write("p-value: ", P_corr[1])
    
    
    with tab3:
    
        plot_param = st.selectbox("Select the parameter to plot", matched_events.columns)
    
        filter = st.checkbox('Do you want to use any filters?', key="filter_plots")
        if filter:
    
            time_smaller = st.number_input('Select T0 (in minutes) for flare start (can be negative if cme is before flare)')
            time_greater = st.number_input('Select T1 (in minutes) for flare start (can be negative if cme is before flare) WARNING: T1 > T0')
    
            st.write("Minimum T: ", np.min(time_delta))
            st.write("Maximum T: ", np.max(time_delta))
            st.write("Use min and max to not use a time filter")
    
    
            cycle = st.select_slider("Select the period of the solar cycle:", options=["Min", "Max"])
            if cycle == "Min":
                cycle_num = 0
            elif cycle == "Max":
                cycle_num = 1
    
            matched_events_temp = matched_events[(matched_events["time_delta"] < time_greater) & (matched_events["cycle"] == cycle_num) & (matched_events["time_delta"] > time_smaller)]
    
    
            # Seaborn histplot with kde of time delta with different color for kde and hist
            fig = plt.figure()
            sns.histplot(matched_events_temp[plot_param], kde=True, color="orange", stat="density", linewidth=0, bins=20)
            plt.title(f"{plot_param} distribution")
            plt.xlabel(f"{plot_param}")
            plt.ylabel("Density")
            # Remove top and right spines
            sns.despine()
    
            st.pyplot(fig)
        
        else:
            # Seaborn histplot with kde of time delta with different color for kde and hist
            fig = plt.figure()
            sns.histplot(matched_events[plot_param], kde=True, color="orange", stat="density", linewidth=0, bins=20)
            plt.title(f"{plot_param} distribution")
            plt.xlabel(f"{plot_param}")
            plt.ylabel("Density")
            # Remove top and right spines
            sns.despine()
    
            st.pyplot(fig)
