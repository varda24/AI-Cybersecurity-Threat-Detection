import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cybersecurity Threat Detection", layout="wide")

# -------------------------------
# TITLE
# -------------------------------
st.markdown(
    "<h1 style='text-align: center; color: red;'>🛡️ Cyber Threat Detection Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown("### Real-time Threat Detection using Machine Learning")

# -------------------------------
# LOAD MODEL
# -------------------------------
@st.cache_resource
def load_model():
    return joblib.load("models/model.pkl")

model = load_model()

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.header("Controls")

uploaded_file = st.sidebar.file_uploader("📂 Upload Network Data CSV")

sample_size = st.sidebar.slider("Select sample size", 500, 5000, 2000)

# -------------------------------
# LOAD DATA
# -------------------------------
def load_default_data():
    try:
        return pd.read_csv("data/sample.csv", header=None)
    except:
        return None

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, header=None)
    st.success("Uploaded file loaded successfully!")
else:
    df = load_default_data()
    if df is None:
        st.warning("⚠️ No dataset found. Please upload a CSV file.")
        st.stop()

# -------------------------------
# DATA PREVIEW
# -------------------------------
st.subheader("📊 Dataset Preview")
st.write(df.head())

# -------------------------------
# SAMPLE DATA
# -------------------------------
df_sample = df.sample(n=min(sample_size, len(df)))

st.subheader("📈 Sampled Data")
st.write(df_sample.head())

# -------------------------------
# COLUMN NAMES (KDD DATASET)
# -------------------------------
columns = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes","land",
    "wrong_fragment","urgent","hot","num_failed_logins","logged_in","num_compromised",
    "root_shell","su_attempted","num_root","num_file_creations","num_shells",
    "num_access_files","num_outbound_cmds","is_host_login","is_guest_login",
    "count","srv_count","serror_rate","srv_serror_rate","rerror_rate",
    "srv_rerror_rate","same_srv_rate","diff_srv_rate","srv_diff_host_rate",
    "dst_host_count","dst_host_srv_count","dst_host_same_srv_rate",
    "dst_host_diff_srv_rate","dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate","dst_host_serror_rate",
    "dst_host_srv_serror_rate","dst_host_rerror_rate",
    "dst_host_srv_rerror_rate","label"
]

df_sample.columns = columns

# -------------------------------
# PREPROCESSING
# -------------------------------
if "label" in df_sample.columns:
    df_sample = df_sample.drop("label", axis=1)

df_sample = pd.get_dummies(df_sample)

# Align with training features
model_features = model.feature_names_in_
df_sample = df_sample.reindex(columns=model_features, fill_value=0)

# -------------------------------
# PREDICTION
# -------------------------------
preds = model.predict(df_sample)

attack_count = (preds == 1).sum()
normal_count = (preds == 0).sum()

# -------------------------------
# METRICS
# -------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("🚨 Attacks Detected", attack_count)
col2.metric("✅ Normal Traffic", normal_count)

threat_percent = (attack_count / (attack_count + normal_count)) * 100
col3.metric("⚠️ Threat %", f"{threat_percent:.2f}%")

# -------------------------------
# ALERT SYSTEM
# -------------------------------
if threat_percent > 70:
    st.error(f"🚨 HIGH THREAT LEVEL: {threat_percent:.2f}% traffic is malicious")
elif threat_percent > 30:
    st.warning(f"⚠️ MEDIUM THREAT LEVEL: {threat_percent:.2f}% suspicious traffic")
else:
    st.success("✅ LOW THREAT LEVEL: Network is stable")

# -------------------------------
# SYSTEM STATUS
# -------------------------------
if attack_count > 0:
    st.warning("⚠️ Suspicious activity detected in network traffic")
else:
    st.success("✅ Network operating normally")

# -------------------------------
# GRAPH
# -------------------------------
st.subheader("📊 Prediction Distribution")

fig, ax = plt.subplots()
pd.Series(preds).value_counts().plot(kind='bar', ax=ax)
ax.set_title("Cyber Threat Detection Results")

st.pyplot(fig)

# -------------------------------
# RESULTS TABLE
# -------------------------------
st.subheader("📄 Prediction Results")
results = pd.DataFrame({"Prediction": preds})
st.write(results.head(50))

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown("Developed by Varda | AI Cybersecurity Project")