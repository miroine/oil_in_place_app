import streamlit as st 
import plotly.express as px
import pandas as pd 
from utils.input_parameters import *
import numpy as np




def main():
    m3_to_bbl_conversion = 6.28981
    st.subheader('MONTE CARLO CALCULATION IN PLACE VOLUME')

    st.write("This is a web based application to create a monte carlo uncertainty for inplace volume estimate ,"
             " based on static inplace volume equation . This is part of the open source initiative by Merouane Hamdani.")
    
    # Read
    c1, c2, c3= st.columns([2,0.3,2])

    
    with c1:
        sample_size = st.slider("sample size", min_value=1000, max_value= 100000)
    with c3:
        seed = st.slider("seed", min_value=10, max_value= 1000)   
    

    st.subheader ("Area Estimate")

    st.write("Define the production area, this could be made in the furte with area vs depth where one could cut by the contact .") 
    with st.expander("Area estimate"):
        area_data= dist_input(sample_size=sample_size, seed=seed, key='area', guess_estimate=100.0, sd_estimate=10.0)

    st.subheader ("Thickness")
    st.write("Gross Reservoir thickness that contains hydrocarbon ")
    with st.expander("thickness estimate"):
        thickness_data= dist_input(sample_size=sample_size, seed=seed,key='thickness', guess_estimate=50.0, sd_estimate=5.0)

    st.subheader ("NTG")
    st.write("Net To Gross parameter to define the net hydrocabon column ")
    with st.expander("NTG estimate"):
        ntg_data= dist_input(sample_size=sample_size, seed=seed,key='ntg', guess_estimate=0.5, sd_estimate=0.1)

    st.subheader ("POROSITY")
    st.write("Net porosity that contains hydrocarbon")
    with st.expander("PORO estimate"):
        poro_data= dist_input(sample_size=sample_size, seed=seed,key='poro', guess_estimate=0.2, sd_estimate=0.01)

    st.subheader ("WATER SATURATION")
    st.write("Estimate of the irreducible water saturation")
    with st.expander("Sw estimate"):
        sw_data= dist_input(sample_size=sample_size, seed=seed, key='sw', guess_estimate=0.4, sd_estimate=0.1)

    st.subheader ("OIL VOLUME RELATIVE FACTOR")
    st.write("Estimate of the BO")
    with st.expander("bo estimate"):
        bo_data= dist_input(sample_size=sample_size, seed=seed, key='bo', guess_estimate=1.2, sd_estimate=0.01)

    st.subheader ("GAS OIL RATIO ")
    st.write("Estimate of the GOR")
    with st.expander("gor estimate"):
        gor_data= dist_input(sample_size=sample_size, seed=seed, key='gor', guess_estimate=150.0, sd_estimate=1.0)

    st.subheader ("RECOVERY FACTOR")
    st.write("Estimate of the recovery factor ")
    with st.expander("Recovery estimate"):
        rf_data= dist_input(sample_size=sample_size, seed=seed, key='rf', guess_estimate=0.5, sd_estimate=0.05)   


    st.subheader('VOLUMETRIC RESULTS')
    st.write("Resulted distribution is ")
    # Calculations
    GRV = area_data * thickness_data                                           # GRV in cubic meters
    NRV = GRV *  ntg_data                                                    # NRV in cubic meters
    HCPV = NRV * poro_data * (1-sw_data)                                             # HCPV in cubic meters
    OIIP_m3 = HCPV / bo_data                                                  # OIIP in cubic meters
    OIIP = (HCPV * m3_to_bbl_conversion) / bo_data                       # OIIP in mmbbls
    ASSOCIATED_GAS = OIIP_m3 * gor_data    /1000                              # ASSOCIATED GAS 
    Resources_m3 = OIIP_m3 * rf_data                                          # Recoverable Resources in cubic meters
    Resources = OIIP * rf_data  

    c1, c2= st.columns([1,3])
    st.subheader('Resulted Distribution plot')
    with c1:
            
            headers = ('Area (1E6m2)','Thickness (m)','NTG','Porosity','Sw','Bo (m3/m3)','RF (%)','GRV (1E6m3)','NRV (1E6m3)','HCPV (1E6m3)','OIIP (m3)',
               'OIIP (mmbo)', 'Ressource (1E6m3)', 'ASSO GAS (1e9m3)')
            data = [area_data, thickness_data, ntg_data, poro_data, sw_data, bo_data,rf_data ,GRV, NRV, HCPV, OIIP_m3, OIIP, Resources_m3,ASSOCIATED_GAS]
            data_dict = dict(zip(headers, data))
            df = pd.DataFrame(data_dict)
            vec_name = st.selectbox('Select Paramter to view:',
        df.columns.to_list(), key= f"Parameter")
            
    with c2:            
            fig = px.histogram(df.loc[:, vec_name], 
                        nbins=200, 
                        title=f"{vec_name} Distribution ",
                        opacity=0.8,
                        color_discrete_sequence=['green'],
                        barmode="overlay",)
            fig.update_layout(xaxis_title="Value", yaxis_title="Frequency")
            # Customize the edge color
            fig.update_traces(marker_line_color='black', marker_line_width=1)
            mean_value = np.mean(df.loc[:, vec_name])
            fig.add_vline(x=mean_value, line_dash="dash", line_color="red", annotation_text=f"Mean ({mean_value:.2f})")
            # Remove the legend
            fig.update_layout(showlegend=False)
            # Display the histogram in the Streamlit app
            st.plotly_chart(fig)
    

    st.subheader('Summary statistics')
    percentiles = [0.1, 0.25, 0.5, 0.75, 0.9]

    with st.expander("⏰ Statistical data"):
        showData=st.multiselect('Filter: ',df.columns,default=df.columns.to_list())
        st.dataframe(df.describe(percentiles=percentiles).loc[:],use_container_width=True)
        st.download_button('export data as', df.to_csv().encode('utf-8'), file_name='data.csv',mime='text/csv',)
    
    st.subheader('Correlation factors')
    vec_list =['GRV (1E6m3)','NRV (1E6m3)','HCPV (1E6m3)','OIIP (m3)',
               'OIIP (mmbo)', 'Ressource (1E6m3)', 'ASSO GAS (1e9m3)']
    vec_name = st.selectbox('Select Paramter to view:',
        vec_list, key= f"2Parameter")
    
    correlation = df.corr(method='pearson')[vec_name]
    # Format the DataFrame to display values as percentages
    df_corr= correlation.to_frame()
    
    # Remove the 'B' column
    df_corr= df_corr.drop(vec_list, axis=0).sort_values(by=vec_name, ascending=True)
    c1, c2,c3= st.columns([2,2,1])
    df_corr_percentage= df_corr.style.format("{:.2%}")
    with c1:
        st.dataframe(df_corr_percentage)
    with c2:
        fig = px.bar(x=df_corr[vec_name], y=df_corr.index, 
                     orientation='h', 
                     title='Correlation factor',
                     color_discrete_sequence=['lightblue'])
        fig.update_layout(xaxis_title="Value", yaxis_title="Frequency")
        st.plotly_chart(fig)

        


if __name__ == '__main__':

    main()
    