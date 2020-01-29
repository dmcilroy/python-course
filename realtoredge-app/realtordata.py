import requests

def get_realtor_data():

    url = 'https://api2.realtor.ca/Listing.svc/PropertySearch_Post'
    opts = {
        'LongitudeMin': -122.845095, 
        'LongitudeMax': -122.8801139, 
        'LatitudeMin': 49.053034, 
        'LatitudeMax': 49.057534, 
        'PriceMin': 900000, 
        'PriceMax': 1500000,
        'CultureId': 1,
        'ApplicationId': 1,
        'PropertySearchTypeId': 1,
        'RecordsPerPage': 10
    }

    r = requests.post(url, opts)
    data = r.json()

    properties = []
    for listing in data["Results"]:
        
        filtered_dictionary = {
            "SizeInterior": listing["Building"]["SizeInterior"],
            "Address": listing["Property"]["Address"]["AddressText"],
            "Latitude": listing["Property"]["Address"]["Latitude"],
            "Longitude": listing["Property"]["Address"]["Longitude"],
            "Price": listing["Property"] ["Price"],
            "LowResPath": listing["Property"]["Photo"][0]["LowResPath"]
            
        }
        
    
        properties.append(filtered_dictionary)
    return properties