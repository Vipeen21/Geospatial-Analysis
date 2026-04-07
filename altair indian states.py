import altair as alt
import pandas as pd

# Sample DataFrame (assuming 'df' is defined as above)
data = {
    'State': ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
              'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand',
              'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
              'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab',
              'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura',
              'Uttar Pradesh', 'Uttarakhand', 'West Bengal'],
    'Population_Density': [308, 17, 398, 1106, 189, 394, 308, 573, 123, 414,
                           319, 860, 236, 365, 128, 132, 52, 119, 270, 551,
                           200, 86, 555, 312, 350, 829, 189, 1028],
    'Forest_Cover_sqkm': [37380, 51540, 28327, 1687, 55717, 2405, 14757, 1588, 15433, 23721,
                          38575, 21144, 77482, 50778, 17219, 17260, 18749, 13197, 51619, 1845,
                          16655, 3343, 26909, 21214, 7726, 16583, 24303, 16805],
    'Average_Annual_Rainfall_mm': [900, 2780, 1900, 1200, 1400, 2900, 800, 600, 1500, 1400,
                                   1100, 3000, 1200, 1000, 2500, 3000, 2500, 2000, 1500, 700,
                                   500, 3000, 1000, 900, 2500, 1000, 1600, 1750],
    'Latitude': [15.9179, 28.2100, 26.2006, 25.0961, 21.2787, 15.2993, 22.2587, 29.0588, 31.1048, 23.6102,
                 15.3173, 10.8505, 22.9734, 19.7515, 24.6637, 25.4670, 23.1645, 26.1584, 20.9517, 31.1471,
                 27.0238, 27.5330, 11.1271, 18.1124, 23.9408, 26.8467, 30.0668, 22.9868],
    'Longitude': [80.1539, 94.7278, 92.9376, 85.3130, 81.8661, 74.1240, 71.1924, 76.0856, 77.1734, 85.2799,
                  75.7139, 76.2711, 78.6569, 75.7139, 93.9062, 91.8330, 92.9376, 94.5624, 85.0985, 75.3412,
                  74.2179, 88.5122, 78.6569, 79.0193, 91.9882, 80.9462, 79.0193, 87.8550]
}

try:
    print("Creating visualizations with Altair...")
    df = pd.DataFrame(data)

    # Configure Altair to save as HTML
    alt.renderers.enable('html')

    # --- 1. Interactive Scatter Plot ---
    print("Generating scatter plot...")
    chart_scatter = alt.Chart(df).mark_circle().encode(
        x=alt.X('Population_Density:Q', 
                scale=alt.Scale(type="log"), 
                title="Population Density"),
        y=alt.Y('Forest_Cover_sqkm:Q', title="Forest Cover (sq km)"),
        size=alt.Size('Average_Annual_Rainfall_mm:Q', title="Average Rainfall (mm)"),
        color='State:N',
        tooltip=['State', 'Population_Density', 'Forest_Cover_sqkm', 'Average_Annual_Rainfall_mm']
    ).properties(
        width=800,
        height=500,
        title='Population Density vs. Forest Cover'
    ).interactive()

    # Save scatter plot
    chart_scatter.save('altair_scatter_plot.html')
    print("Scatter plot saved as 'altair_scatter_plot.html'")

    # --- 2. Interactive Bar Chart ---
    print("Generating bar chart...")
    chart_bar = alt.Chart(df).mark_bar().encode(
        x=alt.X('State:N', 
                sort='-y', 
                title="State",
                axis=alt.Axis(labelAngle=45)),  # Rotate labels for better readability
        y=alt.Y('Average_Annual_Rainfall_mm:Q', 
                title="Average Annual Rainfall (mm)"),
        color=alt.Color('State:N', legend=None),  # Remove legend as it's redundant
        tooltip=['State', 'Average_Annual_Rainfall_mm']
    ).properties(
        width=800,
        height=500,
        title='Average Annual Rainfall by State in India'
    ).interactive()

    # Save bar chart
    chart_bar.save('altair_bar_chart.html')
    print("Bar chart saved as 'altair_bar_chart.html'")

    print("\nAll visualizations have been generated successfully!")
    print("Open the generated HTML files in your web browser to view the interactive charts.")

except Exception as e:
    print(f"An error occurred: {str(e)}")
