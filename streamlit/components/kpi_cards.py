import streamlit as st

def render_kpis(kpis):
    col1, col2, col3, col4 = st.columns(4)
    for i, (key, value) in enumerate(kpis.items()):
        col = [col1, col2, col3, col4][i]
        col.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 15px;
            padding: 20px;
            color: white;
            text-align:center;
            font-size:20px;
            transition: all 0.3s ease;
        '>
            <strong>{key}</strong><br>{value}
        </div>
        """, unsafe_allow_html=True)
