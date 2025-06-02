from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

font_path = "C:\\Windows\\Fonts\\CascadiaMono.ttf"
bold_path = "C:\\Windows\\Fonts\\NotoSansHebrew-Bold.ttf"


font_name = "Normal"
pdfmetrics.registerFont(TTFont(font_name, font_path))

bold_name = "Bold"
pdfmetrics.registerFont(TTFont(bold_name, bold_path))

# PDF fájl létrehozása
pdf_path = "Romantika_javitott_megoldas.pdf"
c = canvas.Canvas(pdf_path, pagesize=A4)
width, height = A4

# Segédfüggvény: többsoros szöveg kiírása
def draw_paragraph(text, x, y, max_width):
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.enums import TA_JUSTIFY
    styleSheet = getSampleStyleSheet()
    style = styleSheet['BodyText']
    style.alignment = TA_JUSTIFY
    style.fontName = font_name
    style.fontSize = 10
    para = Paragraph(text, style)
    para_width, para_height = para.wrap(max_width, 1000)
    para.drawOn(c, x, y - para_height)
    return para_height

# Oldal tetején margó
x_margin = 20 * mm
y_margin = 20 * mm
current_y = height - y_margin

# Cím
c.setFont(bold_name, 14)
c.drawString(x_margin, current_y, "ZIR_7-8_2025 megoldások - Ancsin Ádám")
current_y -= 10 * mm

# 1. FELADAT
c.setFont(bold_name, 12)
c.drawString(x_margin, current_y, "1. FELADAT: Liszt Ferenc magyarsága és hazatérése Magyarországra")
current_y -= 8 * mm

c.setFont(bold_name, 11)
c.drawString(x_margin, current_y, "1.1. Terek, utcák és parkok 1838-ban:")
current_y -= 6 * mm

c.setFont(font_name, 10)
lines = [
    "- Terek:",
    "  • Ferenciek tere",
    "  • Széna tér",
    "  • Kálvin tér",
    "",
    "- Utcák:",
    "  • Hatvani utca (ma Kossuth Lajos utca)",
    "  • Haris köz",
    "  • Szerb utca",
    "",
    "- Parkok:",
    "  • Orczy-kert",
    "  • Városliget",
    "  • Népkert (ma Népliget)",
]
for line in lines:
    c.drawString(x_margin + 5 * mm, current_y, line)
    current_y -= 5 * mm

current_y -= 3 * mm
c.setFont(bold_name, 11)
c.drawString(x_margin, current_y, "1.2. Hol ért véget 1838-ban Pest?")
current_y -= 6 * mm

c.setFont(font_name, 10)
lines = [
    "A korabeli városhatár nagyjából a következő vonalak mentén húzódott:",
    "  1. Múzeum körút",
    "  2. Vámház körút",
    "  3. Orczy-kert",
]
for line in lines:
    c.drawString(x_margin + 5 * mm, current_y, line)
    current_y -= 5 * mm

current_y -= 3 * mm
c.setFont(bold_name, 11)
c.drawString(x_margin, current_y, "1.3. Területek az árvízkor – áldozatul esett vs. szárazon maradt")
current_y -= 6 * mm

c.setFont(font_name, 10)
lines = [
    "- Áldozatul estek:",
    "  • Belváros (Duna-parti részek)",
    "  • Lipótváros",
    "  • Józsefváros",
    "",
    "- Megúszták szárazon:",
    "  • Várnegyed",
    "  • Gellérthegy",
    "  • Rózsadomb"
]
for line in lines:
    c.drawString(x_margin + 5 * mm, current_y, line)
    current_y -= 5 * mm

# Új oldal, ha szükséges
if current_y < 50 * mm:
    c.showPage()
    current_y = height - y_margin


current_y -= 5*mm *2


# 2. FELADAT
c.setFont(bold_name, 12)
c.drawString(x_margin, current_y, "2. FELADAT: Levél értelmezése és kérdések megválaszolása")
current_y -= 8 * mm

# 2.1
c.setFont(bold_name, 11)
c.drawString(x_margin, current_y, "2.1. Hogyan definiálja Liszt a „haza” fogalmát?")
current_y -= 4 * mm
c.setFont(font_name, 10)
haza_text = "Liszt számára a „haza” nem pusztán földrajzi hely, hanem az a közösség és szellemi tér, amelyhez kötődik, és amelyet szolgálni szeretne."
paragraph_height = draw_paragraph(haza_text, x_margin + 5 * mm, current_y, width - 2* x_margin - 10 * mm)
current_y -= paragraph_height + 4 * mm

