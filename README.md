# Backend for Switch Games Recommendation

# Backend Change
Debido a los costos del despliegue de todos los recursos (SSL, Modelo Predictivo, MariaDB, Meilisearch, API), que eran mayores a los esperado, se optó por simplificar el despliegue eliminando la base de datos y moviendo todo a Algolia y un servidor para el Modelo Predictivo.