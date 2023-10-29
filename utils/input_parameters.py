from utils.distribution import normal_distribution, triangular_distribution, uniform_distribution
import streamlit as st 
import seaborn as sns
import plotly.express as px


def dist_input(sample_size, seed, key='area', guess_estimate= 200, sd_estimate=1):

    st.subheader('Input Parameter')
    c1, c2, c3= st.columns([2,0.2,2])

    with c1:
        dist = st.selectbox(
        'Select Distribution type:',
        ('Normal Dist', 'Triangular Dist', 'Uniform Dist'), key= f"selectbox_{key}"
    )
    


    if dist == 'Normal Dist' :

        truncated_limits = None
        with c3:
            truncated = st.checkbox('Truncated Distribution', value=False,key=f'checkbox_{key}')
        c1, c2= st.columns([3,1])
        if truncated:
            c1, c2, c3, = st.columns(3)
            with c1:
                mean_value = st.number_input("Mean_value", value=guess_estimate, step=0.1, key=f"number1_{key}")
            with c2:
                std_value = st.number_input("Standard deviation", value=sd_estimate, step=0.1, key=f"number2_{key}")
            with c3:
                truncated_limits= st.slider("Truncated limites", min_value=(mean_value-4*std_value), max_value=(mean_value+4*std_value), value=(mean_value-3*std_value, mean_value+3*std_value), key=f"number3_{key}")


        else:
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                mean_value = st.number_input("Mean_value", value=guess_estimate, step=0.1, key=f"number4_{key}")
            with c2:
                std_value = st.number_input("Standard deviation", value=sd_estimate, step=0.1, key=f"number5_{key}")

        data = normal_distribution(mean_value=mean_value, std_value=std_value, size=sample_size, truncated_limites =truncated_limits, seed=seed)


    elif dist == 'Triangular Dist': 
            c1, c2 = st.columns([1,3])
            with c1:
                ml_value = st.number_input("Most Likely value", value=guess_estimate, step=0.1)
            with c2:
                min_value, max_value = st.slider("Min Max values", min_value=(-2*ml_value), max_value=(4*ml_value), value=(-ml_value, 3*ml_value))   
        
            data = triangular_distribution(ml_value=ml_value, min_value=min_value, max_value= max_value, size=sample_size, seed=seed)
        


    elif dist == 'Uniform Dist':  
        c1, c2 = st.columns([3,1])
        with c1:
            min_value, max_value = st.slider("Min Max values", 0.5*guess_estimate, 1.5*guess_estimate, value=(0.5*guess_estimate, 1.5*guess_estimate))   

        data = uniform_distribution(min_value=min_value, max_value=max_value, size=sample_size, random_state=seed)
    

    c1, c2, c3= st.columns(3)
    with c1:
            fig = px.histogram(data, 
                        nbins=200, 
                        title="Normal Distribution",
                        opacity=0.9,
                        color_discrete_sequence=['lightblue'],
                        barmode="overlay",)
            fig.update_layout(xaxis_title="Value", yaxis_title="Frequency")
            # Remove the legend
            fig.update_layout(showlegend=False)
            # Display the histogram in the Streamlit app
            st.plotly_chart(fig)
    return data
        


if __name__ == '__main__':
    dist_input()




