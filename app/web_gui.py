from flask import Flask, render_template, request, redirect
from app.config_manager import load_config, save_config

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    config = load_config()
    if request.method == "POST":
        new_config = request.form.to_dict()
        for k in config:
            value = new_config.get(k, config[k])
            config[k] = value if value.lower() not in ["true", "false"] else value.lower() == "true"
        save_config(config)
        return redirect("/")
    return render_template("index.html", config=config)

def start_web_gui():
    app.run(host="0.0.0.0", port=8080)
