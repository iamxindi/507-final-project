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
def jobs():
    return render_template("jobs.html")

@app.route('/job_result', methods=['GET', 'POST'])
def job_result():
    if request.method == 'POST':
        keyword = request.form['keyword']
        country = request.form['country']
        time = request.form['time']
        type = request.form['type']

        if time != 'most_recent':
            start_time = request.form['start_time']
            end_time = request.form['end_time']
            result = model.search_job(keyword, country, time,type, start_time, end_time)
            num = len(result)
            return render_template('job_result.html', result=result, num = num)
        else:
            result = model.search_job(keyword, country, time,type)
            num = len(result)
            return render_template('job_result.html', result=result, num = num)
    else:
        result = model.search_job()
        num = len(result)
        return render_template('job_result.html', result=result, num=num)


@app.route('/company')
def company():
    return render_template("company.html")

@app.route('/company_result',methods=['GET', 'POST'])
def company_r():
    if request.method == 'POST':
        keyword = request.form['keyword']
        country = request.form['country']
        company_job_dic = model.search_company(keyword, country)
    else:
        company_job_dic = model.search_company()
    return render_template("company_result.html", company_job_dic = company_job_dic)

@app.route('/plot',methods=['GET', 'POST'])
def plot():
    if request.method == 'POST':
        companyname = request.form['companyname']
        lat = float(request.form['lat'])
        lon = float(request.form['lon'])
    else:
        companyname = ''
        lat = 0
        lon = 0
    return render_template("plot.html", companyname = companyname, lat = lat, lon = lon, api_google = secret.api_google)







if __name__ == '__main__':


    app.run(debug=True)
