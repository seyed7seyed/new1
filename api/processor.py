# api/processor.py

import matplotlib.pyplot as plt
import io
import base64

def compute_sum(y: list[float]) -> float:
    return sum(y)

# plot
def generate_plot(x: list[float], y: list[float]) -> str:
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Scatter Plot")

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return encoded

import pandas as pd
from fastapi import UploadFile
import requests

# Upload a file
def parse_uploaded_file(file: UploadFile) -> tuple[list[float], list[float]]:
    content = file.file.read()
    if file.filename.endswith(".json"):
        data = pd.read_json(io.BytesIO(content))
    elif file.filename.endswith(".csv"):
        data = pd.read_csv(io.BytesIO(content))
    else:
        raise ValueError("Unsupported file format. Use CSV or JSON.")
    return data["x"].tolist(), data["y"].tolist()

# file Url
def parse_remote_file(url: str) -> tuple[list[float], list[float]]:
    response = requests.get(url)
    if url.endswith(".json"):
        data = pd.read_json(io.BytesIO(response.content))
    elif url.endswith(".csv"):
        data = pd.read_csv(io.BytesIO(response.content))
    else:
        raise ValueError("Unsupported URL format. Use CSV or JSON.")
    return data["x"].tolist(), data["y"].tolist()


import pandas as pd
# Enter by Hand
def parse_text_input(text: str) -> tuple[list[float], list[float]]:
    try:
        df = pd.read_csv(io.StringIO(text.strip()))
        return df["x"].tolist(), df["y"].tolist()
    except Exception as e:
        raise ValueError(f"Failed to parse text input: {e}")

# Improve Validation & Feedback
def validate_dataframe(df: pd.DataFrame) -> tuple[list[float], list[float]]:
    if not {"x", "y"}.issubset(df.columns):
        raise ValueError("Input must contain 'x' and 'y' columns.")
    if df.empty:
        raise ValueError("Input data is empty.")
    return df["x"].tolist(), df["y"].tolist()
    
def parse_uploaded_file(file: UploadFile) -> tuple[list[float], list[float]]:
    content = file.file.read()
    if file.filename.endswith(".json"):
        df = pd.read_json(io.BytesIO(content))
    elif file.filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(content))
    else:
        raise ValueError("Unsupported file format. Use CSV or JSON.")
    return validate_dataframe(df)

def parse_remote_file(url: str) -> tuple[list[float], list[float]]:
    response = requests.get(url)
    if url.endswith(".json"):
        df = pd.read_json(io.BytesIO(response.content))
    elif url.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(response.content))
    else:
        raise ValueError("Unsupported URL format. Use CSV or JSON.")
    return validate_dataframe(df)

def parse_text_input(text: str) -> tuple[list[float], list[float]]:
    df = pd.read_csv(io.StringIO(text.strip()))
    return validate_dataframe(df)



