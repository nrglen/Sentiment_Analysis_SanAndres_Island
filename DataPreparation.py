from GoogleNews import GoogleNews
import pandas as pd

# Data Collection
def dataCollection(fecha_inicio, fecha_fin, ciudad):

    googlenews = GoogleNews(lang='es', region='CO')

    googlenews.set_time_range(fecha_inicio, fecha_fin)

    consulta = f'turismo "{ciudad}" Colombia sector turístico'

    googlenews.search(consulta)

    results = googlenews.result()

    df = pd.DataFrame(results)

    #df.to_csv(f'noticias_turismo_{ciudad}.csv', index=False)
    print(df)
    # Data Preparation

    contents = df["desc"]
    contents.name = 'Descripcion de la noticia'
    return contents
    #print(f"Noticias entre {fecha_inicio} y {fecha_fin}")