current_y -= 5*mm *1

# 2.2
c.setFont(bold_name, 11)
c.drawString(x_margin, current_y, "2.2. Melyik két ország között kell Lisztnek „hazát” választania?")
current_y -= 4 * mm
c.setFont(font_name, 10)
orszag_text = "Lisztnek Magyarország és Franciaország között kellett döntenie: anyanyelvi, családi kötődés szempontjából Magyarország volt a haza, ugyanakkor korábban Párizsban töltötte fiatalkorát, tehát a művészi pályája is Franciaországhoz kapcsolta."
paragraph_height = draw_paragraph(orszag_text, x_margin + 5 * mm, current_y, width - 2* x_margin - 10 * mm)
current_y -= paragraph_height + 4 * mm

current_y -= 5*mm *1

# 2.3
c.setFont(bold_name, 11)
c.drawString(x_margin, current_y, "2.3. Mi jellemzi a fiatalságot Liszt szerint?")
current_y -= 4 * mm
c.setFont(font_name, 10)
fiatal_text = "Liszt úgy látja, hogy a fiatalságot az álmok, vágyak, örömök és bánatok intenzív megélése jellemzi: ez az életszakasz tele van szenvedélyekkel, lelkesedéssel és egyfajta idealizmussal."
paragraph_height = draw_paragraph(fiatal_text, x_margin + 5 * mm, current_y, width - 2* x_margin - 10 * mm)
current_y -= paragraph_height + 4 * mm

current_y -= 5*mm *1

c.showPage()
current_y = height - y_margin

# 2.4
c.setFont(bold_name, 11)
c.drawString(x_margin, current_y, "2.4. Egyetértesz-e Liszt jellemzésével, amelyet a fiatalságról ír? Fejtsd ki!")
current_y -= 4 * mm
c.setFont(font_name, 10)
egye_text = ("Véleményem szerint Liszt megfogalmazása találó, hiszen a fiatalságot valóban jellemzi "
           "az erős érzelmi hullámzás és az a hit, hogy az ember képes nagy dolgokat véghezvinni. "
           "Sokan átéljük, hogy a tanulás, a szerelem és az önismeret ebben az időszakban rendkívül "
           "intenzív, ezért úgy gondolom, hogy Liszt meglátása hitelesen ragadja meg a fiatal kor sajátosságait.")
paragraph_height = draw_paragraph(egye_text, x_margin + 5 * mm, current_y, width - 2* x_margin - 10 * mm)
current_y -= paragraph_height + 4 * mm

current_y -= 5*mm *1

# 2.5
c.setFont(bold_name, 11)
c.drawString(x_margin, current_y, "2.5. Hogyan jellemzi a magyarokat Liszt Ferenc?")
current_y -= 4 * mm
c.setFont(font_name, 10)
magy_text = "Liszt a magyarokat büszke, szenvedélyes és a kultúrájukra mélyen kötődő nemzetként ábrázolja, akik az évszázados elnyomás ellenére is megőrizték nemzeti identitásukat és küzdenek a szabadságukért."
paragraph_height = draw_paragraph(magy_text, x_margin + 5 * mm, current_y, width - 2* x_margin - 10 * mm)
current_y -= paragraph_height + 4 * mm

current_y -= 5*mm *1

# 2.6
c.setFont(bold_name, 11)
c.drawString(x_margin, current_y, "2.6. Változott-e a magyarság Liszt kora óta, vagy ma is igaz az általa leírt?")
current_y -= 4 * mm
c.setFont(font_name, 10)
valtoz_text = ("Véleményem szerint a magyarság sokat változott Liszt óta (átélte a két világháborút, "
              "a kommunista rendszert, majd a rendszerváltást), ugyanakkor az a belső tartás és "
              "a kultúránk iránti elkötelezettség, amit Liszt érzékelt, ma is jelen van. Ugyanakkor a "
              "nyitottság és a globalizáció hatására sok új érték is megjelent. Összességében az ő korabeli "
              "és a mai magyar identitás között van folytonosság is, de a körülmények teljesen mások.")
paragraph_height = draw_paragraph(valtoz_text, x_margin + 5 * mm, current_y, width - 2* x_margin - 10 * mm)
current_y -= paragraph_height + 4 * mm

