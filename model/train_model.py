import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..'
        )
    )
)

import pandas as pd
import joblib

from sklearn.model_selection import (
    train_test_split
)

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from sklearn.naive_bayes import (
    MultinomialNB
)

from sklearn.metrics import (
    accuracy_score
)

from utils.preprocessing import (
    preprocess_text
)

# ======================
# BASE PATH
# ======================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..'
    )
)

DATASET_DIR = os.path.join(
    BASE_DIR,
    'dataset'
)

SAVE_DIR = os.path.join(
    BASE_DIR,
    'saved_model'
)

# ======================
# ENGLISH DATASET
# ======================

df_en = pd.read_csv(
    os.path.join(
        DATASET_DIR,
        'spam.csv'
    ),
    encoding='latin-1'
)

df_en = df_en[
    ['v1', 'v2']
]

df_en.columns = [
    'label',
    'message'
]

# normalize label
df_en['label'] = (
    df_en['label']
    .astype(str)
    .str.lower()
    .str.strip()
    .replace({
        'ham': 'safe',
        'spam': 'scam'
    })
)

# ======================
# INDONESIA DATASET
# ======================

df_id = pd.read_csv(
    os.path.join(
        DATASET_DIR,
        'dataset_sms_spam_v1.csv'
    ),
    on_bad_lines='skip'
)

# handle possible column names
df_id.columns = (
    df_id.columns
    .str.strip()
    .str.lower()
)

df_id = df_id.rename(
    columns={
        'teks': 'message',
        'text': 'message',
        'label': 'label'
    }
)

df_id = df_id[
    ['message', 'label']
]

# normalize label
df_id['label'] = (
    df_id['label']
    .astype(str)
    .str.lower()
    .str.strip()
    .replace({
        'promo': 'safe',
        'penipuan': 'scam',
        'normal': 'safe'
    })
)

# ======================
# CUSTOM DATASET
# ======================

df_custom = pd.read_csv(
    os.path.join(
        DATASET_DIR,
        'spam_dataset.csv'
    )
)

df_custom.columns = (
    df_custom.columns
    .str.strip()
    .str.lower()
)

df_custom = df_custom.rename(
    columns={
        'message': 'message',
        'label': 'label'
    }
)

df_custom = df_custom[
    ['label', 'message']
]

# normalize label
df_custom['label'] = (
    df_custom['label']
    .astype(str)
    .str.lower()
    .str.strip()
    .replace({
        'spam': 'scam',
        'ham': 'safe',
        'scam': 'scam',
        'safe': 'safe'
    })
)

# ======================
# MERGE DATASET
# ======================

df = pd.concat(
    [
        df_en,
        df_id,
        df_custom
    ],
    ignore_index=True
)

# final normalize
df['label'] = (
    df['label']
    .replace({
        'spam': 'scam',
        'ham': 'safe',
        'promo': 'scam',
        'penipuan': 'scam',
        'normal': 'safe'
    })
)

# remove null
df = df.dropna()

# remove duplicates
df = df.drop_duplicates()

# keep only valid labels
df = df[
    df['label'].isin(
        ['safe', 'scam']
    )
]

print("\n===== LABEL COUNT =====")
print(df['label'].value_counts())

print("\n===== TOTAL DATASET =====")
print(len(df))

# ======================
# PREPROCESSING
# ======================

df['cleaned_text'] = (
    df['message']
    .astype(str)
    .apply(preprocess_text)
)

X = df[
    'cleaned_text'
]

y = df[
    'label'
]

# ======================
# TF-IDF
# ======================

vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)

X_vectorized = (
    vectorizer.fit_transform(X)
)

# ======================
# TRAIN TEST SPLIT
# ======================

X_train, X_test, y_train, y_test = (
    train_test_split(
        X_vectorized,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )
)

# ======================
# TRAIN MODEL
# ======================

model = MultinomialNB()

model.fit(
    X_train,
    y_train
)

# ======================
# TEST MODEL
# ======================

predictions = (
    model.predict(X_test)
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(
    f'\nAccuracy: {accuracy * 100:.2f}%'
)

# ======================
# SAVE MODEL
# ======================

os.makedirs(
    SAVE_DIR,
    exist_ok=True
)

joblib.dump(
    model,
    os.path.join(
        SAVE_DIR,
        'model.pkl'
    )
)

joblib.dump(
    vectorizer,
    os.path.join(
        SAVE_DIR,
        'vectorizer.pkl'
    )
)

print(
    '\nModel saved successfully!'
)