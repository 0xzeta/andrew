from flask import Flask, render_template, request
import json
w_txt= json.load(open('worldl.json'))
for coty in w_txt:
    coty['tld'] = coty['tld'][1:]
app = Flask(__name__) #creat an flask object or create an server
page_size=10
  

@app.route('/')#specific path of address that path associate with this function
def mainpage():
    return render_template('index.html',
            page_number=0,
            page_size=page_size,
            w_txt = w_txt[0:page_size]
            )

@app.route('/begin/<b>')#specific path of address that path associate with this function
def beginpage(b):
    nb = int(b) # initial need to converse to int to 'b'
    return render_template('index.html',
            w_txt = w_txt[nb:nb+page_size],
            page_number = nb,
            page_size = page_size
            )


@app.route('/country/<i>')# 'i' is parameter
def countrypage(i):
    return render_template('country.html',
            coty = w_txt[int(i)]
            )#passed to country template


@app.route('/countryname/<n>')# 'i' is parameter
def countrynamepage(n):
    return render_template('country.html',
            coty = next(x for x in w_txt if x['name']==n), )#passed to country template


@app.route('/continent/<c>')# 'c' is parameter
def continentpage(c):
    cl = [coty for coty in w_txt if coty['continent']==c]
    return render_template('continent.html',
            length_of_cl = len(cl),
            cl = cl,
            c = c)

#-----------------------------------------------------

@app.route('/delete/<n>')
def deleteCountryPage(n):
	i=0
	for coty in w_txt:
		if coty['name'] == n:
			break
		i+=1

	del w_txt[i]
	return render_template('index.html',
		page_number=0,
		page_size=page_size,
		w_txt = w_txt[0:page_size])
#all deleted country will be back on the list after restarting the server

@app.route('/editcountryByName/<n>')
def editcountryByNamePage(n):
	coty = None
	for x in w_txt:
		if x['name'] == n:
			coty = x
	return render_template(
		'country-edit.html',
		coty = coty)

@app.route('/updatecountrybyname')
def updatecountryByNamePage():
	n=request.args.get('name')
	coty = None
	for x in w_txt:
		if x['name'] == n:
			coty = x
	coty['capital']=request.args.get('capital')
	coty['continent']=request.args.get('continent')
	coty['population']=request.args.get('population')
	coty['gdp']=request.args.get('gdp')
	coty['area']=request.args.get('area')
	return render_template(
		'country.html',
		coty = coty)

@app.route('/newcountry')
def newcountrypage():
        coty = None
        return render_template('country-create.html',coty = coty)

@app.route('/createcountryByNamePage')
def createcountryByNamePage():
	coty['name']=request.args.get('name')
	coty['capital']=request.args.get('capital')
	coty['continent']=request.args.get('continent')
	coty['population']=request.args.get('population')
	coty['gdp']=request.args.get('gdp')
	coty['area']=request.args.get('area')
	coty['tld']=request.args.get('tld')
	w_txt.sort(key=lambda coty: coty['name'])
	return render_template(
		'country.html',
		coty = coty)
    

if (__name__=='__main__'):
    app.run(host='0.0.0.0',port=5621,debug=True)#default port is 5000

'''
@app.route('/awh/<i>')# 'i' is parameter
def awhpage(i):
    return w_txt[int(i)]['name']+'  '+w_txt[int(i)]['continent']+'  '+w_txt[int(i)]['capital'] 
'''
