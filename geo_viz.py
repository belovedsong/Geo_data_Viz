'''
Jessica Song

As part of the data exploration regarding geographic data,
manipulate and process the data saved in a dataframe to get 
the desired visualized result and plot those data on the 
interactive folium map and save it as .html file.

'''

# Visualization Libraries
import folium
from folium import plugins
import pylab as pl
import json

# Reading in Geojson data
rfile = open('../data/korea_geo.json')
jsonData = json.loads(rfile.read())


# Data Preparation# Data  
geo = pd.read_csv("../data/total_geo_knames.csv")
geo = geo.drop('Unnamed: 0', axis=1)

pop = pd.read_csv("../data/pop.csv")
pop = pop.drop('Unnamed: 0', axis=1)

withpop = pd.merge(geo,pop[['kcube_id','pop']], on='kcube_id', how='left')
withpop['pop'] = withpop['pop'].fillna(withpop['pop'].mean())

result.dropna(subset=['kcube_id'], how='all', inplace = True)
result['kcube_id'] = pd.to_numeric(result['kcube_id'], errors='coerce')
df = pd.merge(result, withpop, on='kcube_id', how='right')



# Data processing
# Find the area that pc occurs the most
  
# Create a binary column 'pc'
test2['pc'] = np.where(test2['event_type']=='PurchaseComplete',1,0)
test2['area_count'] = test2[test2['pc']==1].groupby(["kcube_id"])["pc"].transform("count")
test2['area_count'].fillna(0, inplace=True)
test2['area_count_pop'] = np.log(test2['area_count']/test2['pop']+1)


# For sanity check
test = test2[test2['pc']==1]
test = test[['kcube_id', 'area_count_pop','kcube_name']]
test = test.drop_duplicates()


# Setting the color map
from branca.colormap import linear

colormap = linear.PuBuGn_09.scale(
    test2['area_count_pop'].min(),
    test2['area_count_pop'].max())




temp = test2[['kcube_id', 'area_count_pop','kcube_name']]temp = temp.drop_duplicates()
temp = temp.dropna()
temp.isnull().sum()


# Using kcube id to match with GeoJson file
# Have to handle duplicated data
area_dict = temp.set_index('kcube_name')['area_count_pop']

# Matching with the color accordingly
color_dict = {}
for k,v in area_dict.items():
    color_dict[k] = colormap(v)

# Setting the default map
k_map = folium.Map(location=[37.566345, 126.977893],zoom_start=10)


folium.GeoJson(
    jsonData, 
    style_function=lambda feature: {
        'fillColor': color_dict[(feature['properties']['name'])],
        'color': 'black',
        'weight': 1,
        'dashArray': '5, 5',
        'fillOpacity': 0.9,
    }
).add_to(k_map)

folium.LayerControl().add_to(k_map)
# k_map.save('../data/pop_oaid08_10_geojson.html')





