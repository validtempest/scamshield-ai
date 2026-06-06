"""
ScamShield AI - Advanced Risk Analysis System
This module handles threat classification scoring and risk evaluation.
It provides high-precision keyword scoring and composite threat assessment.
Designed to be modular, scalable, and highly explainable for academic presentations.
"""

def get_scam_category(message):
    """
    Classifies a message into specific scam categories using a modular Keyword Scoring System.
    Analyzes all matches, counts occurrences per category, and selects the category 
    with the highest intensity score (using max() scoring model).
    
    Args:
        message (str): The raw text message input from the threat analyzer terminal.
        
    Returns:
        str: The classified category in Indonesian, or 'Penipuan Tidak Dikenal' if no keywords match.
    """
    if not message:
        return 'Penipuan Tidak Dikenal'

    # Convert to lowercase for case-insensitive keyword scanning
    text = message.lower()

    # Modular registry of threat categories and their corresponding key indicators
    CATEGORIES_REGISTRY = {
        'Penipuan Undian / Hadiah': [
            'hadiah', 'reward', 'bonus', 'lottery', 'cash', 'money', 
            'gratis', 'voucher', 'prize', 'menang', 'undian'
        ],
        'Penipuan Perbankan / OTP': [
            'bank', 'rekening', 'account', 'password', 'verify', 
            'verifikasi', 'otp', 'saldo', 'atm', 'transfer', 'blokir', 'akun'
        ],
        'Penipuan Phishing / Tautan Palsu': [
            'klik', 'click', 'link', 'claim', 'confirm', 
            'http', 'https', 'bit.ly', 'tinyurl', 'login'
        ],
        'Penipuan Investasi': [
            'investasi', 'profit', 'cuan', 'trading', 
            'deposit', 'keuntungan', 'return'
        ],
        'Penipuan Lowongan Kerja': [
            'kerja online', 'freelance', 'gaji besar', 
            'part time', 'kerja dari rumah'
        ]
    }

    # Dictionary to keep track of match frequency scores for each category
    category_scores = {}

    # Calculate match frequency per category
    for category, keywords in CATEGORIES_REGISTRY.items():
        score = 0
        for keyword in keywords:
            # Count occurrences of the keyword in the text message body
            score += text.count(keyword)
        category_scores[category] = score

    # Find the maximum score across all scanned categories
    max_score = max(category_scores.values())

    # If the highest score is 0, no threat signature keywords were detected
    if max_score == 0:
        return 'Penipuan Tidak Dikenal'

    # Retrieve all categories that tied for the maximum score
    candidates = [cat for cat, score in category_scores.items() if score == max_score]

    # Select the first candidate as the primary threat category
    return candidates[0]


def calculate_risk_score(prediction, confidence):
    """
    Computes a standardized threat intensity scale (0-100) based on prediction and confidence.
    
    Args:
        prediction (str): Binary AI classification result ('scam' or 'safe').
        confidence (float): Raw probability index from predict_proba() (0.0 to 1.0).
        
    Returns:
        int: Standardized integer score scale between 0 and 100.
    """
    try:
        # Standardize confidence to float scale
        conf_val = float(confidence)
    except (ValueError, TypeError):
        conf_val = 0.0

    if prediction == 'scam':
        # High confidence in scam maps directly to high threat risk
        score = conf_val * 100
    else:
        # High confidence in safe maps to low threat risk (100 - confidence * 100)
        score = 100 - (conf_val * 100)

    # Clean outputs to fall strictly within standard integer limits
    return max(0, min(100, int(round(score))))


def get_risk_level(score):
    """
    Categorizes threat scores into simplified, presentable hazard intensity thresholds.
    
    Args:
        score (int): Threat index score between 0 and 100.
        
    Returns:
        str: Dual-language risk assessment indicator for UI/academic presentations.
    """
    if score >= 80:
        return 'High Risk (Risiko Tinggi)'
    elif score >= 50:
        return 'Medium Risk (Risiko Sedang)'
    else:
        return 'Low Risk (Risiko Rendah)'


