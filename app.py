import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_loader import loader
from analyzer import analyzer
import io

# --- Page Config ---
st.set_page_config(
    page_title="Creator-Catalyst | Growth AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling ---
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    .metric-card {
        background-color: #1a1c24;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #7f00ff;
        margin-bottom: 20px;
    }
    .action-card {
        background: linear-gradient(135deg, #1f2937, #111827);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #374151;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        transition: 0.3s;
    }
    .action-card:hover {
        border-color: #7f00ff;
        transform: translateY(-5px);
    }
    .catalyst-title {
        background: -webkit-linear-gradient(#00d2ff, #7f00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0px;
    }
    .stMetric {
        background-color: #1a1c24;
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/nolan/128/lightning-bolt.png", width=80)
    st.markdown("### Creator-Catalyst")
    st.markdown("クリエイターの成長を加速させる『触媒』")
    
    st.divider()
    
    uploaded_file = st.file_uploader("YouTube/noteのCSVをアップロード", type=["csv"])
    
    if uploaded_file:
        st.success("ファイルを受理しました。分析を開始します。")
    else:
        st.info("YouTubeアナリティクス、またはnoteのアクセス状況CSVファイルをアップロードしてください。")
        
    st.divider()
    st.markdown("#### 使い方")
    st.markdown("1. CSVを保存してアップロード\n2. 成長要因を自動特定\n3. 戦略アクションを実行")

# --- Main Dashboard ---
st.markdown('<h1 class="catalyst-title">Creator-Catalyst 🚀</h1>', unsafe_allow_html=True)
st.markdown("#### Growth Intelligence Engine")

if uploaded_file:
    # データ読み込みと分析
    try:
        df = loader.load_csv(uploaded_file)
        analysis = analyzer.analyze_data(df)
        
        # 1. 概要メトリクス
        st.subheader("📊 Performance Overview")
        col1, col2, col3 = st.columns(3)
        
        metrics = analysis['summary_metrics']
        col1.metric("最新の数値", f"{int(metrics['latest_value']):,}", f"{metrics['wow_growth']:.1f}% WoW", delta_color="normal")
        col2.metric("週間平均", f"{int(metrics['avg_value']):,}", "安定度: 高" if metrics['avg_value'] > 0 else "データ不足")
        col3.metric("検知されたスパイク", f"{len(analysis['spikes'])}回", "成長の特異点")

        st.divider()

        # 2. メイングラフ
        st.subheader("📈 Growth Singularity Chart")
        
        fig = go.Figure()
        
        # メインデータライン
        fig.add_trace(go.Scatter(
            x=df['date'], y=df['metric'],
            mode='lines+markers',
            name='Daily Metrics',
            line=dict(color='#00d2ff', width=3),
            fill='tozeroy',
            fillcolor='rgba(0, 210, 255, 0.1)'
        ))
        
        # スパイクのハイライト
        if analysis['spikes']:
            spike_dates = [s['date'] for s in analysis['spikes']]
            spike_values = [s['value'] for s in analysis['spikes']]
            fig.add_trace(go.Scatter(
                x=spike_dates, y=spike_values,
                mode='markers',
                name='Spike Detected',
                marker=dict(color='#ff007f', size=15, symbol='star', line=dict(width=2, color='white'))
            ))
            
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e0e0e0',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#374151'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=30, b=0),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # 3. 戦略セクション
        st.subheader("💡 Strategic Actions (Next 3 Steps)")
        st.markdown("_あなたのデータから導き出された、即時実行可能な成長アクションです。_")
        
        for i, action in enumerate(analysis['actions']):
            st.markdown(f"""
            <div class="action-card">
                <h3 style="color: #7f00ff; margin-bottom: 10px;">ACTION {i+1}: {action['title']}</h3>
                <p style="font-size: 1.1rem; line-height: 1.6;">{action['detail']}</p>
            </div>
            """, unsafe_allow_html=True)

        # 4. 詳細ログ / エクスプローラ
        with st.expander("詳細データ・分析ログを表示"):
            st.write(df)
            if analysis['top_content']:
                st.write("### コンテンツ別寄与度")
                st.bar_chart(pd.Series(analysis['top_content']))

    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
else:
    # ウェルカム画面 / デモ表示
    st.info("👈 サイドバーからCSVファイルをアップロードして、あなたのチャンネル/記事の成長を加速させましょう。")
    
    # ダミー表示でWOW感を出す
    st.markdown("### プロフェッショナルな分析体験")
    st.image("https://images.unsplash.com/photo-1551288049-bbbda5366391?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80")
    
    st.markdown("""
    #### このツールでできること：
    - **複雑なデータの自動整理**: カラム名の違いを気にせずアップロード可能。
    - **統計的スパイク検知**: たまたま伸びたのか、真のヒットなのかを判定。
    - **具体的な戦術提案**: 「何を」「いつ」「どうするか」まで踏み込んだアドバイス。
    """)
