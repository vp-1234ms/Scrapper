import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import urllib.request
from flask import Flask,request,render_template,redirect,app
from flask_cors import CORS,cross_origin
import pymongo


application=Flask(__name__)
app=application
@app.route("/",methods=["GET","POST"])
@cross_origin()
def home():
     return render_template("home.html")

@app.route("/review",methods=["GET","POST"])
@cross_origin()
def review():
    if request.method == 'POST':
        product = request.form['content'].replace(" ","")
        flipkart_url = "https://www.flipkart.com/search?q=" 
        flipkart_url = flipkart_url + product
        urlclient=urlopen(flipkart_url)
        flipkart_page=urlclient.read()
        flipkart_html=bs(flipkart_page,"html.parser")
        bigbox=flipkart_html.find_all("div",{"class":"_1AtVbE col-12-12"})

        main_url_list=[]
        for i in bigbox:
            try:
                main_url = i.div.div.div.a["href"]
            except AttributeError:
                pass
            except TypeError:
                pass
            except Exception as e:
                pass
            else:
                final_url = flipkart_url + main_url
                main_url_list.append(final_url)

        img_list=[]
        price_list=[]
        review_list=[]      
        Overall_Product=[]

        for i in range(len(main_url_list)):
            urlclient=urlopen(main_url_list[i])
            flipkart_page=urlclient.read()
            flipkart_html=bs(flipkart_page,"html.parser")
            try:
                img=flipkart_html.find_all("img",{"class":["_2r_T1I _396QI4","_396cs4 _2amPTt _3qGmMb","CXW8mj _3nMexc"]})[0]
            except Exception as e:
                pass
            else:
                img_list.append(img["src"])

            try:
                newprice=(flipkart_html.find_all("div",{"class":"_30jeq3 _16Jk6d"})[0]).text
                originalprice=(flipkart_html.find_all("div",{"class":"_3I9_wc _2p6lqe"})[0]).text 
                discount=(flipkart_html.find_all("div",{"class":["_3Ay6Sb _31Dcoz pZkvcx","_3Ay6Sb _31Dcoz"]})[0]).text
                discount=discount.replace(" ", "")
            except Exception as e:
                pass
            else:
                d={"New Price":newprice,"Original Price":originalprice,"Discount":discount}
                price_list.append(d)

            try:
                l=[]
                rating=flipkart_html.find_all("div",{"class":["_3LWZlK _1BLPMq _3B8WaH","_3LWZlK _1BLPMq"]})
                for j in range(len(rating)):
                    ratings=(flipkart_html.find_all("div",{"class":["_3LWZlK _1BLPMq _3B8WaH","_3LWZlK _1BLPMq"]})[j]).text
                    overall=(flipkart_html.find_all(["div","p"],{"class":["_6K-7Co","_2-N8zT"]})[j]).text
                    d={"Ratings":ratings,"Comment":overall}
                    l.append(d)
            except Exception as e:
                pass
            else:
                review_list.append(l)

            try:
                o=flipkart_html.find_all("div",{"class":["_3LWZlK _138NNC","col-12-12 _1azcI6"]})[0].text
            except Exception as e:
                pass
            else:
                Overall_Product.append(o)
        for i in range(len(img_list)):
            img_list[i]=img_list[i][:-5]
        
       

        if(len(img_list)==0):
            return("Invalid Input")

        
        else:
            return render_template("new.html",images=img_list,prices=price_list,overall=Overall_Product,review=review_list,link=main_url_list,x=len(img_list))


if __name__=="__main__":
    app.run(host="0.0.0.0")
