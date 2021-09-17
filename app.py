from flask import Flask,redirect,url_for,render_template,request
import recomm_system

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template("index.html");

@app.route('/recommend',methods=['POST','GET'])
def recommend():
	if request.method == 'POST':
		s = request.form['product']
	try:
		cb_product_list = recomm_system.content_recomm(s)
		cf_product_list = recomm_system.CF_items(s)
		return render_template("recommend.html",cf_product_list=cf_product_list,cb_product_list=cb_product_list,item=s);
	except Exception as e:
		return render_template("error.html",item=s);	
	



if __name__ == '__main__':
    app.run(debug=True)