"""Add a focused batch of historic, amphibious, kit, aerobatic and glider aircraft."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLEET_PATH = ROOT / "data" / "fleet.json"


def tr(zh: str, en: str, ja: str) -> dict[str, str]:
    return {"zh": zh, "en": en, "ja": ja}


CATEGORIES = {
    "supersonic": tr("超音速客機", "Supersonic airliner", "超音速旅客機"),
    "amphibian": tr("水陸兩用機", "Amphibious aircraft", "水陸両用機"),
    "sport": tr("輕型運動機", "Light sport aircraft", "軽量スポーツ機"),
    "kit": tr("套件機", "Kit aircraft", "キット機"),
    "aerobatic": tr("特技機", "Aerobatic aircraft", "曲技飛行機"),
    "glider": tr("滑翔機", "Glider", "グライダー"),
}


# id, name, maker, category, first flight, span, seats, range/endurance, engine,
# ICAO, zh/en/ja summary, official source
AIRCRAFT = [
    ("concorde", "Aérospatiale / BAC Concorde", "Aérospatiale / BAC", "supersonic", "1969", "25.6 m", "100", "7,223 km (3,900 nmi)", "4 × Rolls-Royce/Snecma Olympus 593", "CONC", "唯一投入定期跨大西洋客運的超音速客機，以三角翼、可下垂機鼻與約 Mach 2 巡航聞名。", "The supersonic airliner that operated scheduled transatlantic service, recognizable by its delta wing, droop nose, and roughly Mach 2 cruise.", "定期大西洋横断便に就航した超音速旅客機で、デルタ翼、可動式機首、約マッハ2の巡航で知られます。", "https://heritage.baesystems.com/page/bac-concorde"),
    ("icona5", "ICON A5", "ICON Aircraft", "amphibian", "2008", "10.61 m", "2", "791 km (427 nmi)", "1 × Rotax 912 iS Sport", "", "可折疊機翼、具整機降落傘與抗尾旋機體的雙座輕型水陸兩用機。", "A two-seat light amphibian with folding wings, a whole-aircraft parachute, and a spin-resistant airframe.", "折り畳み翼、機体パラシュート、耐スピン機体を備える2座軽量水陸両用機です。", "https://www.iconaircraft.com/a5/"),
    ("xcub", "CubCrafters XCub / NXCub", "CubCrafters", "sport", "2016", "10.46 m", "2", "1,287 km (800 mi)", "1 × Lycoming O-360-C1G / CubCrafters CC393i", "CC19", "具短場性能、高有效載重與尾輪／前三點起落架選項的現代越野機。", "A modern backcountry aircraft combining STOL performance, useful load, and tailwheel or nosewheel configurations.", "STOL性能と高い有効搭載量を備え、尾輪式または前輪式を選べる現代的なブッシュプレーンです。", "https://cubcrafters.com/xcub"),
    ("carboncub", "CubCrafters Carbon Cub SS", "CubCrafters", "sport", "—", "10.46 m", "2", "—", "1 × CubCrafters CC340", "CC11", "以低重量、高功率與極短場起降能力為核心的現代化 Cub 系列輕型運動機。", "A modern Cub-family light sport aircraft centered on low weight, high power, and very short-field performance.", "軽量、高出力、極めて短い離着陸性能を特徴とする現代的なCub系軽量スポーツ機です。", "https://cubcrafters.com/"),
    ("rv10", "Van's Aircraft RV-10", "Van's Aircraft", "kit", "2003", "9.68 m", "4", "—", "1 × Lycoming IO-540", "RV10", "可載四名成人、採低翼與前三點起落架的高速旅行套件機。", "A fast four-adult touring kit aircraft with a low wing and tricycle landing gear.", "大人4名を搭載できる低翼・前輪式の高速旅行用キット機です。", "https://www.vansaircraft.com/rv-10/"),
    ("rv14", "Van's Aircraft RV-14 / 14A", "Van's Aircraft", "kit", "2012", "8.23 m", "2", "—", "1 × Lycoming IO-390", "RV14", "寬敞雙座、可執行基礎特技飛行的現代低翼旅行套件機。", "A roomy modern two-seat low-wing touring kit aircraft capable of basic aerobatics.", "広い2座キャビンを持ち、基本曲技飛行にも対応する現代的な低翼旅行用キット機です。", "https://www.vansaircraft.com/rv-14/"),
    ("sling2", "Sling 2", "Sling Aircraft", "kit", "2008", "9.17 m", "2", "1,537 km (830 nmi)", "1 × Rotax 912 iS", "SLG2", "全金屬雙座旅行與訓練機，可採套件或工廠協助建造。", "An all-metal two-seat touring and training aircraft offered as a kit or factory-assisted build.", "キットまたは工場支援製作で提供される全金属製2座旅行・訓練機です。", "https://slingaircraft.com/aircraft/sling-2/"),
    ("slingtsi", "Sling TSi", "Sling Aircraft", "kit", "2018", "9.54 m", "4", "1,852 km (1,000 nmi)", "1 × Rotax 916 iS", "", "具四座、渦輪增壓動力與長航程的高性能全金屬套件機。", "A high-performance all-metal four-seat kit aircraft with turbocharged power and long range.", "4座、ターボ過給動力、長航続距離を備える高性能全金属キット機です。", "https://slingaircraft.com/aircraft/sling-tsi/"),
    ("velise", "Pipistrel Velis Electro", "Pipistrel", "sport", "—", "10.70 m", "2", "最長 56 min", "1 × Pipistrel E-811 electric motor", "", "全球首款取得型別認證的電動飛機，主要用於安靜、低營運成本的日間目視飛行訓練。", "The world's first type-certified electric aircraft, aimed primarily at quiet, low-operating-cost day-VFR training.", "世界初の型式証明を取得した電動航空機で、静かで低運航費の日中VFR訓練を主用途とします。", "https://www.pipistrel-aircraft.com/products/velis-electro/"),
    ("explorer", "Pipistrel Explorer", "Pipistrel", "sport", "—", "10.70 m", "2", "1,196 km (646 nmi)", "1 × Rotax 912 S3", "", "具碳纖維機體、整機降落傘與 IFR-ready 航電的雙座認證訓練／旅行機。", "A certified two-seat trainer and tourer with a carbon airframe, whole-aircraft parachute, and IFR-ready avionics.", "炭素繊維機体、機体パラシュート、IFR対応準備済みアビオニクスを備える認証2座練習・旅行機です。", "https://www.pipistrel-aircraft.com/products/explorer/"),
    ("extrang", "Extra NG", "Extra Aircraft", "aerobatic", "2019", "8.30 m", "2", "—", "1 × Lycoming AEIO-580-B1A", "", "採全碳纖維硬殼機身、可承受正負 10 g 的雙座無限制級特技機。", "A two-seat unlimited-class aerobatic aircraft with a carbon monocoque airframe and ±10 g certification.", "全炭素モノコック機体を採用し、±10 g認証を持つ2座アンリミテッド級曲技機です。", "https://extraaircraft.com/ng/"),
    ("ventus3", "Schempp-Hirth Ventus 3", "Schempp-Hirth", "glider", "2016", "15 / 18 m", "1", "—", "無動力／Turbo／FES／Solo self-launch", "", "可選 15 或 18 公尺翼展，以及純滑翔、續航或自力起飛動力的高性能單座滑翔機。", "A high-performance single-seat glider with 15- or 18-metre wings and pure, sustainer, or self-launching options.", "15m／18m翼と、純滑空・サステナー・自力発航仕様を選べる高性能単座グライダーです。", "https://www.schempp-hirth.com/en/sailplanes/ventus/"),
    ("arcus", "Schempp-Hirth Arcus", "Schempp-Hirth", "glider", "2009", "20.0 m", "2", "—", "無動力／Solo sustainer／Solo self-launch", "", "二十公尺級雙座高性能滑翔機，可選純滑翔、返航輔助或自力起飛版本。", "A 20-metre-class two-seat high-performance glider offered in pure, sustainer, and self-launching versions.", "純滑空、サステナー、自力発航仕様がある20m級2座高性能グライダーです。", "https://www.schempp-hirth.com/flugzeuge/arcus/"),
    ("as33me", "Alexander Schleicher AS 33 Me", "Alexander Schleicher", "glider", "—", "15 / 18 m", "1", "—", "Electric self-launch system", "", "AS 33 高性能滑翔機的電動自力起飛型，可使用 15 或 18 公尺翼尖。", "The electric self-launching AS 33 high-performance glider with interchangeable 15- and 18-metre tips.", "15m／18m翼端を交換できるAS 33高性能グライダーの電動自力発航型です。", "https://www.alexander-schleicher.de/flugzeuge/as-33/"),
    ("ask21b", "Alexander Schleicher ASK 21 B", "Alexander Schleicher", "glider", "2018", "17.0 m", "2", "—", "無動力", "AS21", "經典 ASK 21 的現行改良雙座型，持續用於初級、越野與特技滑翔訓練。", "The current improved two-seat ASK 21, used for primary, cross-country, and aerobatic glider training.", "初等・クロスカントリー・曲技滑翔訓練に使われる、現行改良型の2座ASK 21です。", "https://www.alexander-schleicher.de/en/flugzeuge/ask-21-b/"),
]

PART_NAMES = {
    "overview": tr("整體外型", "Overall profile", "全体外観"),
    "cockpit": tr("駕駛艙", "Cockpit", "コックピット"),
    "windshield": tr("駕駛艙外窗", "Cockpit windows", "コックピット窓"),
    "fuselage": tr("機身與艙門", "Fuselage and doors", "胴体とドア"),
    "engine": tr("動力系統", "Powerplant", "動力系統"),
    "wingtip": tr("翼尖", "Wingtip", "翼端"),
    "wing": tr("主翼", "Main wing", "主翼"),
    "vstab": tr("垂直尾翼", "Vertical stabilizer", "垂直尾翼"),
    "hstab": tr("水平尾翼", "Horizontal stabilizer", "水平尾翼"),
    "gear": tr("起落架", "Landing gear", "着陸装置"),
}
PART_ORDER = list(PART_NAMES)

# 每架新機型的可辨識部位說明；照片會在後續實機圖片批次另行補入。
PROFILES = {
    "concorde": [
        tr("細長機身、可下垂機鼻、四發與無尾式哥德三角翼，組成協和號獨一無二的超音速輪廓。", "A slender fuselage, droop nose, four engines and tailless ogival delta wing form Concorde's unmistakable supersonic profile.", "細長い胴体、可動機首、4発、無尾翼のオージー型デルタ翼がコンコルド特有の超音速外形を作ります。"),
        tr("三人制駕駛艙保留大量類比儀表；正副駕駛之外另設飛航工程師席，負責複雜的燃油、進氣與電力系統。", "The three-crew flight deck is dominated by analogue instruments, with a flight engineer managing fuel, intake and electrical systems.", "3名乗務の操縦室はアナログ計器が中心で、航空機関士が燃料、吸気、電気系統を管理します。"),
        tr("狹窄多片風擋配合可升降整流罩；起降時機鼻下垂以改善視野，高速巡航時復位形成流線外形。", "Narrow multi-pane glazing works with a movable visor; the nose droops for takeoff and landing, then streamlines for supersonic cruise.", "細い多面窓と可動バイザーを備え、離着陸時は機首を下げ、超音速巡航時は流線形へ戻します。"),
        tr("加壓機身極為細長，客艙通常採 2+2 座位與小型窗；機體會因氣動加熱在巡航時伸長。", "The very slender pressure fuselage uses a 2+2 cabin and small windows, and expands measurably from aerodynamic heating in cruise.", "非常に細長い与圧胴体は2+2配列と小窓を採用し、巡航中の空力加熱で機体が伸びます。"),
        tr("四具 Olympus 593 渦噴成對置於翼下，具可變進氣道與加力燃燒器，以支援起飛及約 Mach 2 巡航。", "Four paired Olympus 593 turbojets use variable intakes and reheat for takeoff and roughly Mach 2 cruise.", "翼下に2基ずつ配置したOlympus 593ターボジェットは可変吸気口と再燃焼装置を使い、離陸と約マッハ2巡航を支えます。"),
        tr("翼尖是三角翼本體的尖細延伸，沒有獨立翼尖小翼；平面形由寬大的翼根逐漸收束。", "The tip is the tapered end of the delta wing rather than a separate winglet, narrowing from an exceptionally broad root.", "翼端は独立したウイングレットではなく、非常に広い翼根から細くなるデルタ翼そのものです。"),
        tr("哥德式三角翼利用渦升力改善低速升力，沒有傳統襟翼；後緣升降副翼同時控制俯仰與滾轉。", "The ogival delta uses vortex lift at low speed and has no conventional flaps; trailing-edge elevons control pitch and roll.", "オージー型デルタ翼は低速で渦揚力を利用し、通常のフラップを持たず、後縁エレボンでピッチとロールを制御します。"),
        tr("單一後掠垂尾位於細長機身末端，方向舵分段以兼顧高速控制與系統冗餘。", "A single swept fin caps the slender aft fuselage, with a segmented rudder for high-speed control and redundancy.", "細長い後部胴体に単一後退垂直尾翼を置き、分割方向舵で高速操縦と冗長性を確保します。"),
        tr("協和號沒有獨立水平尾翼，俯仰控制由三角翼後緣的升降副翼完成。", "Concorde has no separate horizontal tail; pitch control comes from elevons along the delta wing's trailing edge.", "独立した水平尾翼はなく、デルタ翼後縁のエレボンがピッチを制御します。"),
        tr("高迎角起降需要特別修長的前三點式起落架；主腳使用四輪轉向架，尾部另有防擦尾小輪。", "Its high takeoff attitude requires tall tricycle gear, with four-wheel main bogies and a small tail bumper wheel.", "高い離陸姿勢に対応する長い前輪式脚、4輪主脚ボギー、尾部のテールバンパーを備えます。"),
    ],
    "icona5": [
        tr("A5 是雙座高翼水陸兩用機，以船形機身、翼尖浮筒、折疊翼與後置推進螺旋槳辨識。", "The A5 is a two-seat high-wing amphibian identified by its boat hull, tip floats, folding wings and pusher propeller.", "A5は船形胴体、翼端フロート、折り畳み高翼、後置推進プロペラで識別できる2座水陸両用機です。"),
        tr("並排雙座座艙採接近汽車的簡潔介面，降低休閒飛行員進入門檻，並整合 Angle of Attack 顯示。", "The side-by-side cockpit uses an automotive-style simplified interface and a prominent angle-of-attack display.", "並列2座の操縦室は自動車的で簡潔な操作系と目立つ迎角表示を採用します。"),
        tr("大面積曲面透明罩提供前方與側向視野；前方窗框較少，適合水面進場與休閒觀景。", "A broad curved canopy provides generous forward and side visibility with minimal framing for water operations and touring.", "大型曲面キャノピーは枠が少なく、水上進入や遊覧に広い前方・側方視界を提供します。"),
        tr("複合材料機身下半部形成船底與滑水面，左右翼根附近的突出結構協助水上穩定。", "The composite lower fuselage forms a planing boat hull, while lateral sponson-like forms help stability on water.", "複合材胴体下部が滑走艇形状を作り、左右の張り出しが水上安定性を助けます。"),
        tr("Rotax 912 iS 安裝在座艙後上方，以三葉螺旋槳向後推進，讓機鼻保持開闊並遠離浪花。", "A Rotax 912 iS drives a rear-facing three-blade pusher propeller above and behind the cabin, clear of spray.", "Rotax 912 iSが客室後上方の3翅プッシャープロペラを駆動し、飛沫から離して機首視界を確保します。"),
        tr("翼尖向下整合小型浮筒，水上時支撐機翼；翼面可向後折疊以縮小停放寬度。", "Downturned tip floats support the wings on water, and the wings fold aft to reduce storage width.", "下向き翼端フロートが水上で翼を支え、主翼は後方へ折り畳めます。"),
        tr("高翼採無支柱懸臂布局並以抗尾旋設計為核心，兼顧低速操控、視野與水面淨空。", "The strutless high wing emphasizes spin resistance, low-speed handling, visibility and water clearance.", "支柱なし高翼は耐スピン性、低速操縦、視界、水面クリアランスを重視します。"),
        tr("單一垂尾位於推進螺旋槳後方，能直接利用螺旋槳滑流維持低速方向控制。", "The single fin sits behind the pusher propeller and benefits from propwash for low-speed directional control.", "単一垂直尾翼はプッシャープロペラ後方にあり、低速時に後流を利用できます。"),
        tr("低置水平尾翼安裝於尾端，避開高置螺旋槳並形成傳統尾翼布局。", "A low-mounted tailplane clears the elevated propeller and forms a conventional tail arrangement.", "低位置の水平尾翼は高いプロペラを避け、通常尾翼配置を構成します。"),
        tr("可收放前三點式起落架讓 A5 能在陸地與水面操作；收起後輪組貼合船形機身。", "Retractable tricycle gear permits land and water operations, stowing closely against the boat hull.", "引込式前輪脚により陸上と水上の両方で運用でき、格納時は船形胴体に沿います。"),
    ],
    "xcub": [
        tr("XCub／NXCub 是現代高翼越野機，保留 Cub 的串列雙座、翼支柱與大輪胎比例，但採用更流線的複合材料整流。", "XCub/NXCub modernizes the classic Cub formula with tandem seating, braced high wings, large tyres and cleaner composite fairings.", "XCub／NXCubはタンデム座席、支柱付き高翼、大径タイヤというCub様式を現代的な複合材整流で更新しています。"),
        tr("串列雙座讓機身保持狹窄，前後席以中央操縱桿飛行；大面積側窗利於低空與野外觀察。", "Tandem seating keeps the fuselage narrow, with center sticks and broad side glazing for low-level and backcountry visibility.", "タンデム2座で胴体を細く保ち、中央操縦桿と大きな側窓で低空・野外視界を確保します。"),
        tr("前風擋近乎直立並與透明側門相連，形成典型 Cub 的高翼下全景視野。", "A nearly upright windshield joins transparent side doors to create the panoramic under-wing view typical of Cubs.", "ほぼ直立した前面窓と透明側ドアがつながり、Cubらしい高翼下の広い視界を作ります。"),
        tr("鋼管骨架與整流外皮形成狹長機身，寬大的側門方便在未鋪面場地裝卸人員與裝備。", "A streamlined skin surrounds a steel-tube structure, with broad side access for people and equipment in remote operations.", "鋼管構造を流線形外皮で覆い、大型側ドアが辺地での人員・装備積載を容易にします。"),
        tr("機鼻活塞引擎驅動大型兩葉或三葉螺旋槳，以低速大推力配合短場起降。", "A nose-mounted piston engine turns a large two- or three-blade propeller for strong low-speed thrust and short-field work.", "機首ピストンエンジンが大型2翅または3翅プロペラを回し、短距離運用向けの低速推力を生みます。"),
        tr("翼尖接近方形且沒有翼尖小翼，重點是可預測的低速失速特性與易修復性。", "Near-square tips omit winglets, favoring predictable low-speed behavior and field simplicity.", "ほぼ角形の翼端はウイングレットを持たず、予測しやすい低速特性と現場整備性を重視します。"),
        tr("長弦高翼以 V 型支柱支撐，搭配大型襟翼，提供低速升力與地面障礙物淨空。", "A long-chord braced high wing and large flaps provide low-speed lift and clearance from ground obstacles.", "長い翼弦の支柱付き高翼と大型フラップが低速揚力と地上障害物クリアランスを提供します。"),
        tr("圓弧前緣垂尾與大型方向舵延續 Cub 家族輪廓，低速時仍保有方向控制。", "The rounded fin and large rudder retain the Cub-family silhouette and directional authority at low speed.", "丸い前縁の垂直尾翼と大型方向舵がCub系の外形と低速方向制御を保ちます。"),
        tr("傳統低置水平尾翼以支索／支柱強化，升降舵面積大，適合短場高迎角操作。", "The conventional low tailplane is externally braced and carries large elevators for high-angle short-field operations.", "低位置の水平尾翼は外部支持され、大型昇降舵が短距離・高迎角操作を支えます。"),
        tr("XCub 採尾輪式，NXCub 改為前三點式；兩者都可配大尺寸 tundra tire 或浮筒。", "XCub uses tailwheel gear while NXCub uses tricycle gear; both can accept large tundra tyres or floats.", "XCubは尾輪式、NXCubは前輪式で、どちらも大型ツンドラタイヤやフロートに対応します。"),
    ],
    "carboncub": [
        tr("Carbon Cub SS 將經典 Cub 外型與輕量化、高功率結合，是以極短場操作為核心的雙座高翼機。", "Carbon Cub SS combines classic Cub proportions with low weight and high power for extreme short-field performance.", "Carbon Cub SSは古典的Cub外形に軽量・高出力を組み合わせ、極短距離運用を重視します。"),
        tr("串列雙座與中央操縱桿維持窄機身，透明側門可向上開啟，便於觀察地面與野外降落點。", "Tandem seats, center sticks and upward-opening transparent doors preserve a narrow cabin and excellent ground visibility.", "タンデム座席、中央操縦桿、上開き透明側ドアが細い客室と良好な地上視界を実現します。"),
        tr("近直立風擋配大側窗，窗框輪廓比現代流線旅行機更方正，是 Cub 家族的重要辨識點。", "The upright windshield and large side windows look squarer than modern tourers and strongly identify the Cub family.", "直立気味の前面窓と大きな側窓は現代旅行機より角張り、Cub系の重要な識別点です。"),
        tr("輕量鋼管機身搭配複合材料部件，寬側門與後方行李空間服務野外飛行用途。", "A lightweight tube fuselage with composite components, broad side access and aft baggage space supports backcountry use.", "軽量鋼管胴体と複合材部品、大型側ドア、後部荷物室が野外飛行を支えます。"),
        tr("高功率 CC340 活塞引擎驅動大型螺旋槳，以高推重比縮短起飛滑跑並改善爬升。", "The high-output CC340 piston engine drives a large propeller, giving strong power-to-weight ratio for short takeoff and climb.", "高出力CC340が大型プロペラを駆動し、高い出力重量比で短い離陸滑走と上昇を実現します。"),
        tr("方形翼尖沒有翼尖小翼，簡單耐用的外形配合低速飛行與野外維修需求。", "Square tips omit winglets, using a simple durable form suited to low-speed flight and field maintenance.", "角形翼端はウイングレットを持たず、低速飛行と野外整備に適した簡潔で丈夫な形です。"),
        tr("支柱高翼與大型襟翼產生強大低速升力；較高翼位也讓翼面遠離灌木與碎石。", "Braced high wings and large flaps generate strong low-speed lift while keeping the wing clear of brush and debris.", "支柱付き高翼と大型フラップが強い低速揚力を生み、翼を草木や石から離します。"),
        tr("圓形垂尾前緣與寬大方向舵提供短場進場時所需的低速偏航控制。", "A rounded fin and broad rudder provide the low-speed yaw authority required during short-field approaches.", "丸い垂直尾翼と幅広い方向舵が短距離進入に必要な低速ヨー制御を提供します。"),
        tr("低置支撐式水平尾翼與大升降舵可在低速、高迎角狀態維持俯仰控制。", "A braced low tailplane and large elevators retain pitch authority at low speed and high angle of attack.", "支持付き低位置水平尾翼と大型昇降舵が低速・高迎角でのピッチ制御を保ちます。"),
        tr("固定式尾輪起落架通常配大型低壓輪胎，能吸收崎嶇地面衝擊並降低陷入鬆土的風險。", "Fixed tailwheel gear commonly carries large low-pressure tyres to absorb rough terrain and resist sinking into soft ground.", "固定尾輪脚は大型低圧タイヤを装備し、荒地の衝撃を吸収して軟地への沈み込みを抑えます。"),
    ],
}


def generic_profile(row: tuple[str, ...]) -> list[dict[str, str]]:
    """Build concise model-specific sections for conventional aircraft not overridden above."""
    ident, name, _maker, cat, _first, _span, seats, _endurance, engine, _icao, zh, en, ja, _source = row
    layouts = {
        "kit": tr("低翼、單發、傳統尾翼的旅行／套件機布局，重點是良好效率與私人飛行實用性。", "A low-wing single-engine touring/kit layout emphasizes efficiency and practical personal travel.", "低翼単発・通常尾翼の旅行／キット機配置で、効率と個人旅行の実用性を重視します。"),
        "sport": tr("輕型雙座布局兼顧訓練、休閒飛行與低營運成本。", "A light two-seat layout balances training, recreation and low operating cost.", "軽量2座配置が訓練、レジャー、低運航費を両立します。"),
        "aerobatic": tr("緊湊雙座特技機以高結構強度、低慣性與精確操控為核心。", "This compact two-seat aerobatic design prioritizes structural strength, low inertia and precise control.", "コンパクトな2座曲技機は高強度、低慣性、精密操縦を重視します。"),
        "glider": tr("高展弦比複合材料滑翔機以降低阻力、保存能量與精確熱氣流飛行為核心。", "This high-aspect-ratio composite sailplane minimizes drag, preserves energy and supports precise thermal flying.", "高アスペクト比複合材グライダーは抵抗低減、エネルギー保持、精密なサーマル飛行を重視します。"),
    }
    layout = layouts[cat]
    cockpit = tr(f"{seats} 座座艙依用途配置飛行儀表與操縱裝置，兼顧視野與人體工學。", f"The {seats}-seat cockpit arranges flight instruments and controls for visibility and ergonomic operation.", f"{seats}座の操縦室は視界と操作性を考慮して計器と操縦装置を配置します。")
    windshield = tr("大面積透明罩／風擋提供前方與側向視野，其窗框與座艙罩輪廓也是辨識該機型的重要線索。", "Large windshield or canopy glazing provides forward and side visibility; its framing is also a useful identification cue.", "大型風防／キャノピーが前方・側方視界を提供し、窓枠形状も機種識別の手掛かりです。")
    fuselage = tr("機身尺度依座位與任務最佳化，將座艙、行李或動力系統收納在最小阻力的外形內。", "The fuselage is sized around occupants, baggage and mission equipment while keeping frontal area and drag low.", "胴体は乗員、荷物、任務装備に合わせつつ、前面面積と抵抗を抑えています。")
    power = tr(f"動力為 {engine}；安裝方式依機型用途在效率、冷卻、噪音與維護性之間取捨。", f"Power comes from {engine}; its installation balances efficiency, cooling, noise and maintainability.", f"動力は{engine}で、搭載方式は効率、冷却、騒音、整備性を両立します。")
    wingtip = tr("翼尖外形配合該機的速度範圍與誘導阻力需求；部分滑翔機使用可更換翼尖或翼端小翼。", "The tip geometry suits the aircraft's speed range and induced-drag goals; some sailplanes use interchangeable tips or winglets.", "翼端形状は速度域と誘導抵抗に合わせ、一部グライダーは交換翼端やウイングレットを使います。")
    wing = tr("主翼翼型與操縱面依任務調校：旅行機平衡巡航與低速，特技機追求對稱操控，滑翔機則追求高升阻比。", "Wing sections and controls follow the mission: touring aircraft balance cruise and low speed, aerobatic types symmetry, and gliders lift-to-drag ratio.", "翼型と操縦面は任務別で、旅行機は巡航と低速、曲技機は対称操縦、グライダーは揚抗比を重視します。")
    vstab = tr("單一垂直尾翼與方向舵提供航向穩定及側滑修正，尺寸配合低速控制需求。", "A single fin and rudder provide directional stability and sideslip correction, sized for low-speed authority.", "単一垂直尾翼と方向舵が方向安定と横滑り修正を担い、低速操縦に合わせた面積を持ちます。")
    hstab = tr("水平尾翼與升降舵負責俯仰穩定；其安裝高度與翼面形狀用來避開主翼或螺旋槳擾流。", "The tailplane and elevators provide pitch stability, positioned to manage wing or propeller wake.", "水平尾翼と昇降舵がピッチ安定を担い、主翼やプロペラ後流を考慮して配置されます。")
    gear = tr("起落架配置依任務在地面穩定、阻力、重量與未鋪面操作之間取捨。", "The landing gear balances ground stability, drag, weight and any rough-field requirement.", "着陸装置は地上安定、抵抗、重量、未舗装地運用の要件を調整します。")
    return [tr(zh, en, ja), cockpit, windshield, fuselage, power, wingtip, wing, vstab, hstab, gear]


PROFILE_OVERRIDES = {
    "rv10": {
        "cockpit": tr("前排並排雙座、後排再容納兩名成人，採雙操縱桿與旅行機航電配置。", "Two side-by-side front seats and two adult rear seats use dual sticks and a touring-oriented avionics panel.", "前席並列2座と成人用後席2座を備え、複操縦桿と旅行向け計器盤を採用します。"),
        "windshield": tr("前風擋與側窗形成寬廣四座座艙視野，左右大型鷗翼門是 RV-10 的明顯特徵。", "Broad windshield and side glazing surround the four-seat cabin; large gull-wing doors are a clear RV-10 cue.", "広い前面・側面窓が4座客室を囲み、大型ガルウイングドアがRV-10の特徴です。"),
        "fuselage": tr("RV-10 的機身比雙座 RV 系列更深更長，提供四個成人座位與後方行李空間。", "The RV-10 fuselage is deeper and longer than two-seat RVs, providing four adult seats and aft baggage space.", "RV-10の胴体は2座RVより深く長く、成人4席と後部荷物室を備えます。"),
        "wing": tr("懸臂低翼採無支柱全金屬結構與大型襟翼，重點是高速巡航、穩定進場及旅行載重。", "The all-metal cantilever low wing and large flaps balance fast cruise, stable approaches and touring payload.", "全金属片持ち低翼と大型フラップが高速巡航、安定進入、旅行搭載量を両立します。"),
        "gear": tr("固定式前三點起落架配流線輪罩；它不像多數雙座 RV 提供尾輪版本。", "Fixed tricycle gear carries streamlined wheel fairings; unlike many two-seat RVs, the RV-10 is not offered as a taildragger.", "固定前輪式脚に流線形ホイールフェアリングを備え、RV-10には多くの2座RVのような尾輪型はありません。"),
    },
    "rv14": {
        "cockpit": tr("寬敞並排雙座採雙操縱桿，座艙尺寸與進出便利性比早期雙座 RV 更佳。", "A roomy side-by-side cockpit with dual sticks improves space and access over earlier two-seat RV designs.", "広い並列2座と複操縦桿を備え、初期2座RVより空間と乗降性を改善しています。"),
        "windshield": tr("大型一體式透明座艙罩提供良好全向視野；RV-14 常見向上翻起式罩，RV-14A 外觀相近。", "A large one-piece canopy gives broad visibility; the tip-up canopy is a prominent RV-14/14A feature.", "大型一体キャノピーが広い視界を提供し、上方へ開く構造がRV-14／14Aの特徴です。"),
        "fuselage": tr("雙座機身在座艙後保留行李空間，金屬蒙皮與圓滑上機身兼顧套件製造與低阻力。", "The two-seat metal fuselage includes aft baggage space and a rounded upper deck for practical kit construction and low drag.", "2座金属胴体は後部荷物室と丸い上部胴体を備え、組立性と低抵抗を両立します。"),
        "wing": tr("低翼採對稱性較高的翼型與全翼展操縱面配置，可兼顧旅行效率與核准範圍內的基礎特技。", "The low wing and control layout support efficient touring and approved basic aerobatics.", "低翼と操縦面配置が効率的な旅行飛行と承認範囲内の基本曲技を両立します。"),
        "gear": tr("RV-14 為固定尾輪式，RV-14A 為固定前三點式；兩者常配流線輪罩降低巡航阻力。", "RV-14 uses fixed tailwheel gear and RV-14A fixed tricycle gear; streamlined wheel pants reduce cruise drag.", "RV-14は固定尾輪式、RV-14Aは固定前輪式で、流線形ホイールパンツが巡航抵抗を減らします。"),
    },
    "sling2": {
        "cockpit": tr("並排雙座採中央或雙側操縱裝置與現代玻璃座艙，設計兼顧飛行訓練及長途旅行。", "The side-by-side two-seat cockpit uses modern glass avionics and controls suited to both training and touring.", "並列2座の操縦室は現代的グラスアビオニクスを備え、訓練と旅行の両方に適します。"),
        "windshield": tr("大型泡形座艙罩向兩側延伸，前方窗框少，形成 Sling 系列流線、開闊的座艙輪廓。", "A broad bubble canopy with minimal forward framing creates the Sling family's open, streamlined cabin profile.", "前枠の少ない大型バブルキャノピーがSling系の開放的で流線形の客室外観を作ります。"),
        "fuselage": tr("鉚接鋁合金半硬殼機身採修長尾錐，座艙後方設行李空間，適合套件製造與維修。", "A riveted aluminum semi-monocoque fuselage, tapered tailcone and aft baggage bay suit kit construction and maintenance.", "リベット接合アルミ半モノコック胴体、細い尾部、後部荷物室がキット製作と整備に適します。"),
        "wing": tr("直線形懸臂低翼配襟翼與副翼，以溫和失速、訓練操控和巡航效率為主要取捨。", "The straight cantilever low wing uses flaps and ailerons, balancing benign stall behavior, training handling and cruise efficiency.", "直線的片持ち低翼はフラップと補助翼を備え、穏やかな失速、訓練操縦、巡航効率を両立します。"),
        "gear": tr("固定式前三點起落架配輪罩，結構簡單、維護成本低，符合訓練與私人飛行需求。", "Fixed tricycle gear with wheel fairings keeps operation simple and economical for training and private flying.", "ホイールフェアリング付き固定前輪式脚が訓練・個人飛行向けの簡潔さと低費用を実現します。"),
    },
    "slingtsi": {
        "cockpit": tr("四座並排雙排座艙採大型玻璃航電與雙操縱裝置，定位為快速跨國旅行機。", "The four-seat two-row cockpit combines large glass displays and dual controls for fast cross-country touring.", "4座2列の操縦室は大型グラス表示と複操縦装置を備え、高速長距離旅行向けです。"),
        "windshield": tr("寬大風擋、側窗與左右鷗翼門形成明亮座艙；後排另有獨立側窗。", "A broad windshield, side glazing and twin gull-wing doors create a bright cabin, with separate windows for rear occupants.", "広い前面・側面窓と左右ガルウイングドアが明るい客室を作り、後席にも独立窓があります。"),
        "fuselage": tr("全金屬四座機身比 Sling 2 更長更深，容納後排、行李與渦輪增壓動力系統。", "The all-metal four-seat fuselage is longer and deeper than the Sling 2, accommodating rear seats, baggage and turbocharged systems.", "全金属4座胴体はSling 2より長く深く、後席、荷物、ターボ系統を収容します。"),
        "wing": tr("低翼油箱與襟翼兼顧較高巡航速度、四座載重及合理的起降性能。", "Low-wing fuel capacity and flaps balance higher cruise speed, four-seat payload and practical field performance.", "低翼内燃料とフラップが高い巡航速度、4座搭載量、実用的な離着陸性能を両立します。"),
        "gear": tr("固定式前三點起落架使用流線輪罩，以較低複雜度換取可靠性，同時控制巡航阻力。", "Fixed tricycle gear uses streamlined fairings, trading retractable complexity for reliability while limiting cruise drag.", "固定前輪式脚は流線形カバーを使い、引込機構の複雑さを避けながら巡航抵抗を抑えます。"),
    },
    "velise": {
        "cockpit": tr("並排雙座訓練座艙沿用 Virus SW 121 架構，以數位顯示器監控電池、馬達與剩餘能量。", "The side-by-side training cockpit derives from the Virus SW 121 and digitally monitors battery, motor and remaining energy.", "並列2座訓練操縦室はVirus SW 121を基に、電池、モーター、残存エネルギーをデジタル監視します。"),
        "windshield": tr("大型前風擋與透明側門提供教練和學員良好視野，高翼不遮擋下方觀察。", "A large windshield and glazed side doors give instructor and student broad visibility, with the high wing aiding downward views.", "大型前面窓と透明側ドアが教官・訓練生に広い視界を与え、高翼が下方視界を助けます。"),
        "fuselage": tr("輕量複合材料雙座機身將電池分布於機鼻與座艙後方，維持重心並降低阻力。", "The lightweight composite fuselage distributes battery mass ahead of and behind the cabin to manage center of gravity and drag.", "軽量複合材胴体は電池を機首と客室後方に分散し、重心と抵抗を管理します。"),
        "engine": tr("液冷 E-811 電動馬達驅動機鼻螺旋槳；低噪音、即時扭力與較少活動零件適合反覆訓練架次。", "A liquid-cooled E-811 electric motor drives the nose propeller; low noise, instant torque and fewer moving parts suit repetitive training sorties.", "液冷E-811電動モーターが機首プロペラを駆動し、低騒音、即時トルク、少ない可動部が反復訓練に適します。"),
        "wing": tr("長展弦比懸臂高翼配襟翼與擾流板，承襲 Pipistrel 高效率滑翔特性並降低能量消耗。", "The high-aspect-ratio cantilever wing uses flaps and spoilers, retaining Pipistrel's glider-like efficiency to reduce energy use.", "高アスペクト比片持ち高翼はフラップとスポイラーを備え、Pipistrelの滑空的効率で消費電力を抑えます。"),
        "hstab": tr("T 型水平尾翼位於垂尾頂端，遠離主翼尾流，是 Velis／Virus 家族醒目的外觀線索。", "The T-tail places the tailplane atop the fin, away from wing wake, and is a strong Velis/Virus family cue.", "T字尾翼は水平尾翼を垂直尾翼頂部に置き、主翼後流を避けるVelis／Virus系の特徴です。"),
        "gear": tr("固定前三點式起落架與輪罩結構簡單，適合飛行學校高頻率起降與低維護需求。", "Fixed faired tricycle gear is simple and suited to frequent flight-school takeoffs and landings.", "固定前輪式脚とホイールカバーは簡潔で、飛行学校の高頻度離着陸に適します。"),
    },
    "explorer": {
        "cockpit": tr("並排雙座認證訓練座艙可配置 IFR 航電，操縱與顯示兼顧初學訓練及進階程序。", "The certified side-by-side trainer can carry IFR-ready avionics for both primary training and advanced procedures.", "認証並列2座練習機はIFR対応アビオニクスを搭載でき、初等から高度手順訓練まで対応します。"),
        "windshield": tr("寬大前風擋與透明側門提供廣角視野，適合目視訓練、航行與地面參考。", "Broad windshield and glazed side doors provide wide-angle visibility for visual training, navigation and ground reference.", "広い前面窓と透明側ドアが目視訓練、航法、地上目標確認に広い視界を提供します。"),
        "fuselage": tr("碳纖維雙座機身整合整機降落傘，外形修長低阻，座艙後方保留行李空間。", "The carbon-fiber two-seat fuselage integrates a whole-aircraft parachute, low-drag contours and aft baggage capacity.", "炭素繊維2座胴体は機体パラシュート、低抵抗外形、後部荷物室を統合します。"),
        "wing": tr("長展弦比高翼配襟翼與擾流板，可用於陡降控制並提供接近滑翔機的高效率。", "The high-aspect-ratio high wing uses flaps and spoilers for descent control and glider-like efficiency.", "高アスペクト比高翼はフラップとスポイラーで降下を制御し、グライダーに近い効率を得ます。"),
        "hstab": tr("T 型尾翼使水平尾翼遠離主翼擾流，輪廓與同家族 Velis Electro 十分相近。", "A T-tail keeps the tailplane clear of wing wake and closely resembles the related Velis Electro profile.", "T字尾翼が水平尾翼を主翼後流から離し、同系Velis Electroに近い外形です。"),
        "gear": tr("固定前三點式起落架配整流罩，維持訓練機可靠性並減少巡航阻力。", "Fixed faired tricycle gear preserves trainer reliability while reducing cruise drag.", "整流カバー付き固定前輪式脚が練習機の信頼性を保ち、巡航抵抗を減らします。"),
    },
    "extrang": {
        "cockpit": tr("前後串列雙座位於機翼附近，飛行員以中央操縱桿與大型方向舵踏板進行精確特技操控。", "Tandem seats near the wing use center sticks and large rudder pedals for precise aerobatic control.", "翼付近のタンデム2座は中央操縦桿と大型ラダーペダルで精密な曲技操縦を行います。"),
        "windshield": tr("大型泡形座艙罩幾乎無遮蔽地包覆兩席，提供編隊、倒飛與垂直機動所需的全向視野。", "A large bubble canopy surrounds both seats with near-unobstructed visibility for formation, inverted and vertical maneuvers.", "大型バブルキャノピーが両席を包み、編隊、背面、垂直機動に必要な全周視界を提供します。"),
        "fuselage": tr("全碳纖維硬殼機身以低重量與高剛性承受正負高 g 載荷，短機身也降低旋轉慣性。", "The carbon monocoque fuselage combines low mass and high stiffness for positive and negative g, while its compact length reduces rotational inertia.", "全炭素モノコック胴体は軽量・高剛性で正負高gに耐え、短い機体が回転慣性を抑えます。"),
        "wing": tr("低翼採近對稱翼型與大型副翼，使正飛、倒飛的操控反應接近並提高滾轉率。", "The low wing uses a near-symmetrical section and large ailerons for similar upright/inverted response and high roll rate.", "低翼はほぼ対称翼型と大型補助翼を使い、正立・背面で似た応答と高ロール率を得ます。"),
        "vstab": tr("高大的垂尾與寬方向舵在低前進速度、側滑及旋轉動作中仍維持強大偏航控制。", "A tall fin and broad rudder preserve strong yaw control at low forward speed, in sideslip and during rotation maneuvers.", "高い垂直尾翼と幅広い方向舵が低速、横滑り、回転演技中も強いヨー制御を保ちます。"),
        "gear": tr("固定式尾輪起落架短而堅固，主輪常加流線罩；配置也替大型螺旋槳保留地面淨空。", "Short robust fixed tailwheel gear often carries wheel pants and provides clearance for the large propeller.", "短く強固な固定尾輪脚はホイールパンツを備え、大型プロペラの地上間隔も確保します。"),
    },
    "ventus3": {
        "cockpit": tr("單座座艙採半躺姿勢與窄機身，大型一體式透明罩降低迎風面並提供良好上方視野。", "The single pilot reclines in a narrow fuselage beneath a large one-piece canopy, reducing frontal area while preserving upward visibility.", "単座操縦者は細い胴体内で半仰臥し、大型一体キャノピーが前面面積を減らしつつ上方視界を確保します。"),
        "fuselage": tr("碳纖維機身前段容納座艙與收放主輪，細長尾樑將阻力與濕面積降至最低。", "The carbon fuselage houses cockpit and retractable main wheel forward, then tapers into a very low-drag tailboom.", "炭素胴体前部に操縦室と引込主輪を収め、細い尾部で抵抗と濡れ面積を最小化します。"),
        "engine": tr("依版本可為純滑翔、Turbo 返航輔助、FES 前緣電動螺旋槳或 Solo 自力起飛系統。", "Versions include pure sailplane, Turbo sustainer, FES nose-mounted electric propeller, or Solo self-launch systems.", "純滑空、Turboサステナー、FES機首電動プロペラ、Solo自力発航仕様があります。"),
        "wingtip": tr("可交換 15 m 與 18 m 翼尖，均以向上彎曲翼端小翼控制翼尖渦與跨距效率。", "Interchangeable 15 m and 18 m tips use upturned winglets to manage tip vortices and span efficiency.", "交換可能な15m／18m翼端は上向きウイングレットで翼端渦とスパン効率を管理します。"),
        "wing": tr("超高展弦比複合材料翼配全翼展襟副翼，可隨速度調整翼型彎度並兼顧熱氣流與高速滑翔。", "Very high-aspect-ratio composite wings use full-span flaperons to vary camber for thermalling and fast cruise.", "超高アスペクト比複合材翼は全幅フラッペロンでキャンバーを変え、サーマルと高速滑空を両立します。"),
        "hstab": tr("小型 T 型水平尾翼位於垂尾頂端，遠離主翼尾流並降低尾翼與地面碰撞風險。", "A small T-tail sits atop the fin, clear of wing wake and less exposed to ground contact.", "小型T字水平尾翼は垂直尾翼頂部にあり、主翼後流と地面接触を避けます。"),
        "gear": tr("可收放單主輪降低飛行阻力，翼尖靠小滑橇保護；地面移動通常另接翼輪。", "A retractable monowheel cuts drag, with small tip skids for protection and detachable dollies for ground handling.", "引込単輪が抵抗を減らし、翼端スキッドで保護し、地上移動には着脱式翼輪を使います。"),
    },
    "arcus": {
        "cockpit": tr("前後串列雙座位於長透明罩下，前後席都具完整操縱，供訓練、競賽與長途雙人飛行。", "Tandem seats beneath a long canopy provide full dual controls for training, competition and two-person cross-country flight.", "長いキャノピー下のタンデム2座は複操縦装置を備え、訓練、競技、2人長距離飛行に対応します。"),
        "fuselage": tr("較深的雙座複合材料前機身後接細長尾樑，在容納兩人與動力選項的同時維持低阻力。", "A deeper two-seat composite nose tapers into a slender boom, accommodating two occupants and power options while limiting drag.", "深い2座複合材前胴体から細い尾部へ絞り、2人と動力装置を収めながら抵抗を抑えます。"),
        "engine": tr("可選純滑翔、Solo 返航輔助或可收放螺旋槳的自力起飛版本；動力關閉後收回機身以恢復滑翔效率。", "Pure, Solo sustainer and retractable-propeller self-launch variants are offered; the power unit retracts to restore glide efficiency.", "純滑空、Soloサステナー、格納式プロペラ自力発航型があり、停止後は胴体へ収納して滑空効率を戻します。"),
        "wingtip": tr("20 m 翼端以明顯上彎翼端小翼收尾，減少誘導阻力並改善低速盤旋效率。", "The 20 m span ends in pronounced upturned winglets that reduce induced drag and improve low-speed circling.", "20m翼は明確な上向きウイングレットで終わり、誘導抵抗を減らし低速旋回効率を高めます。"),
        "wing": tr("長翼展複合材料翼配襟副翼，可改變翼型彎度，讓雙座機兼顧熱氣流爬升與高速越野。", "Long composite wings use flaperons to vary camber, balancing thermal climb and fast cross-country performance with two occupants.", "長い複合材翼はフラッペロンでキャンバーを変え、2座でのサーマル上昇と高速長距離を両立します。"),
        "hstab": tr("T 型水平尾翼置於垂尾頂端，輪廓修長，能避開主翼後流並保持精確俯仰控制。", "The slender T-tail clears wing wake and preserves precise pitch control.", "細いT字水平尾翼は主翼後流を避け、精密なピッチ制御を保ちます。"),
        "gear": tr("可收放單主輪設於雙座座艙下方，尾部與翼尖設保護滑橇；地面需以翼輪輔助。", "A retractable monowheel sits below the tandem cabin, with tail and tip protection and detachable wing dollies for ground handling.", "引込単輪はタンデム客室下にあり、尾部・翼端保護と着脱式翼輪を使います。"),
    },
    "as33me": {
        "cockpit": tr("單座半躺座艙採一體式透明罩與競賽級儀表配置，窄機鼻把迎風面積降到最低。", "The reclined single-seat cockpit uses a one-piece canopy and competition instruments, with a very narrow nose to minimize frontal area.", "半仰臥単座操縦室は一体キャノピーと競技計器を備え、極細機首で前面面積を抑えます。"),
        "fuselage": tr("高剛性碳纖維殼體由短而圓滑的座艙段迅速收束成細尾樑，以降低高速滑翔阻力。", "The stiff carbon shell tapers rapidly from the compact cockpit into a fine tailboom to reduce drag in fast glide.", "高剛性炭素殻は短い操縦室から細い尾部へ急速に絞り、高速滑空抵抗を減らします。"),
        "engine": tr("Me 型的電動自力起飛裝置可由機身伸出螺旋槳與支架；不用時完全收納以避免持續阻力。", "The Me electric self-launch unit raises a propeller and mast from the fuselage, retracting fully when unused to avoid continuous drag.", "Me型電動自力発航装置は胴体からプロペラ支柱を展開し、不使用時は完全格納して抵抗を避けます。"),
        "wingtip": tr("15 m 與 18 m 可交換翼尖配不同翼端小翼，使同一機體能在競賽級別與滑翔性能間切換。", "Interchangeable 15 m and 18 m tips with tailored winglets let one airframe switch competition classes and performance emphasis.", "専用ウイングレット付き15m／18m交換翼端により、競技クラスと性能重点を切り替えられます。"),
        "wing": tr("細長複合材料翼採多段操縱面與可變彎度襟翼，針對寬廣速度範圍維持高升阻比。", "Slender composite wings use segmented controls and camber-changing flaps to retain high lift-to-drag ratio across a wide speed range.", "細長い複合材翼は分割操縦面と可変キャンバーフラップで広い速度域の高揚抗比を保ちます。"),
        "hstab": tr("小型 T 型水平尾翼位於垂尾頂端，減少主翼後流影響並保持尾部整潔。", "A small T-tail clears wing wake and keeps the aft profile aerodynamically clean.", "小型T字水平尾翼が主翼後流を避け、尾部外形を空力的に整えます。"),
        "gear": tr("可收放單主輪與尾輪支撐機身，翼尖著地由保護滑橇承受；起飛時常由翼輪輔助平衡。", "A retractable monowheel and tailwheel support the fuselage, with tip skids and a detachable wing dolly for takeoff balance.", "引込単輪と尾輪が胴体を支え、翼端スキッドと着脱式翼輪で離陸時の平衡を補助します。"),
    },
    "ask21b": {
        "cockpit": tr("寬敞串列雙座配完整雙操縱系統，前席供學員、後席供教練，透明罩提供良好示範視野。", "A roomy tandem cockpit has full dual controls, with student forward and instructor aft beneath a broad training canopy.", "広いタンデム2座は完全複操縦で、前席訓練生・後席教官を大型キャノピーが覆います。"),
        "fuselage": tr("堅固玻璃纖維機身著重訓練耐用性與易修復性，較寬座艙後平順收束至 T 型尾翼。", "The robust glass-fiber fuselage prioritizes training durability and repairability, tapering from a broad cabin to the T-tail.", "丈夫なガラス繊維胴体は訓練耐久性と修理性を重視し、広い客室からT字尾翼へ絞ります。"),
        "engine": tr("ASK 21 B 是純滑翔機，沒有引擎；由拖曳機或絞盤起飛，能量管理完全依靠高度與氣流。", "ASK 21 B is unpowered, launching by aerotow or winch and relying entirely on altitude and atmospheric lift for energy.", "ASK 21 Bは無動力で、曳航またはウインチ発航し、高度と上昇気流だけでエネルギーを管理します。"),
        "wingtip": tr("圓滑翼尖沒有獨立翼端小翼，耐用且失速特性溫和，符合初級訓練需求。", "Rounded tips omit separate winglets, favoring durability and benign stall behavior for primary training.", "丸い翼端は独立ウイングレットを持たず、初等訓練向けの耐久性と穏やかな失速特性を重視します。"),
        "wing": tr("17 m 中置翼沒有襟翼，使用副翼與上翼面擾流板；簡化操控有利於基礎及特技訓練。", "The 17 m mid-wing has no flaps, using ailerons and upper-surface airbrakes for simple primary and aerobatic training.", "17m中翼はフラップを持たず、補助翼と上面エアブレーキで初等・曲技訓練を簡潔にします。"),
        "hstab": tr("T 型水平尾翼高置於垂尾頂端，避開主翼尾流與地面碰撞，也是 ASK 21 家族辨識點。", "The high T-tail clears wing wake and ground contact and is a defining ASK 21 family feature.", "高いT字水平尾翼は主翼後流と地面接触を避け、ASK 21系の特徴です。"),
        "gear": tr("固定主輪、機鼻輪與尾輪讓訓練起降更穩定；翼尖仍設滑橇以承受停止時的接地。", "Fixed main, nose and tail wheels improve training stability, while tip skids protect the wing when it settles after stopping.", "固定主輪、前輪、尾輪が訓練着陸を安定させ、停止時は翼端スキッドが翼を保護します。"),
    },
}


def detail(row: tuple[str, ...]) -> dict:
    ident, name, _maker, _cat, first, span, seats, endurance, engine, _icao, zh, en, ja, source = row
    descriptions = PROFILES[ident] if ident in PROFILES else generic_profile(row)
    overrides = PROFILE_OVERRIDES.get(ident, {})
    parts = {}
    for pid, summary in zip(PART_ORDER, descriptions, strict=True):
        summary = overrides.get(pid, summary)
        parts[pid] = {
            "name": PART_NAMES[pid],
            "en": PART_NAMES[pid]["en"].upper(),
            "summary": summary,
            "specs": [],
            "fact": tr("", "", ""),
            "bullets": [],
            "images": [],
        }
    return {
        "title": name,
        "sub": tr(zh, en, ja),
        "sources": [source],
        "partOrder": PART_ORDER,
        "parts": parts,
        "specifications": {
            "機組員與載客": [["座位數", seats], ["首飛年份", first]],
            "尺寸": [["翼展", span]],
            "性能": [["航程／續航", endurance]],
            "發動機": [["型號", engine]],
        },
    }


def fleet_entry(row: tuple[str, ...]) -> dict:
    ident, name, maker, cat, first, span, seats, _endurance, _engine, icao, zh, en, ja, _source = row
    return {
        "id": ident, "name": name, "manufacturer": maker, "category": CATEGORIES[cat],
        "firstFlight": first, "span": span, "seats": seats, "tagline": tr(zh, en, ja),
        "thumb": "assets/thumb_nomodel.svg", "icao": icao, "iata": "", "has3d": False,
    }


def main() -> None:
    ids = [row[0] for row in AIRCRAFT]
    assert len(ids) == len(set(ids))
    assert all(row[-1].startswith("https://") for row in AIRCRAFT)
    fleet = json.loads(FLEET_PATH.read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in fleet["aircraft"]}
    old_order = [item["id"] for item in fleet["aircraft"]]
    for row in AIRCRAFT:
        aircraft_detail = detail(row)
        assert aircraft_detail["partOrder"] == list(aircraft_detail["parts"])
        assert all(all(part["summary"][lang] for lang in ("zh", "en", "ja")) for part in aircraft_detail["parts"].values())
        by_id[row[0]] = fleet_entry(row)
        (ROOT / "data" / f"{row[0]}.json").write_text(
            json.dumps(aircraft_detail, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    fleet["aircraft"] = [by_id[ident] for ident in old_order]
    fleet["aircraft"].extend(by_id[ident] for ident in ids if ident not in old_order)
    FLEET_PATH.write_text(json.dumps(fleet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Added or updated {len(AIRCRAFT)} special aircraft.")


if __name__ == "__main__":
    main()
