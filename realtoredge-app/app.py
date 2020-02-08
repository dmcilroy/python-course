from flask import Flask, render_template, jsonify
from flask_bootstrap import Bootstrap
from realtordata import get_realtor_data, get_csv_data

from flask_googlemaps import GoogleMaps, Map

app = Flask(__name__)

app.config['GOOGLEMAPS_KEY'] = "AIzaSyBgk4xlA90gmaW-itRDlPgokqU5SgETb4k"

Bootstrap(app)

GoogleMaps(app)


@app.route("/")
def hello():
    return render_template("index-simple.html")

@app.route("/about") 
def about():
    return render_template('about.html')

@app.route("/data")
def data():
    my_data = get_realtor_data()
    return jsonify(my_data)

@app.route("/map")
def mapview():
    filepath = "data/property-analysis.csv"
    property_list = get_csv_data(filepath)
    # creating a map in the view
    markers = []

    for property in property_list:
        
        if int(property["Inflatedvalue"]) > 100000:
            icon = "http://maps.google.com/mapfiles/ms/icons/red-dot.png"

        elif -10000 <=int(property["Inflatedvalue"]) <=100000:
            icon = "http://maps.google.com/mapfiles/ms/icons/green-dot.png"

        elif -10000 <=int(property["Inflatedvalue"]) <-100000:
            icon = "http://maps.google.com/mapfiles/ms/icons/blue.png"

        else:
            icon = "http://maps.google.com/mapfiles/ms/icons/msmarker.shadow.png"
        
        marker = {
            "icon": icon,
            "lat": property["Latitude"],
            "lng": property["Longitude"],
            "infobox":
                "<p> Address " + property["Address"] +"</p>" + 
                "<p> Price " + property["Price"] +"</p>" +
                "<p> Inflated Value " + property["Inflatedvalue"] +"</p>" 
                
        }

        markers.append(marker)


    mymap = Map(
        identifier="mymap",
        lat=49.0385985,
        lng=-122.7433667,
        zoom=12,
        markers=markers
          
    )
    return render_template('map.html', flask_gmap=mymap)


    

if __name__ == '__main__':
     app.run(debug=True)