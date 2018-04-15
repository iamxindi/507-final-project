from flask import Flask, render_template, request
import secret
import model

app = Flask(__name__)

@app.route('/street')
def street_init():
    return render_template("map.html", api_google = secret.api_google,
    lat = 38.9695545, lon = -77)


@app.route('/street', methods=['GET', 'POST'])
def street():
    if request.method == 'POST':
        try:
            companyname = request.form['companyname']
            location = model.search_company_lon_lat(companyname)
            lat = location[0]
            lon = location[1]
            return render_template("map.html", api_google = secret.api_google,
            lat = lat, lon = lon, error_msg= '', companyname = companyname)
        except:
            error_msg = 'Please enter valid input.'
            return render_template("map.html", api_google = secret.api_google,
            lat = 38.9695545, lon = -77, error_msg= error_msg, companyname = 'Some random company')
    else:
        return render_template("map.html", api_google = secret.api_google,
        lat = 38.9695545, lon = -77)



if __name__ == '__main__':


    app.run(debug=True)
