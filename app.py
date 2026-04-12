import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_loader import loader
from analyzer import analyzer
import io

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
    # ユーザー指示に基づき、トグルを特定のコンテナで識別できるようにする
    st.markdown('<div class="theme-toggle-container">', unsafe_allow_html=True)
    is_dark = st.toggle("🌙 ダークモードに切り替え", value=(st.session_state.theme == 'Dark'))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.session_state.theme = 'Dark' if is_dark else 'Light'
    
    st.markdown('<div class="sidebar-brand-area">', unsafe_allow_html=True)
    
    st.markdown('<div class="logo-wrapper">', unsafe_allow_html=True)
    try:
        st.image("Creator_Catalyst_Official_Logo.png", use_container_width=True)
    except:
        st.markdown('<div style="width:160px;height:160px;background:#333;border-radius:50%;margin:auto;">Logo</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h1 class="brand-title-main">Creator Catalyst</h1>', unsafe_allow_html=True)
    st.markdown('<p class="brand-subtitle-sub">CONTENT ANALYTICS<br>&<br>GROWTH AI</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("#### 🌍 戦略的分析コンテキスト")
    platform = st.selectbox(
        "A. コンテンツ形式 (Format)", 
        ["動画（YouTube/ニコニコ等）", "記事（note/ブログ/Zenn等）", "ライブ配信（Twitch等）", "素材販売（BOOTH/FANBOX等）", "スキル提供（ココナラ等）", "その他"],
        index=0
    )
    genre = st.selectbox(
        "B. ジャンル (Genre)",
        ["エンタメ", "音楽/BGM", "教育/解説", "ビジネス/教養", "創作（小説/イラスト）", "ゲーム実況", "日常/Vlog", "その他"],
        index=2
    )
    core_desire = st.selectbox(
        "C. ターゲットの欲求 (Core Desire)",
        ["生存・欲望（稼ぎたい等）", "承認・自己実現（賢くなりたい等）", "娯楽・逃避（癒やされたい等）", "愛・帰属（仲間が欲しい等）", "恐怖・回避（失敗したくない等）"],
        index=1
    )
    goal = st.selectbox(
        "D. 分析目的 (Goal)",
        ["認知拡大（バズ狙い）", "即時収益化（成約重視）", "資産構築（ストック性重視）"],
        index=2
    )
    
    st.divider()
    
    st.markdown("#### 📥 データ・インポーター")
    uploaded_file = st.file_uploader("各種解析CSVデータをアップロード", type=["csv"])
    
    st.divider()
    
    st.markdown("#### 🧠 クリエイター・インサイト")
    target_audience = st.text_input("1. ターゲット層", placeholder="例：20代の音楽制作に関心がある人")
    pain_points = st.text_area("2. 現在の悩み", placeholder="例：視聴維持率が2分で急落してしまう")
    success_manual = st.text_area("3. 成功パターン（任意）", placeholder="例：冒頭で結論を言うと伸びる傾向がある")
    
    st.divider()
    
    # 🧪 テストデータ生成ダッシュボード
    st.markdown("#### 🧪 開発・検証用ツール")
    if st.button("🧪 テストデータを生成", use_container_width=True):
        import datetime
        import random
        
        # ジャンル別シナリオの設定
        if "音楽" in genre:
            view_range = (200, 800)
            dur_range = (300, 600) # 5-10分
            ctr_range = (2, 5)
        elif "教育" in genre or "ビジネス" in genre:
            view_range = (1500, 4000)
            dur_range = (90, 240)  # 1.5-4分
            ctr_range = (8, 18)
        else:
            view_range = (500, 2000)
            dur_range = (120, 300)
            ctr_range = (4, 10)
            
        # 擬似データ生成（CSV文字列として作成し、loaderのクレンジングをテスト）
        csv_rows = ["日付,コンテンツ名,インプレッション,視聴回数（PV）,CTR(%),平均視聴時間"]
        for i in range(14):
            date_str = (datetime.date.today() - datetime.timedelta(days=14-i)).strftime("%Y-%m-%d")
            views = random.randint(*view_range)
            # カンマの罠
            views_str = f'"{views:,}"' if random.random() > 0.5 else str(views)
            ctr = random.uniform(*ctr_range)
            imps = int(views / (ctr/100))
            # 時間形式の罠
            secs = random.randint(*dur_range)
            dur_str = f"{secs//3600:01}:{ (secs%3600)//60:02}:{secs%60:02}"
            
            csv_rows.append(f"{date_str},コンテンツ_{i+1},{imps},{views_str},{ctr:.2f}%,{dur_str}")
        
        # 合計行の罠
        csv_rows.append("合計,サマリー,999999,99999,5.00%,0:10:00")
        
        st.session_state.test_data = "\n".join(csv_rows)
        st.toast("テストデータを生成しました。解析を開始します！", icon="🧪")

# --- Dynamic CSS Injection ---
placeholder_styles = f"""
    ::placeholder, textarea::placeholder, input::placeholder {{
        color: #888888 !important;
        opacity: 1 !important;
        -webkit-text-fill-color: #888888 !important;
    }}
"""

brand_styles = """
    .sidebar-brand-area {
        text-align: center; padding: 10px 0; width: 100%;
    }
    .logo-wrapper {
        display: block; margin-left: auto; margin-right: auto; width: 160px; margin-bottom: 15px;
    }
    .logo-wrapper img, .mascot-wrapper img {
        filter: drop-shadow(0 0 20px #007BFF) !important;
        mix-blend-mode: screen !important;
        background-color: transparent !important;
    }
    .brand-title-main {
        font-size: 2.2rem !important; font-weight: 900 !important; margin: 5px 0 !important;
        letter-spacing: -1px !important; text-align: center !important; text-transform: uppercase;
    }
    .brand-subtitle-sub {
        font-size: 0.7rem !important; font-weight: 600 !important; letter-spacing: 3px !important;
        line-height: 1.6 !important; margin-top: 5px !important; margin-bottom: 25px !important;
        text-transform: uppercase; opacity: 0.8 !important; text-align: center !important;
    }
    .main-title-gradient {
        background: linear-gradient(to right, #007BFF, #9370DB);
        -webkit-background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        color: transparent;
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 20px;
        line-height: 1.2;
        display: inline-block;
    }
"""

if st.session_state.theme == 'Dark':
    theme_css = f"""
    <style>
        {placeholder_styles}
        {brand_styles}
        /* 強制CSS適用：トータル・ブラックアウト */
        header[data-testid="stHeader"], .stApp, section[data-testid="stSidebar"] {{
            background-color: #0E1117 !important;
        }}
        /* サイドバー視認性修正 */
        section[data-testid="stSidebar"] {{
            background-color: #0E1117 !important;
            color: #FFFFFF !important;
            border-right: 1px solid #333333 !important;
        }}
        section[data-testid="stSidebar"] .stMarkdown, 
        section[data-testid="stSidebar"] label, 
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] p {{
            color: #FFFFFF !important;
        }}
        /* ファイルアップロード / 入力エリア */
        div[data-testid="stFileUploadDropzone"] {{
            background: #1E1E1E !important;
            color: #FFFFFF !important;
            border: 1px dashed #444 !important;
        }}
        div[data-baseweb="select"] > div, div[data-baseweb="base-input"], textarea, input {{
            background-color: #1E1E1E !important;
            color: #FFFFFF !important;
            border: 1px solid #444 !important;
        }}
        /* テキスト色強制 */
        label, p, span, h1, h2, h3, h4, h5, h6, .stMarkdown {{
            color: #FFFFFF !important;
        }}
        /* メトリクス表示の最適化 */
        [data-testid="stMetricLabel"] p {{
            color: #E0E0E0 !important;
            font-size: 1rem !important;
        }}
        .brand-title-main {{
            color: #FFFFFF !important;
        }}
        .brand-subtitle-sub {{
            color: #007BFF !important;
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
        {placeholder_styles}
        {brand_styles}
        /* ライトモードでもサイドバー視認性を確保 */
        .stApp, header, [data-testid="stHeader"] {{
            background-color: #FFFFFF !important;
        }}
        section[data-testid="stSidebar"] {{
            background-color: #F8FAFC !important;
            border-right: 1px solid #E2E8F0 !important;
        }}
        section[data-testid="stSidebar"] .stMarkdown, 
        section[data-testid="stSidebar"] label, 
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] p {{
            color: #31333F !important;
        }}
        h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {{
            color: #31333F !important;
        }}
        [data-testid="stMetricLabel"] p {{
            color: #666666 !important;
        }}
        div[data-baseweb="select"] > div, div[data-baseweb="base-input"], textarea, input {{
            background-color: #FFFFFF !important;
            color: #31333F !important;
            border: 1px solid #DDD !important;
        }}
        .brand-title-main {{
            color: #31333F !important;
        }}
        .brand-subtitle-sub {{
            color: #007BFF !important;
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
st.markdown('<h1 class="main-title-gradient">Creator Catalyst 🚀</h1>', unsafe_allow_html=True)
st.markdown("#### コンテンツ成長AIエンジン：CatScope")

# --- Analysis Flow ---
# アップロードまたはテストデータの有無を確認
target_input = uploaded_file if uploaded_file else (io.StringIO(st.session_state.test_data) if 'test_data' in st.session_state else None)

if target_input:
    try:
        load_result = loader.load_csv(target_input)
        df = load_result['data']
        has_date = load_result['has_date']
        
        analysis = analyzer.analyze_data(
            df, has_date=has_date, platform=platform, genre=genre,
            core_desire=core_desire, goal=goal,
            target_audience=target_audience, pain_points=pain_points, success_manual=success_manual
        )
        
        # テストデータ使用中の警告
        if not uploaded_file and 'test_data' in st.session_state:
            st.warning("⚠️ 現在、テスト用に生成された擬似データを使用しています。")
        
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
    # Empty State: 役割分担に基づき、マスコットがメッセージを表示
    st.info("👈 左側のサイドバーから分析対象のレポート(CSV)をアップロードしてください。")
    st.markdown("""
    ### 🐈‍⬛ Creative Catalyst Agent: Ready to Start
    
    Hi Creator! 私はあなたの専属エージェントです。
    サイドバーからデータをアップロードしていただければ、すぐに私の「解析エンジン」がフル回転して、あなただけの成長戦略を提案します。
    
    準備ができたら教えてくださいね！
    """)
    st.markdown('<div class="mascot-wrapper">', unsafe_allow_html=True)
    try:
        # 指示に従い、黒背景のあるアイコンを screen 合成で配置
        st.image("Creator Catalyst icon.png", width=240)
    except:
        st.image("Creator_Catalyst_icon_transparent.png", width=240)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Startup Message ---
if 'startup_msg_shown' not in st.session_state:
    st.toast("Creator Catalyst：戦略・市場分析エンジン起動。あなたのコンテンツを市場の『資産』へ変換します。", icon="🐈‍⬛")
    st.session_state.startup_msg_shown = True