current_y -= 5*mm *1

# 2.7
c.setFont(bold_name, 11)
c.drawString(x_margin, current_y, "2.7. Milyen jellegzetes magyar vidékeket említ Liszt és te milyeneket mutatnál be?")
current_y -= 6 * mm
c.setFont(font_name, 10)
lines = [
    "- Liszt által említett vidékek:",
    "  1. Alföld (végtelen síkság, puszta)",
    "  2. Erdély (hegyek, mély erdők, népzene-költészet)",
    "",
    "- Én, mint személyes ajánlás:",
    "  • Balaton és Balaton-felvidék (a „magyar tenger”)",
    "  • Tokaj–Hegyalja (borvidék, dombok, történelmi pincék)",
    "  • Hortobágy (puszta, pásztorélet, gulyáskultúra)",
    "  • Dunakanyar (Duna kanyarulata), Visegrád, Esztergom)",
]
for line in lines:
    c.drawString(x_margin + 5 * mm, current_y, line)
    current_y -= 5 * mm

current_y -= 5*mm *2

# Új oldal, ha szükséges
if current_y < 60 * mm:
    c.showPage()
    current_y = height - y_margin

# 3. FELADAT
c.setFont(bold_name, 12)
c.drawString(x_margin, current_y, "3. FELADAT: Zenei elemzés")
current_y -= 8 * mm

# 3.A
c.setFont(bold_name, 11)
c.drawString(x_margin, current_y, "3.A. Melyik felvételen hallható „vízizene”?")
current_y -= 4 * mm
c.setFont(font_name, 10)
viz_text = ("• Smetana: Moldva (Má Vltava) – az 1-es számú felvétel, a folyó áramlását zenekari eszközökkel ábrázolja.\n"
            "• Liszt: A wallenstadti tónál (Zarándokévek I. kötet, 2. darab) – a 3-as számú felvétel, zongorára írt „vízizene”.")
paragraph_height = draw_paragraph(viz_text, x_margin + 5 * mm, current_y, width - 2* x_margin - 10 * mm)
current_y -= paragraph_height + 4 * mm

current_y -= 5*mm *1

# 3.B
c.setFont(bold_name, 11)
c.drawString(x_margin, current_y, "3.B. Liszt: Hősi sirató – formálisan: Bevezetés–A–B–A")
current_y -= 4 * mm
c.setFont(font_name, 10)
lines = [
    "1. Bevezetés: gyászinduló, bánat, harangozás, vontatott menet, pontozott ritmusok.",
    "2. A-első: gyász, bánat, remény halk felsejlése („sírva-vigadó” gyász-remény kettősség).",
    "3. B: düh, elszántság, fanfár-motívumok, harci lendület („vigadó” rész).",
    "4. A-újra: gyász, fájdalom, beletörődés (rövidített gyászmotívum).",
]
for line in lines:
    c.drawString(x_margin + 5 * mm, current_y, line)
    current_y -= 5 * mm

current_y -= 5*mm *1

# Új oldal, ha szükséges
if current_y < 60 * mm:
    c.showPage()
    current_y = height - y_margin

# 4. FELADAT
c.setFont(bold_name, 12)
c.drawString(x_margin, current_y, "4. FELADAT: Noktürn")
current_y -= 8 * mm

# 4.1
c.setFont(bold_name, 11)
c.drawString(x_margin, current_y, "4.1. Mit jelent a „noktürn” kifejezés a zenében?")
current_y -= 4 * mm
c.setFont(font_name, 10)
not1_text = ("A „noktürn” (francia: nocturne) eredetileg éjszakai muzsikát jelentett, romantikus értelemben "
             "egytételes, lírai zongoradarabot takar, amely az éjszaka, a melankólia és a magány hangulatát idézi.")
paragraph_height = draw_paragraph(not1_text, x_margin + 5 * mm, current_y, width - 2* x_margin - 10 * mm)
current_y -= paragraph_height + 4 * mm

current_y -= 5*mm *1

# 4.2
c.setFont(bold_name, 11)
c.drawString(x_margin, current_y, "4.2. Ki írt számos noktürnt?")
current_y -= 4 * mm
c.setFont(font_name, 10)
not2_text = "Frédéric Chopin komponált a legtöbbet: 21 zongorára írt nocturne (pl. op. 9/2), amelyek a romantikus éjhangulat esszenciáját adják."
paragraph_height = draw_paragraph(not2_text, x_margin + 5 * mm, current_y, width - 2* x_margin - 10 * mm)
current_y -= paragraph_height + 4 * mm

