
from flask import Flask, request, render_template, jsonify
from bs4 import BeautifulSoup as bs
import requests
from flask_cors import CORS, cross_origin
from urllib.request import urlopen as uo


app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/reviews", methods = ["GET", "POST"])
def reviews():
    if request.method == "POST":
        product_name = request.form["product_name"].replace(" ","")
        try:
            required_url = "https://www.amazon.in/s?k="+product_name
            url_client = uo(required_url)
            html_scrap = url_client.read()
            url_client.close()
            formatted_html_scrap = bs(html_scrap, "html.parser")
            search_result = formatted_html_scrap.find_all("div", {"class":"sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16"})
            product_link = search_result[0].find_all("a")[0]["href"]
            product_url = "https://www.amazon.in"+product_link
            url_client = uo(product_url)
            product_html_scrap = url_client.read()
            formatted_product_scrap = bs(product_html_scrap,"html.parser")
            all_reviews = formatted_product_scrap.find_all("div", {"class" : "a-section review aok-relative"})
            data = list()
            for value in all_reviews:
                
                try:
                    name = value.div.div.div.find_all("div", {"class" : "a-profile-content"})[0].text
                except:
                    name = "AN AMAZON CUSTOMER"

                try:
                    rating = value.div.div.i.text
                except:
                    rating = "RATING NOT FOUND"
                    
                try:
                    heading = value.div.div.find_all("span")[3].text
                except:
                    heading = "AN AMAZON REVIEW"
                    
                try:
                    date = value.div.div.find_all("span")[4].text
                except:
                    date = "DATE NOT FOUND"
                    
                try:
                    details = value.div.div.find_all("span")[7].text
                except:
                    details = "NO DETAILS FOUND"
                    
                element = {
                    "name" : name,
                    "rating" : rating,
                    "heading" : heading,
                    "review date" : date,
                    "details" : details
                }
                
                data.append(element)
        
        except Exception as e:
            return "FATAL ERROR : "+str(e)
        
        return render_template("result.html", data = data[0:len(data)-1])
    
    return "DON'T TRY TO BE OVERSMART"                    
                 
            
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="6969")