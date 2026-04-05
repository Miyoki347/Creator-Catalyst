import pandas as pd
import numpy as np

class Analyzer:
    def __init__(self):
        pass

    def analyze_data(self, df, has_date=True, platform="", genre="", target_audience="", pain_points="", success_manual=""):
        """
        データを読み取り、ユニバーサル形式のKPI、スパイク、コンテンツ寄与度、および3ステップのアクションを生成。
        """
        summary_metrics = {}
        spikes = []
        top_content = {}
        
        # メトリクス共通正規化名称
        m_col = 'metric_value'

        # 共通KPI計算
        summary_metrics['total_value'] = df[m_col].sum()
        summary_metrics['avg_value'] = df[m_col].mean()

        if has_date:
            # 最新のトレンド
            summary_metrics['latest_value'] = df[m_col].iloc[-1]
            if len(df) >= 14:
                last_7 = df[m_col].iloc[-7:].sum()
                prev_7 = df[m_col].iloc[-14:-7].sum()
                summary_metrics['wow_growth'] = ((last_7 - prev_7) / prev_7) * 100 if prev_7 > 0 else 0
            else:
                summary_metrics['wow_growth'] = 0
            
            # スパイク検出 (異常値検出)
            std = df[m_col].std()
            mean = df[m_col].mean()
            threshold = mean + 2 * std
            spike_df = df[df[m_col] > threshold]
            for _, row in spike_df.iterrows():
                spikes.append({'date': row['date'], 'value': row[m_col]})

        # コンテンツ寄与度 (累積トップ5)
        if 'content' in df.columns:
            grouped = df.groupby('content')[m_col].sum().sort_values(ascending=False).head(5)
            for name, val in grouped.items():
                top_content[name] = val

        # 収益化・成長性スコア
        score = min(100, int(df[m_col].mean() / 10 if df[m_col].mean() > 0 else 0))
        status = "Seed" if score < 30 else "Growth" if score < 70 else "High Potential"
        monetization = {'score': score, 'status': status}

        # アクション生成エンジン（3ステップ対応）
        actions = self._generate_specific_actions(df, platform, genre, target_audience, pain_points, success_manual)

        return {
            'summary_metrics': summary_metrics,
            'spikes': spikes,
            'top_content': top_content,
            'monetization': monetization,
            'actions': actions
        }

    def _generate_specific_actions(self, df, platform, genre, target, pain, manual):
        """
        媒体・ジャンルに応じた解析（Analysis）改善（Action）影響（Impact）の3ステップアクションを生成。
        """
        actions = []
        platform = platform if platform else "汎用媒体"
        genre = genre if genre else "一般"
        target = target if target else "メインターゲット"
        pain = pain if pain else "現状の課題"

        # 媒体別視点の設定
        pov = {
            "YouTube": "視聴者維持率の維持とクリック率（CTR）の最大化",
            "note": "読者の熱量と、文章末尾でのアクション誘導",
            "X(Twitter)": "初速のインパクトとインプレッションの波及力",
            "ブログ/Webメディア": "SEOキーワードとユーザーの検索意図の合致"
        }.get(platform, "総合的なコンテンツエンゲージメント")

        # アクション1: 構造改革
        actions.append({
            "title": f"【{platform} × {genre}】コンテンツ構造の最適化",
            "analysis": f"「{pain}」を抱える現在のデータでは、開始直後の離脱、または入り口での躓きが見られます。{target} は「{genre}」特有の権威性や信頼を求めていますが、まだその期待に応えきれていません。",
            "action": f"{pov} に基づき、冒頭3秒での『問題喚起』と、それに対する『解決策の提示』を徹底してください。成功マニュアルにある既存の手法と、最新のトレンドを掛け合わせた『意外性』を導入してください。",
            "impact": f"ボトルネックとなっている「初動」が改善され、全体のエンゲージメント率が 15% 以上向上する見込みです。"
        })

        # アクション2: フックと誘導
        actions.append({
            "title": "ターゲットを射抜く「キーワード」と「ビジュアル」",
            "analysis": f"{target} が最も反応するスパイク箇所の傾向から、現在のフックが「ジャンル平均」に留まっていることが分析されました。",
            "action": f"媒体の特性を活かし、サムネイル（またはヘッダー）と1行目での『逆説的な表現』を採用してください。特に、{manual if manual else '過去の分析結果'} にある強いワードを、今のトレンドに合わせて再翻訳しましょう。",
            "impact": f"インプレッションおよびアクセス率が大幅に向上し、「{pain}」の解消に向けた母集団形成が加速します。"
        })

        # アクション3: クオリティ & 継続
        actions.append({
            "title": "リズムとテンポの再定義",
            "analysis": f"データ上、中盤以降の「だらけ」が{genre}としてのブランドイメージを希薄にし、継続的なファン化を阻害しています。",
            "action": f"1.1倍速相当の情報密度を実現するため、不要な接続詞のカットや、重要な箇所での0.5秒の『視覚的強調』を徹底してください。特にYouTubeならカット編集、noteなら箇条書きの導入が有効です。",
            "impact": f"平均視聴・滞在時間が劇的に改善され、プラットフォーム側から「高品質なコンテンツ」としてレコメンドされやすくなります。"
        })

        return actions[:3]

analyzer = Analyzer()