current_y -= 5*mm *1

# 4.3
c.setFont(bold_name, 11)
c.drawString(x_margin, current_y, "4.3. Melyik (a feladatlapban is bemutatott) noktürn zenéjét használták fel az alábbi mesében?")
current_y -= 4 * mm
c.setFont(font_name, 10)
not3_text = "A mesében Chopin Op. 9 No. 2-es Nocturne zenéjét (E-flat major) alkalmazták aláfestésként."
paragraph_height = draw_paragraph(not3_text, x_margin + 5 * mm, current_y, width - 2* x_margin - 10 * mm)
current_y -= paragraph_height + 4 * mm

current_y -= 5*mm *1

# 4.4
c.setFont(bold_name, 11)
c.drawString(x_margin, current_y, "4.4. Miért használható a noktürn más tartalom aláfestésére is?")
current_y -= 4 * mm
c.setFont(font_name, 10)
not4_text = ("A noktürn lírai, meditatív hangulata univerzálisan alkalmazható: a lassan hömpölygő, finom dallamok "
             "könnyen kiemelik a jelenet érzelmi mélységét, legyen szó romantikus, melankolikus vagy békés jelenetről. "
             "Így nem csak „éjszakai” képekhez, hanem bármilyen belső, elmélkedő hangulathoz illik.")
paragraph_height = draw_paragraph(not4_text, x_margin + 5 * mm, current_y, width - 2* x_margin - 10 * mm)
current_y -= paragraph_height + 4 * mm

current_y -= 5*mm *3

# Új oldal, ha szükséges
if current_y < 60 * mm:
    c.showPage()
    current_y = height - y_margin

# 5. FELADAT
c.setFont(bold_name, 12)
c.drawString(x_margin, current_y, "5. FELADAT: Zenei művek jellemzése")
current_y -= 8 * mm

# 5.1
c.setFont(bold_name, 11)
c.drawString(x_margin, current_y, "5.1. Antonín Dvořák – Nocturne, Op. 40")
current_y -= 8 * mm
c.setFont(font_name, 10)
lines = [
    "- Műfaji háttér: Egytételes, romantikus zongoranoktürn.",
    "",
    "- Hangulatfestés: Lírai, álmodozó, „éjszakai” karakter.",
    "",
    "- Szerkezet: Díszített dallam és finom akkordkíséret jellemzi, amelyben a",
    "             hármashangzat- és kvartugrások a csendes melankóliát hozza elő.",
    "",
    "- Karakter: Nosztalgikus, bensőséges, mintha a hallgató a holdfényben merengne.",
    ""
]
for line in lines:
    c.drawString(x_margin + 5 * mm, current_y, line)
    current_y -= 5 * mm

current_y -= 5*mm *1

# 5.2
c.setFont(bold_name, 11)
c.drawString(x_margin, current_y, "5.2. Gustav Mahler – 1. szimfónia, I. tétel")
current_y -= 8 * mm
c.setFont(font_name, 10)
lines = [
    "- Műfaji háttér: Kései romantikus, nagy léptékű szimfónia.",
    "",
    "- Hangulatfestés, programosság: Bár Mahler nem jelölt konkrét programot,",
    "                                a tételben a természet („erdőhangok”), a",
    "                                pásztorhangszer és az emberi sors",
    "                                allegóriája jelenik meg.",
    "",
    "- Szerkezet: Lassú bevezetés (Adagio: erdő-misztérium), majd élénkebb rész",
    "             (Allegro: ébresztő), végül diadalmas zárás (Tempo I visszatérése).",
    "",
    "- Zenei eszközök: Határozott ritmusú fúvósok, Schubert-idézet (tollajkász‐hangzás),",
    "                  népdalszerű témák, dinamikai váltások, gazdag hangszerelés.",
    "",
    "- Karakter: A természet és az ember története, végül",
    "            melankolikus–diadalmas kettősségben zárul.",
    ""
]
for line in lines:
    c.drawString(x_margin + 5 * mm, current_y, line)
    current_y -= 5 * mm

# Menti a PDF-et
c.save()

# Link a letöltéshez
print(f"[Letöltés: Romantika_javitott_megoldas.pdf](sandbox:{pdf_path})")
