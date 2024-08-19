from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt

# Configurar la API de Google Trends
pytrends = TrendReq(hl='es-', tz=360)

# Especificar el término de búsqueda y el periodo de tiempo
kw_list = ["San Andrés Islas Colombia", "viajes a San Andrés", "hoteles en San Andrés"]
pytrends.build_payload(kw_list, cat=0, timeframe='2024-01-01 2024-08-01', gprop='')

# Obtener el interés a lo largo del tiempo
interest_over_time_df = pytrends.interest_over_time()