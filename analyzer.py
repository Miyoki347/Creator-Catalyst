import pandas as pd
import numpy as np

class Analyzer:
    def __init__(self):
        pass

    def analyze_data(self, df):
        """
        データを多角的に分析し、スパイク検知とアクション生成を行う。
        """
        analysis_results = {
            'summary_metrics': {},
            'spikes': [],
            'top_content': [],
            'actions': []
        }

        # 1. 概要指標（最新日 vs 前週平均など）
        latest_value = df['metric'].iloc[-1]
        last_7_days_avg = df['metric'].iloc[-8:-1].mean() if len(df) > 7 else df['metric'].mean()
        wow_growth = ((latest_value / last_7_days_avg) - 1) * 100 if last_7_days_avg > 0 else 0
        
        analysis_results['summary_metrics'] = {
            'latest_value': latest_value,
            'avg_value': last_7_days_avg,
            'wow_growth': wow_growth
        }

        # 2. ✨ あなたがバズった瞬間（スパイク検出）
        mean_val = df['metric'].mean()
        std_val = df['metric'].std()
        if std_val > 0:
            df['z_score'] = (df['metric'] - mean_val) / std_val
            # Z-score > 2 をスパイクと見なす
            spikes_df = df[df['z_score'] > 2].copy()
            for _, row in spikes_df.iterrows():
                analysis_results['spikes'].append({
                    'date': row['date'],
                    'value': row['metric'],
                    'content': row.get('content', 'Unknown'),
                    'z_score': row['z_score']
                })

        # 3. 📈 伸びのきっかけになった動画（寄与度分析）
        if df['content'].nunique() > 1:
            # Overall以外のコンテンツを集計
            content_df = df[df['content'] != 'Overall']
            if not content_df.empty:
                top_content = content_df.groupby('content')['metric'].sum().sort_values(ascending=False).head(5)
                analysis_results['top_content'] = top_content.to_dict()

        # 4. 💡 次にやるといいこと（戦略提案 / アクションプラン）
        analysis_results['actions'] = self.generate_strategic_actions(df, analysis_results)

        return analysis_results

    def generate_strategic_actions(self, df, analysis):
        """
        分析結果に基づき、即実行可能な具体的アクションを生成する。
        """
        actions = []
        metrics = analysis['summary_metrics']
        spikes = analysis['spikes']

        # ロジック1: 最近大きなスパイクがあった場合
        if len(spikes) > 0:
            recent_spike = spikes[-1]
            spike_content = recent_spike['content']
            
            # スパイクの要因分析（仮説）
            actions.append({
                "title": f"【続編制作】「{spike_content}」の深掘り（リテンション / 継続率向上）",
                "detail": f"データによると、直近の「{spike_content}」で統計的に有意なバズ（スパイク）を検知しました。このトピックは視聴者の関心が極めて高い『特異点』です。同じ切り口、または逆の視点での続編を48時間以内に構成し、ファンの定着（リテンション）を狙いましょう。"
            })
        
        # ロジック2: 全体的な傾向（WoW%が正の場合）
        if metrics['wow_growth'] > 10:
             actions.append({
                "title": "【拡散ブースト】ショート展開による新規流入（新規獲得 / アクquisition）",
                "detail": f"前週比+{metrics['wow_growth']:.1f}%の急成長を記録しています。メインコンテンツの中から『最も心が躍る瞬間（キラーコンテンツ）』を切り出し、ショート動画へ展開することで、爆発的な新規層の獲得が可能です。"
            })
        else:
            actions.append({
                "title": "【安定成長】21時の投稿固定（エンゲージメント最適化）",
                "detail": "現在、成長が安定フェーズにあります。視聴者のライフスタイルに合わせた『21時』に投稿を固定することで、初動の視聴密度（エンゲージメント密度）を高め、アルゴリズムによる推奨を強化できます。"
            })

        # ロジック3: クオリティ/CTA
        actions.append({
            "title": "【視聴維持率の改善】冒頭15秒でのメリット提示（PREP法）",
            "detail": "次の動画/記事では、『冒頭ですぐに結論を言う（P）』構成を徹底してください。視聴者が『この動画を見続けてくれる割合（視聴維持率）』を10%改善できる余地があります。"
        })

        return actions[:3] # 常に3つ返す

analyzer = Analyzer()
