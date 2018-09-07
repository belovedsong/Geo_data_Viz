# Getting lat, long info from Google Map API
with open('data/kcube_geo_info.pkl', 'rb') as handle:
    kcube = pickle.load(handle)
    
addresses = kcube['kcube_geo_info.full_addr'].tolist()
SLEEP_FOR = 30
OUTPUT_NAME = "../data/geo.csv"

# def limit_len(kcube, num=3):
#     cut_adds = []
#     for i in range(kcube.shape[0]):
#         length = len(str(kcube['kcube_geo_info.full_addr'][i]).split())
#         if length == num:
#             cut_adds.append(kcube['kcube_geo_info.full_addr'])
#         else:
#             continue
#     return cut_adds

def get_geo2(address, key=API_KEY):
    # for address in addresses
    #pickling_on = open(OUTPUT_NAME, "wb")

    for i in range(len(address)):
        
        geo_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(address, key)
    
        try:
            r = requests.get(geo_url)
            r = r.json()
        except Exception as e:
            print(e)
        
        if len(r['results']) == 0:
            output = {
                "formatted_address": None,
                "latitude": None,
                "longitude": None,
                #"google_place_id": None,
                "type": None,
                "status": r['status']
            }
        else:
            result = r['results'][0]
            output = {
                "formatted_address": result['formatted_address'],
                "latitude": result['geometry']['location']['lat'],
                "longitude": result['geometry']['location']['lng'],
                #"google_place_id": result['place_id'],
                "type": ",".join(result['types']),
                "status": r['status']
            }
            #print(result)
        
        #output['status'] = r.get('status')
        
        #pickle.dump(output, pickling_on)
    
    #pickling_on.close()
        
    return output
    
    
def run_geo(addresses):

    results = []

    for address in addresses:
        coded = False
        while coded is not True:
            try:
                geo_result = get_geo2(address, API_KEY)
            except Exception as e:
                #logger.exception(e)
                #logger.error("Exception here: {}".format(address))
                #logger.error("Skipped :(")
                print("ERROR MESSAGE: {} AT {}".format(e, address))
                coded = True

            if geo_result['status'] == 'OVER_QUERY_LIMIT':
                #logger.info("Hit the Limit.")
                print("HIT THE LIMIT {}".format(address))
                time.sleep(SLEEP_FOR*60)
                coded = False
            else:
                print("GOT IT :)")
                results.append(geo_result)
                coded = True
                
            if len(results) % 100 == 0:
                print("Done 100 :D")

            if len(results) % 500 == 0:
                pd.DataFrame(results).to_csv("{}_backup.format(OUTPUT_NAME)")
                
    #logger.info("Finished :)")
    print("Finished :)")

    pd.DataFrame(results).to_csv(OUTPUT_NAME, encoding='utf8')
    
    return None


# Combine with kcube_id 
kcubeid = kcube['kcube_geo_info.area_code'].tolist()
kcubeid_df = pd.DataFrame(kcubeid, columns=['kcube_id'])
test = geo_info.copy()
test = test.assign(kcube_id=kcubeid_df.values)
test.to_csv('data/total_geo.csv')