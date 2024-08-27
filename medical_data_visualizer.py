
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def draw_cat_plot():
    # 1. Importar los datos
    df = pd.read_csv('medical_examination.csv')

    # 2. Crear la columna overweight
    df['overweight'] = (df['weight'] / (df['height'] / 100) ** 2) > 25
    df['overweight'] = df['overweight'].astype(int)

    # 3. Normalizar los datos
    df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x == 1 else 1)
    df['gluc'] = df['gluc'].apply(lambda x: 0 if x == 1 else 1)

    # 4. Crear DataFrame para el gráfico categórico
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])
    
    # Agrupar y reformatear los datos
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')

    # 5. Crear el gráfico categórico
    g = sns.catplot(x='variable', y='total', hue='value', col='cardio', data=df_cat, kind='bar', height=5, aspect=0.8)
    
    # Etiquetar los ejes
    g.set_axis_labels("variable", "total")
    
    # Guardar el gráfico
    g.savefig("cat_plot.png")
    
    # Devolver la figura
    return g.fig

def draw_heat_map():
    # 1. Importar los datos
    df = pd.read_csv('medical_examination.csv')

    # 2. Limpiar los datos
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # Seleccionar columnas relevantes
    columns = ['id', 'age', 'sex', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'cardio']
    df_heat = df_heat[columns]

    # 3. Calcular la matriz de correlación
    corr = df_heat.corr()

    # 4. Generar máscara para el triángulo superior
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 5. Configurar la figura
    fig, ax = plt.subplots(figsize=(12, 12))

    # 6. Graficar el mapa de calor
    sns.heatmap(corr, annot=True, fmt='.1f', mask=mask, square=True, linewidths=1, cbar_kws={'shrink': 0.5}, ax=ax)
    
    # Guardar el gráfico
    plt.savefig("heat_map.png")
    
    # Devolver la figura
    return fig

# Llamar a las funciones para generar los gráficos
if __name__ == "__main__":
    draw_cat_plot()
    draw_heat_map()


