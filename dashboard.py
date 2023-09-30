import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

dfMuestra = pd.read_excel("muestra1500.xlsx")

st.set_page_config(page_title="Heart Attack Risk Dashboard", page_icon=":mending_heart:", layout="wide")

#* ----- SIDEBAR -----
st.sidebar.header("Filtros")

Sexo = st.sidebar.multiselect(
    "Seleccione el sexo:",
    options=dfMuestra["Sex"].unique(),
    default=dfMuestra["Sex"].unique()
)

Fuma = st.sidebar.multiselect(
    "Seleccione si fuma (1 si; 0 no):",
    options=dfMuestra["Smoking"].unique(),
    default=dfMuestra["Smoking"].unique()
)

Alcohol = st.sidebar.multiselect(
    "Seleccione si consume alcohol (1 si; 0 no):",
    options=dfMuestra["Alcohol Consumption"].unique(),
    default=dfMuestra["Alcohol Consumption"].unique()
)

Dieta = st.sidebar.multiselect(
    "Seleccione el tipo de dieta:",
    options=dfMuestra["Diet"].unique(),
    default=dfMuestra["Diet"].unique()
)

Pais = st.sidebar.multiselect(
    "Seleccione el pais:",
    options=dfMuestra["Country"].unique(),
    default=dfMuestra["Country"].unique()
)

df_selection = dfMuestra.query(
    'Sex == @Sexo & Smoking == @Fuma & `Alcohol Consumption` == @Alcohol & Diet == @Dieta & Country == @Pais'
)

#* ------ MAIN PAGE --------
st.title(":bar_chart: Heart Attack Risk Dashboard")
st.markdown("##")

# st.dataframe(df_selection)

col1, col2 = st.columns((2))

# Group data by 'Age' and calculate the average heart attack risk for each age group
average_heart_attack_risk = df_selection.groupby('Age')['Heart Attack Risk'].mean()

# Create a figure and axes
fig6 = plt.figure(figsize=(25, 8))
ax = plt.gca()

# Plot the data
sns.lineplot(x=average_heart_attack_risk.index, y=average_heart_attack_risk.values, marker='o', color='#16A34A', ax=ax)

# Customize the plot
plt.xlabel('Edad')
plt.ylabel('Promedio del riesgo de ataques al corazon')
plt.title('Promedio del riesgo de ataques al corazon en funcion de la edad')
plt.grid(True, linestyle='--', alpha=0.7)
sns.despine()

# Add labels for interesting points
interesting_points = [(40, "Adultos medios"), (65, "Adultos mayores")]
for x, label in interesting_points:
    y_value = average_heart_attack_risk.get(x,None)
    ax.annotate(f'{label}', (x, y_value), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=12, color='#18181B')


# Customize the x-axis ticks
plt.xticks(range(20, 100, 10))

st.pyplot(fig6)
    
with col1:
    st.subheader("Histogramas")
    fig1, ax1 = plt.subplots(figsize=(7, 3))
    ax1.hist(df_selection['Age'], bins=50, alpha=0.7, label='Edad', color='#D80032')
    ax1.set_xlabel('Edad')
    ax1.set_ylabel('Frecuencia')
    ax1.set_title('Distribución de edad por riesgo de ataque al corazón')
    ax1.legend()
    st.pyplot(fig1)

    st.subheader("Diagramas")
    gender_heart_attack = df_selection.groupby(['Sex', 'Heart Attack Risk']).size().unstack().fillna(0)
    fig4 = plt.figure(figsize=(8, 5))
    gender_heart_attack.plot(kind='bar', stacked=True, color=['#EF4444', '#FEF9C3'], ax=plt.gca())
    plt.xlabel('Gender')
    plt.ylabel('Count')
    plt.title('Gender Distribution by Heart Attack Risk Male/Female')
    plt.xticks(rotation=0)
    plt.legend(['No Heart Attack', 'Heart Attack'])

    st.pyplot(fig4)
    

with col2:
    st.subheader("Gráfico de densidad")
    fig2, ax2 = plt.subplots(figsize=(7, 3))
    sns.kdeplot(df_selection['Age'], shade=True, color='#FACC15', ax=ax2)
    ax2.set_xlabel('Edad')
    ax2.set_ylabel('Densidad')
    ax2.set_title('Distribución de densidad de edad por riesgo de ataque al corazón')
    st.pyplot(fig2)

    st.subheader("Boxplot")
    fig3, ax3 = plt.subplots(figsize=(7, 3))
    sns.boxplot(x='Heart Attack Risk', y='Age', data=df_selection, ax=ax3, palette='Set1')
    ax3.set_xlabel('Riesgo de ataque al corazón')
    ax3.set_ylabel('Edad')
    ax3.set_title('Boxplot de edad por riesgo de ataque al corazón')
    ax3.set_xticks([0, 1])
    ax3.set_xticklabels(['Sin ataque al corazón', 'Con ataque al corazón'])

    # Add annotations for median ages
    medians = df_selection.groupby('Heart Attack Risk')['Age'].median()
    medians_labels = [f'Mediana de edad: {medians[0]}', f'Mediana de edad: {medians[1]}']
    for i, median in enumerate(medians):
        ax3.text(i, median, medians_labels[i], horizontalalignment='center', verticalalignment='bottom', fontsize=10, color='black', fontweight='bold')
    # Adjust spacing between subplots
    # 

    st.pyplot(fig3)



# Calcular porcentajes de fumadores, obesos y consumidores de alcohol por riesgo de ataque al corazón
smoking_percentage = df_selection.groupby('Heart Attack Risk')['Smoking'].mean() * 100
obesity_percentage = df_selection.groupby('Heart Attack Risk')['Obesity'].mean() * 100
alcohol_percentage = df_selection.groupby('Heart Attack Risk')['Alcohol Consumption'].mean() * 100

# Crear subplots
fig5, axes = plt.subplots(1, 3, figsize=(25, 8))

# Gráfico de barras para fumadores
sns.barplot(x=smoking_percentage.index, y=smoking_percentage.values, ax=axes[0], palette=['#FEF9C3', '#D80032'])
axes[0].set_title('Porcentaje de fumadores por riesgo de ataque al corazón')
axes[0].set_xlabel('Riesgo de ataque al corazón')
axes[0].set_ylabel('Porcentaje de fumadores')

# Gráfico de barras para obesidad
sns.barplot(x=obesity_percentage.index, y=obesity_percentage.values, ax=axes[1], palette=['#FEF9C3', '#D80032'])
axes[1].set_title('Porcentaje de obesos por riesgo de ataque al corazón')
axes[1].set_xlabel('Riesgo de ataque al corazón')
axes[1].set_ylabel('Porcentaje de obesos')

# Gráfico de barras para consumo de alcohol
sns.barplot(x=alcohol_percentage.index, y=alcohol_percentage.values, ax=axes[2], palette=['#FEF9C3', '#D80032'])
axes[2].set_title('Porcentaje de consumidores de alcohol por riesgo de ataque al corazón')
axes[2].set_xlabel('Riesgo de ataque al corazón')
axes[2].set_ylabel('Porcentaje de consumidores de alcohol')

st.pyplot(fig5)