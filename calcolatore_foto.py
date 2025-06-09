import streamlit as st

def consigli_fotografia(iso, tempo_s, diaframma, mano_libera, giorno, interno):
    consigli = []
    soglia_tempo_mano = 1/60
    iso_basso = 160
    iso_medio = 800
    iso_alto = 3200
    diaframma_aperto = 2.8
    diaframma_chiuso = 16
    
    if giorno:
        if iso > iso_medio:
            consigli.append(f"ISO {iso} alto per luce diurna, prova a ridurlo per miglior qualità.")
        elif iso < iso_basso:
            consigli.append(f"ISO {iso} molto basso, ottimo per qualità se c'è abbastanza luce.")
    else:
        if iso < iso_medio:
            consigli.append(f"ISO {iso} basso per scatti notturni, potresti ottenere foto sottoesposte.")
        elif iso > iso_alto:
            consigli.append(f"ISO {iso} molto alto, attenzione al rumore nelle foto.")
    
    if mano_libera:
        if tempo_s > soglia_tempo_mano:
            consigli.append(f"Tempo {tempo_s:.3f}s troppo lungo per mano libera, usa treppiede o aumenta ISO.")
    else:
        if tempo_s > 30:
            consigli.append("Tempo di esposizione molto lungo (>30s), considera modalità bulb o scatto remoto.")
    
    if diaframma < diaframma_aperto:
        consigli.append(f"Diaframma {diaframma} molto aperto, profondità di campo ridotta.")
    elif diaframma > diaframma_chiuso:
        consigli.append(f"Diaframma {diaframma} molto chiuso, potrebbe causare diffrazione e perdita di nitidezza.")
    
    if interno and giorno and iso < 400:
        consigli.append("Interno di giorno, ISO basso va bene se luce forte, altrimenti aumenta ISO.")
    if interno and not giorno and iso < 800:
        consigli.append("Interno di notte, ISO probabilmente troppo basso per luce scarsa.")
    if not interno:
        if giorno and iso > iso_medio:
            consigli.append("Esterno di giorno con ISO alto, prova a ridurre per migliore qualità.")
        if not giorno and iso < iso_medio:
            consigli.append("Esterno di notte con ISO basso, potresti avere scatti scuri.")
    
    if mano_libera and tempo_s > soglia_tempo_mano:
        consigli.append("Consiglio: usa stabilizzazione o treppiede per tempi lunghi.")
    if not mano_libera and tempo_s > 1:
        consigli.append("Con treppiede puoi usare tempi lunghi, usa scatto remoto o autoscatto per evitare vibrazioni.")
    
    if len(consigli) == 0:
        consigli.append("Impostazioni corrette per le condizioni date.")
    
    return consigli

st.title("Calcolatore esposizione fotografia")

iso = st.number_input("Inserisci ISO", min_value=50, max_value=51200, value=160, step=50)
tempo_s = st.number_input("Inserisci tempo esposizione (in secondi)", min_value=0.0001, max_value=120.0, value=0.01, format="%.4f")
diaframma = st.number_input("Inserisci diaframma (f/)", min_value=1.0, max_value=22.0, value=5.6, step=0.1)

mano_libera = st.checkbox("Scatto a mano libera", value=True)
giorno = st.checkbox("Scatto di giorno", value=True)
interno = st.checkbox("Scatto all'interno", value=False)

if st.button("Calcola consigli"):
    risultati = consigli_fotografia(iso, tempo_s, diaframma, mano_libera, giorno, interno)
    st.subheader("Consigli per il tuo scatto:")
    for r in risultati:
        st.write("- " + r)
