'''
There is a lot of ways to use the database without the use of SQL directly.

Here we demonstrate the power of geopandas coupled with geoalchemy2.

We construct the query and compile it using postgres. Then submit it to
geopandas which creates a dataframe for us to use.

The constructed query is searching for pit layers whose comments had the word
graupel in it. Allowing us to gather locations of all pits where graupel was
noted by snowex data collectors

'''

from snowxsql.data import LayerData
from snowxsql.db import get_db
import geopandas as gpd
from sqlalchemy.dialects import postgresql

# Connect to the database we made.
db_name = 'postgresql+psycopg2:///snowex'
engine, metadata, session = get_db(db_name)

# Query the database looking at LayerData, filter on comments containing graupel (case insensitive)
q = session.query(LayerData).filter(LayerData.comments.contains('graupel'))

# Fill out the variables in the query
sql = q.statement.compile(dialect=postgresql.dialect())

# Get dataframe from geopandas using the query and engine
df = gpd.GeoDataFrame.from_postgis(sql, engine)

# Close the geoalchemy2 session
session.close()

# Write data to a shapefile
df['geom'].to_file('graupel_locations.shp')
