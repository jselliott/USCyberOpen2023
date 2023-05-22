from flask import Flask, render_template, request, Response, send_file, jsonify, make_response, abort
from sqlalchemy.sql import text
from application.database import db, Hacker, Flag
from logging.config import dictConfig
import json

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
app.config.from_object('application.config.Config')

flag = open("/flag.txt").read()

# Set up DB
with app.app_context():

    db.init_app(app)
    db.create_all()

    #Clear DB first
    db.session.query(Hacker).delete()
    db.session.commit()

    # Add flag
    db.session.add(Flag(flag=flag))
    db.session.commit()

    # Add Hackers
    with open("/hackers.json") as H:
        import_hackers = json.loads(H.read())
        for h in import_hackers:
            db.session.add(Hacker(name=h[0],specialization=h[1],location=h[2],price=h[3]))
            db.session.commit()


@app.route('/',methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/api/contact',methods=['POST'])
def contact():
    return ""

@app.route('/api/search',methods=['GET'])
def search():

    try:

        search_val = request.args.get("search[value]")

        all_hackers = Hacker.query.count()
        hackers = Hacker.query.filter(text("name LIKE '%%%s%%'" % search_val))

        hacker_count = hackers.count()

        for i in range(4):

            order_col = request.args.get("order[%d][column]" % i,None)
            order_dir = request.args.get("order[%d][dir]" % i,None)

            if order_col is None or order_dir is None:
                break
            
            if order_col == "0":
                if order_dir == "asc":
                    hackers = hackers.order_by(Hacker.name.asc())
                else:
                    hackers = hackers.order_by(Hacker.name.desc())
            elif order_col == "1":
                if order_dir == "asc":
                    hackers = hackers.order_by(Hacker.specialization.asc())
                else:
                    hackers = hackers.order_by(Hacker.specialization.desc())
            elif order_col == "2":
                if order_dir == "asc":
                    hackers = hackers.order_by(Hacker.location.asc())
                else:
                    hackers = hackers.order_by(Hacker.location.desc())
            elif order_col == "3":
                if order_dir == "asc":
                    hackers = hackers.order_by(Hacker.price.asc())
                else:
                    hackers = hackers.order_by(Hacker.price.desc())

        hackers = hackers.limit(request.args.get("length",10))
        hackers = hackers.offset(request.args.get("start",0))

        data = [[h.name,h.specialization,h.location,"$%s / Hr" % str(h.price),"<button type='button' class='contact btn btn-primary' data-hackerid='%s'>Request Info</button>" % str(h.id)] for h in hackers.all()]

        R = {"draw": request.args.get("draw",1),
        "recordsTotal": all_hackers,
        "recordsFiltered": hacker_count,
        "data":data}

        return make_response(jsonify(R))
    
    except:
        abort(500)

@app.route('/favicon.ico',methods=['GET'])
def icon():
    return send_file("static/favicon.ico")
        
        
    



