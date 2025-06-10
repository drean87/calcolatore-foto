import streamlit as st
from fractions import Fraction

st.set_page_config(page_title="Calcolatore Fotografico", layout="centered")
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Text&display=swap');

        body, .block-container {
            background-color: #1c1c1e;
            color: #f0f0f5;
            font-family: 'SF Pro Text', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
                         Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
            padding-top: 3rem;
        }
        .stSelectbox, .stNumberInput, .stTextInput, .stSlider {
            background-color: #2c2c2e !important;
            color: #f0f0f5 !important;
            border-radius: 12px;
            border: 1px solid #3a3a3c !important;
            padding: 0.3rem 0.6rem;
            font-size: 1rem;
            transition: border-color 0.3s ease;
        }
        .stSelectbox:hover, .stNumberInput:hover, .stTextInput:hover, .stSlider:hover {
            border-color: #0a84ff !important;
        }
        .stSelectbox > div[role="listbox"] {
            background-color: #2c2c2e !important;
            color: #f0f0f5 !important;
            border-radius: 12px;
        }
        .stMarkdown h1 {
            font-weight: 700;
            font-size: 3rem;
            letter-spacing: -0.03em;
            color: #f5f5f7;
            margin-bottom: 2rem;
            text-align: center;
        }
        .intervallo-container {
            text-align: center;
            margin-top: 1.5rem;
            user-select: none;
        }
        .intervallo-label {
            font-size: 1.8rem;   /* leggermente più piccolo */
            font-weight: 600;
            color: #ff9500; /* arancione Apple */
            letter-spacing: 0.04em;
            white-space: nowrap; /* non andare a capo */
            display: inline-block;
            margin-bottom: 0.3rem;
        }
        .intervallo-valori {
            color: white !important;
            font-weight: 700;
            font-family: 'SF Pro Text', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
                         Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
            font-size: 2.8rem;
            display: block;
        }
        label[data-baseweb="select"] > div:first-child {
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 0.3rem;
            color: #f5f5f7;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📷 Calcolatore Fotografico")

col1, col2 = st.columns(2)

with col1:
    ambiente = st.selectbox("Condizioni di luce 🌤️", ["-", "Interno 🏠", "Esterno - Alba 🌅", "Esterno - Giorno ☀️", "Esterno - Notte 🌙"])
    supporto = st.selectbox("Tipo di supporto 🦾", ["-", "Mano libera ✋", "Treppiedi 📷"])
    iso = st.selectbox("ISO 🎚️", ["-"] + [str(i) for i in [160, 200, 320, 400, 800, 1600]])

with col2:
    diaframma = st.selectbox("Diaframma (f) 🔆", ["-"] + ["f/2", "f/2.8", "f/4", "f/5.6", "f/8", "f/11", "f/16", "f/22"])

def semplifica(t):
    standard = [60, 30, 15, 8, 4, 2, 1, 1/2, 1/4, 1/8, 1/16, 1/32, 1/64, 1/125, 1/250, 1/500, 1/1000, 1/2000, 1/4000, 1/8000]
    return min(standard, key=lambda x: abs(x - t))

def formatta_tempo(t):
    if t >= 1:
        return f"{int(t)}\""
    else:
        f = Fraction(t).limit_denominator()
        return f"{f.numerator}/{f.denominator} s"

def calcola_intervallo(ambiente, supporto, iso, diaframma):
    try:
        if iso == "-" or diaframma == "-" or ambiente == "-" or supporto == "-":
            return None, None

        iso_val = int(iso)
        diaf_val = float(diaframma.replace("f/", ""))

        if ambiente == "Interno 🏠" and supporto == "Treppiedi 📷":
            if 160 <= iso_val <= 400 and 5.6 <= diaf_val <= 8:
                return 5, 30
            else:
                return 2, 20
        elif ambiente == "Interno 🏠" and supporto == "Mano libera ✋":
            return 1/15, 1/4
        elif ambiente == "Esterno - Alba 🌅":
            if supporto == "Treppiedi 📷" and diaf_val == 8 and 160 <= iso_val <= 400:
                return 1/10, 1/60
            elif supporto == "Mano libera ✋":
                return 1/125, 1/250
        elif ambiente == "Esterno - Giorno ☀️":
            if supporto == "Treppiedi 📷":
                return 1/60, 1/125
            elif supporto == "Mano libera ✋":
                return 1/125, 1/500
        elif ambiente == "Esterno - Notte 🌙":
            if supporto == "Treppiedi 📷":
                if iso_val <= 160:
                    return 5, 30
                elif iso_val == 320:
                    return 3, 20
            else:
                return 1/2, 2
        return 1/125, 1/500

    except Exception as e:
        return None, None

t1, t2 = calcola_intervallo(ambiente, supporto, iso, diaframma)

if t1 is not None and t2 is not None:
    t1_s = semplifica(t1)
    t2_s = semplifica(t2)
    st.markdown(f"""
        <div class='intervallo-container'>
            <span class='intervallo-label'>⏳ Intervallo tempo di esposizione consigliato:</span><br>
            <span class='intervallo-valori'>{formatta_tempo(t1_s)} – {formatta_tempo(t2_s)}</span>
        </div>
    """, unsafe_allow_html=True)
else:
    st.info("Seleziona almeno 4 parametri validi per il calcolo.")
