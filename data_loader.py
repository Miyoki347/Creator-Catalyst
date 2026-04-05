import pandas as pd
import numpy as np
from datetime import datetime

class DataLoader:
    def __init__(self):
        # カラム名のマッピング（表記揺れ吸収用）
        self.column_mapping = {
            'date': ['日付', 'date', 'day', '作成日', '公開日', '年月日'],
            'metric': ['ビュー数', 'views', '視聴数', '視聴回数', 'スキ数', 'likes', 'アクセス数', 'pv'],
            'content': ['タイトル', 'title', 'コンテンツ名', '動画', '記事タイトル', '動画タイトル']
        }

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
                    # ストリームの位置をリセットするために再度オープンが必要
                    # uploaded_fileの場合はseek(0)が必要
                    if hasattr(file_path, 'seek'):
                        file_path.seek(0)
                    df = pd.read_csv(file_path, encoding=encoding)
                    break
                except (UnicodeDecodeError, Exception):
                    continue
            
            if df is None:
                raise ValueError("CSVファイルの読み込みに失敗しました（エンコーディングエラー）。")

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
        
        # 必須カラムのチェック
        if 'date' not in found_columns:
            # 日付が見つからない場合、最初の日付っぽいカラムを推測
            for col in df.columns:
                if '日' in col or 'time' in col.lower() or 'date' in col.lower():
                    found_columns['date'] = col
                    break
        
        if 'metric' not in found_columns:
            # メトリクスが見つからない場合、数値型のカラムを推測
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                found_columns['metric'] = numeric_cols[0]

        # リネーム
        rename_dict = {found_columns[k]: k for k in found_columns}
        normalized_df = normalized_df.rename(columns=rename_dict)

        # データのクリーニング
        # 1. 日付の変換
        if 'date' in normalized_df.columns:
            normalized_df['date'] = pd.to_datetime(normalized_df['date'], errors='coerce')
            normalized_df = normalized_df.dropna(subset=['date'])
            normalized_df = normalized_df.sort_values('date')

        # 2. メトリクスの数値化（カンマ除去等）
        if 'metric' in normalized_df.columns:
            if normalized_df['metric'].dtype == object:
                normalized_df['metric'] = normalized_df['metric'].str.replace(',', '').astype(float)
            normalized_df['metric'] = normalized_df['metric'].fillna(0)

        # 3. コンテンツ名の補完（ない場合は「全体」とする）
        if 'content' not in normalized_df.columns:
            normalized_df['content'] = 'Overall'

        # 必要なカラムのみ抽出（または優先的に配置）
        target_cols = ['date', 'metric', 'content']
        existing_target_cols = [c for c in target_cols if c in normalized_df.columns]
        other_cols = [c for c in normalized_df.columns if c not in target_cols]
        
        return normalized_df[existing_target_cols + other_cols]

# インスタンス化して外部から使いやすくする
loader = DataLoader()
