from flask import Flask,render_template,request,abort
from flask import jsonify
from flask_cors import CORS
import couchdb
import scipy.stats as st

suburbName = ["Flemington", "Carlton", "Docklands", "East Melbourne", "Kensington", "Melbourne", "North Melbourne", "Parkville", "Southbank", "Port Melbourne", "South Yarra - East"]


app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route("/")
def hello_world():
    return 'Hello World!'
# def index():
#     return render_template("index.html")

@app.errorhandler(501)
def error_501_handler(err):
    print("MapReduce Function went wrong,Error occurs, ")
    print(err)
    return None

@app.errorhandler(404)
def error_404_handler(err):
    print("Something went wrong, because of  ")
    print(err)
    return None


@app.route("/Scenario1",methods=["GET","POST"])
def set1():
    
    print(1)
    map_fun_rm = """
                           function(doc) {
                               emit([doc.userid,doc.text], 1)
           }
                         """
    reduce_fun_rm = "_count"
    design = {'views': {
        'get_view': {
            'map': map_fun_rm,
            'reduce': reduce_fun_rm
        }
    }}
    
    print(2)
    db1["_design/users"] = design
    
    if(db1.view('users/get_unames', group_level=2)==None):
        abort(501)
        
    uname_list = db1.view('users/get_view', group_level=2)
    for i in uname_list:
        if (i.value > 1):
            temp = None
            
            for doc in db1.find({'selector': {'userid': i.key[0], "text": i.key[1]}}):
                temp = doc
            if (temp is not None):
                db1.delete(temp)  
                
                
    print(3)
    db1.delete(db1["_design/users"])  
    

    map_fun = """
                    function(doc) {

                        emit([doc.suburb,doc.emotion], 1)
    }
                  """
    reduce_fun = "_count"
    design = {'views': {
        'get_unames': {
            'map': map_fun,
            'reduce': reduce_fun
        }
    }}
    if(db1.view('users/get_unames', group_level=2)==None):
        abort(501)
    db1["_design/users"] = design
    uname_list = db1.view('users/get_unames', group_level=2)
    dic1 = {}
    rate = []
    x = []
    
    res = dict.fromkeys(suburbName, 0)
    for i in range(len(suburbName)):
        res[suburbName[i]] = {'pos': 0}
    
    for i in range(len(suburbName)):
        dic1[suburbName[i]]=[0,0]
    

    for r in uname_list:
        if r.key[1] == 'neg':
            dic1[r.key[0]] = [r.value,0]
        elif r.key[1] == 'neu':
            dic1[r.key[0]][1] = r.value 
        elif r.key[1] == 'pos':
            neg_num = dic1[r.key[0]][0]
            neu_num = dic1[r.key[0]][1]
            pos_num = r.value
            dic1[r.key[0]] = pos_num / (neg_num + neu_num + pos_num)
        else:
            continue
    for r in uname_list:
        res[r.key[0]]['pos'] = dic1[r.key[0]]
    
    
    for sub in suburbName:
        for doc in aurin1.find({'selector': {'sub': sub}}):
            rate.append(doc['rate'])
            res[sub]['aurin'] = doc['chart']
        x.append(res[sub]['pos'])
    
    newRate = []
    for i in rate:
        newRate.append(float(i))

    for r in uname_list:
        slope, intercept, r_value, p_value, std_err = st.linregress(x, newRate)
        res[r.key[0]]['b0'] = intercept
        res[r.key[0]]['b1'] = slope
    
    db1.delete(db1["_design/users"])
    return jsonify(res)

