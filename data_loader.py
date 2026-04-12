import pandas as pd
import numpy as np

class DataLoader:
    def __init__(self):
        # 多角的カラムマッピング（各媒体の個別指標に対応）
        self.column_mapping = {
            'date': ['日付', 'date', 'day', '作成日', '公開日', '年月日', '日次', '掲載日', 'timestamp', '公開時刻', '投稿日', '作成日時'],
            'views': ['視聴回数', 'ビュー数', '閲覧数', 'views', '視聴数', '再生回数', '再生数', '固定表示数'],
            'ctr': ['クリック率', 'ctr', 'クリック率(%)', 'ctr(%)', 'クリックスルー率'],
            'duration': ['平均視聴時間', '平均再生時間', '滞在時間', 'duration', 'average duration', '視聴維持'],
            'metric_value': [ # フォールバック（他の主要な数値）
                'スキ数', 'likes', 'アクセス数', 'pv', 'クリック数', 'インプレッション', 'インプ', '閲覧', '読了数', 'リプライ数'
            ],
            'content': ['タイトル', 'title', 'コンテンツ名', '動画', '記事タイトル', '動画タイトル', '動画のタイトル', '記事名', '名前', 'name', 'アイテム', '作品名']
        }

    def convert_duration_to_seconds(self, duration_str):
        """
        '0:02:06' 形式の文字列を、計算可能な秒数（float）に変換。
        ValueErrorを回避するための堅牢なロジックを維持。
        """
        try:
            if not isinstance(duration_str, str):
                return float(duration_str) if duration_str is not None else 0.0
            
            # pd.to_timedelta は標準的な時間形式 ('0:02:06') を正確に扱える
            td = pd.to_timedelta(duration_str)
            return td.total_seconds()
        except:
            # フォールバック: 手動パース（コロン区切り）
            try:
                parts = str(duration_str).split(':')
                if len(parts) == 3: return float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
                if len(parts) == 2: return float(parts[0])*60 + float(parts[1])
                return float(duration_str)
            except:
                return 0.0

    def load_csv(self, file_path):
        """
        CSVファイルを読み込み、正規化して返す。合計行の除外を徹底。
        """
        try:
            df = None
            encodings = ['utf-8-sig', 'cp932', 'shift_jis', 'utf-16']
            for encoding in encodings:
                try:
                    if hasattr(file_path, 'seek'):
                        file_path.seek(0)
                    df = pd.read_csv(file_path, encoding=encoding)
                    break
                except:
                    continue
            
            if df is None:
                raise ValueError("CSVデータの読み込みに失敗しました。")

            # 合計行、サマリー行、または特定のノイズを高い精度で除外
            noise_patterns = ['合計', 'Total', 'サマリー', '総計', '平均', 'Average', 'Summary']
            mask = df.apply(lambda row: row.astype(str).str.contains('|'.join(noise_patterns), case=False).any(), axis=1)
            df = df[~mask].reset_index(drop=True)

            return self.normalize_dataframe(df)
        except Exception as e:
            raise Exception(f"データロード中にエラーが発生しました: {str(e)}")

    def normalize_dataframe(self, df):
        """
        カラム名を 'metric_value' 等に正規化し、型をクレンジング（カンマ・％・記号の除去）。
        """
        normalized_df = df.copy()
        found_columns = {}

        # カラム名のマッチング
        for target, synonyms in self.column_mapping.items():
            for col in df.columns:
                if col.strip().lower() in [s.lower() for s in synonyms]:
                    found_columns[target] = col
                    break
        
        # 日付カラムの推測フォールバック
        if 'date' not in found_columns:
            for col in df.columns:
                if any(x in col for x in ['日', 'time', 'date', '時刻']):
                    found_columns['date'] = col
                    break
        
        # メトリクスカラムの推測フォールバック
        if 'metric_value' not in found_columns:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                found_columns['metric_value'] = numeric_cols[0]

        # 正規名称へのリネーム
        rename_dict = {v: k for k, v in found_columns.items()}
        normalized_df = normalized_df.rename(columns=rename_dict)

        # 1. 日付の変換
        if 'date' in normalized_df.columns:
            normalized_df['date'] = pd.to_datetime(normalized_df['date'], errors='coerce')
            normalized_df = normalized_df.dropna(subset=['date'])

        # 2. メトリクスの数値化（クレンジング徹底：カンマ、%、空白、および時間形式の対応）
        numeric_targets = ['views', 'ctr', 'duration', 'metric_value']
        for target in numeric_targets:
            if target in normalized_df.columns:
                if normalized_df[target].dtype == object:
                    # 文字列をクレンジング
                    def clean_numeric(val):
                        val_str = str(val).strip()
                        # 時間形式（コロンを含む）なら秒数へ
                        if ':' in val_str:
                            return self.convert_duration_to_seconds(val_str)
                        # 記号除去
                        import re
                        clean_v = re.sub(r'[,\%\s\¥\$]', '', val_str)
                        try:
                            return float(clean_v)
                        except:
                            return 0.0
                    
                    normalized_df[target] = normalized_df[target].apply(clean_numeric)
                
                normalized_df[target] = pd.to_numeric(normalized_df[target], errors='coerce').fillna(0.0)

        # 互換性担保: metric_value がない場合、最有力な数値を割り当てる
        if 'metric_value' not in normalized_df.columns or normalized_df['metric_value'].sum() == 0:
            for p in ['views', 'pv', '閲覧数']:
                if p in normalized_df.columns:
                    normalized_df['metric_value'] = normalized_df[p]
                    break
        
        # 最終フォールバック
        if 'metric_value' not in normalized_df.columns:
            for col in normalized_df.select_dtypes(include=[np.number]).columns:
                if col not in ['views', 'ctr', 'duration']:
                    normalized_df['metric_value'] = normalized_df[col]
                    break

        # 3. コンテンツ名のデフォルト補完
        if 'content' not in normalized_df.columns:
            normalized_df['content'] = 'Overall'
        
        # 最終的な合計行チェック（正規化後の列内容も考慮）
        noise_patterns = ['合計', 'Total', '総計']
        mask = normalized_df.apply(lambda row: row.astype(str).str.contains('|'.join(noise_patterns), case=False).any(), axis=1)
        normalized_df = normalized_df[~mask]

        return {
            'data': normalized_df,
            'has_date': 'date' in normalized_df.columns
        }

loader = DataLoader()