def get_analysis_reason(prediction, confidence, message, category):
    """
    Generates a clear, explainable, and academic-friendly justification 
    for why the AI classified the message as Scam or Safe.
    
    Args:
        prediction (str): Classification result ('scam' or 'safe').
        confidence (float): Confidence percentage (0-100).
        message (str): Raw input message text.
        category (str): The identified category.
        
    Returns:
        dict: A dictionary containing 'summary' and 'details' of the reason.
    """
    if not message:
        return {
            'summary': 'Pesan kosong.',
            'details': 'Tidak ada konten pesan yang dikirim untuk dianalisis.'
        }
        
    text = message.lower()
    
    # Kategori siber dan kata kunci pendeteksi
    CATEGORIES_REGISTRY = {
        'Penipuan Undian / Hadiah': [
            'hadiah', 'reward', 'bonus', 'lottery', 'cash', 'money', 
            'gratis', 'voucher', 'prize', 'menang', 'undian'
        ],
        'Penipuan Perbankan / OTP': [
            'bank', 'rekening', 'account', 'password', 'verify', 
            'verifikasi', 'otp', 'saldo', 'atm', 'transfer', 'blokir', 'akun'
        ],
        'Penipuan Phishing / Tautan Palsu': [
            'klik', 'click', 'link', 'claim', 'confirm', 
            'http', 'https', 'bit.ly', 'tinyurl', 'login'
        ],
        'Penipuan Investasi': [
            'investasi', 'profit', 'cuan', 'trading', 
            'deposit', 'keuntungan', 'return'
        ],
        'Penipuan Lowongan Kerja': [
            'kerja online', 'freelance', 'gaji besar', 
            'part time', 'kerja dari rumah'
        ]
    }
    
    # Mencari kata kunci yang cocok dalam pesan
    detected_keywords = []
    for cat_name, keywords in CATEGORIES_REGISTRY.items():
        for keyword in keywords:
            if keyword in text:
                detected_keywords.append(keyword)
                
    # Menghapus duplikasi kata kunci
    detected_keywords = list(dict.fromkeys(detected_keywords))
    
    if prediction == 'scam':
        summary = f"AI mendeteksi pola teks mencurigakan dengan tingkat keyakinan {confidence}%."
        
        details = (
            f"Berdasarkan analisis klasifikasi Naive Bayes, pesan ini memiliki indikasi kuat penipuan. "
            f"Sistem mengklasifikasikannya ke dalam kelompok '{category}'."
        )
        
        if detected_keywords:
            details += f" Faktor pemicu utama adalah deteksi kata kunci sensitif berikut: {', '.join([f'\"{w}\"' for w in detected_keywords])}."
        else:
            details += " Analisis probabilistik TF-IDF mendeteksi struktur kalimat yang identik dengan basis data pesan scam kami."
            
        return {
            'summary': summary,
            'details': details,
            'keywords': detected_keywords
        }
    else:
        summary = f"AI memverifikasi pesan ini sebagai interaksi aman dengan keyakinan {confidence}%."
        
        details = (
            "Model Naive Bayes dan pembobotan kata TF-IDF tidak menemukan karakteristik penipuan yang signifikan. "
            "Struktur bahasa, diksi, dan susunan kalimat yang digunakan sangat identik dengan pola komunikasi normal sehari-hari."
        )
        
        if detected_keywords:
            details += (
                f" Meskipun terdapat kata kunci umum {', '.join([f'\"{w}\"' for w in detected_keywords])}, "
                "konteks keseluruhan pesan tetap dinilai aman karena tidak memenuhi intensitas bobot ancaman siber."
            )
        else:
            details += " Tidak ada kata kunci pemicu bahaya (seperti paksaan transaksi, iming-iming hadiah, atau tautan mencurigakan) yang terdeteksi."
            
        return {
            'summary': summary,
            'details': details,
            'keywords': detected_keywords
        }