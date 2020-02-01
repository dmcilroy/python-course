import requests
import csv

def get_realtor_data():

    url = 'https://api2.realtor.ca/Listing.svc/PropertySearch_Post'
    opts = {
        'LongitudeMin': -122.8884917, 
        'LongitudeMax': -122.7154137, 
        'LatitudeMin': 49.0160805, 
        'LatitudeMax': 49.0509935, 
        'PriceMin': 800000, 
        'PriceMax': 1200000,
        'CultureId': 1,
        'ApplicationId': 1,
        'PropertySearchTypeId': 1,
        'RecordsPerPage': 50
    }

    r = requests.post(url, opts)
    data = r.json()

    properties = []
    for listing in data["Results"]:
        
        filtered_dictionary = {
            "SizeInterior": listing["Building"]["SizeInterior"],
            "Address": listing["Property"]["Address"]["AddressText"],
            "PostalCode": listing["PostalCode"],
            "Latitude": listing["Property"]["Address"]["Latitude"],
            "Longitude": listing["Property"]["Address"]["Longitude"],
            "Price": listing["Property"] ["Price"],
            "LowResPath": listing["Property"]["Photo"][0]["LowResPath"]
            
        }
        
    
        properties.append(filtered_dictionary)
    return data["Results"]

def get_csv_data(filepath):
    assessment_data = []
    with open(filepath, mode="r", newline="") as inputfile:
        data = csv.DictReader(inputfile, delimiter=',')
        for eachRow in data:
            assessment_data.append(eachRow)
    return assessment_data

def match_properties(realtor_property, city_data):

    realtor_address = realtor_property["Property"]["Address"]["AddressText"].split("|")[0]

    realtor_postalcode = realtor_property["PostalCode"][0:3] + " " + realtor_property["PostalCode"][3:6]

    if len(realtor_address.split(" ")[0]) > 3:
        realtor_house = realtor_address.split(" ")[0]
        realtor_unit = " "
    else:
        realtor_house = realtor_address.split(" ")[1]
        realtor_unit = realtor_address.split(" ")[0]
        
    # selected_city_data_properties_pc = []

    # for property in city_data:
    #     if property["POSTAL_CODE"] == realtor_postalcode:
    #         selected_city_data_properties_pc.append(property)

    selected_city_data_properties_house = []

    for eachProperty in city_data:
        if eachProperty["HOUSE"] == realtor_house:
            selected_city_data_properties_house.append(eachProperty)

    selected_city_data_property = []

    if len(selected_city_data_properties_house) > 1:
        for eachProperty in selected_city_data_properties_house:
            if eachProperty["UNIT"] == realtor_unit:
                selected_city_data_property.append(eachProperty)

    else:
        selected_city_data_property = selected_city_data_properties_house

    if len(selected_city_data_property) > 0:
    
        print(
            realtor_address, 
            selected_city_data_property[0]["UNIT"],
            selected_city_data_property[0]["HOUSE"],
            selected_city_data_property[0]["STREET"],
            selected_city_data_property[0]["POSTAL_CODE"]        
        )
    else:
        print("No city property found")


 


def main():
    csv_data = get_csv_data("data/assessment2020.csv")
    
    realtor_data = get_realtor_data()

    for listing in realtor_data:
        match_properties(listing, csv_data)

    match_properties(realtor_data[0], csv_data)
    

    
if __name__ == "__main__":
    main()

        

