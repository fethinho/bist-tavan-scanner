import os
import requests
import yfinance as yf
from datetime import datetime, timezone, timedelta

IS_GH = os.environ.get('GITHUB_ACTIONS', 'false').lower() == 'true'
TZ_IST = timezone(timedelta(hours=3))

def now_ist(): return datetime.now(TZ_IST)
def now_str(): return now_ist().strftime('%d.%m.%Y %H:%M')
def now_ts(): return now_ist().strftime('%H:%M:%S')

BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')

def send_telegram(msg):
    try:
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
        requests.post(url, data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'HTML'}, timeout=15)
    except Exception as e:
        print(f'Telegram hata: {e}')

RAW = 'ACSEL,ADEL,ADESE,AEFES,AFYON,AGESA,AGHOL,AGROT,AHSGY,AKBNK,AKCNS,AKENR,AKFGY,AKFIS,AKFYE,AKGRT,AKHAN,AKMGY,AKSA,AKSEN,AKSGY,AKSUE,AKYHO,ALARK,ALBRK,ALCAR,ALCTL,ALFAS,ALGYO,ALKA,ALKIM,ALKLC,ALTNY,ALVES,ANELE,ANGEN,ANHYT,ANSGR,ARCLK,ARDYZ,ARENA,ARFYE,ARSAN,ARTMS,ARZUM,ASELS,ASGYO,ASTOR,ASUZU,ATAGY,ATAKP,ATATR,AVGYO,AVHOL,AVOD,AVTUR,AYDEM,AYGAZ,AZTEK,BAGFS,BAHKM,BAKAB,BALSU,BANVT,BARMA,BASGZ,BAYRK,BERA,BESLR,BESTE,BEYAZ,BFREN,BIENY,BIGEN,BIGTK,BIMAS,BINBN,BINHO,BIOEN,BIZIM,BJKAS,BLCYT,BLUME,BMSCH,BMSTL,BNTAS,BORLS,BORSK,BOSSA,BRISA,BRKO,BRKSN,BRKVY,BRLSM,BRMEN,BRSAN,BRYAT,BSOKE,BTCIM,BUCIM,BURCE,BURVA,BYDNR,CANTE,CCOLA,CELHA,CEMAS,CEMTS,CIMSA,CLEBI,CMBTN,CMENT,COSMO,CRFSA,CUSAN,CVKMD,CWENE,DARDL,DENGE,DERHL,DESA,DESPC,DEVA,DITAS,DMSAS,DOAS,DOHOL,DOKTA,DURDO,DYOBY,DZGYO,EBEBK,ECILC,ECZYT,EFORC,EGEEN,EGEPO,EGSER,EKGYO,EKIZ,EKSUN,ELITE,EMKEL,EMNIS,ENPLA,ENTRA,EPLAS,ERBOS,ERGE,ERSU,ESCAR,ESCOM,ESEN,ETILR,EUHOL,EUKYO,EUPWR,EUROB,EUROD,EXCLB,FENER,FORTE,FROTO,FZLGY,GARAN,GEDIK,GEDZA,GENIL,GENTS,GEREL,GESAN,GIPTA,GLCVY,GLRYH,GLYHO,GMTAS,GOLTS,GOODY,GOZDE,GRSEL,GRTRK,GSDDE,GSDHO,GSRAY,GUBRF,GWIND,HALKB,HATEK,HEDEF,HEKTS,HLGYO,HNSGY,HOROZ,HRKET,HTTBT,HUBVC,HUNER,HURGZ,ICBCT,IDEAS,IDGYO,IHLAS,IHLGM,IHYAY,INDES,INFO,INTEK,INTEM,INVEO,ISGSY,ISGYO,ISMEN,ISSEN,IZENR,IZMDC,IZTAR,JANTS,KARMA,KARSN,KAYSE,KBORU,KCAER,KCHOL,KENT,KERVN,KERVT,KGYO,KIMMR,KLGYO,KLKIM,KLMSN,KLRHO,KLSER,KLSYN,KMPUR,KNFRT,KOCMT,KONYA,KOPOL,KORDS,KOTON,KOZAA,KOZAL,KRDMA,KRDMB,KRDMD,KRPLS,KRSTL,KRTEK,KRVGD,KSTUR,KTLEV,KTSKR,KUTPO,KUYAS,LIDER,LIDFA,LILAK,LINK,LMKDC,LOGO,LUKSK,LYDHO,MAALT,MAGEN,MAHYT,MANAS,MARBL,MARKA,MARTI,MAVI,MEDTR,MEGAP,MERCN,MERIT,MERKO,METRO,METUR,MGROS,MIPAZ,MNDRS,MNDTR,MOBTL,MPARK,MRGYO,MRSHL,MSGYO,MTRKS,MTSAS,NATEN,NETAS,NIBAS,NTGAZ,NTHOL,NTTUR,NUGYO,NUHCM,OBASE,ODAS,ODINE,ONCSM,ONEN,ONRYT,ORCAY,ORGE,ORMA,OSMEN,OSTIM,OTKAR,OTTO,OYAKC,OYAYO,OYLUM,OYYAT,OZGYO,OZKGY,OZRDN,OZSUB,PAGYO,PAMEL,PAPIL,PARSN,PASEU,PATEK,PCILT,PEKGY,PENGD,PENTA,PETKM,PETUN,PGSUS,PINSU,PKART,PKENT,PLTUR,POLHO,POLTK,PRDGS,PRZMA,PSGYO,PTOFS,QNBFB,QNBFL,RALYH,RAYSG,REGAL,RGYAS,RNPOL,RODRG,ROYAL,RTALB,RUBNS,RYSAS,SAFKR,SAHOL,SAMAT,SANEL,SANFM,SANKO,SARKY,SASA,SAYAS,SDTTR,SEGMN,SEKFK,SEKUR,SELGD,SELVA,SEYKM,SILVR,SISE,SKBNK,SKTAS,SMART,SMRTG,SNGYO,SNKRN,SOKM,SONME,SRVGY,SUMAS,SUNTK,SURGY,SUWEN,TABGD,TARKM,TATEN,TATGD,TAVHL,TBORG,TCELL,TDGYO,TEKTU,TEZOL,THYAO,TILES,TLMAN,TMPOL,TNSAS,TOASO,TRCAS,TRGYO,TRILC,TSPOR,TTKOM,TTRAK,TUCLK,TUKAS,TURGZ,TURSG,TUPRS,ULUFA,ULUSE,ULUUN,UMPAS,UNLU,UNYEC,USAK,USDTR,UTPYA,VAKBN,VAKFN,VAKKO,VANGD,VBTYZ,VCYT,VERTU,VERUS,VESBE,VKGYO,VKFYO,VRGYO,YAPRK,YATAS,YATRS,YBTAS,YEOTK,YESIL,YGGYO,YKBNK,YKSLN,YONGA,YOYO,YPKYO,YUNSA,YYLGD,ZEDUR,ZOREN,ZRGYO'
BIST_TICKERS = sorted(RAW.split(','))

