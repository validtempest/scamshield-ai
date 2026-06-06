import time

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

from config import Config

from database.models import (
    db,
    ScanHistory
)

from model.predictor import (
    predict_message
)

from utils.risk_analyzer import (
    get_scam_category,
    calculate_risk_score,
    get_risk_level,
    get_analysis_reason
)

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

@app.route('/')
def home():
    return render_template(
        'index.html'
    )
    
@app.route('/dashboard')
def dashboard():

    total_scan = (
        ScanHistory.query.count()
    )

    total_scam = (
        ScanHistory.query.filter_by(
            prediction='scam'
        ).count()
    )

    total_safe = (
        ScanHistory.query.filter_by(
            prediction='safe'
        ).count()
    )

    scam_rate = 0

    if total_scan > 0:
        scam_rate = round(
            (
                total_scam
                / total_scan
            ) * 100,
            2
        )

    recent_scans = (
        ScanHistory.query
        .order_by(
            ScanHistory.created_at.desc()
        )
        .limit(5)
        .all()
    )

    return render_template(
        'dashboard.html',
        total_scan=total_scan,
        total_scam=total_scam,
        total_safe=total_safe,
        scam_rate=scam_rate,
        recent_scans=recent_scans,

        scam_chart=total_scam,
        safe_chart=total_safe
    )

@app.route(
    '/analyze',
    methods=['POST']
)
def analyze():

    message = request.form.get(
        'message'
    )
    
    time.sleep(
        app.config[
            'FAKE_LOADING_TIME'
        ]
    )

    prediction, confidence, cleaned_text = (
        predict_message(message)
    )

    risk_score = calculate_risk_score(
        prediction,
        confidence
    )

    risk_level = get_risk_level(risk_score)

    category = (
        get_scam_category(message)
        if prediction == 'scam'
        else 'Percakapan Aman'
    )

    reason = get_analysis_reason(
        prediction,
        round(confidence * 100, 2),
        message,
        category
    )

    # save database
    new_scan = ScanHistory(
        message=message,
        cleaned_text=cleaned_text,
        prediction=prediction,
        confidence=confidence,
        risk_score=risk_score,
        category=category
    )

    db.session.add(new_scan)
    db.session.commit()

    return render_template(
        'result.html',
        message=message,
        cleaned_text=cleaned_text,
        prediction=prediction,
        confidence=round(
            confidence * 100,
            2
        ),
        risk_score=risk_score,
        risk_level=risk_level,
        category=category,
        reason=reason
    )
    
@app.route('/history')
def history():

    # Ambil nomor halaman dari query string, default = 1
    page = request.args.get('page', 1, type=int)

    # Pagination: 10 item per halaman, tidak error jika halaman tidak valid
    pagination = (
        ScanHistory.query
        .order_by(ScanHistory.created_at.desc())
        .paginate(page=page, per_page=10, error_out=False)
    )

    return render_template(
        'history.html',
        histories=pagination.items,
        pagination=pagination
    )

@app.route('/history/delete/<int:id>', methods=['POST'])
def delete_history(id):
    scan_item = ScanHistory.query.get_or_404(id)
    try:
        db.session.delete(scan_item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('history'))

@app.route('/history/clear', methods=['POST'])
def clear_all_history():
    try:
        ScanHistory.query.delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('history'))

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(
        debug=app.config[
            'FLASK_DEBUG'
        ]
    )