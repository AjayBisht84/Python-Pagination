from email import message
from logging import exception
from pstats import Stats
from pydoc import doc
import re
from shutil import register_unpack_format
from winreg import REG_WHOLE_HIVE_VOLATILE

from flask import Flask,jsonify,request,render_template
import pymongo
import json
from sqlalchemy import desc
from werkzeug import Response
from bson.objectid import ObjectId
app=Flask(__name__)

try:
       
        mongo=pymongo.MongoClient(host="localhost",port=27017)        
        db=mongo.Customer      
        
except:
        
        print("error- can not connect with db")

@app.route("/users",methods=["POST"])
def create_users():
        
        try:
            data={
                "_id": int(request.form["id"]),
                "FirstName":request.form["Fname"],
                "LastName":request.form["Lname"]
                }
            #data={"Fname":"Python","Lname":"Flask"}
            db_inset=db.user.insert_one(data)
           
            return Response(
                response=json.dumps({"message":"User created","id":f"{db_inset.inserted_id}"}),
                status=200,
                mimetype="application/json"
            )
        except: 
            return Response(
                response=json.dumps({"message":"User not created"}),
                status=500,
                mimetype="application/json"
            )
      

#pagination code
@app.route("/getUser/",methods=["GET"])
def get_users():
        
    try:    
            page_size=4
            
            kk= list(db.user.find())
           
            last=str(int(len(kk)/page_size))

            m = []
            for i in range(1, (int(last)+1)):                
                    m.append(i)
            
            
            page=str(request.args.get("no"))           
           
            if (not str(page).isnumeric()):
                page = 1
                data= list(db.user.find().skip(page_size*(page-1)).limit(page_size))
                

            if(int(page)==1):
                    
                    prev="#"
                    page=1
                    nxt="/getUser/?no=" + str(page+1)
                    data= list(db.user.find().skip(page_size*(page-1)).limit(page_size))
                   
            elif(page==last):                   
                    
                    page=int(page) 
                    data= list(db.user.find().skip(page_size*(page-1)).limit(page_size))

                    nxt="#" 
                    prev="/getUser/?no=" + str(page-1)
            
            else:
                   
                    page=int(page)  
                   
                   
                    data= list(db.user.find().skip(page_size*(page-1)).limit(page_size))
                    nxt="/getUser/?no=" + str(page+1)
                    prev="/getUser/?no=" + str(page-1)
                   
                    
            return render_template("page.html",d=data,nxt=nxt,prev=prev,m=m)
        
    except Exception as ex: 
                return jsonify("Error")
            


@app.route("/updateUser/<id>",methods=["PATCH"])
def update_User(id):
    print(id)
    try:    
            update=db.user.update_one(
                {"_id":ObjectId(id)},
                {"$set":{"FirstName":request.form["FirstName"]}
            })
            return Response(
            response=json.dumps({"message":"user update"}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex: 
                return Response(
                response=json.dumps({"message":"User can not update"}),
                status=500,
                mimetype="application/json"
            )    

@app.route("/deleteUser/<id>",methods=["DELETE"])
def delete_User(id):
    
    try:    
            val=db.user.delete_one({"_id":ObjectId(id)})
            return Response(
            response=json.dumps({"message":"user deleted","id":f"{id}"}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex: 
                return Response(
                response=json.dumps({"message":"User can not delete"}),
                status=500,
                mimetype="application/json"
            )  

app.run(debug=True)

