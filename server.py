from flask import Flask, render_template, request
import json

page_size=10
w_txt= json.load(open('worldl.json'))
lota = sorted(list(set([c['name'][0] for c in w_txt]))) #get the first unique character from the json file
print(lota)

for coty in w_txt:
    coty['tld'] = coty['tld'][1:]
app = Flask(__name__)                                   #creat an flask object or create an server

  
######################################################################################

@app.route('/')                                         #specific path of address that path associate with this function
def mainpage():
    '''It is the main page where all the country are shown
    page by page'''
    return render_template('index.html',                #pass data to webpage
            page_number=0,              
            page_size=page_size,
            w_txt = w_txt[0:page_size]
            )

######################################################################################

@app.route('/begin/<b>')                                #specific path of address that path associate with this function
def beginpage(b):
    '''This function mean which will work when we click next
    or previous. It plus the page number 20.'''
    nb = int(b)                                         # initial make the 'b' as int
    return render_template('index.html',
            w_txt = w_txt[nb:nb+page_size],
            page_number = nb,
            page_size = page_size
            )

######################################################################################

@app.route('/country/<i>')                              #specific path of address that path associate with this function
def countrypage(i):
    '''It show the detail about country by country number'''
    return render_template('country.html',              #passed to web template
            coty = w_txt[int(i)]
            )                                               

######################################################################################

@app.route('/countryname/<n>')                          #specific path of address that path associate with this function
def countrynamepage(n):
    '''It show the detail about country by country name'''
    return render_template('country.html',              #passed the result to web template
            coty = next(x for x in w_txt if x['name']==n), )

######################################################################################

@app.route('/continent/<c>')                            #specific path of address that path associate with this function
def continentpage(c):
    '''It show each continent's all country'''
    cl = [coty for coty in w_txt if coty['continent']==c]   
    return render_template('continent.html',            #passed the result to web template
            length_of_cl = len(cl),
            cl = cl,
            c = c)

######################################################################################

@app.route('/startwith/<c>')                            #specific path of address that path associate with this function
def letterpage(c):
    '''It show each continent's all country'''
    cl = [coty for coty in w_txt if coty['name'][0]==c]   
    return render_template('continent.html',            #passed the result to web template
            length_of_cl = len(cl),
            cl = cl,
            c = c)

######################################################################################

@app.route('/delete/<n>')                               #specific path of address that path associate with this function
def deleteCountryPage(n):
    '''It will delete the page when we click the delet button.
     All deleted country will be back on the list after restarting the server'''
    i=0
    for coty in w_txt:
        if coty['name'] == n:                           #Delete the country when the 'name' is equal with 'n'
            break
        i+=1

    del w_txt[i]
    return render_template('index.html',                #Pass this result to the web template
            page_number=0,
            page_size=page_size,
            w_txt = w_txt[0:page_size])

######################################################################################
    
@app.route('/editcountryByName/<n>')                    #specific path of address that path associate with this function
def editcountryByNamePage(n):
    '''It shown the form to edit respective data from web page.'''
    coty = None
    for x in w_txt:
        if x['name'] == n:
            coty = x
    return render_template(                             #Pass this result to the web template
		'country-edit.html',
		coty = coty)

######################################################################################
    
@app.route('/updatecountrybyname')                      #specific path of address that path associate with this function
def updatecountryByNamePage():
    '''It shown detail user edited result to the user.'''
    n=request.args.get('name')
    coty = None
    for x in w_txt:
        if x['name'] == n:
            coty = x
    coty['capital']=request.args.get('capital')         #Request the capital data from user
    coty['continent']=request.args.get('continent')     #Request the continent data from user
    coty['population']=request.args.get('population')   #Request the population data from user
    coty['gdp']=request.args.get('gdp')                 #Request the gdp data from user
    coty['area']=request.args.get('area')               #Request the area data from user
    return render_template(                             #Pass this result to the web template
		'country.html',
		coty = coty)

######################################################################################
    
@app.route('/newcountry')                                    #specific path of address that path associate with this function
def newcountrypage():
    '''Initial define the coty none and pass to other'''
    coty = None
    return render_template('country-create.html',coty = coty)#Pass this result to the web template

@app.route('/createcountryByNamePage')
def createcountryByNamePage():
    '''Request the data from user to create new country'''
    coty['name']=request.args.get('name')               #Request the name data from user
    coty['capital']=request.args.get('capital')         #Request the capital data from user
    coty['continent']=request.args.get('continent')     #Request the continent data from user
    coty['population']=request.args.get('population')   #Request the population data from user
    coty['gdp']=request.args.get('gdp')                 #Request the gdp data from user
    coty['area']=request.args.get('area')               #Request the area data from user
    coty['tld']=request.args.get('tld')                 #Request the tld data from user
    w_txt.sort(key=lambda coty: coty['name'])           #sort the data
    return render_template(                             #Pass this result to the web template
		'country.html',
		coty = coty)
    
######################################################################################
    
if (__name__=='__main__'):
    app.run(host='0.0.0.0',port=5620,debug=True)#default port is 5000

'''
@app.route('/awh/<i>')# 'i' is parameter
def awhpage(i):
    return w_txt[int(i)]['name']+'  '+w_txt[int(i)]['continent']+'  '+w_txt[int(i)]['capital'] 
'''
