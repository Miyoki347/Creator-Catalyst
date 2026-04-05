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
        color: #FFFFFF; /* 高コントラストの白 */
    }
    .metric-card {
        background-color: #252525; /* 少し明るいグレー */
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #444444;
        box-shadow: 0 4px 15px rgba(0,0,0,0.6);
        margin-bottom: 25px;
    }
    .action-card {
        background: linear-gradient(135deg, #2d3748, #1a202c);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #4A5568;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
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
        margin-bottom: 0px;
    }
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        color: #FF8C00 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #E2E8F0 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    .stMetric {
        background-color: #252525;
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #444444;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    h1, h2, h3, p {
        color: #FFFFFF !important;
    }
    .stInfo {
        background-color: #2d3748 !important;
        color: #FFFFFF !important;
        border: 1px solid #4A5568 !important;
        background-color: #1a1a1a !important;
        color: #FFFFFF !important;
        border: 1px solid #333333 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("C:/Users/kiyom/.gemini/antigravity/brain/0df2e595-8300-4509-9cac-5d9157ed09b6/catscope_logo_1775368089418.png", width=120)
    st.markdown("### CatScope 🚀")
    st.markdown("クリエイターの成長を加速させる『触媒』")
    
    st.divider()
    
    uploaded_file = st.file_uploader("📥 分析データの読み込み（CSVアップロード）", type=["csv"])
    
    if uploaded_file:
        st.success("データの読み込みに成功しました。CatScopeを起動します。")
    else:
        st.info("YouTubeアナリティクス、またはnoteのアクセス状況CSVファイルをアップロードしてください。")
        
    st.divider()
    st.markdown("#### 🤔 使い方（ご利用ステップ）")
    st.markdown("1. データを読み込む\n2. グラフでバズった瞬間を探す\n3. CatScopeの提案を実行する")

# --- Main Dashboard ---
col_logo, col_title = st.columns([1, 6])
with col_logo:
    st.image("C:/Users/kiyom/.gemini/antigravity/brain/0df2e595-8300-4509-9cac-5d9157ed09b6/catscope_logo_1775368089418.png", width=80)
with col_title:
    st.markdown('<h1 class="catalyst-title">CatScope 🚀</h1>', unsafe_allow_html=True)
st.markdown("#### 成長を加速させるAIインテリジェンス（CatScope Engine）")

# パーソナライズメッセージ
st.info("お疲れ様です、七輝さん！ CatScope（分析エンジン）が、あなたの才能がさらに輝くヒント（インサイト）を見つけました。")

if uploaded_file:
    # データ読み込みと分析
    try:
        df = loader.load_csv(uploaded_file)
        analysis = analyzer.analyze_data(df)
        
        # 1. 概要メトリクス
        st.subheader("📊 今の状態・健康診断（KPIメトリクス）")
        col1, col2, col3 = st.columns(3)
        
        metrics = analysis['summary_metrics']
        col1.metric("最新の数値（最新指標）", f"{int(metrics['latest_value']):,}", f"{metrics['wow_growth']:.1f}% WoW", delta_color="normal")
        col2.metric("週間平均（ベースライン）", f"{int(metrics['avg_value']):,}", "安定フェーズ")
        col3.metric("✨ あなたがバズった瞬間（スパイク検出）", f"{len(analysis['spikes'])}回", "成長の特異点")

        st.divider()

        # 2. メイングラフ
        st.subheader("📈 伸びのきっかけになった動画（寄与度分析 / トレンド）")
        
        fig = go.Figure()
        
        # メインデータライン (エナジーオレンジ)
        fig.add_trace(go.Scatter(
            x=df['date'], y=df['metric'],
            mode='lines',
            name='あなたの成長曲線（メトリクス推移）',
            line=dict(color='#FF8C00', width=4), # エナジーオレンジ
            fill='tozeroy',
            fillcolor='rgba(255, 140, 0, 0.1)'
        ))
        
        # 投稿タイミングの可視化 (ビビッドパープル)
        post_df = df[df['content'] != 'Overall'].copy()
        if not post_df.empty:
            # 垂直線 (Vline) の追加
            for post_date in post_df['date']:
                fig.add_vline(x=post_date, line_width=1, line_dash="dash", line_color="rgba(147, 112, 219, 0.4)")
            
            # 投稿マーカー
            fig.add_trace(go.Scatter(
                x=post_df['date'], y=post_df['metric'],
                mode='markers',
                name='コンテンツ投稿日（パブリッシュ）',
                text=[f"{title} を投稿した日" for title in post_df['content']],
                marker=dict(color='#9370DB', size=12, symbol='diamond', line=dict(width=2, color='white')),
                hovertemplate="<b>%{text}</b><br>数値: %{y}<extra></extra>"
            ))
        
        # スパイクのハイライト
        if analysis['spikes']:
            spike_dates = [s['date'] for s in analysis['spikes']]
            spike_values = [s['value'] for s in analysis['spikes']]
            fig.add_trace(go.Scatter(
                x=spike_dates, y=spike_values,
                mode='markers',
                name='あなたがバズった瞬間（スパイク）',
                marker=dict(color='#FF007F', size=15, symbol='star', line=dict(width=2, color='white')),
                hovertemplate="<b>バズった瞬間（スパイク）</b><br>日付: %{x}<br>数値: %{y}<extra></extra>"
            ))
            
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e0e0e0',
            xaxis=dict(showgrid=False, title="日付（タイムライン）"),
            yaxis=dict(showgrid=True, gridcolor='#374151', title="数値（ヒット指数）"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=30, b=0),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # 3. 戦略セクション
        st.subheader("💡 次にやるといいこと（戦略提案 / アクションプラン）")
        st.markdown("_CatScopeがあなたのデータから導き出した、才能を伸ばすための具体的ヒントです。_")
        
        for i, action in enumerate(analysis['actions']):
            st.markdown(f"""
            <div class="action-card">
                <h3 style="color: #9D00FF; margin-bottom: 10px;">ACTION {i+1}: {action['title']}</h3>
                <p style="font-size: 1.1rem; line-height: 1.6;">{action['detail']}</p>
            </div>
            """, unsafe_allow_html=True)

        # 4. 詳細ログ / エクスプローラ
        with st.expander("詳細データ・分析ログ（ローデータ）を表示"):
            st.write(df)
            if analysis['top_content']:
                st.write("### 📈 伸びのきっかけになった動画（寄与度分析）")
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
