from flask import Flask, render_template, request
from subprocess import PIPE, run, STDOUT, check_output, CalledProcessError
import os

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello from Flask!'
@app.route('/embed')
def embed():
  params = request.args
  defcode = ""
  if ("code" in params):
    defcode = params["code"]
  if (params["lang"] == "js"):
    
    return render_template("js.html", code=defcode)
  if (params["lang"] == "py"):
    return render_template("py.html",code=defcode)
  return render_template("lua.html",code=defcode)
    
@app.route('/eval', methods=["POST"])
def eval():
    data = request.get_json()
    params = request.args
    if (params["lang"] == "js"):
      print(data)
      with open('test.js', 'w') as f:
        f.write(data["code"])       
      try:
        output = check_output(
            "node test.js", stderr=STDOUT, shell=True, timeout=3,
            universal_newlines=True)
      except CalledProcessError as exc:
        error = "Process exited with return code " + str(exc.returncode) + "\n" + str(exc.output)
        print(error)
        return {"result":error.split("\n"), "error": True}
      else:
        print(output)
        return {"result":output.split("\n"), "error": False}
    if (params["lang"] == "lua"):
      print(data)
      with open('test.lua', 'w') as f:
        f.write(data["code"])       
      try:
        output = check_output(
            "lua test.lua", stderr=STDOUT, shell=True, timeout=3,
            universal_newlines=True)
      except CalledProcessError as exc:
        error = "Process exited with return code " + str(exc.returncode) + "\n" + str(exc.output)
        print(error)
        return {"result":error.split("\n"), "error": True}
      else:
        print(output)
        return {"result":output.split("\n"), "error": False}
    if (params["lang"] == "py"):
      print(data)
      with open('test.py', 'w') as f:
        f.write(data["code"])       
      try:
        output = check_output(
            "python test.py", stderr=STDOUT, shell=True, timeout=3,
            universal_newlines=True)
      except CalledProcessError as exc:
        error = "Process exited with return code " + str(exc.returncode) + "\n" + str(exc.output)
        print(error)
        return {"result":error.split("\n"), "error": True}
      else:
        print(output)
        return {"result":output.split("\n"), "error": False}
    return {"result":""}
app.run(host='0.0.0.0', debug=True)
