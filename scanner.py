import os, sys, requests, base64, warnings
warnings.filterwarnings("ignore")
from datetime import datetime, timezone, timedelta
import yfinance as yf

IS_GH = os.environ.get("GITHUB_ACTIONS","false").lower()=="true"
BOT = os.environ.get("TELEGRAM_TOKEN","")
CID = os.environ.get("TELEGRAM_CHAT_ID","")
TZ  = timezone(timedelta(hours=3))

def tg(msg):
    try: requests.post(f"https://api.telegram.org/bot{BOT}/sendMessage",data={"chat_id":CID,"text":msg,"parse_mode":"HTML"},timeout=15)
    except Exception as e: print("TG err:",e)

now = datetime.now(TZ)
if now.weekday() in (5, 6):
        gun = "Cumartesi" if now.weekday()==5 else "Pazar"
        tg(f"<b>BIST TAVAN AVCI PRO</b>\nBorsa bugun kapali ({gun}). Tarama yapilmiyor.")
        import sys; sys.exit(0)
RAW="ACSEL,ADEL,ADESE,AEFES,AFYON,AGESA,AGHOL,AGROT,AHSGY,AKBNK,AKCNS,AKENR,AKFGY,AKFIS,AKFYE,AKGRT,AKHAN,AKMGY,AKSA,AKSEN,AKSGY,AKSUE,AKYHO,ALARK,ALBRK,ALCAR,ALCTL,ALFAS,ALGYO,ALKA,ALKIM,ALKLC,ALTNY,ALVES,ANELE,ANGEN,ANHYT,ANSGR,ARCLK,ARDYZ,ARENA,ARFYE,ARSAN,ARTMS,ARZUM,ASELS,ASGYO,ASTOR,ASUZU,ATAGY,ATAKP,ATATR,AVGYO,AVHOL,AVOD,AVTUR,AYDEM,AYGAZ,AZTEK,BAGFS,BAHKM,BAKAB,BALSU,BANVT,BARMA,BASGZ,BAYRK,BERA,BESLR,BESTE,BEYAZ,BFREN,BIENY,BIGEN,BIGTK,BIMAS,BINBN,BINHO,BIOEN,BIZIM,BJKAS,BLCYT,BLUME,BMSCH,BMSTL,BNTAS,BORLS,BORSK,BOSSA,BRISA,BRKO,BRKSN,BRKVY,BRLSM,BRMEN,BRSAN,BRYAT,BSOKE,BTCIM,BUCIM,BURCE,BURVA,BYDNR,CANTE,CCOLA,CELHA,CEMAS,CEMTS,CIMSA,CLEBI,CMBTN,CMENT,COSMO,CRFSA,CUSAN,CVKMD,CWENE,DARDL,DENGE,DERHL,DESA,DESPC,DEVA,DITAS,DMSAS,DOAS,DOHOL,DOKTA,DURDO,DYOBY,DZGYO,EBEBK,ECILC,ECZYT,EGEEN,EGEPO,EGSER,EKGYO,EKIZ,EKSUN,ELITE,EMKEL,EMNIS,ENPLA,ENTRA,EPLAS,ERBOS,ERGE,ERSU,ESCAR,ESCOM,ESEN,ETILR,EUHOL,EUKYO,EUPWR,EUROB,EUROD,EXCLB,FENER,FORTE,FROTO,FZLGY,GARAN,GEDIK,GEDZA,GENIL,GENTS,GEREL,GESAN,GIPTA,GLCVY,GLRYH,GLYHO,GMTAS,GOLTS,GOODY,GOZDE,GRSEL,GRTRK,GSDDE,GSDHO,GSRAY,GUBRF,GWIND,HALKB,HATEK,HEDEF,HEKTS,HLGYO,HNSGY,HOROZ,HRKET,HTTBT,HUBVC,HUNER,HURGZ,ICBCT,IDEAS,IDGYO,IHLAS,IHLGM,IHYAY,INDES,INFO,INTEK,INTEM,INVEO,ISGSY,ISGYO,ISMEN,ISSEN,IZENR,IZMDC,IZTAR,JANTS,KARMA,KARSN,KAYSE,KBORU,KCAER,KCHOL,KENT,KERVN,KERVT,KGYO,KIMMR,KLGYO,KLKIM,KLMSN,KLRHO,KLSER,KLSYN,KMPUR,KNFRT,KOCMT,KONYA,KOPOL,KORDS,KOTON,KOZAA,KOZAL,KRDMA,KRDMB,KRDMD,KRPLS,KRSTL,KRTEK,KRVGD,KSTUR,KTLEV,KTSKR,KUTPO,KUYAS,LIDER,LIDFA,LILAK,LINK,LMKDC,LOGO,LUKSK,LYDHO,MAALT,MAGEN,MAHYT,MANAS,MARBL,MARKA,MARTI,MAVI,MEDTR,MEGAP,MERCN,MERIT,MERKO,METRO,METUR,MGROS,MIPAZ,MNDRS,MNDTR,MOBTL,MPARK,MRGYO,MRSHL,MSGYO,MTRKS,MTSAS,NATEN,NETAS,NIBAS,NTGAZ,NTHOL,NTTUR,NUGYO,NUHCM,OBASE,ODAS,ODINE,ONCSM,ONEN,ONRYT,ORCAY,ORGE,ORMA,OSMEN,OSTIM,OTKAR,OTTO,OYAKC,OYAYO,OYLUM,OYYAT,OZGYO,OZKGY,OZRDN,OZSUB,PAGYO,PAMEL,PAPIL,PARSN,PASEU,PATEK,PCILT,PEKGY,PENGD,PENTA,PETKM,PETUN,PGSUS,PINSU,PKART,PKENT,PLTUR,POLHO,POLTK,PRDGS,PRZMA,PSGYO,PTOFS,QNBFB,QNBFL,RALYH,RAYSG,REGAL,RGYAS,RNPOL,RODRG,ROYAL,RTALB,RUBNS,RYSAS,SAFKR,SAHOL,SAMAT,SANEL,SANFM,SANKO,SARKY,SASA,SAYAS,SDTTR,SEGMN,SEKFK,SEKUR,SELGD,SELVA,SEYKM,SILVR,SISE,SKBNK,SKTAS,SMART,SMRTG,SNGYO,SNKRN,SOKM,SONME,SRVGY,SUMAS,SUNTK,SURGY,SUWEN,TABGD,TARKM,TATEN,TATGD,TAVHL,TBORG,TCELL,TDGYO,TEKTU,TEZOL,THYAO,TILES,TLMAN,TMPOL,TNSAS,TOASO,TRCAS,TRGYO,TRILC,TSPOR,TTKOM,TTRAK,TUCLK,TUKAS,TURGZ,TURSG,TUPRS,ULUFA,ULUSE,ULUUN,UMPAS,UNLU,UNYEC,USAK,USDTR,UTPYA,VAKBN,VAKFN,VAKKO,VANGD,VBTYZ,VCYT,VERTU,VERUS,VESBE,VKGYO,VKFYO,VRGYO,YAPRK,YATAS,YATRS,YBTAS,YEOTK,YESIL,YGGYO,YKBNK,YKSLN,YONGA,YOYO,YPKYO,YUNSA,YYLGD,ZEDUR,ZOREN,ZRGYO,ARASE,AVPGY,AYCES,AYEN,ARMGD,BIGCH,BRKO,CCOLA,CWENE,DOCO,DNISI,DOGUB,FONET,FORMT,GARFA,GLBMD,GOKTU,GZNMI,HDTMS,HKTM,HUBVC,ICUGS,IEYHO,IHAAS,IHEVA,IHGZT,IMASM,LRSHO,MACKO,MEKAG,MNVHO,OBAMS,OFSYM,PEGYO,PNLSN,PSDTC,RBLTUR,SILVR,TABGD"
TICKERS=sorted(set(RAW.split(",")))
print(f"Hisse: {len(TICKERS)}")