def run_scan():
    print(f'[{now_ts()} UTC+3] Tarama: {len(BIST_TICKERS)} hisse')
    tavan_list = []
    yakin_list = []
    batch_size = 50
    batches = [BIST_TICKERS[i:i+batch_size] for i in range(0, len(BIST_TICKERS), batch_size)]
    for batch in batches:
        symbols = [t+'.IS' for t in batch]
        try:
            data = yf.download(symbols, period='5d', interval='1d',
                               group_by='ticker', auto_adjust=True,
                               progress=False, threads=True)
            for ticker in batch:
                sym = ticker+'.IS'
                try:
                    df = data[sym] if len(batch) > 1 else data
                    df = df.dropna()
                    if len(df) < 2: continue
                    prev = float(df['Close'].iloc[-2])
                    curr = float(df['Close'].iloc[-1])
                    high = float(df['High'].iloc[-1])
                    vol  = int(df['Volume'].iloc[-1])
                    tavan = round(prev * 1.10, 2)
                    pct = (curr - prev) / prev * 100
                    tpct = (high - prev) / prev * 100
                    if tpct >= 9.5 or curr >= tavan * 0.999:
                        tavan_list.append({'t': ticker, 'c': curr, 'p': round(pct,2), 'v': vol})
                    elif pct >= 7.0:
                        yakin_list.append({'t': ticker, 'c': curr, 'p': round(pct,2), 'v': vol})
                except Exception:
                    continue
        except Exception as e:
            print(f'Batch hata: {e}')
    return tavan_list, yakin_list

def send_ozet(tavan_list, yakin_list):
    ts = now_str()
    if not tavan_list and not yakin_list:
        send_telegram(f'<b>BIST Tavan Tarama</b> {ts}\nSonuc yok.')
        return
    msg = f'<b>BIST TAVAN AVCI PRO</b> {ts}\n<b>{len(BIST_TICKERS)} hisse tarandy</b>\n\n'
    if tavan_list:
        msg += f'<b>TAVANDA ({len(tavan_list)})</b>\n'
        for h in sorted(tavan_list, key=lambda x: x["p"], reverse=True):
            msg += f'TAVAN {h["t"]} {h["c"]:.2f} ({h["p"]:+.2f}%) Vol:{h["v"]:,}\n'
        msg += '\n'
    if yakin_list:
        msg += f'<b>TAVANA YAKIN ({len(yakin_list)})</b>\n'
        for h in sorted(yakin_list, key=lambda x: x["p"], reverse=True)[:15]:
            msg += f'YAKIN {h["t"]} {h["c"]:.2f} ({h["p"]:+.2f}%)\n'
    if len(msg) > 4000: msg = msg[:4000] + '...'
    send_telegram(msg)
    print(f'Telegram: Tavan={len(tavan_list)}, Yakin={len(yakin_list)}')

if __name__ == '__main__':
    print(f'[{now_ts()} UTC+3] Basladi | GH Actions: {IS_GH}')
    tavan_list, yakin_list = run_scan()
    print(f'Tavan: {len(tavan_list)} | Yakin: {len(yakin_list)}')
    for h in tavan_list:
        print(f'  TAVAN {h["t"]} {h["p"]:+.2f}%')
    send_ozet(tavan_list, yakin_list)
    if not IS_GH:
        print('WebSocket: Colab modunda acik, GitHub Actions modunda KAPALI.')
    print(f'[{now_ts()} UTC+3] Tamamlandi.')
