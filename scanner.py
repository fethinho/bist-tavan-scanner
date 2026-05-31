import os
import sys
import time
import threading
import requests
import numpy as np
import pandas as pd
from datetime import datetime, timezone, timedelta

# ==========================================
# GITHUB ACTIONS modunda WebSocket KAPALI
# ==========================================
IS_GH = os.environ.get('GITHUB_ACTIONS', 'false').lower() == 'true'

# UTC+3 Istanbul
TZ_IST = timezone(timedelta(hours=3))

def now_ist():
    return datetime.now(TZ_IST)

def now_str():
    return now_ist().strftime('%d.%m.%Y %H:%M')

def now_ts():
    return now_ist().strftime('%H:%M:%S')

# ==========================================
# TELEGRAM
# ==========================================
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN', '8792118863:AAFvpNIuJ5nRipxe3oHIVHkx4gIhhWuqUjA')
CHAT_ID   = os.environ.get('TELEGRAM_CHAT_ID', '314746106')

def send_telegram(msg, parse_mode='HTML'):
    try:
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
        r = requests.post(url, data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': parse_mode}, timeout=15)
        return r.json()
    except Exception as e:
        print(f'Telegram hata: {e}')

# ==========================================
# BIST HISSE LISTESI - 560 HISSE
# ==========================================
BIST_TICKERS = sorted(list(set([
    'A1CAP','A1YEN','AAGYO','ACSEL','ADEL','ADESE','ADGYO','AEFES','AFYON','AGESA',
    'AGHOL','AGROT','AGYO','AHGAZ','AHSGY','AKBNK','AKCNS','AKENR','AKFGY','AKFIS',
    'AKFYE','AKGRT','AKHAN','AKMGY','AKSA','AKSEN','AKSGY','AKSUE','AKYHO','ALARK',
    'ALBRK','ALCAR','ALCTL','ALFAS','ALGYO','ALKA','ALKIM','ALKLC','ALTNY','ALVES',
    'ANELE','ANGEN','ANHYT','ANSGR','ARASE','ARCLK','ARDYZ','ARENA','ARFYE','ARMGD',
    'ARSAN','ARTMS','ARZUM','ASELS','ASGYO','ASTOR','ASUZU','ATAGY','ATAKP','ATATP',
    'ATATR','AVGYO','AVHOL','AVOD','AVPGY','AVTUR','AYCES','AYDEM','AYEN','AYGAZ',
    'AZTEK','BAGFS','BAHKM','BAKAB','BALSU','BANVT','BARMA','BASGZ','BAYRK','BEGYO',
    'BERA','BESLR','BESTE','BEYAZ','BFREN','BIENY','BIGCH','BIGEN','BIGTK','BIMAS',
    'BINBN','BINHO','BIOEN','BIZIM','BJKAS','BLCYT','BLUME','BMSCH','BMSTL','BNTAS',
    'BOBET','BORLS','BORSK','BOSSA','BRISA','BRKO','BRKSN','BRKVY','BRLSM','BRMEN',
    'BRSAN','BRYAT','BSOKE','BTCIM','BUCIM','BULGS','BURCE','BURVA','BVSAN','BYDNR',
    'CANTE','CCOLA','CELHA','CEMAS','CEMTS','CEOEM','CIMSA','CLEBI','CMBTN','CMENT',
    'CONSE','COSMO','CRDFA','CRFSA','CUSAN','CVKMD','CWENE','DAGHL','DAPGM','DARDL',
    'DENGE','DERHL','DESA','DESPC','DEVA','DGATE','DGNMO','DITAS','DMSAS','DNISI',
    'DOAS','DOCO','DOGUB','DOHOL','DOKTA','DURDO','DYOBY','DZGYO','EBEBK','ECILC',
    'ECZYT','EFORC','EGEEN','EGEPO','EGSER','EKGYO','EKIZ','EKSUN','ELITE','EMKEL',
    'EMNIS','ENPLA','ENTRA','EPLAS','ERBOS','ERCB','ERGE','ERSU','ESCAR','ESCOM',
    'ESEN','ETILR','ETYAT','EUHOL','EUKYO','EUPWR','EUREN','EUROB','EUROD','EUROS',
    'EXCLB','FENER','FENrb','FLAP','FMIZP','FONET','FORMT','FORTE','FROTO','FZLGY',
    'GARFA','GARAN','GEDIK','GEDZA','GENIL','GENTS','GEREL','GESAN','GIPTA','GLBMD',
    'GLCVY','GLRYH','GLYHO','GMTAS','GOKTU','GOLTS','GOODY','GOZDE','GRNYO','GRSEL',
    'GRTRK','GSDDE','GSDHO','GSRAY','GUBRF','GWIND','GZNMI','HALKB','HATEK','HDFGS',
    'HDTMS','HEDEF','HEKTS','HKTM','HLGYO','HNSGY','HOROZ','HRKET','HTTBT','HUBVC',
    'HUNER','HURGZ','ICBCT','ICUGS','IDEAS','IDGYO','IEYHO','IHAAS','IHEVA','IHGZT',
    'IHLAS','IHLGM','IHYAY','IMASM','INDES','INFO','INTEK','INTEM','INVEO','ISGSY',
    'ISGYO','ISMEN','ISSEN','IZENR','IZMDC','IZTAR','JANTS','KARMA','KARSN','KAYSE',
    'KBORU','KCAER','KCHOL','KENT','KERVN','KERVT','KFEIN','KGYO','KIMMR','KLGYO',
    'KLKIM','KLMSN','KLRHO','KLSER','KLSYN','KMPUR','KNFRT','KOCMT','KONYA','KOPOL',
    'KORDS','KOTON','KOZAA','KOZAL','KRDMA','KRDMB','KRDMD','KRPLS','KRSTL','KRTEK',
    'KRVGD','KSTUR','KTLEV','KTSKR','KUTPO','KUYAS','KZBGY','LIDER','LIDFA','LILAK',
    'LINK','LMKDC','LOGO','LRSHO','LUKSK','LYDHO','MAALT','MACKO','MAGEN','MAHYT',
    'MANAS','MARBL','MARKA','MARTI','MAVI','MEDTR','MEGAP','MEKAG','MERCN','MERIT',
    'MERKO','METRO','METUR','MGROS','MIPAZ','MNDRS','MNDTR','MNVHO','MOBTL','MPARK',
    'MRGYO','MRSHL','MSGYO','MTRKS','MTSAS','NATEN','NETAS','NIBAS','NTGAZ','NTHOL',
    'NTTUR','NUGYO','NUHCM','OBAMS','OBASE','ODAS','ODINE','OFSYM','ONCSM','ONEN',
    'ONRYT','ORCAY','ORGE','ORMA','OSMEN','OSTIM','OTKAR','OTTO','OYAKC','OYAYO',
    'OYLUM','OYYAT','OZGYO','OZKGY','OZRDN','OZSUB','PAGYO','PAMEL','PAPIL','PARSN',
    'PASEU','PATEK','PCILT','PEGYO','PEKGY','PENGD','PENTA','PETKM','PETUN','PGSUS',
    'PINSU','PKART','PKENT','PLTUR','PNLSN','POLHO','POLTK','PRDGS','PRZMA','PSDTC',
    'PSGYO','PTOFS','QNBFB','QNBFL','RALYH','RAYSG','RBLTUR','REGAL','RGYAS','RNPOL',
    'RODRG','ROYAL','RTALB','RUBNS','RYSAS','SAFKR','SAHOL','SAMAT','SANEL','SANFM',
    'SANKO','SARKY','SASA','SAYAS','SDTTR','SEGMN','SEKFK','SEKUR','SELGD','SELVA',
    'SEYKM','SILVR','SISE','SKBNK','SKTAS','SMART','SMRTG','SNGYO','SNKRN','SOKM',
    'SONME','SRVGY','SUMAS','SUNTK','SURGY','SUWEN','TABGD','TARKM','TATEN','TATGD',
    'TAVHL','TBORG','TCELL','TDGYO','TEKTU','TEZOL','THYAO','TILES','TLMAN','TMPOL',
    'TNSAS','TOASO','TRCAS','TRGYO','TRILC','TSPOR','TTKOM','TTRAK','TUCLK','TUKAS',
    'TURGZ','TURSG','TUREX','TUPRS','ULUFA','ULUSE','ULUUN','UMPAS','UNLU','UNYEC',
    'USAK','USDTR','UTPYA','UYGN','VAKBN','VAKFN','VAKKO','VANGD','VBTYZ','VCYT',
    'VERTU','VERUS','VESBE','VKGYO','VKFYO','VRGYO','YAPRK','YATAS','YATRS','YBTAS',
    'YEOTK','YESIL','YGGYO','YKBNK','YKSLN','YONGA','YOYO','YPKYO','YUNSA','YYLGD',
    'ZEDUR','ZOREN','ZRGYO'
]))

# ==========================================
# YFINANCE ILE VERI CEK
# ==========================================
import yfinance as yf

def get_tickers_yf(tickers, period='5d', interval='1d'):
    symbols = [t + '.IS' for t in tickers]
    try:
        data = yf.download(symbols, period=period, interval=interval,
                           group_by='ticker', auto_adjust=True, progress=False, threads=True)
        return data
    except Exception as e:
        print(f'veri hata: {e}')
        return None

def get_daily_limit(prev_close):
    """BIST tavan/taban = onceki kapanis +/- %10"""
    tavan = round(prev_close * 1.10, 2)
    taban = round(prev_close * 0.90, 2)
    return tavan, taban

# ==========================================
# ANA TARAMA
# ==========================================
def run_scan():
    print(f'[{now_ts()} UTC+3] Tarama basliyor... {len(BIST_TICKERS)} hisse')
    
    tavan_list = []
    yakin_tavan_list = []
    
    # Batch halinde cek (50'lik gruplar)
    batch_size = 50
    batches = [BIST_TICKERS[i:i+batch_size] for i in range(0, len(BIST_TICKERS), batch_size)]
    
    for batch in batches:
        symbols = [t + '.IS' for t in batch]
        try:
            data = yf.download(symbols, period='5d', interval='1d',
                               group_by='ticker', auto_adjust=True,
                               progress=False, threads=True)
            
            for ticker in batch:
                sym = ticker + '.IS'
                try:
                    if len(batch) == 1:
                        df = data
                    else:
                        if sym not in data.columns.get_level_values(0):
                            continue
                        df = data[sym]
                    
                    df = df.dropna()
                    if len(df) < 2:
                        continue
                    
                    prev_close = float(df['Close'].iloc[-2])
                    curr_close = float(df['Close'].iloc[-1])
                    curr_high  = float(df['High'].iloc[-1])
                    curr_open  = float(df['Open'].iloc[-1])
                    volume     = float(df['Volume'].iloc[-1])
                    
                    tavan, taban = get_daily_limit(prev_close)
                    
                    pct = ((curr_close - prev_close) / prev_close) * 100
                    tavan_pct = ((curr_high - prev_close) / prev_close) * 100
                    
                    # Tavanda mi? (%9.5 ve uzeri)
                    if tavan_pct >= 9.5 or curr_close >= tavan * 0.999:
                        tavan_list.append({
                            'ticker': ticker,
                            'prev_close': prev_close,
                            'close': curr_close,
                            'high': curr_high,
                            'tavan': tavan,
                            'pct': round(pct, 2),
                            'tavan_pct': round(tavan_pct, 2),
                            'volume': int(volume)
                        })
                    # Tavana yakin mi? (%7-9.5)
                    elif pct >= 7.0:
                        yakin_tavan_list.append({
                            'ticker': ticker,
                            'prev_close': prev_close,
                            'close': curr_close,
                            'tavan': tavan,
                            'pct': round(pct, 2),
                            'volume': int(volume)
                        })
                        
                except Exception:
                    continue
                    
        except Exception as e:
            print(f'Batch hata {batch[0]}: {e}')
            continue
    
    return tavan_list, yakin_tavan_list

# ==========================================
# TELEGRAM OZET GONDER
# ==========================================
def send_ozet(tavan_list, yakin_tavan_list):
    ts = now_str()
    
    if not tavan_list and not yakin_tavan_list:
        msg = f'<b>BIST Tavan Tarama</b> {ts}\n\nTavanda hisse yok.'
        send_telegram(msg)
        return
    
    # TAVAN listesi
    msg = f'<b>BIST TAVAN AVCI PRO</b> {ts}\n'
    msg += f'<b>Toplam Tarama: {len(BIST_TICKERS)} hisse</b>\n\n'
    
    if tavan_list:
        msg += f'<b>TAVANDA ({len(tavan_list)} hisse)</b>\n'
        for h in sorted(tavan_list, key=lambda x: x['pct'], reverse=True):
            msg += f'TAVAN {h["ticker"]} {h["close"]:.2f} ({h["pct"]:+.2f}%) Vol:{h["volume"]:,}\n'
        msg += '\n'
    
    if yakin_tavan_list:
        msg += f'<b>TAVANA YAKIN ({len(yakin_tavan_list)} hisse)</b>\n'
        for h in sorted(yakin_tavan_list, key=lambda x: x['pct'], reverse=True)[:20]:
            msg += f'YAKIN {h["ticker"]} {h["close"]:.2f} ({h["pct"]:+.2f}%)\n'
    
    # 4096 karakter siniri
    if len(msg) > 4000:
        msg = msg[:4000] + '...'
    
    send_telegram(msg)
    print(f'Telegram gonderildi. Tavan: {len(tavan_list)}, Yakin: {len(yakin_tavan_list)}')

# ==========================================
# MAIN
# ==========================================
if __name__ == '__main__':
    print(f'[{now_ts()} UTC+3] BIST Tavan Scanner basliyor')
    print(f'GitHub Actions modu: {IS_GH}')
    
    tavan_list, yakin_tavan_list = run_scan()
    
    print(f'Tavan: {len(tavan_list)} | Yakin: {len(yakin_tavan_list)}')
    for h in tavan_list:
        print(f'  TAVAN {h["ticker"]} {h["pct"]:+.2f}%')
    
    send_ozet(tavan_list, yakin_tavan_list)
    
    # WebSocket: GitHub Actions'ta KAPALI
    if not IS_GH:
        print('WebSocket canli stream baslatiliyor...')
        # Colab'da canli takip icin WebSocket baslat
        try:
            import websocket
            WS_SYMBOLS = [h['ticker'] + '.IS' for h in tavan_list[:20]]
            print(f'WebSocket: {WS_SYMBOLS}')
            # ... canli stream kodu buraya
        except Exception as e:
            print(f'WebSocket hata: {e}')
    else:
        print('[GitHub Actions] WebSocket KAPALI - sadece tarama yapildi.')
    
    print(f'[{now_ts()} UTC+3] Tamamlandi.')