ts=datetime.now(TZ).strftime("%d.%m.%Y %H:%M")
tavan=[]; yakin=[]
batches=[TICKERS[i:i+50] for i in range(0,len(TICKERS),50)]
for batch in batches:
    syms=[t+".IS" for t in batch]
    try:
        d=yf.download(syms,period="5d",interval="1h",group_by="ticker",auto_adjust=True,progress=False,threads=True)
        for t in batch:
            s=t+".IS"
            try:
                df=d[s] if len(batch)>1 else d
                df=df.dropna()
                if len(df)<2: continue
                                    son_mum=df.index[-1]
                                try:
                                                        if son_mum.tzinfo is None: son_mum=son_mum.tz_localize("UTC").tz_convert(TZ)
                                                                                else: son_mum=son_mum.astimezone(TZ)
                                                                                                        if son_mum.date()!=now.date(): continue
                                                                                                                            except: pass
                prev=float(df["Close"].iloc[-2]); curr=float(df["Close"].iloc[-1])
                high=float(df["High"].iloc[-1]); vol=int(df["Volume"].iloc[-1])
                pct=(curr-prev)/prev*100; tpct=(high-prev)/prev*100
                if tpct>=9.5 or curr>=round(prev*1.10,2)*0.999:
                    tavan.append({"t":t,"c":curr,"p":round(pct,2),"v":vol})
                elif pct>=7.0:
                    yakin.append({"t":t,"c":curr,"p":round(pct,2),"v":vol})
            except: continue
    except Exception as e: print(f"batch hata:{e}")

print(f"Tavan:{len(tavan)} Yakin:{len(yakin)}")
msg=f"<b>BIST TAVAN AVCI PRO</b> {ts}
<b>{len(TICKERS)} hisse tarandy</b>

"
if tavan:
    msg+=f"<b>TAVANDA ({len(tavan)})</b>
"
    for h in sorted(tavan,key=lambda x:x["p"],reverse=True):
        msg+=f"TAVAN {h["t"]} {h["c"]:.2f} ({h["p"]:+.2f}%) Vol:{h["v"]:,}
"
    msg+="
"
if yakin:
    msg+=f"<b>TAVANA YAKIN ({len(yakin)})</b>
"
    for h in sorted(yakin,key=lambda x:x["p"],reverse=True)[:20]:
        msg+=f"YAKIN {h["t"]} {h["c"]:.2f} ({h["p"]:+.2f}%)
"
if not tavan and not yakin:
    msg+="Borsa kapali veya tavan yok."
if len(msg)>4000: msg=msg[:4000]+"..."
tg(msg)
print("TG gonderildi!")
if not IS_GH:
    print("WebSocket: Colab modunda acik, GH Actions modunda KAPALI.")
print(f"Tamamlandi.")
