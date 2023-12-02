def preprocess_stock_data(df):
    """
    株価データの前処理を行う関数

    :param df: pandas DataFrame, 株価データが含まれるデータフレーム
    :return: pandas DataFrame, 前処理後のデータフレーム
    """
    # 0. Dateカラムをインデックスに設定する
    if df.index.name != 'Date':
        if 'Date' in df.columns:
            df.set_index('Date', inplace=True)
        else:
            raise ValueError("DataFrameにDateカラムが見つかりません。")

    # 1. 3連続以上のNaNを含む行を削除する
    # 連続するNaNの数をカウント
    nan_counts = df.isna().astype(int)
    nan_counts[nan_counts == 0] = None
    nan_counts = nan_counts.fillna(method='ffill', limit=2).fillna(method='bfill', limit=2)
    
    # 3連続以上NaNを含む行を削除
    df = df[nan_counts.isna().all(axis=1)]

    # 2. 断続的なNaNを前後の値の平均で埋める
    df.interpolate(method='linear', limit_direction='both', inplace=True)

    # 3. NaNがないことを確認し、差分系列に変換する
    if df.isna().sum().sum() == 0:
        df = df.pct_change()
        df.dropna(inplace=True)
    return df
