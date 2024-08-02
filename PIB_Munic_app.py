# Import libraries
import geobr
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
# Page configuration
st.set_page_config(
    page_title="PIB do Municípios Brasileiros",
    page_icon= "mip_consult_icon.ico",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")
#
st.markdown(
    """
<style>
[data-testid="stMetricValue"] {
    font-size: 25px;
}
</style>
""",
    unsafe_allow_html=True,
)

# Load data
@st.cache_data  # 👈 Add the caching decorator
def load_data1(url1,url2,url3,url4):
    df1 = pd.read_csv(url1,sep=';', encoding='latin1')
    df2 = pd.read_csv(url2,sep=',')
    df3 = pd.read_csv(url3,sep=',')
    df4 = pd.read_csv(url4,sep=';', encoding='latin1')
    return df1, df2, df3, df4
#
def map_munic(UF,Munic, Selec):
    full_state = geobr.read_municipality(code_muni=str(UF), year=2020)
    full_munic = geobr.read_municipality(code_muni=Munic, year=2020)
    fig, ax = plt.subplots(figsize=(4,4), dpi=300)
    full_state.plot(facecolor="#FFFFFF", edgecolor="#696969", linewidth=.1, ax=ax)
    full_munic.plot(facecolor="#3572EF", edgecolor="#3572EF", linewidth=.1,ax=ax)
    ax.set_title("Município "+Selec+ " - "+ str(UF), fontsize=12)
    ax.axis("off")
    st.pyplot(fig)
#
def graf_pip(cod_mun,df):
    #df_dados_pib[df_dados_pib.COD_MUNIC==cod_mun]
    txdf = df_taxas_[df_taxas_['COD_MUNIC']==cod_mun]
    fig1 = px.line(df, x="ANO",
                   y="PIB",
                   title='Taxa de Crescimento real de ' + '{:.3f}%a.a.'.format(txdf.iloc[0,2]))
    fig1.add_annotation(x=2010, y=0.95*min(df['PIB']),
            text="Fonte: IBGE",
            showarrow=False,
            yshift=10)
    st.plotly_chart(fig1)
#
def graf_per(cod_mun,df):
    #df_dados_pib[df_dados_pib.COD_MUNIC==cod_mun]
    txdf = df_taxas_[df_taxas_['COD_MUNIC']==cod_mun]
    fig2 = px.line(df, x="ANO",
                   y="PIB_CAP",
                   title='Taxa de Crescimento real de ' + '{:.3f}%a.a.'.format(txdf.iloc[0,3]))
    fig2.add_annotation(x=2010, y=0.95*min(df['PIB_CAP']),
            text="Fonte: IBGE",
            showarrow=False,
            yshift=10)
    st.plotly_chart(fig2)
#
def graf_pie(cod_mun,df):
    #dfn = df.iloc[:,9:5]
    pie_data = df.iloc[:, 9:13].tail(1).T
    pie_data["Compon."] = ["Agropec.", "Indústria", "Serviços", "Adm. Púb."]
    pie_data.columns = ["Valor Adic.", "Compon."]
    fig3 = px.pie(pie_data,
                  values='Valor Adic.', 
                  names='Compon.', 
                  title='Partic. do Valor Adicionado',
                  color = 'Valor Adic.',
                hole=.5)
    fig3.add_annotation(x=0, y=0,
            text="Fonte: IBGE",
            showarrow=False,
            yshift=10)
    st.plotly_chart(fig3)
#
# tabela do PIB
def tab_pib(UF, Municipio):
    df_est = df_dados_pib[(df_dados_pib['ANO']==2021) & (df_dados_pib.UF==UF)][['COD_MUNIC','NOME_MUNIC','PIB','PIB_CAP']]
    #
    df_est = df_est.sort_values("PIB", ascending=False)
    df_est['RPIB'] = list(range(1,len(df_est)+1))
    df_est = df_est.sort_values("PIB_CAP", ascending=False)
    df_est['RPCAP'] = list(range(1,len(df_est)+1))
    # PIB Total
    idx = df_est.index[df_est['COD_MUNIC'] == Municipio].tolist()
    pib_pos = int(df_est.loc[idx,"RPIB"])
    per_pos = int(df_est.loc[idx,"RPCAP"])
    #if PIP5up.isin([Municipio]).any().any():
    if pib_pos <= 5:
        table_pib = df_est.sort_values("PIB", ascending=False).head()
        table_pib = table_pib[['NOME_MUNIC','PIB','RPIB']]
        table_pib.columns = ['Munic.', 'PIB (Milhões)', 'Rank']
    else:
        ext_mun = df_est[df_est['COD_MUNIC']==Municipio]
        table_pib = pd.concat([df_est.sort_values("PIB", ascending=False).head(4),ext_mun])
        table_pib = table_pib[['NOME_MUNIC','PIB','RPIB']]
        table_pib.columns = ['Munic.', 'PIB (Milhões)', 'Rank']
    #
    table_pib['PIB (Milhões)'] = table_pib['PIB (Milhões)']/1000
    table_pib['PIB (Milhões)'] = table_pib['PIB (Milhões)'].map("R$ {:,.2f}".format)
    table_pib['Rank'] = table_pib['Rank'].map("{:,.0f}\u00BA".format)
    #table_pib = table_pib.style.applymap(lambda x: f"{'text-align: left;':<15}", subset=table_pib.Rank)
    #
    if per_pos <=5:
        table_per = df_est.sort_values("PIB_CAP", ascending=False).head()
        table_per = table_per[['NOME_MUNIC','PIB_CAP','RPCAP']]
        table_per.columns = ['Munic.', 'PIB(per cap.)', 'Rank']
    else:
        ext_mun = df_est[df_est['COD_MUNIC']==Municipio]
        table_per = pd.concat([df_est.sort_values("PIB_CAP", ascending=False).head(4),ext_mun])
        table_per = table_per[['NOME_MUNIC','PIB_CAP','RPCAP']]
        table_per.columns = ['Munic.', 'PIB(per cap.)', 'Rank']

    table_per['PIB(per cap.)'] = table_per['PIB(per cap.)'].map("R$ {:,.2f}".format)
    table_per['Rank'] = table_per['Rank'].map("{:,.0f}\u00BA".format)
    #
    return table_pib, table_per, pib_pos, per_pos    
#
# # Convert PIB to text
def format_numberPIB(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} Bilhôes'
        return f'{round(num / 1000000, 1)} Bilhões'
    return f'{num // 1000} Milhões'
#   
# # Convert PIB to text
def format_numberPER(num):
    if num > 1000:
        if not num % 1000:
            return f'{num // 1000} Mil'
        return f'{round(num / 1000, 1)} Mil'
    return f'{num // 1000}'
# dados básicos dos municípios
git = 'https://raw.githubusercontent.com/rllopes2uem/classDashBoard/main/'
df_dados_pib, df_taxas_, IDHM_df, IPS_df = load_data1(git + 'cl_Dados_2010_21_defl.csv', git + 'Munic_2021.csv', git + 'IDHM_df.csv', git + 'ips_2024.csv')
#
# criando um dicionário Estado-Municípios
states = list(df_dados_pib.NOME_UF.unique())
munic = dict()
for state in range(len(states)):
    munic[states[state]] = list(df_dados_pib[df_dados_pib.NOME_UF== states[state]].NOME_MUNIC.unique())
#
#st.title(':blue[MIP Consult]')
st.markdown("<h1 style='text-align: center; color: blue;'>MIP Consult</h1>", unsafe_allow_html=True)
# Add a sidebar
with st.sidebar:
    st.title('PIB Municipal')
    # selecionando o Estado
    state_selec = st.selectbox('Selecione o Estado', options=list(munic.keys()))
    if state_selec != 'select':
        munic_selec = st.selectbox('Selecione o Município', options=munic[state_selec])
    press_button = st.button('Mostrar')
    #
    if press_button: #st.button('Submit'):
        SG_UF = df_dados_pib[df_dados_pib.NOME_UF==state_selec].UF.unique()[0]
        
        cod_mun = df_dados_pib[(df_dados_pib.NOME_UF==state_selec)&
                               (df_dados_pib.NOME_MUNIC==munic_selec)].COD_MUNIC.unique()[0]
        
        TAB_PIB = df_taxas_[df_taxas_.COD_MUNIC==cod_mun]
        
        dados_mun = df_dados_pib[(df_dados_pib.UF==SG_UF) & 
                                 (df_dados_pib.COD_MUNIC==cod_mun)]
        
        
        map_munic(SG_UF,cod_mun, munic_selec)

# App layout
col = st.columns((1.5, 3.25, 3.25), gap='small')
## Column 1
with col[0]:
    with st.container(border=True):
        st.markdown('<a href="https://www.undp.org/pt/brazil/desenvolvimento-humano/painel-idhm" target="_blank"><abbr title="Índice de Desenvolvimento Humano Municipal">IDHM</abbr></a>', unsafe_allow_html=True)
        if press_button:
            txdf = df_taxas_[df_taxas_['COD_MUNIC']==cod_mun]
            IDHM = IDHM_df[IDHM_df['COD_MUNIC']==cod_mun]
            X = IDHM.iloc[0,8]
            if X >= 0.800:
                lab = "Muito Alto"
            elif X >= 0.700:
                lab = "Alto"
            elif X >= 0.556:
                lab = "Médio"
            elif X == 0.000:
                lab = "Sem Informação"
            else:
                lab = "Baixo"
            st.metric(label=lab, value='{:.3f}'.format(IDHM.iloc[0,8]))
        #
    #st.empty()
    #st.markdown('---')
    with st.container(border=True):
        st.markdown('<span style="font-size: 20px;"><a href="https://ipsbrasil.org.br/" target="_blank"><abbr title="Índice de Progresso Social">IPS</abbr></a></span>', unsafe_allow_html=True)
        if press_button:
            IPS = IPS_df[IPS_df['COD_MUNIC']==cod_mun]
            st.metric(label='ips 2024', value='{:.3f}'.format(IPS.iloc[0,4]))
    
    #st.markdown('---')
    with st.container(border=True):
        st.markdown('<span style="font-size: 20px;">PIB</span>', unsafe_allow_html=True)
        if press_button:
            st.metric(label="2021", value='R$'+format_numberPIB(txdf.iloc[0,4]))
        
    #st.markdown('---')
    with st.container(border=True):
        st.markdown('<span style="font-size: 20px;">PIB per Cap.</span>', unsafe_allow_html=True)
        if press_button:
            st.metric(label="Hab.Ano", value='R$'+format_numberPER(txdf.iloc[0,5]))

    #st.markdown('---')
    #st.markdown('[^1]: Índice de Desenvolvimento Humano Municipal')
    ##----------------------------------------------------------
## Column 2
with col[1]:
    st.markdown('#### Evolução do PIB')
    #st.subheader("A wide column with a chart")
    if press_button:
        df = df_dados_pib[df_dados_pib.COD_MUNIC==cod_mun]
        graf_pip(cod_mun, df)
    else:
        st.write('Aguardando a seleção do Município' )
    
    st.markdown('### PIB')
    if press_button:
        #
        tab1, tab2, pib_p, per_p = tab_pib(SG_UF,cod_mun)
        #
        if pib_p >4:
            st.dataframe(tab1.style.map(lambda _: 'color:blue;background-color: yellow', subset=(tab1.index[4:,],)),hide_index=True)
        else:
            a = pib_p
            b = a - 1
            st.dataframe(tab1.style.map(lambda _: 'color:blue;background-color: yellow', subset=(tab1.index[b:a,],)),hide_index=True)
        #st.dataframe(tab1.style.map(lambda _: 'background-color: yellow', subset=(tab1.index[4:,],)),hide_index=True)

    st.markdown('#### Componentes do VA')
    if press_button:
        
        graf_pie(cod_mun, df)
#
## Column 3
with col[2]:
    st.markdown('#### Evolução do PIB per Capita')
    if press_button:
        graf_per(cod_mun, df)
    
    st.markdown('### PIB per Capita')
    if press_button:
        if per_p >4:
            st.dataframe(tab2.style.map(lambda _: 'color:blue;background-color: yellow', subset=(tab2.index[4:,],)),hide_index=True)
        else:
            a = per_p
            b = a - 1
            st.dataframe(tab2.style.map(lambda _: 'color:blue;background-color: yellow', subset=(tab2.index[b:a,],)),hide_index=True)
        #st.dataframe(tab2.style.map(lambda _: 'background-color: yellow', subset=(tab2.index[0:1,],)),hide_index=True)
#
