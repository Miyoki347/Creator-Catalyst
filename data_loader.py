import pandas as pd
import numpy as np
from datetime import datetime

class DataLoader:
    def __init__(self):
        # カラム名のマッピング（マルチプラットフォーム対応）
        self.column_mapping = {
            'date': ['日付', 'date', 'day', '作成日', '公開日', '年月日', '日次', '掲載日', 'timestamp', '公開時刻', '投稿日'],
            'metric': ['視聴回数', 'ビュー数', '閲覧数', 'views', '視聴数', 'スキ数', 'likes', 'アクセス数', 'pv', '再生回数', '再生数', 'クリック数', 'ctr'],
            'content': ['タイトル', 'title', 'コンテンツ名', '動画', '記事タイトル', '動画タイトル', '動画のタイトル', '記事名', '名前', 'name', 'アイテム']
        }

    def convert_duration_to_seconds(self, duration_str):
        """
        '0:02:06' 形式の文字列を秒数（float）に変換する。
        ValueError を回避し、失敗した場合は 0.0 を返す。
        """
        try:
            if not isinstance(duration_str, str):
                return float(duration_str) if duration_str is not None else 0.0
            
            if ':' not in duration_str:
                return float(duration_str) if duration_str.strip() != "" else 0.0

            parts = duration_str.split(':')
            if len(parts) == 3: # HH:MM:SS
                return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
            elif len(parts) == 2: # MM:SS
                return float(parts[0]) * 60 + float(parts[1])
            return 0.0
        except (ValueError, TypeError):
            return 0.0

    def load_csv(self, file_path):
        """
        CSVファイルを読み込み、データを正規化して返す。
        """
        try:
            # 汎用的な読み込み（エンコーディングの試行）
            df = None
            encodings = ['utf-8-sig', 'cp932', 'shift_jis', 'utf-16']
            for encoding in encodings:
                try:
                    if hasattr(file_path, 'seek'):
                        file_path.seek(0)
                    df = pd.read_csv(file_path, encoding=encoding)
                    break
                except (UnicodeDecodeError, Exception):
                    continue
            
            if df is None:
                raise ValueError("CSVファイルの読み込みに失敗しました。")

            # YouTubeの「表データ.csv」などの特有構造に対応（合計行のスキップ）
            # データフレーム全体を文字列としてチェックし、「合計」や「Total」を含む行を削除
            mask = df.apply(lambda row: row.astype(str).str.contains('合計|Total', case=False).any(), axis=1)
            df = df[~mask].reset_index(drop=True)

            return self.normalize_dataframe(df)
        except Exception as e:
            raise Exception(f"データロード中にエラーが発生しました: {str(e)}")

    def normalize_dataframe(self, df):
        """
        DataFrameのカラム名を正規化し、型を変換する。
        """
        normalized_df = df.copy()
        found_columns = {}

        # 各標準カラムに対して、ソースDFから一致するものを探す
        for target, synonyms in self.column_mapping.items():
            for col in df.columns:
                if col.lower() in [s.lower() for s in synonyms]:
                    found_columns[target] = col
                    break
        
        # 必須カラムのチェック（見つからない場合は推測）
        if 'date' not in found_columns:
            for col in df.columns:
                if '日' in col or 'time' in col.lower() or 'date' in col.lower():
                    found_columns['date'] = col
                    break
        
        if 'metric' not in found_columns:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                found_columns['metric'] = numeric_cols[0]

        # リネーム
        rename_dict = {found_columns[k]: k for k in found_columns}
        normalized_df = normalized_df.rename(columns=rename_dict)

        # 1. 日付の変換
        if 'date' in normalized_df.columns:
            normalized_df['date'] = pd.to_datetime(normalized_df['date'], errors='coerce')
            normalized_df = normalized_df.dropna(subset=['date'])
            normalized_df = normalized_df.sort_values('date')

        # 2. メトリクスの数値化（カンマ除去、時間変換、型変換等）
        if 'metric' in normalized_df.columns:
            # 型がオブジェクト（文字列）の場合、クレンジングを行う
            if normalized_df['metric'].dtype == object:
                # 文字列として扱い、共通のノイズ（, や %）を除去
                metric_clean = normalized_df['metric'].astype(str).str.replace(',', '').str.replace('%', '').str.replace(' ', '').str.strip()
                
                # '0:02:06' 形式の変換を試行、失敗は to_numeric で NaN に、最終的に 0.0 に
                normalized_df['metric'] = metric_clean.apply(self.convert_duration_to_seconds)
                normalized_df['metric'] = pd.to_numeric(normalized_df['metric'], errors='coerce')
            
            # 数値型へ強制変換
            normalized_df['metric'] = normalized_df['metric'].astype(float).fillna(0.0)

        # 3. コンテンツ名の補完
        if 'content' not in normalized_df.columns:
            normalized_df['content'] = 'Overall'
        
        # 4. 「合計」行の再チェック（最終的な除外）
        mask = normalized_df.apply(lambda row: row.astype(str).str.contains('合計|Total', case=False).any(), axis=1)
        normalized_df = normalized_df[~mask]

        # 5. 空白行の除外
        normalized_df = normalized_df.dropna(how='all')

        # 結果を辞書形式で返す
        return {
            'data': normalized_df[['date', 'metric', 'content']] if 'date' in normalized_df.columns else normalized_df,
            'has_date': 'date' in normalized_df.columns
        }

loader = DataLoader()
