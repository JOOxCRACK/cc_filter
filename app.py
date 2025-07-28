from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        combo_file = request.files["combo"]
        output_name = request.form["output_name"]

        lines = combo_file.read().decode("utf-8").splitlines()
        cleaned_lines = []

        for line in lines:
            parts = line.split("|")
            if len(parts) >= 3 and "/" in parts[1]:
                card = parts[0].strip()
                exp_month, exp_year = parts[1].split("/")
                cvv = parts[2].strip()
                result_line = f"{card}|{exp_month.strip()}|{exp_year.strip()}|{cvv}"
                cleaned_lines.append(result_line)

        output_path = f"{output_name}.txt"
        with open(output_path, "w") as f:
            f.write("\n".join(cleaned_lines))

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
