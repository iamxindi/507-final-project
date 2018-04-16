from flask import Flask, render_template, request, redirect, session, url_for
import secret
import model

app = Flask(__name__)
session = {}
@app.route('/street')
def street_init():
    return render_template("street.html", api_google = secret.api_google,
    lat = 38.9695545, lon = -77)


@app.route('/street', methods=['GET', 'POST'])
def street():
    if request.method == 'POST':
        try:
            companyname = request.form['companyname']
            location = model.search_company_lon_lat(companyname)
            lat = location[0]
            lon = location[1]
            return render_template("street.html", api_google = secret.api_google,
            lat = lat, lon = lon, error_msg= '', companyname = companyname)
        except:
            error_msg = 'Please enter valid input.'
            return render_template("street.html", api_google = secret.api_google,
            lat = 38.9695545, lon = -77, error_msg= error_msg, companyname = 'Some random company')
    else:
        return render_template("street.html", api_google = secret.api_google,
        lat = 38.9695545, lon = -77)

@app.route('/jobs')
def job_result():
    return render_template("jobs.html")

@app.route('/job_result', methods=['GET', 'POST'])
def jobs():
    if request.method == 'POST':
        # session['keyword'] = request.form['keyword']
        keyword = request.form['keyword']
        country = request.form['country']
        time = request.form['time']
        type = request.form['type']
        result = model.search_job(keyword, country, time,type)
    else:
        result = model.search_job()
        # session['country'] = request.form['country']
        # session['time'] = request.form['time']
        # session['type'] =request.form['type']
    return render_template('job_result.html', result=result)

@app.route('/company')
def company():
    return render_template("company.html")







if __name__ == '__main__':


    app.run(debug=True)
