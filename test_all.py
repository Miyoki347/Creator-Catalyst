from data_loader import loader
from analyzer import analyzer
import pandas as pd
import io

def test_data_cleansing():
    print("--- 1. データクレンジングの検証 ---")
    # テスト用CSVデータ（ノイズ、合計行、カンマ、時間形式を含む）
    csv_content = """日付,ビュー数,タイトル,平均視聴時間
合計,15000,全データ,0:01:30
2026-03-20,"1,200",動画A,0:02:06
2026-03-21,1350,動画A,0:01:45
サマリー,999,サマリー,0:00:50
"""
    file_obj = io.StringIO(csv_content)
    result = loader.load_csv(file_obj)
    df = result['data']
    
    # 1.1 合計行・サマリー行の除外を確認
    rows = len(df)
    print(f"有効な行数: {rows} (期待値: 2)")
    assert rows == 2, f"合計行の除外に失敗しました (rows={rows})"
    
    # 1.2 カンマ付き数値のパースを確認
    val_with_comma = df.iloc[0]['metric_value']
    print(f"カンマ付き数値のパース: {val_with_comma} (期待値: 1200.0)")
    assert val_with_comma == 1200.0, "カンマ付き数値のパースに失敗しました"

    # 1.3 時間形式の変換（秒数）を確認
    # loader.normalize_dataframe 内で metric_value が時間形式の場合の処理を検証
    # 今回のテストデータでは 'ビュー数' が metric_value に選ばれているため、
    # 直接 convert_duration_to_seconds を検証
    time_str = "0:02:06"
    secs = loader.convert_duration_to_seconds(time_str)
    print(f"時間形式の変換: {time_str} -> {secs}秒 (期待値: 126.0)")
    assert secs == 126.0, "時間形式の変換に失敗しました"
    print("[OK] データクレンジング検証合格\n")
    return df

def test_analyzer_logic(df):
    print("--- 2. 分析エンジン（3大指標生成）の検証 ---")
    # パラメータ設定
    platform = "動画（YouTube/ニコニコ等）"
    genre = "教育/解説"
    desire = "承認・自己実現（賢くなりたい等）"
    goal = "資産構築（ストック性重視）"
    
    analysis = analyzer.analyze_data(
        df, has_date=True, platform=platform, genre=genre,
        core_desire=desire, goal=goal
    )
    
    actions = analysis['actions']
    print(f"生成されたアドバイス数: {len(actions)} (期待値: 3)")
    assert len(actions) == 3, "アドバイスが3つ生成されていません"
    
    # 各アドバイスに特定のキーワードが含まれているか確認
    keywords = ["【需給バランス】", "【推定収益効率（RPM）】", "【資産性（Asset Score）】"]
    for i, action in enumerate(actions):
        print(f"STRATEGY {i+1}: {action['title']}")
        # どの項目にキーワードが含まれているかチェック
        content = action['action']
        found = False
        for kw in keywords:
            if kw in content:
                print(f"  - キーワード発見: {kw}")
                found = True
        assert found, f"アドバイス {i+1} に主要指標が含まれていません"

    print("[OK] 分析エンジン検証合格\n")

if __name__ == "__main__":
    try:
        df = test_data_cleansing()
        test_analyzer_logic(df)
        print("[SUCCESS] すべてのテストに合格しました！")
    except Exception as e:
        print(f"[FAILED] テスト失敗: {str(e)}")
        import traceback
        traceback.print_exc()