@app.route("/Scenario2",methods=["GET","POST"])
def set2():
    
    
    map_fun_rm = """
                            function(doc) {
                                emit([doc.userid,doc.text], 1)
            }
                          """
    reduce_fun_rm = "_count"
    design = {'views': {
        'get_unames': {
            'map': map_fun_rm,
            'reduce': reduce_fun_rm
        }
    }}
    db2["_design/users"] = design
    
    if(db2.view('users/get_unames', group_level=2)==None):
        abort(501)
        
    uname_list = db2.view('users/get_unames', group_level=2)
    for i in uname_list:
        if (i.value > 1):
            temp = None
            
            for doc in db2.find({'selector': {'userid': i.key[0], "text": i.key[1]}}):
                temp = doc
            if (temp is not None):
                db2.delete(temp) 
    db2.delete(db2["_design/users"]) 
   

    map_fun = """
                    function(doc) {

                        emit([doc.suburb,doc.emotion], 1)
    }
                  """
    reduce_fun = "_count"
    design = {'views': {
        'get_unames': {
            'map': map_fun,
            'reduce': reduce_fun
        }
    }}

    db2["_design/users"] = design
    
    if(db2.view('users/get_unames', group_level=2)==None):
        abort(501)
        
    uname_list = db2.view('users/get_unames', group_level=2)
    dic2 = {}
    rate = []
    x = []
        
    res = dict.fromkeys(suburbName, 0)
    print(res)
    for i in range(len(suburbName)):
        res[suburbName[i]] = {'pos': 0}
    for i in range(len(suburbName)):
        dic2[suburbName[i]]=[0,0]
        
    for r in uname_list:
        if r.key[1] == 'neg':
            dic2[r.key[0]] = [r.value,0]
        elif r.key[1] == 'neu':
            dic2[r.key[0]][1] = r.value 
        elif r.key[1] == 'pos':
            neg_num = dic2[r.key[0]][0]
            neu_num = dic2[r.key[0]][1]
            pos_num = r.value
            dic2[r.key[0]] = pos_num / (neg_num + neu_num + pos_num)
        else:
            continue
    for r in uname_list:
        res[r.key[0]]['pos'] = dic2[r.key[0]]
    for sub in suburbName:
        for doc in aurin2.find({'selector': {'sub': sub}}):
            rate.append(doc['rate'])
            res[sub]['aurin'] = doc['chart']
        x.append(res[sub]['pos'])
    
    newRate = []
    for i in rate:
        newRate.append(float(i))
    
    for r in uname_list:
        slope, intercept, r_value, p_value, std_err = st.linregress(x, newRate)
        res[r.key[0]]['b0'] = intercept
        res[r.key[0]]['b1'] = slope
    
    db2.delete(db2["_design/users"])
    return jsonify(res)

@app.route("/Scenario3",methods=["GET","POST"])
def set3():
   
    
    map_fun_rm = """
                            function(doc) {
                                emit([doc.userid,doc.text], 1)
            }
                          """
    reduce_fun_rm = "_count"
    design = {'views': {
        'get_unames': {
            'map': map_fun_rm,
            'reduce': reduce_fun_rm
        }
    }}
    db3["_design/users"] = design
    
    if(db3.view('users/get_unames', group_level=2)==None):
        abort(501)
        
    uname_list = db3.view('users/get_unames', group_level=2)
    for i in uname_list:
        if (i.value > 1):
            temp = None
            
            for doc in db3.find({'selector': {'userid': i.key[0], "text": i.key[1]}}):
                temp = doc
            if (temp is not None):
                db3.delete(temp)  
    db3.delete(db3["_design/users"])  
   



    map_fun = """
                    function(doc) {

                        emit([doc.suburb,doc.lan], 1)
    }
                  """
    reduce_fun = """
                function(keys, values) {
                    return values[0];
                }
              """
    design = {'views': {
        'get_unames': {
            'map': map_fun,
            'reduce': reduce_fun
        }
    }}

    db3["_design/users"] = design
    
    if(db3.view('users/get_unames', group_level=2)==None):
        abort(501)
        
    uname_list = db3.view('users/get_unames', group_level=2)
    rate = []
    x = []

    res = dict.fromkeys(suburbName, 0)
    print(res)
    for i in range(len(suburbName)):
        res[suburbName[i]] = {'lang': 0}
    for r in uname_list:
        res[r.key[0]]['lang'] += 1
    for sub in suburbName:
        for doc in aurin3.find({'selector': {'sub': sub}}):
            rate.append(doc['rate'])
            res[sub]['aurin'] = doc['chart']
        x.append(res[sub]['lang'])
            
    newRate = []
    for i in rate:
        newRate.append(float(i))
        
    for r in uname_list:
        slope, intercept, r_value, p_value, std_err = st.linregress(x, newRate)
        res[r.key[0]]['b0'] = intercept
        res[r.key[0]]['b1'] = slope
            
    db3.delete(db3["_design/users"])
    return jsonify(res)


if __name__ == '__main__':
    server = couchdb.Server("http://admin:admin@172.26.132.76:5984")
    db1 = server['baup_scenario1']
    db2 = server['scenario2']
    db3 = server['scenario3']
    aurin1 = server['aurin1']
    aurin2 = server['aurin2']
    aurin3 = server['aurin3']
    app.run(host="0.0.0.0")
