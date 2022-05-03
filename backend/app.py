from flask import Flask,render_template,request
from flask import jsonify
from flask_cors import CORS
import couchdb

suburbName = ["Flemington", "Carlton", "Docklands", "East Melbourne", "Kensington", "Melbourne", "North Melbourne", "Parkville", "Southbank", "Port Melbourne", "South Yarra - East"]


app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/Scenario1",methods=["GET","POST"])
def set1():
    #############################去重开始#################################
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
    db1["_design/users"] = design
    uname_list = db1.view('users/get_unames', group_level=2)
    for i in uname_list:
        if (i.value > 1):
            temp = None
            #### userid 就是tweet的id  text就是tweeet 的内容
            for doc in db1.find({'selector': {'userid': i.key[0], "text": i.key[1]}}):
                temp = doc

            db1.delete(temp)  ##删除重复的数据
    db1.delete(db1["_design/users"])  ##删除视图
    #############################去重结束#################################

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

    db1["_design/users"] = design
    uname_list = db1.view('users/get_unames', group_level=2)
    dic1 = {}
    print(uname_list)

    for r in uname_list:
        if r.key[1] == 'neg':
            dic1[r.key[0]] = r.value
        elif r.key[1] == 'pos':
            neg_num = dic1[r.key[0]]
            pos_num = r.value
            dic1[r.key[0]] = pos_num / (neg_num + pos_num)
        else:
            continue
    print(dic1)
    db1.delete(db1["_design/users"])
    return jsonify(dic1)

@app.route("/Scenario2",methods=["GET","POST"])
def set2():
    #############################去重开始#################################
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
    uname_list = db2.view('users/get_unames', group_level=2)
    for i in uname_list:
        if (i.value > 1):
            temp = None
            #### userid 就是tweet的id  text就是tweeet 的内容
            for doc in db2.find({'selector': {'userid': i.key[0], "text": i.key[1]}}):
                temp = doc

            db2.delete(temp)  ##删除重复的数据
    db2.delete(db2["_design/users"])  ##删除视图
    #############################去重结束#################################

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
    uname_list = db2.view('users/get_unames', group_level=2)
    dic2 = {}
    print(uname_list)

    for r in uname_list:
        if r.key[1] == 'neg':
            dic2[r.key[0]] = r.value
        elif r.key[1] == 'pos':
            neg_num = dic2[r.key[0]]
            pos_num = r.value
            dic2[r.key[0]] = pos_num / (neg_num + pos_num)
        else:
            continue
    print(dic2)
    db2.delete(db2["_design/users"])
    return jsonify(dic2)

@app.route("/Scenario3",methods=["GET","POST"])
def set3():
    #############################去重开始#################################
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
    uname_list = db3.view('users/get_unames', group_level=2)
    for i in uname_list:
        if (i.value > 1):
            temp = None
            #### userid 就是tweet的id  text就是tweeet 的内容
            for doc in db3.find({'selector': {'userid': i.key[0], "text": i.key[1]}}):
                temp = doc

            db3.delete(temp)  ##删除重复的数据
    db3.delete(db3["_design/users"])  ##删除视图
    #############################去重结束#################################

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
    uname_list = db3.view('users/get_unames', group_level=2)

    res = dict.fromkeys(suburbName, 0)
    for r in uname_list:
        res[r.key[0]] += 1
    print(res)  # 发送给前端的东西
    db3.delete(db3["_design/users"])
    return jsonify(res)

if __name__ == '__main__':
    server = couchdb.Server("http://admin:admin@172.26.132.76:5984")
    db1 = server['scenario1']
    db2 = server['scenario2']
    db3 = server['scenario3']
    app.run()
