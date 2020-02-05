import requests
import csv

def get_realtor_data():
    url = 'https://api2.realtor.ca/Listing.svc/PropertySearch_Post'
    
    opts = {
        'LongitudeMin': -122.8714107, 
        'LongitudeMax': -122.7433667, 
        'LatitudeMin': 49.0385985, 
        'LatitudeMax': 49.2094745, 
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
            # Added a couple more items to this dict
            "ListingUrl": listing["RelativeDetailsURL"],
            "Type": listing["Building"]["Type"],
            # Existing
            "SizeInterior": listing["Building"]["SizeInterior"],
            "Address": listing["Property"]["Address"]["AddressText"],
            "PostalCode": listing["PostalCode"],
            "Latitude": listing["Property"]["Address"]["Latitude"],
            "Longitude": listing["Property"]["Address"]["Longitude"],
            "Price": listing["Property"]["Price"],
#             "LowResPath": listing["Property"]["Photo"][0]["LowResPath"] if listing["Property"]["Photo"] else 'Photo Not Available'
        }
        properties.append(filtered_dictionary)
    return properties

def get_csv_data(filepath):
    assessment_data = []
    with open(filepath, mode="r", newline="") as inputfile:
        data = csv.DictReader(inputfile, delimiter=',')
        for eachRow in data:
            assessment_data.append(eachRow)
    return assessment_data

def calc_difference(realtor_price, assessment_price):
    # Convert assessment_price to an integer
    assessment_price = int(assessment_price)
    
    # Convert realtor_price to an integer
    realtor_price = int(realtor_price.strip('$').replace(',', ''))
    
    # Subtract and return the difference
    return realtor_price - assessment_price

def match_properties(realtor_listing, assessment_data, writer):
    # First parse the realtor property address into components
    realtor_address = realtor_listing["Address"].split("|")[0]
    
    # Identify the HOUSE & UNIT number
    if len(realtor_address.split(" ")[0]) > 3:
        realtor_house = realtor_address.split(" ")[0]
        realtor_unit = 'NA'
    else:
        realtor_unit = realtor_address.split(" ")[0]
        realtor_house = realtor_address.split(" ")[1]
    
    # Then compare the realtor and city house numbers
    filtered_by_house = []

    for property in assessment_data:
        if property["HOUSE"] == realtor_house:
            filtered_by_house.append(property)
    
    # Finally, if applicable, compare the realtor and city unit numbers
    
    selected_city_properties = []
    
    if len(filtered_by_house) > 1:
        print("Multiple properties with same house number")
        for property in filtered_by_house:
            if property["UNIT"] == realtor_unit:
                selected_city_properties.append(property)
    else:
        selected_city_properties = filtered_by_house
         
    if len(selected_city_properties) > 0:
        city_address = selected_city_properties[0]['UNIT'] + " " + selected_city_properties[0]['HOUSE']
        
        # Here we want to add some city data to our realtor_listing variable
        realtor_listing["Assessment"] = selected_city_properties[0]["GROSS_ASSESSMENT"]
        realtor_listing["Inflatedvalue"] = calc_difference(realtor_listing["Price"], realtor_listing["Assessment"])
        
        # Write rows with the following keys and values:
        writer.writerow(
            {
            'ListingUrl':  realtor_listing['ListingUrl'],
            'Type': realtor_listing['Type'],
            'SizeInterior': realtor_listing['SizeInterior'],
            'Address': realtor_listing['Address'], 
            'PostalCode': realtor_listing['PostalCode'],
            'Latitude': realtor_listing['Latitude'],
            'Longitude': realtor_listing['Longitude'],
            'Price': realtor_listing['Price'],
#             'LowResPath': realtor_listing['LowResPath'],
            'Assessment': realtor_listing['Assessment'],
            'Inflatedvalue': realtor_listing['Inflatedvalue']
            }
        )
        
    else:
        print('No city data found for address:', realtor_address)
        
def main():
    filepath = 'data/assessment2020.csv'
    city_data = get_csv_data(filepath)
    realtor_data = get_realtor_data()
    
    outputfile = 'data/property-analysis.csv'
    
    column_names = ['ListingUrl', 'Type', 'SizeInterior', 'Address', 'PostalCode', 'Latitude', 'Longitude', 'Price', 'LowResPath', 'Assessment', 'Inflatedvalue']
    
    with open(outputfile, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_names)
        writer.writeheader()


        for property in realtor_data:
            match_properties(property, city_data, writer)

if __name__ == "__main__":
    main()

        

