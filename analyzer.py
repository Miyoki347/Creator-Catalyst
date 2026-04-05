import pandas as pd
import numpy as np

class Analyzer:
    def __init__(self):
        pass

    def analyze_data(self, df, has_date=True, target_audience="", pain_points=""):
        """
        データを分析し、KPI、スパイク、トップコンテンツ、および具体的なアクションプランを返す。
        """
        summary_metrics = {}
        spikes = []
        top_content = {}
        
        if has_date:
            # 時系列分析
            summary_metrics['latest_value'] = df['metric'].iloc[-1]
            summary_metrics['avg_value'] = df['metric'].mean()
            
            # 前週比 (WoW)
            if len(df) >= 14:
                last_week = df['metric'].iloc[-7:].sum()
                prev_week = df['metric'].iloc[-14:-7].sum()
                if prev_week > 0:
                    summary_metrics['wow_growth'] = ((last_week - prev_week) / prev_week) * 100
                else:
                    summary_metrics['wow_growth'] = 0
            else:
                summary_metrics['wow_growth'] = 0
                
            # スパイク検出 (平均+2標準偏差)
            threshold = df['metric'].mean() + 2 * df['metric'].std()
            spike_df = df[df['metric'] > threshold]
            for _, row in spike_df.iterrows():
                spikes.append({'date': row['date'], 'value': row['metric']})
        else:
            # 累積分析 (重複を排除して集計)
            summary_metrics['total_value'] = df['metric'].sum()
            summary_metrics['avg_per_content'] = df['metric'].mean()
            summary_metrics['content_count'] = len(df)
            
            # コンテンツごとに集計してトップ5を抽出
            grouped = df.groupby('content')['metric'].sum().sort_values(ascending=False).head(5)
            for content_name, val in grouped.items():
                top_content[content_name] = val

        # 収益化ポテンシャル（簡易計算）
        score = min(100, int(df['metric'].mean() / 10))
        status = "要改善" if score < 30 else "成長中" if score < 70 else "高ポテンシャル"
        monetization = {'score': score, 'status': status}

        # アクションプランの生成 (超具体化)
        actions = self._generate_specific_actions(df, target_audience, pain_points)

        return {
            'summary_metrics': summary_metrics,
            'spikes': spikes,
            'top_content': top_content,
            'monetization': monetization,
            'actions': actions
        }

    def _generate_specific_actions(self, df, target, pain):
        """
        ターゲットと悩みに基づき、具体的（日本語）なアクションを3つ生成する。
        """
        actions = []
        
        # デフォルト値の設定
        target = target if target else "全般的な視聴者"
        pain = pain if pain else "再生数の伸び悩み"

        # メトリクスに基づいた分析
        avg_metric = df['metric'].mean()
        max_metric = df['metric'].max()
        
        # 1. コンテンツ構成へのアドバイス
        actions.append({
            "title": f"【{target}向け】冒頭15秒の「引き」を強化",
            "detail": f"「{pain}」を解決するため、動画開始直後にターゲットが自分事化できる問いかけを行ってください。データによると平均数値は {avg_metric:.0f} ですが、最大値 {max_metric:.0f} を出した時の構成を分析し、最初の数秒に最も重要な情報を凝縮しましょう。"
        })

        # 2. 離脱ポイントへの具体的指示
        actions.append({
            "title": "中盤の離脱を防ぐ「予告型」の差し込み",
            "detail": f"ターゲットが「{target}」であれば、動画の3分地点（中盤）で後半のハイライトを0.5秒だけ見せる「チラ見せ」を導入してください。これにより、{pain}の原因である視聴維持率の低下を物理的に食い止めます。"
        })

        # 3. タイトル・サムネイルの改善
        actions.append({
            "title": "ターゲットの「不満」を突くタイトル変更",
            "detail": f"「{pain}」を抱える視聴者は、解決策を求めています。タイトルを『〇〇する方法』から『ターゲットが知らない〇〇の落とし穴』のように、痛点を突く形に明日書き換えてください。クリック率(CTR)の向上が見込めます。"
        })

        return actions[:3]

analyzer = Analyzer()
