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

# --- Custom Styling ---
st.markdown("""
<style>
    /* 全体背景とヘッダーを黒に固定 */
    .stApp, header[data-testid="stHeader"] {
        background-color: #0E1117 !important;
    }
    /* サイドバーの背景を濃い黒に固定 */
    section[data-testid="stSidebar"] {
        background-color: #0E1117 !important;
        border-right: 1px solid #333 !important;
    }
    /* サイドバー内の文字、ラベルを全て白に強制 */
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p {
        color: #FFFFFF !important;
    }
    /* ファイルアップロード部分の背景を暗くし、文字をはっきりさせる */
    [data-testid="stFileUploadDropzone"] {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
        border: 1px dashed #444 !important;
    }
    /* アップローダー内のボタンとテキストの可読性向上 */
    [data-testid="stFileUploader"] button {
        background-color: #333333 !important;
        color: #FFFFFF !important;
        border: 1px solid #555 !important;
    }
    [data-testid="stFileUploader"] button p {
        color: #FFFFFF !important;
        font-weight: 900 !important;
        -webkit-text-stroke: 0.5px #000; /* 縁取りでさらに強調 */
    }
    [data-testid="stFileUploader"] small {
        color: #E0E0E0 !important;
    }
    /* メトリクスのラベル（グレーの文字）を明るく */
    [data-testid="stMetricLabel"] p {
        color: #E0E0E0 !important;
    }
    /* UI全般の文字色を白に */
    h1, h2, h3, h4, h5, h6, p, label, span {
        color: #FFFFFF !important;
    }
    .metric-card {
        background-color: #1a1c22;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #333333;
        box-shadow: 0 4px 15px rgba(0,0,0,0.6);
        margin-bottom: 25px;
    }
    .action-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #334155;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        transition: 0.3s;
    }
    .action-card:hover {
        border-color: #FF8C00;
        transform: translateY(-5px);
    }
    .catalyst-title {
        background: -webkit-linear-gradient(#FF8C00, #9370DB);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 3.5rem;
        margin-bottom: 10px;
    }
    /* st.metric の視認性強化 */
    [data-testid="stMetric"] {
        background-color: #1a1c22 !important;
        border: 1px solid #444444 !important;
        border-radius: 15px;
        padding: 20px !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
    }
    .welcome-box {
        background-color: #1E3A5F !important;
        color: #FFFFFF !important;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #FF8C00;
        margin-bottom: 20px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown('<h1 style="text-align: center; color: #FFFFFF !important; margin-bottom: 0px;">Creator Catalyst</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #E0E0E0 !important;">分析エンジン: CatScope</p>', unsafe_allow_html=True)
    
    st.divider()
    
    with st.container():
        st.markdown("#### 📥 分析データの同期")
        uploaded_file = st.file_uploader("CSVファイルを選択", type=["csv"])
    
    st.divider()
    
    with st.container():
        st.markdown("#### 🧠 AI戦略オプション")
        target_audience = st.text_input("入力1：ターゲット", placeholder="例：20代の音楽好き、読者")
        pain_points = st.text_input("入力2：現在の悩み", placeholder="例：離脱が早い、登録者が増えない")

    st.divider()
    st.markdown("#### 🤔 使い方")
    st.markdown("1. データを読み込む\n2. AI戦略オプションを入力\n3. 戦略アクションを実行する")

# --- Main Dashboard ---
st.markdown('<h1 class="catalyst-title">Creator Catalyst 🚀</h1>', unsafe_allow_html=True)
st.markdown("#### コンテンツ成長AIエンジン（CatScope Engine）")

# 歓迎メッセージ
st.markdown('<div class="welcome-box">クリエイティブの分析ルームへようこそ。あなたのデータを成長の触媒に変えましょう。</div>', unsafe_allow_html=True)

if uploaded_file:
    try:
        load_result = loader.load_csv(uploaded_file)
        df = load_result['data']
        has_date = load_result['has_date']
        
        # 分析実行 (ターゲットと悩みを渡す)
        analysis = analyzer.analyze_data(
            df, 
            has_date=has_date, 
            target_audience=target_audience, 
            pain_points=pain_points
        )
        
        # 1. 概要指標（主要メトリクス）
        st.subheader("📊 主要メトリクス（コンテンツ健康診断）")
        col1, col2, col3, col4 = st.columns(4)
        
        metrics = analysis['summary_metrics']
        monetization = analysis['monetization']
        
        if has_date:
            col1.metric("最新の数値", f"{int(metrics['latest_value']):,}", f"{metrics['wow_growth']:.1f}% 前週比", delta_color="normal")
            col2.metric("週間平均", f"{int(metrics['avg_value']):,}")
            col3.metric("急上昇（スパイク）", f"{len(analysis['spikes'])}回")
        else:
            col1.metric("累計の数値", f"{int(metrics['total_value']):,}")
            col2.metric("コンテンツ平均", f"{int(metrics['avg_per_content']):,}")
            col3.metric("対象アイテム数", f"{metrics['content_count']}件")
            
        col4.metric("収益化ポテンシャル", f"{monetization['score']}/100", monetization['status'])

        st.divider()

        # 2. メイングラフ
        if has_date:
            st.subheader("📈 成長の軌跡（トレンド分析）")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['date'], y=df['metric'], mode='lines', name='成長曲線',
                line=dict(color='#FF8C00', width=4), fill='tozeroy', fillcolor='rgba(255, 140, 0, 0.1)'
            ))
            
            # スパイクのプロット
            if analysis['spikes']:
                spike_dates = [s['date'] for s in analysis['spikes']]
                spike_values = [s['value'] for s in analysis['spikes']]
                fig.add_trace(go.Scatter(
                    x=spike_dates, y=spike_values, mode='markers', name='バズった瞬間',
                    marker=dict(color='#FF007F', size=15, symbol='star', line=dict(width=2, color='white'))
                ))
                
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#FFFFFF',
                xaxis=dict(showgrid=False, title="日付"), yaxis=dict(showgrid=True, gridcolor='#333333', title="数値"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), margin=dict(l=0, r=0, t=30, b=0), height=450
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.subheader("📊 コンテンツ寄与度")
            if analysis['top_content']:
                top_df = pd.DataFrame(analysis['top_content'].items(), columns=['コンテンツ', '数値'])
                fig = px.bar(top_df, x='数値', y='コンテンツ', orientation='h', color_discrete_sequence=['#FF8C00'])
                # バーが一本の時に太くなりすぎないよう調整
                bar_width = 0.4 if len(top_df) <= 1 else 0.7
                fig.update_traces(width=bar_width, marker_line_color='black', marker_line_width=1)
                
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#FFFFFF',
                    xaxis=dict(showgrid=True, gridcolor='#333333', title="累積数値", 
                               range=[0, top_df['数値'].max() * 1.2]), # 右側に余白
                    yaxis=dict(showgrid=False, title=""),
                    margin=dict(l=0, r=20, t=30, b=0), height=400
                )
                st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # 3. 戦略セクション
        st.subheader("💡 明日からできる「超具体的」指示アクション")
        for i, action in enumerate(analysis['actions']):
            st.markdown(f"""
            <div class="action-card">
                <h3 style="color: #FF8C00 !important; margin-bottom: 10px;">指示 {i+1}: {action['title']}</h3>
                <p style="font-size: 1.1rem; line-height: 1.6; color: #FFFFFF !important;">{action['detail']}</p>
            </div>
            """, unsafe_allow_html=True)

        # 4. 詳細ログ
        with st.expander("詳細なデータログ（生データ）"):
            st.write(df)

    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
else:
    # ウェルカム画面
    st.info("👈 サイドバーから分析対象のCSVをアップロードしてください。")
    st.markdown("""
    ### 🐈‍⬛ CatScope Engine
    
    各種プラットフォームのレポートをアップロードするだけで、AIがあなたの成長要因を特定し、超具体的なアクションプランを提案します。
    
    #### 🚀 特徴
    - **ターゲット別最適化**: あなたのターゲット層に合わせた具体的なアドバイス。
    - **スパイク保持力分析**: 統計的に有意な「バズ」を逃さない。
    - **徹底したブラックアウトUI**: 分析に集中できる高コントラスト、プレミアムデザイン。
    """)
