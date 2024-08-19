from flask import Flask, request, jsonify, render_template
from src.npc_attack import npc_attack
app = Flask(__name__, template_folder='templates')


    
@app.route("/")
def index():
    return render_template("response.html")

@app.route("/add")
def make_cron():
    location = request.args.get('location', '')
    stage = request.args.get('stage', '')
    cron = request.args.get('cron', '')
    
    data = {"location": location, "stage": stage, "cron": cron}
    npc_attackk = npc_attack()
    npc_attackk.attack_npcs(location, stage)
    return jsonify(data) 


if __name__ == '__main__':
    app.run(debug=True)