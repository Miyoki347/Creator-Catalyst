import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_loader import loader
from analyzer import analyzer

# --- Page Config ---
st.set_page_config(
    page_title="Creator Catalyst",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Theme Management ---
if 'theme' not in st.session_state:
    st.session_state.theme = 'Light'

# --- Sidebar: Universal & Theme Workflow ---
with st.sidebar:
    is_dark = st.toggle("🌙 ダークモードに切り替え", value=(st.session_state.theme == 'Dark'))
    st.session_state.theme = 'Dark' if is_dark else 'Light'
    
    # 1. ブランド & マスコット (背景透過版を採用)
    st.markdown('<div class="mascot-container">', unsafe_allow_html=True)
    try:
        # 以前の Creator Catalyst icon.png (背景黒) から 透過済み PNG へ変更
        st.image("Creator_Catalyst_icon_transparent.png", width=140)
    except:
        st.markdown('<div style="width:140px;height:140px;background:#333;border-radius:50%;display:flex;align-items:center;justify-content:center;">Icon</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="brand-title">Creator Catalyst</h2>', unsafe_allow_html=True)
    st.markdown('<p class="brand-subtitle">CONTENT ANALYTICS & GROWTH AI</p>', unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("#### 🌍 媒体・ジャンル設定")
    platform = st.selectbox(
        "分析対象の媒体 (Platform)", 
        ["YouTube", "note", "X(Twitter)", "ブログ/Webメディア", "その他"],
        index=0
    )
    genre = st.selectbox(
        "コンテンツの系統 (Genre)",
        ["音楽/アート", "教育/解説", "エンタメ/ゲーム", "ビジネス/教養", "日常/Vlog", "創作小説/エッセイ", "その他"],
        index=0
    )
    
    st.divider()
    
    st.markdown("#### 📥 データ・インポーター")
    uploaded_file = st.file_uploader("各種解析CSVデータをアップロード", type=["csv"])
    
    st.divider()
    
    st.markdown("#### 🧠 クリエイター・インサイト設定")
    target_audience = st.text_input("1. ターゲット層（誰に届けたいか）", placeholder="例：20代の音楽制作に関心がある人")
    pain_points = st.text_area("2. 現在の悩み（具体的に）", placeholder="例：視聴維持率が2分で急落してしまう")
    success_manual = st.text_area("3. 成功体験・勝ちパターン（任意）", placeholder="例：冒頭で結論を言うと伸びる傾向がある")

# --- Dynamic CSS Injection ---
placeholder_css = """
    ::placeholder, textarea::placeholder, input::placeholder {
        color: #888888 !important;
        opacity: 1 !important;
        -webkit-text-fill-color: #888888 !important;
    }
"""

mascot_css = """
    .mascot-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
        background-color: transparent !important;
    }
    .mascot-container img {
        background-color: transparent !important;
        /* 背景透過 PNG のため mix-blend-mode: screen は不要 */
        filter: drop-shadow(0 0 12px #007BFF) !important;
        border-radius: 50% !important;
        padding: 5px;
    }
"""

if st.session_state.theme == 'Dark':
    theme_css = f"""
    <style>
        {placeholder_css}
        {mascot_css}
        header, [data-testid="stHeader"], [data-testid="stSidebar"], .stApp, [data-testid="stSidebar"] > div {{
            background-color: #0E1117 !important;
        }}
        [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, .stMarkdown, h1, h2, h3, h4, h5, h6, p, label {{
            color: #FFFFFF !important;
        }}
        div[data-baseweb="select"] > div, div[data-baseweb="base-input"], textarea, input {{
            background-color: #1E1E1E !important;
            color: #FFFFFF !important;
            border: 1px solid #444 !important;
        }}
        .brand-title {{
            text-align: center; font-weight: 900; color: #FFFFFF !important;
        }}
        .brand-subtitle {{
            text-align: center; color: #007BFF !important; font-size: 0.85rem; letter-spacing: 1px;
        }}
        .action-card {{
            background: linear-gradient(135deg, #1e293b, #0f172a);
            padding: 25px; border-radius: 15px; border: 1px solid #334155; margin: 15px 0;
            box-shadow: 0 6px 20px rgba(0,0,0,0.6);
        }}
    </style>
    """
else:
    theme_css = f"""
    <style>
        {placeholder_css}
        {mascot_css}
        .stApp, header, [data-testid="stHeader"], [data-testid="stSidebar"], [data-testid="stSidebar"] > div {{
            background-color: #FFFFFF !important;
        }}
        h1, h2, h3, h4, h5, h6, p, label, span, .stMarkdown, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {{
            color: #31333F !important;
        }}
        [data-testid="stFileUploader"] label p {{
            color: #31333F !important;
            font-weight: bold !important;
        }}
        div[data-baseweb="select"] > div, div[data-baseweb="base-input"], textarea, input {{
            background-color: #F0F2F6 !important;
            color: #31333F !important;
            border: 1px solid #DDD !important;
        }}
        .brand-title {{
            text-align: center; font-weight: 900; color: #31333F !important;
        }}
        .brand-subtitle {{
            text-align: center; color: #007BFF !important; font-size: 0.85rem; letter-spacing: 1px;
        }}
        .action-card {{
            background: #F8FAFC;
            padding: 25px; border-radius: 15px; border: 1px solid #E2E8F0; margin: 15px 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }}
    </style>
    """

st.markdown(theme_css, unsafe_allow_html=True)

# --- Main Page Content ---
main_title_color = "#007BFF" if st.session_state.theme == 'Dark' else "#31333F"
st.markdown(f'<h1 style="background: -webkit-linear-gradient({main_title_color}, #9370DB); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3.5rem; font-weight: 900; margin-bottom: 0;">Creator Catalyst 🚀</h1>', unsafe_allow_html=True)
st.markdown("### Creator Catalystへようこそ。")
st.markdown("#### データという触媒を用いて、あなたのコンテンツを次のステージへ加速させます。")

if uploaded_file:
    try:
        load_result = loader.load_csv(uploaded_file)
        df = load_result['data']
        has_date = load_result['has_date']
        
        analysis = analyzer.analyze_data(
            df, has_date=has_date, platform=platform, genre=genre,
            target_audience=target_audience, pain_points=pain_points, success_manual=success_manual
        )
        
        st.subheader(f"📊 {platform} × {genre} 分析レポート")
        col1, col2, col3, col4 = st.columns(4)
        m = analysis['summary_metrics']
        mon = analysis['monetization']
        
        if has_date:
            col1.metric("最新の数値", f"{int(m['latest_value']):,}", f"{m['wow_growth']:.1f}% WoW")
            col2.metric("週間平均", f"{int(m['avg_value']):,}")
            col3.metric("📈 成長の特異点", f"{len(analysis['spikes'])}回")
        else:
            col1.metric("累計の数値", f"{int(m['total_value']):,}")
            col2.metric("コンテンツ平均", f"{int(m['avg_value']):,}")
            col3.metric("解析件数", f"{len(df)}件")
            
        col4.metric("💰 成長性スコア", f"{mon['score']}/100", mon['status'])

        st.divider()

        chart_color = "#007BFF" if st.session_state.theme == 'Dark' else "#636EFA"
        if has_date:
            st.subheader("📈 トレンド・インパクト分析")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['date'], y=df['metric_value'], mode='lines', line=dict(color=chart_color, width=4), fill='tozeroy'
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                font_color="#FFF" if st.session_state.theme == 'Dark' else "#333",
                xaxis=dict(showgrid=False, range=[df['date'].min(), df['date'].max()]),
                yaxis=dict(showgrid=True, gridcolor='#333333' if st.session_state.theme == 'Dark' else '#EEE', range=[0, df['metric_value'].max() * 1.2]),
                margin=dict(l=0,r=0,t=0,b=0), height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.subheader("📈 コンテンツ別貢献度")
            if analysis['top_content']:
                top_df = pd.DataFrame(analysis['top_content'].items(), columns=['Item', 'Value'])
                fig = px.bar(top_df, x='Value', y='Item', orientation='h', color_discrete_sequence=[chart_color])
                bw = 0.4 if len(top_df) <= 1 else 0.7
                fig.update_traces(width=bw)
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                    font_color="#FFF" if st.session_state.theme == 'Dark' else "#333",
                    xaxis=dict(showgrid=True, gridcolor='#333333' if st.session_state.theme == 'Dark' else '#EEE', range=[0, top_df['Value'].max() * 1.2]),
                    margin=dict(l=0,r=20,t=30,b=0), height=400
                )
                st.plotly_chart(fig, use_container_width=True)

        st.divider()

        st.subheader("💡 Creatorへの超具体的アクション提案")
        text_color = "#FFFFFF" if st.session_state.theme == 'Dark' else "#31333F"
        for i, action in enumerate(analysis['actions']):
            with st.container():
                st.markdown(f"""
                <div class="action-card">
                    <h3 style="color: #007BFF !important; margin-bottom: 15px;">STRATEGY {i+1}: {action['title']}</h3>
                    <div style="margin-bottom: 12px;">
                        <span style="color: #FF8C00; font-weight: bold;">【現状分析】</span><br>
                        <p style="font-size: 1.05rem; line-height: 1.6; color: {text_color} !important;">{action['analysis']}</p>
                    </div>
                    <div style="margin-bottom: 12px;">
                        <span style="color: #00FF7F; font-weight: bold;">【具体的改善案】</span><br>
                        <p style="font-size: 1.15rem; line-height: 1.7; color: {text_color} !important;">{action['action']}</p>
                    </div>
                    <div>
                        <span style="color: #9370DB; font-weight: bold;">【期待効果】</span><br>
                        <p style="font-size: 1.05rem; font-style: italic; color: {text_color} !important;">{action['impact']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with st.expander("詳細なデータログ (Professional Data Log)"):
            st.write(df)

    except Exception as e:
        st.error(f"解析中にエラーが発生しました: {str(e)}")
else:
    st.info("👈 左側のサイドバーから分析対象のレポート(CSV)をアップロードしてください。")
    st.markdown("""
    ### 🐈‍⬛ Creative Catalyst Engine: Professional Edition
    
    あらゆる媒体・ジャンルのデータを瞬時に解析し、成長のための「触媒」となる具体的アクションを提案します。
    """)
