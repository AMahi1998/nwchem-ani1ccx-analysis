import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json

# Load the JSON file with correlation and regression data
with open("energy_data_error_metrics_and_correlations1.json", "r") as json_file:
    data = json.load(json_file)

# Filter out formulas with null data for the correlation and regression data
molecular_formulas = [formula for formula in data.keys() if data[formula] is not None]

# Load the JSON file with energy data
with open("energy_data1.json", "r") as json_file:
    energy_data = json.load(json_file)

# Get the list of all molecular formulas for energy data
energy_molecular_formulas = list(energy_data.keys())

# Streamlit App
st.title("Ani1x Energy Data Analysis:")
selected_formula = st.sidebar.selectbox("Select Molecular Formula", molecular_formulas, key="energy_molecular_formula")

if selected_formula:
    st.sidebar.write(f"Selected Molecular Formula: {selected_formula}")

    # Get the energy datasets for the selected formula
    energy_datasets = energy_data[selected_formula]

    # Dropdown to select the method
    selected_method = st.sidebar.selectbox("Select Method", list(energy_datasets.keys()), key="energy_method")

    if selected_method:
        st.sidebar.write(f"Selected Method: {selected_method}")

        # Get the energy values for the selected method
        energy_values = energy_datasets[selected_method]

        # Plot the energy values
        plt.figure(figsize=(10, 6))
        plt.plot(energy_values, marker='o')
        plt.xlabel("Data Point")
        plt.ylabel("Energy")
        plt.title(f"Energy Plot for {selected_method} - {selected_formula}")
        st.sidebar.pyplot(plt)

# Display correlation and regression section on the main page
if selected_formula:
    st.subheader(f"Correlation Heatmap for {selected_formula}")

    # Drop-down to select method for correlation
    regression_models = list(data[selected_formula].keys())
    selected_model = st.selectbox("Select Method", regression_models, key="correlation_method")

    if selected_model:
        st.write(f"Selected Method: {selected_model}")

        # Get the correlation matrix for the selected method and formula
        corr_matrix = data[selected_formula][selected_model]["Coefficients"]

        # Convert the correlation matrix to a DataFrame
        column_names = data[selected_formula][selected_model]["Column Names"]
        corr_df = pd.DataFrame(corr_matrix, columns=column_names, index=column_names)

        # Create a matplotlib figure and axes for the heatmap
        fig_heatmap, ax_heatmap = plt.subplots()

        # Display the heatmap on the axes
        sns.heatmap(corr_df, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax_heatmap)

        # Show the correlation heatmap using st.pyplot()
        st.pyplot(fig_heatmap)

        st.subheader("Regression Results(CCSD prediction)")
        # Get the regression results for the selected model and formula
        model_results = data[selected_formula][selected_model]["Regression Results"]

        # Convert the regression results to a DataFrame
        results_df = pd.DataFrame(model_results)

        # Drop-down to select regression model result
        selected_regression_model = st.selectbox("Select Regression Model", results_df.columns, key="regression_model")

        # Display the selected regression model result in a table
        st.dataframe(results_df[selected_regression_model])

        # Display additional information about the selected model (if available)
        if selected_model in ["DFT_DZ_HF_DZ", "DFT_DZ_HF_Diff", "DFT_DZ_HF_NRE", "DFT_DZ_DFT_TZ",
                              "HF_DZ_HF_TZ_HF_QZ", "MP2_DZ_MP2_TZ_MP2_QZ", "NPNO_DZ_NPNO_TZ"]:
            st.subheader("Additional Information")
            st.markdown("This model includes additional features in the input data.")
            st.markdown("Column Names in the model: {}".format(data[selected_formula][selected_model]["Column Names"]))

