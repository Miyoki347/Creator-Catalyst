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

# --- Professional Edition CSS Execution ---
st.markdown("""
<style>
    /* 1. 全体とサイドバーの漆黒固定 (Regression-Free) */
    header, [data-testid="stHeader"], [data-testid="stSidebar"], .stApp, [data-testid="stSidebar"] > div {
        background-color: #0E1117 !important;
    }
    
    /* 2. 視認性の徹底改善（プレースホルダーの白文字化） */
    ::placeholder, textarea::placeholder, input::placeholder {
        color: rgba(255, 255, 255, 0.9) !important;
        opacity: 1 !important;
        -webkit-text-fill-color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* 3. テキスト、ラベル、スパンの白化 */
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, .stMarkdown, h1, h2, h3, h4, h5, h6, p, label {
        color: #FFFFFF !important;
    }

    /* 4. 入力エリアの背景色を深くし、白文字を際立たせる */
    div[data-baseweb="select"] > div, div[data-baseweb="base-input"], textarea, input {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
        border: 1px solid #444 !important;
        border-radius: 8px !important;
    }
    
    /* 5. マスコット画像の完全透過・浮遊エフェクト */
    .mascot-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .mascot-container img {
        background-color: transparent !important;
        mix-blend-mode: screen !important; /* 黒背景部分を透過させる */
        filter: drop-shadow(0 0 15px #007BFF) !important; /* 青い光彩を纏わせる */
        border-radius: 50% !important;
        padding: 5px;
    }

    /* 6. プレミアムデザインのUIカード */
    [data-testid="stMetric"] {
        background-color: #1a1c22 !important;
        border: 1px solid #333 !important;
        border-radius: 12px;
        padding: 15px !important;
    }
    .action-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #334155;
        margin: 15px 0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.6);
        transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .action-card:hover { 
        border-color: #007BFF; 
        transform: translateY(-8px);
        box-shadow: 0 10px 30px rgba(0, 123, 255, 0.2);
    }

    /* 7. CSVアップローダーの視認性復元 */
    [data-testid="stFileUploadDropzone"] {
        background-color: #F0F2F6 !important;
        color: #000 !important;
        border: 2px dashed #007BFF !important;
    }
    [data-testid="stFileUploader"] p, [data-testid="stFileUploader"] span, [data-testid="stFileUploader"] label {
        color: #000 !important;
        font-weight: 700 !important;
    }

    .brand-title {
        text-align: center; font-weight: 900; color: #FFFFFF !important; margin-top: 0;
    }
    .brand-subtitle {
        text-align: center; color: #007BFF !important; font-size: 0.85rem; letter-spacing: 1px; margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar: Universal & Professional Edition Workflow ---
with st.sidebar:
    # 1. ブランド & マスコットの完全統合
    st.markdown('<div class="mascot-container">', unsafe_allow_html=True)
    try:
        # mix-blend-mode: screen を前提として読み込み
        st.image("Creator Catalyst icon.png", width=160)
    except:
        st.markdown('<div style="width:160px;height:160px;background:#333;border-radius:50%;display:flex;align-items:center;justify-content:center;">Icon</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="brand-title">Creator Catalyst</h2>', unsafe_allow_html=True)
    st.markdown('<p class="brand-subtitle">CONTENT ANALYTICS & GROWTH AI</p>', unsafe_allow_html=True)
    
    st.divider()
    
    # 2. 媒体 & 系統選択
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
    
    # 3. インポーター
    st.markdown("#### 📥 データ・インポーター")
    uploaded_file = st.file_uploader("各種解析CSVデータをアップロード", type=["csv"])
    
    st.divider()
    
    # 4. パーソナライズ・インサイト
    st.markdown("#### 🧠 クリエイター・インサイト設定")
    target_audience = st.text_input("1. ターゲット層（誰に届けたいか）", placeholder="例：20代の音楽制作に関心がある人")
    pain_points = st.text_area("2. 現在の悩み（具体的に）", placeholder="例：視聴維持率が2分で急落してしまう")
    success_manual = st.text_area("3. 成功体験・勝ちパターン（任意）", placeholder="例：冒頭で結論を言うと伸びる傾向がある")

# --- Main Page Content ---
st.markdown('<h1 style="background: -webkit-linear-gradient(#007BFF, #9370DB); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3.5rem; font-weight: 900; margin-bottom: 0;">Creator Catalyst 🚀</h1>', unsafe_allow_html=True)
st.markdown("### Creator Catalystへようこそ。")
st.markdown("#### データという触媒を用いて、あなたのコンテンツを次のステージへ加速させます。")

if uploaded_file:
    try:
        load_result = loader.load_csv(uploaded_file)
        df = load_result['data']
        has_date = load_result['has_date']
        
        # 汎用解析エンジン (Professional Edition 3-Step Action)
        analysis = analyzer.analyze_data(
            df, has_date=has_date, platform=platform, genre=genre,
            target_audience=target_audience, pain_points=pain_points, success_manual=success_manual
        )
        
        # 1. 統合メトリクス表示
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

        # 2. 視覚化セクション
        if has_date:
            st.subheader("📈 トレンド・インパクト分析")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['date'], y=df['metric_value'], mode='lines', line=dict(color='#007BFF', width=4), fill='tozeroy'
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#FFF',
                xaxis=dict(showgrid=False, range=[df['date'].min(), df['date'].max()]),
                yaxis=dict(showgrid=True, gridcolor='#333333', range=[0, df['metric_value'].max() * 1.2]),
                margin=dict(l=0,r=0,t=0,b=0), height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.subheader("📈 コンテンツ別貢献度")
            if analysis['top_content']:
                top_df = pd.DataFrame(analysis['top_content'].items(), columns=['Item', 'Value'])
                fig = px.bar(top_df, x='Value', y='Item', orientation='h', color_discrete_sequence=['#007BFF'])
                bw = 0.4 if len(top_df) <= 1 else 0.7
                fig.update_traces(width=bw)
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#FFF', 
                    xaxis=dict(showgrid=True, gridcolor='#333333', range=[0, top_df['Value'].max() * 1.2]),
                    margin=dict(l=0,r=20,t=30,b=0), height=400
                )
                st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # 3. 具体的アクション (3構成プロンプト出力)
        st.subheader("💡 Creatorへの超具体的アクション提案")
        for i, action in enumerate(analysis['actions']):
            with st.container():
                st.markdown(f"""
                <div class="action-card">
                    <h3 style="color: #007BFF !important; margin-bottom: 15px;">STRATEGY {i+1}: {action['title']}</h3>
                    <div style="margin-bottom: 12px;">
                        <span style="color: #FF8C00; font-weight: bold;">【現状分析】</span><br>
                        <p style="font-size: 1.05rem; line-height: 1.6; color: #FFFFFF !important;">{action['analysis']}</p>
                    </div>
                    <div style="margin-bottom: 12px;">
                        <span style="color: #00FF7F; font-weight: bold;">【具体的改善案】</span><br>
                        <p style="font-size: 1.15rem; line-height: 1.7; color: #FFFFFF !important;">{action['action']}</p>
                    </div>
                    <div>
                        <span style="color: #9370DB; font-weight: bold;">【期待効果】</span><br>
                        <p style="font-size: 1.05rem; font-style: italic; color: #FFFFFF !important;">{action['impact']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # 4. ローデータ・エクスパウダー
        with st.expander("詳細なデータログ (Professional Data Log)"):
            st.write(df)

    except Exception as e:
        st.error(f"解析中にエラーが発生しました: {str(e)}")
else:
    st.info("👈 左側のサイドバーから分析対象のレポート(CSV)をアップロードしてください。")
    st.markdown("""
    ### 🐈‍⬛ Creative Catalyst Engine: Professional Edition
    
    あらゆる媒体・ジャンルのデータを瞬時に解析し、成長のための「触媒」となる具体的アクションを提案します。
    
    #### 🚀 ワークフロー
    1. **媒体とジャンル**を選択。
    2. **解析レポート(CSV)**をアップロード。
    3. **ターゲット・悩み**を入力し、AIによる具体的戦略を受け取る。
    """)
