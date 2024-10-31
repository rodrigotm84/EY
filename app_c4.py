import streamlit as st
import pandas 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

file_path='cge4_FIL.xlsx'
df0 = pandas.read_excel(file_path, sheet_name='group0')
df1 = pandas.read_excel(file_path, sheet_name='group1')
df2 = pandas.read_excel(file_path, sheet_name='group2')
df3 = pandas.read_excel(file_path, sheet_name='group3')
df4 = pandas.read_excel(file_path, sheet_name='group4')
df5 = pandas.read_excel(file_path, sheet_name='group5')
taus=['taud[...]','tauz[j]','taum[j]','ssp[...]', 'ssg[...]']
grid=[x * 0.2 for x in range(6)]

udf1 = pandas.DataFrame(df1['variable'].unique(), columns=['variable'])
udf2 = pandas.DataFrame(df2['variable'].unique(), columns=['variable'])
#udf3 = pandas.DataFrame(df3['variable'].unique(), columns=['variable'])
udf4 = pandas.DataFrame(df4['variable'].unique(), columns=['variable'])
udf5 = pandas.DataFrame(df5['variable'].unique(), columns=['variable'])

vars=pandas.concat([udf1,udf2,udf4,udf5],keys=[1, 2, 4, 5],ignore_index=False) #tirei udf3
vars = vars.reset_index()

# Configurando o título e a sidebar
st.title("CGE Models")
st.sidebar.markdown("#### Author: Rodrigo Miyamoto")
st.sidebar.title("Controls")

# Selecionando a variável a ser exibida
shock = st.sidebar.selectbox("Shock:", taus)
variable = st.sidebar.selectbox("Variable:", vars['variable'])

svars = vars[vars['variable'] == variable]

if svars['level_0'].iloc[0] == 1:
    db=df1
    sectors=pandas.DataFrame(db['sector'].unique(), columns=['sector'])
    sector = st.sidebar.selectbox("Sector:", sectors['sector'])
    dbf=db[(db['shock']==shock) & (db['variable'] == variable) & (db['sector'] == sector) ]
elif svars['level_0'].iloc[0] == 2:
    db=df2
    sectors=pandas.DataFrame(db['sector'].unique(), columns=['sector'])
    factors=pandas.DataFrame(db['factor'].unique(), columns=['factor'])
    sector = st.sidebar.selectbox("Sector:", sectors['sector'])
    factor = st.sidebar.selectbox("Factor:", factors['factor'])
    dbf=db[(db['shock']==shock) & (db['variable'] == variable) & (db['sector'] == sector) & (db['factor'] == factor) ]
#elif svars['level_0'] == 3:
elif svars['level_0'].iloc[0] == 4:
    db=df4
    factors=pandas.DataFrame(db['factor'].unique(), columns=['factor'])
    factor = st.sidebar.selectbox("Factor:", factors['factor'])
    dbf=db[(db['shock']==shock) & (db['variable'] == variable) & (db['factor'] == factor) ]
elif svars['level_0'].iloc[0] == 5:
    db=df5
    sub_variable = None 
    dbf=db[(db['shock']==shock) & (db['variable'] == variable)]


# Gráfico da variável selecionada
#st.subheader(f"Graph: {variable}")
plt.figure(figsize=(10, 5))
sns.lineplot(data=dbf, x='shockvalue', y='value', hue='model', marker='o')
plt.title(f"{variable} (percentage) in response to a change in {shock}", fontsize=16)
plt.xlabel(f"New Value of: {shock}", fontsize=14)
plt.ylabel(f"{variable} (percentage)", fontsize=14)
plt.legend(fontsize=14) 
plt.tick_params(axis='both', labelsize=12) 
st.pyplot(plt)

st.markdown("""
### Legend:
- **std**: Standard Model
- **mon**: Monop. Model
- **lrg**: Large Model
- **irs**: Scale Econ Model
""")

st.markdown("Obs: I ignored unfeasible simulations")

