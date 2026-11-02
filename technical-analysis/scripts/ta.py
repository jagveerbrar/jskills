# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "yfinance>=0.2.40",
#     "pandas>=2.0.0",
#     "numpy>=1.24.0",
# ]
# ///

import argparse
import json
import sys
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
import yfinance as yf


def fetch_ticker_data(ticker_symbol: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    """Fetch OHLCV data for a ticker using yfinance."""
    t = yf.Ticker(ticker_symbol.strip().upper())
    df = t.history(period=period, interval=interval)
    if df is not None and not df.empty:
        df = df.dropna(subset=["Close"])
    if df.empty or len(df) < 5:
        raise ValueError(f"No sufficient price data returned for symbol '{ticker_symbol}'. Verify ticker symbol.")
    return df


def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate moving averages, RSI, MACD, Bollinger Bands, ATR, and Volume indicators."""
    data = df.copy()

    # Moving averages
    data["SMA20"] = data["Close"].rolling(window=20).mean()
    data["SMA50"] = data["Close"].rolling(window=50).mean()
    data["SMA200"] = data["Close"].rolling(window=200).mean()
    data["EMA20"] = data["Close"].ewm(span=20, adjust=False).mean()
    data["EMA50"] = data["Close"].ewm(span=50, adjust=False).mean()

    # RSI (14-day standard)
    delta = data["Close"].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    data["RSI14"] = 100 - (100 / (1 + rs))
    data["RSI14"] = data["RSI14"].fillna(50.0)

    # MACD (12, 26, 9)
    ema12 = data["Close"].ewm(span=12, adjust=False).mean()
    ema26 = data["Close"].ewm(span=26, adjust=False).mean()
    data["MACD_Line"] = ema12 - ema26
    data["MACD_Signal"] = data["MACD_Line"].ewm(span=9, adjust=False).mean()
    data["MACD_Hist"] = data["MACD_Line"] - data["MACD_Signal"]

    # Bollinger Bands (20-day, 2 std)
    data["BB_Mid"] = data["SMA20"]
    bb_std = data["Close"].rolling(window=20).std()
    data["BB_Upper"] = data["BB_Mid"] + (2 * bb_std)
    data["BB_Lower"] = data["BB_Mid"] - (2 * bb_std)
    bb_width = data["BB_Upper"] - data["BB_Lower"]
    data["BB_PctB"] = np.where(bb_width > 0, (data["Close"] - data["BB_Lower"]) / bb_width, 0.5)

    # Average True Range (ATR 14)
    high_low = data["High"] - data["Low"]
    high_close = (data["High"] - data["Close"].shift()).abs()
    low_close = (data["Low"] - data["Close"].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    data["ATR14"] = tr.ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()

    # Volume & Flow Indicators
    data["Vol_20D_Avg"] = data["Volume"].rolling(window=20).mean()
    # On-Balance Volume (OBV)
    direction = np.where(data["Close"] > data["Close"].shift(), 1, np.where(data["Close"] < data["Close"].shift(), -1, 0))
    data["OBV"] = (data["Volume"] * direction).cumsum()
    data["OBV_EMA20"] = data["OBV"].ewm(span=20, adjust=False).mean()

    return data


def compute_macro_weekly_context(ticker_symbol: str) -> Dict[str, Any]:
    """Fetch 2-year weekly data and calculate macro trend alignment (40W SMA, 10W SMA, weekly RSI)."""
    try:
        t = yf.Ticker(ticker_symbol.strip().upper())
        df_w = t.history(period="2y", interval="1wk")
        if df_w is not None and not df_w.empty:
            df_w = df_w.dropna(subset=["Close"])
        if df_w.empty or len(df_w) < 40:
            return {"status": "Insufficient weekly history"}

        df_w["SMA10W"] = df_w["Close"].rolling(window=10).mean()  # ~50-day equivalent
        df_w["SMA40W"] = df_w["Close"].rolling(window=40).mean()  # ~200-day equivalent

        delta_w = df_w["Close"].diff()
        gain_w = delta_w.where(delta_w > 0, 0.0)
        loss_w = -delta_w.where(delta_w < 0, 0.0)
        avg_gain_w = gain_w.ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()
        avg_loss_w = loss_w.ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()
        rs_w = avg_gain_w / avg_loss_w.replace(0, np.nan)
        df_w["RSI14W"] = 100 - (100 / (1 + rs_w))

        latest_w = df_w.iloc[-1]
        w_close = float(latest_w["Close"])
        sma10w = float(latest_w["SMA10W"]) if pd.notna(latest_w["SMA10W"]) else None
        sma40w = float(latest_w["SMA40W"]) if pd.notna(latest_w["SMA40W"]) else None
        rsi_w = float(latest_w["RSI14W"]) if pd.notna(latest_w["RSI14W"]) else 50.0

        if sma40w and sma10w:
            if w_close > sma10w > sma40w:
                w_regime = "Strong Macro Bullish"
            elif w_close > sma40w:
                w_regime = "Macro Bullish Consolidation"
            elif w_close < sma10w < sma40w:
                w_regime = "Strong Macro Bearish"
            elif w_close < sma40w:
                w_regime = "Macro Bearish"
            else:
                w_regime = "Neutral Macro"
        else:
            w_regime = "Indeterminate"

        dist_40w = round((w_close - sma40w) / sma40w * 100.0, 2) if sma40w else None
        dist_10w = round((w_close - sma10w) / sma10w * 100.0, 2) if sma10w else None

        return {
            "weekly_close": round(w_close, 2),
            "weekly_regime": w_regime,
            "sma_10w": round(sma10w, 2) if sma10w else None,
            "dist_sma_10w_pct": dist_10w,
            "sma_40w": round(sma40w, 2) if sma40w else None,
            "dist_sma_40w_pct": dist_40w,
            "weekly_rsi14": round(rsi_w, 1),
        }
    except Exception as e:
        return {"error": str(e)}


def evaluate_multi_timeframe_confluence(daily_regime: str, weekly_info: Dict[str, Any], daily_rsi: float) -> Dict[str, Any]:
    """Synthesize Weekly Tide and Daily Wave into an actionable confluence rating."""
    w_regime = weekly_info.get("weekly_regime", "Unknown")

    is_w_bull = "Bullish" in w_regime
    is_d_bull = "Bullish" in daily_regime
    is_w_bear = "Bearish" in w_regime
    is_d_bear = "Bearish" in daily_regime

    if is_w_bull and is_d_bull:
        alignment = "Fully Aligned Bullish (Macro + Daily Trend Coincide)"
        conviction = "High Conviction (Green Light)"
        verdict = "Strongest statistical buying regime. Both macro tide and intermediate daily waves point upward."
    elif is_w_bull and is_d_bear:
        alignment = "Counter-Trend Pullback (Daily Dip inside Macro Bull Market)"
        conviction = "Prime Dip-Buying Opportunity"
        verdict = "Ideal tactical value entry window. Daily weakness is temporarily discounted against a secular macro bull trend."
    elif is_w_bear and is_d_bull:
        alignment = "Bear Market Relief Rally (Counter-Trend Daily Bounce)"
        conviction = "Caution (High Fakeout Risk)"
        verdict = "Daily gains are fighting the macro secular downtrend. Do not mistake short-term momentum for structural safety."
    elif is_w_bear and is_d_bear:
        alignment = "Fully Aligned Bearish (Macro + Daily Markdown)"
        conviction = "Strict Avoid / Capital Preservation"
        verdict = "Severe selling momentum across all timeframes. High risk of multiple compression."
    else:
        alignment = "Mixed / Neutral Transition"
        conviction = "Moderate"
        verdict = "Consolidation phase. Wait for breakout confirmation."

    return {
        "alignment_status": alignment,
        "conviction_tier": conviction,
        "tactical_guidance": verdict,
        "macro_weekly_regime": w_regime,
        "daily_regime": daily_regime,
    }


def detect_peaks_and_trendlines(df: pd.DataFrame, window: int = 4, forward_bars: int = 10) -> Dict[str, Any]:
    """Identify structural swing peaks and troughs and fit forward-projected linear trendlines."""
    n = len(df)
    if n < window * 2 + 2:
        return {}

    highs = df["High"].values
    lows = df["Low"].values
    dates = [d.strftime("%Y-%m-%d") for d in df.index]

    peaks = []
    for i in range(window, n - window):
        if highs[i] == max(highs[i - window : i + window + 1]):
            peaks.append({"index": i, "date": dates[i], "price": float(highs[i])})

    troughs = []
    for i in range(window, n - window):
        if lows[i] == min(lows[i - window : i + window + 1]):
            troughs.append({"index": i, "date": dates[i], "price": float(lows[i])})

    upper_trendline = None
    if len(peaks) >= 2:
        p1, p2 = peaks[-2], peaks[-1]
        idx_diff = p2["index"] - p1["index"]
        if idx_diff > 0:
            slope_h = (p2["price"] - p1["price"]) / idx_diff
            curr_val = p1["price"] + slope_h * (n - 1 - p1["index"])
            proj_val_5d = p1["price"] + slope_h * (n - 1 + 5 - p1["index"])
            proj_val_10d = p1["price"] + slope_h * (n - 1 + forward_bars - p1["index"])
            trend_type = "Descending Ceiling" if slope_h < -0.05 else ("Ascending Resistance" if slope_h > 0.05 else "Horizontal Flat Ceiling")
            upper_trendline = {
                "anchor_1": {"date": p1["date"], "price": round(p1["price"], 2), "bar_index": p1["index"]},
                "anchor_2": {"date": p2["date"], "price": round(p2["price"], 2), "bar_index": p2["index"]},
                "slope_per_day": round(slope_h, 2),
                "type": trend_type,
                "current_level": round(curr_val, 2),
                "projected_target_plus_5d": round(proj_val_5d, 2),
                "projected_target_plus_10d": round(proj_val_10d, 2),
            }

    lower_trendline = None
    if len(troughs) >= 2:
        t1, t2 = troughs[-2], troughs[-1]
        idx_diff = t2["index"] - t1["index"]
        if idx_diff > 0:
            slope_l = (t2["price"] - t1["price"]) / idx_diff
            curr_val = t1["price"] + slope_l * (n - 1 - t1["index"])
            proj_val_5d = t1["price"] + slope_l * (n - 1 + 5 - t1["index"])
            proj_val_10d = t1["price"] + slope_l * (n - 1 + forward_bars - t1["index"])
            trend_type = "Ascending Support" if slope_l > 0.05 else ("Descending Support" if slope_l < -0.05 else "Horizontal Flat Floor")
            lower_trendline = {
                "anchor_1": {"date": t1["date"], "price": round(t1["price"], 2), "bar_index": t1["index"]},
                "anchor_2": {"date": t2["date"], "price": round(t2["price"], 2), "bar_index": t2["index"]},
                "slope_per_day": round(slope_l, 2),
                "type": trend_type,
                "current_level": round(curr_val, 2),
                "projected_target_plus_5d": round(proj_val_5d, 2),
                "projected_target_plus_10d": round(proj_val_10d, 2),
            }

    return {
        "recent_peaks": peaks[-3:],
        "recent_troughs": troughs[-3:],
        "upper_trendline_projection": upper_trendline,
        "lower_trendline_projection": lower_trendline,
        "projection_horizon_days": forward_bars,
    }


def compute_pivots_and_levels(df: pd.DataFrame) -> Dict[str, Any]:
    """Compute classic pivot points, 52-week range, and swing levels."""
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest

    prev_h = float(prev["High"])
    prev_l = float(prev["Low"])
    prev_c = float(prev["Close"])

    p = (prev_h + prev_l + prev_c) / 3.0
    r1 = (2 * p) - prev_l
    s1 = (2 * p) - prev_h
    r2 = p + (prev_h - prev_l)
    s2 = p - (prev_h - prev_l)
    r3 = prev_h + 2 * (p - prev_l)
    s3 = prev_l - 2 * (prev_h - p)

    diff = prev_h - prev_l
    fib_r1 = p + (0.382 * diff)
    fib_r2 = p + (0.618 * diff)
    fib_r3 = p + (1.000 * diff)
    fib_s1 = p - (0.382 * diff)
    fib_s2 = p - (0.618 * diff)
    fib_s3 = p - (1.000 * diff)

    lookback_window = min(len(df), 252)
    h52 = float(df["High"].iloc[-lookback_window:].max())
    l52 = float(df["Low"].iloc[-lookback_window:].min())
    curr_close = float(latest["Close"])
    range_52 = h52 - l52
    pos_52 = ((curr_close - l52) / range_52 * 100.0) if range_52 > 0 else 50.0

    lookback_20 = min(len(df), 20)
    swing_high_20 = float(df["High"].iloc[-lookback_20:].max())
    swing_low_20 = float(df["Low"].iloc[-lookback_20:].min())

    return {
        "52_week_high": round(h52, 2),
        "52_week_low": round(l52, 2),
        "52_week_position_pct": round(pos_52, 1),
        "swing_high_20d": round(swing_high_20, 2),
        "swing_low_20d": round(swing_low_20, 2),
        "classic_pivots": {
            "R3": round(r3, 2),
            "R2": round(r2, 2),
            "R1": round(r1, 2),
            "P": round(p, 2),
            "S1": round(s1, 2),
            "S2": round(s2, 2),
            "S3": round(s3, 2),
        },
        "fibonacci_pivots": {
            "R3": round(fib_r3, 2),
            "R2": round(fib_r2, 2),
            "R1": round(fib_r1, 2),
            "P": round(p, 2),
            "S1": round(fib_s1, 2),
            "S2": round(fib_s2, 2),
            "S3": round(fib_s3, 2),
        },
    }


def get_snapshot(ticker_symbol: str, period: str = "1y", interval: str = "1d") -> Dict[str, Any]:
    """Generate comprehensive technical snapshot including multi-timeframe weekly confluence."""
    raw_df = fetch_ticker_data(ticker_symbol, period=period, interval=interval)
    df = calculate_technical_indicators(raw_df)

    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest

    curr_price = float(latest["Close"])
    prev_close = float(prev["Close"])
    change = curr_price - prev_close
    pct_change = (change / prev_close * 100.0) if prev_close != 0 else 0.0

    sma20 = float(latest["SMA20"]) if pd.notna(latest["SMA20"]) else None
    sma50 = float(latest["SMA50"]) if pd.notna(latest["SMA50"]) else None
    sma200 = float(latest["SMA200"]) if pd.notna(latest["SMA200"]) else None
    ema20 = float(latest["EMA20"]) if pd.notna(latest["EMA20"]) else None
    ema50 = float(latest["EMA50"]) if pd.notna(latest["EMA50"]) else None

    dist_sma20 = round((curr_price - sma20) / sma20 * 100.0, 2) if sma20 else None
    dist_sma50 = round((curr_price - sma50) / sma50 * 100.0, 2) if sma50 else None
    dist_sma200 = round((curr_price - sma200) / sma200 * 100.0, 2) if sma200 else None

    if sma50 and sma200:
        if curr_price > sma50 > sma200:
            regime = "Strong Bullish"
        elif curr_price > sma50 and curr_price > sma200:
            regime = "Bullish"
        elif curr_price < sma50 < sma200:
            regime = "Strong Bearish"
        elif curr_price < sma50 and curr_price < sma200:
            regime = "Bearish"
        else:
            regime = "Neutral / Mixed"
        golden_cross = bool(sma50 > sma200)
    elif sma50:
        regime = "Bullish" if curr_price > sma50 else "Bearish"
        golden_cross = None
    else:
        regime = "Insufficient Data"
        golden_cross = None

    rsi = float(latest["RSI14"])
    rsi_status = "Overbought" if rsi >= 70.0 else ("Oversold" if rsi <= 30.0 else "Neutral")

    macd_line = float(latest["MACD_Line"])
    macd_signal = float(latest["MACD_Signal"])
    macd_hist = float(latest["MACD_Hist"])
    macd_status = "Bullish (Line > Signal)" if macd_line > macd_signal else "Bearish (Line < Signal)"

    bb_upper = float(latest["BB_Upper"]) if pd.notna(latest["BB_Upper"]) else None
    bb_mid = float(latest["BB_Mid"]) if pd.notna(latest["BB_Mid"]) else None
    bb_lower = float(latest["BB_Lower"]) if pd.notna(latest["BB_Lower"]) else None
    bb_pct_b = float(latest["BB_PctB"]) if pd.notna(latest["BB_PctB"]) else None

    atr = float(latest["ATR14"]) if pd.notna(latest["ATR14"]) else None

    # Volume and OBV flow
    vol_curr = int(latest["Volume"])
    vol_avg20 = float(latest["Vol_20D_Avg"]) if pd.notna(latest["Vol_20D_Avg"]) else None
    vol_ratio = round(vol_curr / vol_avg20, 2) if vol_avg20 and vol_avg20 > 0 else 1.0
    obv_curr = int(latest["OBV"]) if pd.notna(latest["OBV"]) else 0
    obv_ema = float(latest["OBV_EMA20"]) if pd.notna(latest["OBV_EMA20"]) else 0
    obv_trend = "Accumulation (OBV > 20D EMA)" if obv_curr >= obv_ema else "Distribution (OBV < 20D EMA)"

    recent_20 = df.tail(20)
    up_vol = recent_20[recent_20["Close"] >= recent_20["Open"]]["Volume"].sum()
    down_vol = recent_20[recent_20["Close"] < recent_20["Open"]]["Volume"].sum()
    up_down_ratio = round(up_vol / down_vol, 2) if down_vol > 0 else 1.0

    levels_info = compute_pivots_and_levels(df)
    trendline_info = detect_peaks_and_trendlines(df)

    # Multi-Timeframe Weekly Context Analysis
    weekly_info = compute_macro_weekly_context(ticker_symbol)
    confluence = evaluate_multi_timeframe_confluence(regime, weekly_info, rsi)

    return {
        "ticker": ticker_symbol.upper(),
        "timestamp": str(latest.name),
        "price": {
            "current": round(curr_price, 2),
            "change": round(change, 2),
            "pct_change": round(pct_change, 2),
            "open": round(float(latest["Open"]), 2),
            "high": round(float(latest["High"]), 2),
            "low": round(float(latest["Low"]), 2),
        },
        "trend": {
            "regime": regime,
            "golden_cross": golden_cross,
            "dist_sma20_pct": dist_sma20,
            "dist_sma50_pct": dist_sma50,
            "dist_sma200_pct": dist_sma200,
        },
        "moving_averages": {
            "SMA20": round(sma20, 2) if sma20 else None,
            "SMA50": round(sma50, 2) if sma50 else None,
            "SMA200": round(sma200, 2) if sma200 else None,
            "EMA20": round(ema20, 2) if ema20 else None,
            "EMA50": round(ema50, 2) if ema50 else None,
        },
        "oscillators": {
            "rsi14": round(rsi, 2),
            "rsi14_status": rsi_status,
            "macd_line": round(macd_line, 2),
            "macd_signal": round(macd_signal, 2),
            "macd_hist": round(macd_hist, 2),
            "macd_status": macd_status,
        },
        "volatility": {
            "bb_upper": round(bb_upper, 2) if bb_upper else None,
            "bb_mid": round(bb_mid, 2) if bb_mid else None,
            "bb_lower": round(bb_lower, 2) if bb_lower else None,
            "bb_pct_b": round(bb_pct_b, 3) if bb_pct_b else None,
            "atr14": round(atr, 2) if atr else None,
        },
        "volume": {
            "current": vol_curr,
            "avg_20d": int(vol_avg20) if vol_avg20 else None,
            "ratio_to_avg": vol_ratio,
            "obv_current": obv_curr,
            "obv_trend": obv_trend,
            "up_down_volume_ratio_20d": up_down_ratio,
        },
        "levels": levels_info,
        "trendline_projections": trendline_info,
        "macro_weekly_context": weekly_info,
        "multi_timeframe_confluence": confluence,
    }


def compare_tickers(tickers: List[str], period: str = "1y") -> List[Dict[str, Any]]:
    """Compare multiple tickers across core technical metrics and multi-timeframe confluence."""
    results = []
    for t in tickers:
        try:
            snap = get_snapshot(t, period=period)
            results.append({
                "ticker": snap["ticker"],
                "price": snap["price"]["current"],
                "change_pct": snap["price"]["pct_change"],
                "regime": snap["trend"]["regime"],
                "rsi14": snap["oscillators"]["rsi14"],
                "macd_status": snap["oscillators"]["macd_status"],
                "dist_sma50_pct": snap["trend"]["dist_sma50_pct"],
                "dist_sma200_pct": snap["trend"]["dist_sma200_pct"],
                "52w_position_pct": snap["levels"]["52_week_position_pct"],
                "vol_ratio": snap["volume"]["ratio_to_avg"],
                "obv_trend": snap["volume"]["obv_trend"],
                "macro_alignment": snap["multi_timeframe_confluence"]["conviction_tier"],
            })
        except Exception as e:
            results.append({"ticker": t.upper(), "error": str(e)})
    return results


def print_formatted_snapshot(data: Dict[str, Any]) -> None:
    """Print readable Markdown snapshot to stdout."""
    p = data["price"]
    t = data["trend"]
    m = data["moving_averages"]
    o = data["oscillators"]
    v = data["volatility"]
    vol = data["volume"]
    lvl = data["levels"]
    tp = data.get("trendline_projections", {})
    mtf = data.get("multi_timeframe_confluence", {})
    macro = data.get("macro_weekly_context", {})

    print(f"### Technical Snapshot: ${data['ticker']} (${p['current']:.2f})")
    print(f"* **Daily Change:** {p['change']:+.2f} ({p['pct_change']:+.2f}%)")
    print(f"* **Trend Regime:** {t['regime']} (vs 50D: {t['dist_sma50_pct']}%, vs 200D: {t['dist_sma200_pct']}%)")
    if t["golden_cross"] is not None:
        gc_str = "Golden Cross active (50 SMA > 200 SMA)" if t["golden_cross"] else "Death Cross active (50 SMA < 200 SMA)"
        print(f"* **Cross Status:** {gc_str}")
    print()

    # Multi-Timeframe Alignment Banner
    if mtf:
        print("#### Multi-Timeframe Alignment (Macro 1W + Intermediate 1D)")
        print(f"* **Confluence Rating:** **{mtf['conviction_tier']}** ({mtf['alignment_status']})")
        print(f"* **Macro Tide (Weekly 1W):** {macro.get('weekly_regime', 'N/A')} (40W SMA: ${macro.get('sma_40w', 'N/A')}, Dist: {macro.get('dist_sma_40w_pct', 'N/A')}%)")
        print(f"* **Tactical Wave (Daily 1D):** {t['regime']} (20D SMA: ${m['SMA20']}, 50D SMA: ${m['SMA50']})")
        print(f"* **Tactical Guidance:** {mtf['tactical_guidance']}")
        print()

    print("| Metric / Indicator | Value | Status / Signal | Context Threshold |")
    print("| :--- | :--- | :--- | :--- |")
    print(f"| **RSI (14D)** | {o['rsi14']} | {o['rsi14_status']} | Overbought > 70, Oversold < 30 |")
    print(f"| **MACD (12, 26, 9)** | Line: {o['macd_line']} / Hist: {o['macd_hist']} | {o['macd_status']} | Momentum confirmation |")
    print(f"| **20-Day SMA** | ${m['SMA20']} | Distance: {t['dist_sma20_pct']}% | Short-term momentum floor |")
    print(f"| **50-Day SMA** | ${m['SMA50']} | Distance: {t['dist_sma50_pct']}% | Medium-term institutional trend |")
    print(f"| **200-Day SMA** | ${m['SMA200']} | Distance: {t['dist_sma200_pct']}% | Macro cycle boundary |")
    if v["bb_upper"] and v["bb_lower"]:
        print(f"| **Bollinger Bands** | Upper: ${v['bb_upper']} / Lower: ${v['bb_lower']} | %B: {v['bb_pct_b']} | 20D ± 2σ channel |")
    if v["atr14"]:
        print(f"| **ATR (14D)** | ${v['atr14']} | Volatility Range | Daily expected swing range |")
    print(f"| **Volume (vs 20D Avg)** | {vol['current']:,} vs {vol['avg_20d']:,} | {vol['ratio_to_avg']}x Avg | Institutional participation |")
    print(f"| **On-Balance Volume (OBV)**| {vol.get('obv_current', 0):,} | {vol.get('obv_trend', 'N/A')} | 20D cumulative volume flow |")
    print(f"| **Up/Down Vol Ratio (20D)**| {vol.get('up_down_volume_ratio_20d', 1.0)}x | {'Buyer Dominance' if vol.get('up_down_volume_ratio_20d', 1.0) >= 1.2 else 'Neutral/Balanced'} | Institutional accumulation ratio |")
    print()
    print("#### Key Support & Resistance Levels")
    print(f"* **52-Week Range:** ${lvl['52_week_low']} - ${lvl['52_week_high']} (Current at {lvl['52_week_position_pct']}% of range)")
    print(f"* **20-Day Swing Extremes:** High: ${lvl['swing_high_20d']} | Low: ${lvl['swing_low_20d']}")
    print(f"* **Classic Pivots:** R2: ${lvl['classic_pivots']['R2']} | R1: ${lvl['classic_pivots']['R1']} | Pivot: ${lvl['classic_pivots']['P']} | S1: ${lvl['classic_pivots']['S1']} | S2: ${lvl['classic_pivots']['S2']}")
    
    if tp.get("upper_trendline_projection") or tp.get("lower_trendline_projection"):
        print()
        print("#### Automated Peak & Trough Trendline Projections")
        if tp.get("upper_trendline_projection"):
            u = tp["upper_trendline_projection"]
            print(f"* **Upper Resistance Line:** Connects {u['anchor_1']['date']} (${u['anchor_1']['price']}) -> {u['anchor_2']['date']} (${u['anchor_2']['price']})")
            print(f"  * Slope: ${u['slope_per_day']}/day | Current: ${u['current_level']} | Projected +5D: ${u['projected_target_plus_5d']} | +10D Target: ${u['projected_target_plus_10d']}")
        if tp.get("lower_trendline_projection"):
            l = tp["lower_trendline_projection"]
            print(f"* **Lower Support Line:** Connects {l['anchor_1']['date']} (${l['anchor_1']['price']}) -> {l['anchor_2']['date']} (${l['anchor_2']['price']})")
            print(f"  * Slope: ${l['slope_per_day']}/day | Current: ${l['current_level']} | Projected +5D: ${l['projected_target_plus_5d']} | +10D Target: ${l['projected_target_plus_10d']}")


def main():
    parser = argparse.ArgumentParser(description="Deterministic Stock Technical Analysis Engine")
    subparsers = parser.add_subparsers(dest="command", required=True)

    snap_p = subparsers.add_parser("snapshot", help="Generate complete technical snapshot")
    snap_p.add_argument("ticker", help="Stock ticker symbol (e.g. AAPL, NVDA)")
    snap_p.add_argument("--period", default="1y", help="Historical period (default: 1y)")
    snap_p.add_argument("--interval", default="1d", help="Interval (default: 1d)")
    snap_p.add_argument("--json", action="store_true", help="Output raw JSON")

    lvl_p = subparsers.add_parser("levels", help="Compute structural support, resistance, and pivot levels")
    lvl_p.add_argument("ticker", help="Stock ticker symbol")
    lvl_p.add_argument("--period", default="1y", help="Historical period")
    lvl_p.add_argument("--json", action="store_true", help="Output raw JSON")

    tr_p = subparsers.add_parser("trendlines", help="Compute automated peak and trough trendline projections")
    tr_p.add_argument("ticker", help="Stock ticker symbol")
    tr_p.add_argument("--period", default="1y", help="Historical period")
    tr_p.add_argument("--json", action="store_true", help="Output raw JSON")

    mtf_p = subparsers.add_parser("confluence", help="Evaluate multi-timeframe weekly tide vs daily wave alignment")
    mtf_p.add_argument("ticker", help="Stock ticker symbol")
    mtf_p.add_argument("--json", action="store_true", help="Output raw JSON")

    cmp_p = subparsers.add_parser("compare", help="Compare technical posture across multiple tickers")
    cmp_p.add_argument("tickers", nargs="+", help="List of tickers to compare")
    cmp_p.add_argument("--period", default="1y", help="Historical period")
    cmp_p.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    try:
        if args.command == "snapshot":
            data = get_snapshot(args.ticker, period=args.period, interval=args.interval)
            if args.json:
                print(json.dumps(data, indent=2))
            else:
                print_formatted_snapshot(data)
        elif args.command == "levels":
            data = get_snapshot(args.ticker, period=args.period)
            if args.json:
                print(json.dumps(data["levels"], indent=2))
            else:
                lvl = data["levels"]
                print(f"### Support & Resistance Levels: ${data['ticker']}")
                print(f"* **52-Week Range:** ${lvl['52_week_low']} - ${lvl['52_week_high']} ({lvl['52_week_position_pct']}% of range)")
                print(f"* **20-Day Swing Extremes:** High ${lvl['swing_high_20d']} | Low ${lvl['swing_low_20d']}")
                print("#### Classic Floor Pivots")
                for k, v in lvl["classic_pivots"].items():
                    print(f"* **{k}:** ${v}")
                print("#### Fibonacci Pivots")
                for k, v in lvl["fibonacci_pivots"].items():
                    print(f"* **{k}:** ${v}")
        elif args.command == "trendlines":
            data = get_snapshot(args.ticker, period=args.period)
            tp = data.get("trendline_projections", {})
            if args.json:
                print(json.dumps(tp, indent=2))
            else:
                print(f"### Peak & Trough Trendline Projections: ${data['ticker']}")
                u = tp.get("upper_trendline_projection")
                l = tp.get("lower_trendline_projection")
                if u:
                    print(f"* **Upper Ceiling ({u['type']}):** ${u['current_level']} (Projected +5D: ${u['projected_target_plus_5d']}, +10D: ${u['projected_target_plus_10d']})")
                if l:
                    print(f"* **Lower Support ({l['type']}):** ${l['current_level']} (Projected +5D: ${l['projected_target_plus_5d']}, +10D: ${l['projected_target_plus_10d']})")
        elif args.command == "confluence":
            data = get_snapshot(args.ticker)
            mtf = data.get("multi_timeframe_confluence", {})
            macro = data.get("macro_weekly_context", {})
            if args.json:
                print(json.dumps({"macro_weekly": macro, "confluence": mtf}, indent=2))
            else:
                print(f"### Multi-Timeframe Alignment Check: ${data['ticker']}")
                print(f"* **Rating:** **{mtf['conviction_tier']}**")
                print(f"* **Alignment:** {mtf['alignment_status']}")
                print(f"* **Weekly Macro Tide:** {macro.get('weekly_regime')} (40W SMA: ${macro.get('sma_40w')})")
                print(f"* **Daily Tactical Wave:** {data['trend']['regime']}")
                print(f"* **Tactical Guidance:** {mtf['tactical_guidance']}")
        elif args.command == "compare":
            data = compare_tickers(args.tickers, period=args.period)
            if args.json:
                print(json.dumps(data, indent=2))
            else:
                print(f"| Ticker | Price | 1D Change | Daily Regime | RSI(14) | MACD Status | vs 50D SMA | vs 200D SMA | Macro Alignment |")
                print(f"| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
                for item in data:
                    if "error" in item:
                        print(f"| {item['ticker']} | Error: {item['error']} | - | - | - | - | - | - | - |")
                    else:
                        print(f"| **{item['ticker']}** | ${item['price']} | {item['change_pct']:+.2f}% | {item['regime']} | {item['rsi14']} | {item['macd_status']} | {item['dist_sma50_pct']:+.1f}% | {item['dist_sma200_pct']:+.1f}% | **{item['macro_alignment']}** |")
    except Exception as e:
        sys.stderr.write(f"Error executing command: {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
