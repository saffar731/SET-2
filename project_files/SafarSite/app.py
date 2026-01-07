from flask import Flask, render_template, request, jsonify
import math
import os

app = Flask(__name__)

def calculate_stability(h, b, ts, tf, pcc, phi, gs, q, mu):
    # Constants
    gamma_c = 25.0  # Density of Concrete
    tf_m = tf / 1000
    ts_m = ts / 1000
    
    # Earth Pressure (Rankine)
    phi_rad = math.radians(phi)
    ka = (1 - math.sin(phi_rad)) / (1 + math.sin(phi_rad))
    
    # Driving Forces
    pa = 0.5 * ka * gs * (h**2)
    pq = ka * q * h
    total_driving = pa + pq
    mo = (pa * h/3) + (pq * h/2)
    
    # Resisting Forces (Weights)
    w_stem = (h - tf_m) * ts_m * gamma_c
    w_base = b * tf_m * gamma_c
    total_v = w_stem + w_base
    
    # Resisting Moment
    mr = (w_stem * (b * 0.6)) + (w_base * (b / 2))
    
    fos_s = (total_v * mu) / total_driving if total_driving > 0 else 99
    fos_o = mr / mo if mo > 0 else 99
    
    return {
        "fos_sliding": round(fos_s, 2),
        "fos_overturning": round(fos_o, 2),
        "is_safe": fos_s > 1.5 and fos_o > 2.0
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        d = request.json
        res = calculate_stability(
            float(d['h']), float(d['b']), float(d['ts']),
            float(d['tf']), float(d['pcc']), float(d['phi']),
            float(d['gs']), float(d['q']), float(d['mu'])
        )
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)