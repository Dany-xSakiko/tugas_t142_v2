import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import base64
import altair as alt

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Simulator Profit",
    page_icon="🌸",
    layout="wide", # Layout lebar lebih modern
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. FUNGSI BACKGROUND & KARTU KACA
# ==========================================
def add_bg_from_local(image_file):
    try:
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        st.markdown(
        f"""
        <style>
        /* Pasang gambar anime ke seluruh latar belakang web */
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        
        /* KUNCI ANTI-NABRAK: Bungkus konten dengan kartu gelap semi-transparan */
        .block-container {{
            background-color: rgba(14, 17, 23, 0.85) !important; /* Gelap transparan 85% */
            border-radius: 20px; /* Sudut membulat */
            padding: 2rem 3rem !important; /* Jarak aman ke pinggir layar */
            margin-top: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5); /* Efek bayangan elegan */
        }}
        
        /* Hilangkan warna background bawaan Streamlit agar tidak dobel */
        .main {{
            background-color: transparent !important; 
        }}
        </style>
        """,
        unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning("Peringatan: File gambar 'bg.png' belum di-upload ke GitHub.")

# Panggil fungsi background (Pastikan ente udah upload bg.png)
add_bg_from_local('bg.png')


# ==========================================
# 3. CUSTOM CSS (STYLING TEKS & WARNA)
# ==========================================
st.markdown(
    """
    <style>
        /* Personalisasi Judul Utama */
        h1 {
            color: #FFFFFF; 
            font-family: 'Poppins', sans-serif;
            text-shadow: 2px 2px 4px rgba(255, 183, 197, 0.3);
            font-size: 3rem !important;
            padding-bottom: 0.5rem;
        }
        
        /* SIDEBAR SOLID: Background gelap pekat, jangan transparan */
        [data-testid="stSidebar"] {
            background-color: #1E1E24 !important; /* Warna abu-abu gelap solid */
            border-right: 3px solid #FFB7C5; /* Garis pembatas pink sakura */
        }
        [data-testid="stSidebar"] h2 {
            color: #FFFFFF; 
        }
        
        /* Personalisasi Slider */
        .stSlider [data-testid="stThumbValue"] {
            color: #FFB7C5; 
        }
        .stSlider label {
            color: #FFFFFF !important;
        }
        
        /* Teks Metrik Angka Hasil */
        div[data-testid="stMetricValue"] {
            color: #FFFFFF; 
            font-size: 3rem;
            font-weight: bold;
        }
        div[data-testid="stMetricDelta"] > div {
            color: #00FF00 !important; /* Warna selisih positif hijau neon */
        }
        
        /* Ubah semua teks deskripsi jadi putih */
        .stMarkdown p, [data-testid="stSidebar"] p {
            color: #FFFFFF; 
        }
        
        /* Bikin background grafik transparan biar nyatu sama kartu */
        [data-testid="stVegaLiteChart"] {
            background-color: transparent !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# 4. PERSIAPAN MODEL & BASELINE
# ==========================================
X_train = np.array([[5, 10], [10, 20], [15, 5], [20, 25], [25, 15]])
y_train = np.array([50, 80, 110, 90, 150])
model = LinearRegression().fit(X_train, y_train)

baseline_input = np.array([[10, 10]])
baseline_pred = model.predict(baseline_input)[0]


# ==========================================
# 5. HEADER APLIKASI
# ==========================================
with st.container():
    col_t1, col_t2 = st.columns([1.5, 3.5]) 
    
    with col_t1:
        # Menampilkan gambar header
        try:
            st.image("test2.jpg", use_container_width=True)
        except Exception:
            st.caption("*(Gambar header belum di-upload)*")
        
    with col_t2:
        st.markdown('<h1>Simulator Profit</h1>', unsafe_allow_html=True)
        st.write("Sesuaikan strategi intervensi untuk melihat dampak langsung pada keuntungan toko kita!")


# ==========================================
# 6. ENGINE SIMULATOR & SIDEBAR
# ==========================================
def run_simulation(new_iklan, new_diskon):
    intervention_input = np.array([[new_iklan, new_diskon]])
    prediction = model.predict(intervention_input)[0]
    delta_y = prediction - baseline_pred
    return prediction, delta_y

st.sidebar.markdown('<h2 style="font-size: 1.5rem;">⚙️ Tuas Intervensi</h2>', unsafe_allow_html=True)
st.sidebar.write("Kendalikan variabel kebijakan:")

iklan_slider = st.sidebar.slider("📉 Anggaran Iklan (Juta)", 0, 50, 10, help="Ubah untuk simulasi skenario iklan")
diskon_slider = st.sidebar.slider("🏷️ Besaran Diskon (%)", 0, 50, 10, help="Ubah untuk simulasi skenario diskon")

# Menjalankan mesin simulasi berdasarkan nilai slider terbaru
hasil_pred, delta = run_simulation(iklan_slider, diskon_slider)


# ==========================================
# 7. TAMPILAN HASIL (METRIK, STIKER & GRAFIK)
# ==========================================
st.write("---") 

col1, col2 = st.columns([2, 3]) 

with col1:
    st.markdown("### ✨ Perkiraan Keuntungan")
    
    # Membelah kolom kiri buat tempat teks dan stiker
    sub_col1, sub_col2 = st.columns([2, 1.5])
    
    with sub_col1:
        st.metric(
            label="Prediksi Keuntungan Baru",
            value=f"Rp {hasil_pred:.2f} Jt",
            delta=f"{delta:.2f} Jt",
            delta_color="normal"
        )
        
        # Teks penjelas kondisional
        if delta > 0:
            st.info(f"Yatta! Untung naik Rp {delta:.2f} Juta dibandingkan kondisi saat ini.")
        elif delta < 0:
            st.warning(f"Waduh... Keuntungan turun Rp {abs(delta):.2f} Juta. Hati-hati!")
        else:
            st.write("Tidak ada perubahan dari kondisi saat ini.")

    with sub_col2:
        # Menampilkan stiker anime kondisional
        try:
            if delta > 0:
                st.image("senang.png", use_container_width=True) 
            elif delta < 0:
                st.image("sedih.png", use_container_width=True)
            else:
                st.image("datar.png", use_container_width=True)
        except Exception:
            st.caption("*(Stiker anime belum di-upload)*")


with col2:
    st.markdown("### 📊 Analisis Perbandingan Skenario")
    
    data_plot = pd.DataFrame({
        'Status Skenario': ['Baseline', 'Intervensi'],
        'Keuntungan (Juta Rp)': [baseline_pred, hasil_pred]
    })
    
    # Membuat grafik kustom dengan Altair agar background transparan
    chart = alt.Chart(data_plot).mark_bar(
        color='#FFB7C5', # Warna batang pink sakura
        size=80, # Ketebalan batang
        cornerRadiusTopLeft=5, # Sudut atas agak membulat
        cornerRadiusTopRight=5
    ).encode(
        x=alt.X('Status Skenario:N', title='Status Skenario', axis=alt.Axis(labelColor='white', titleColor='white', labelAngle=0)),
        y=alt.Y('Keuntungan (Juta Rp):Q', title='Keuntungan (Juta Rp)', axis=alt.Axis(labelColor='white', titleColor='white', gridColor='rgba(255,255,255,0.1)'))
    ).properties(
        background='transparent' # Kunci utama agar tembus pandang
    ).configure_view(
        strokeOpacity=0 # Menghilangkan garis kotak luar
    )

    # Menampilkan grafik dengan mematikan tema bawaan Streamlit
    st.altair_chart(chart, use_container_width=True, theme=None)

# Teks Kaki (Footer)
st.write("---")
st.markdown("<p style='text-align: center; color: #FFFFFF;'>Created by Dany-xSakiko | Simulator v1.1 - Personalization Update</p>", unsafe_allow_html=True)
