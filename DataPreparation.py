from GoogleNews import GoogleNews
import pandas as pd

# Data Collection
googlenews = GoogleNews(lang='es', region='CO')

googlenews.set_time_range('06/03/2024', '07/04/2024')

googlenews.search('turismo "San Andrés Islas" Colombia')

results = googlenews.result()

df = pd.DataFrame(results)

df.to_csv('noticias_turismo_san_andres.csv', index=False)

# Data Preparation

contents = df["desc"]
print(contents)
