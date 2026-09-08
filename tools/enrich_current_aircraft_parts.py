"""Reuse verified family records and add subtype-specific part descriptions."""

from copy import deepcopy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORDER = ["overview", "cockpit", "windshield", "fuselage", "engine", "wingtip", "wing", "vstab", "hstab", "gear"]

BASES = {
    "a319n": "a319", "a320n": "a320", "a321n": "a321", "a321xlr": "a321",
    "a338": "a332", "a339": "a333", "a35k": "a359", "belugaxl": "a332",
    "b37m": "b738", "b38m": "b738", "b39m": "b738", "b3xm": "b738",
}


def tri(zh, en, ja):
    return {"zh": zh, "en": en, "ja": ja}


COMMON_A320NEO = {
    "cockpit": tri(
        "neo 延續 A320 家族的雙人玻璃座艙、側置操縱桿與 fly-by-wire 控制邏輯。顯示與航電可隨批次升級，但基本操作哲學維持家族共通。",
        "The neo retains the A320 family's two-crew glass cockpit, sidesticks and fly-by-wire control philosophy. Displays and avionics evolve by production standard, while the basic operating concept remains common across the family.",
        "neoはA320ファミリーの2名乗務ガラスコックピット、サイドスティック、フライ・バイ・ワイヤの思想を継承します。表示器と電子機器は製造時期で更新されても、基本操作概念は共通です。"),
    "windshield": tri(
        "六片式駕駛艙外窗由中央向側面平順展開，側窗下緣斜切，是 A320 家族正面輪廓的重要特徵。neo 的窗型與 ceo 基本相同。",
        "Six flight-deck panes flow smoothly from the centre to the sides, with a slanted lower edge on the side windows. This is a key A320-family frontal cue and is essentially unchanged from ceo to neo.",
        "6枚の操縦室窓は中央から側面へ滑らかにつながり、側窓下縁が斜めになるA320系の重要な正面特徴です。neoとceoで窓形状は基本的に共通です。"),
    "engine": tri(
        "A320neo 家族可選 CFM LEAP-1A 或 Pratt & Whitney PW1100G-JM 高旁通比渦輪扇。較大的風扇、改良核心與齒輪傳動等技術降低耗油、噪音及排放；這也是與 ceo 世代最醒目的外觀差異。",
        "The A320neo family uses either CFM LEAP-1A or Pratt & Whitney PW1100G-JM high-bypass turbofans. Larger fans and newer cores—plus a geared fan on the PW1100G—reduce fuel burn, noise and emissions, and make the nacelles an obvious cue versus the ceo generation.",
        "A320neoファミリーはCFM LEAP-1AまたはPratt & Whitney PW1100G-JM高バイパス比ターボファンを採用します。大型ファン、新世代コア、PW1100Gの減速機構により燃費・騒音・排出を低減し、ceo世代より大きなナセルが識別点です。"),
    "wingtip": tri(
        "高聳後掠的 Sharklet 為 neo 的標準翼尖裝置，可降低翼尖渦與誘導阻力。它和早期 A320 家族常見的小型三角翼尖柵外型明顯不同。",
        "Tall swept Sharklets are standard on the neo family. They weaken wingtip vortices and induced drag and are visually distinct from the small triangular wingtip fences common on early A320-family aircraft.",
        "背の高い後退角付きSharkletはneoの標準翼端装置で、翼端渦と誘導抵抗を低減します。初期A320ファミリーの小型三角形ウイングチップフェンスとは明確に異なります。"),
    "wing": tri(
        "neo 保留 A320 家族的低翼、後掠翼基本平面形，但針對較重的發動機、Sharklet 與較高操作重量進行局部結構和氣動改良。前緣縫翼與後緣襟翼提供低速升力。",
        "The neo retains the A320 family's low-mounted swept-wing planform, with local structural and aerodynamic changes for heavier engines, Sharklets and higher operating weights. Leading-edge slats and trailing-edge flaps provide low-speed lift.",
        "neoはA320ファミリーの低翼・後退翼平面形を維持しつつ、重いエンジン、Sharklet、高い運用重量に対応する局部構造・空力改良を受けています。前縁スラットと後縁フラップが低速揚力を担います。"),
    "vstab": tri(
        "垂直尾翼與方向舵維持 A320 家族的典型輪廓，前緣根部有明顯背鰭過渡。它提供方向穩定與偏航控制，本身通常無法區分各 neo 子型。",
        "The vertical tail and rudder retain the familiar A320-family outline with a noticeable dorsal-root transition. They provide directional stability and yaw control but normally do not distinguish individual neo variants.",
        "垂直尾翼と方向舵は前縁基部のドーサル部を含むA320系の輪郭を維持します。方向安定とヨー制御を担いますが、neo各型の識別には通常使えません。"),
    "hstab": tri(
        "低置水平尾翼裝在機身尾段兩側，配合升降舵與可調安定面控制俯仰及配平。外形沿用 A320 家族設計，各 neo 型主要差異仍在機身長度。",
        "The low-mounted horizontal tail sits on either side of the aft fuselage; elevators and the trimmable stabilizer control pitch and trim. Its A320-family form is shared, leaving fuselage length as the stronger neo-variant cue.",
        "低位置の水平尾翼は後部胴体両側に付き、昇降舵と可動安定板でピッチとトリムを制御します。形状はA320系で共通し、neo各型は胴体長の方が識別しやすい特徴です。"),
    "gear": tri(
        "標準前三點式起落架由雙輪前架與左右雙輪主架構成，向機身內收。A321XLR 等較高重量衍生型會強化結構，但基本輪組仍維持家族共通外觀。",
        "The standard tricycle gear has twin nose wheels and twin-wheel main units that retract inward. Higher-weight derivatives such as the A321XLR receive structural changes, while the basic wheel arrangement remains familiar.",
        "標準前輪式降着装置は前脚2輪と左右各2輪の主脚で、機体内側へ格納されます。A321XLRなど高重量派生型は強化されますが、基本輪構成は共通です。"),
}

COMMON_A330NEO = {
    "engine": tri("A330neo 僅使用 Rolls-Royce Trent 7000 高旁通比渦輪扇。大型風扇、光滑圓形進氣口與較長短艙明顯不同於 A330ceo 的 Trent 700、CF6 或 PW4000。", "The A330neo exclusively uses Rolls-Royce Trent 7000 high-bypass turbofans. Their large fans, smooth round inlets and longer nacelles differ visibly from the Trent 700, CF6 or PW4000 installations on the A330ceo.", "A330neoはRolls-Royce Trent 7000高バイパス比ターボファンのみを使用します。大型ファン、滑らかな円形吸気口、長いナセルはA330ceoのTrent 700、CF6、PW4000と明確に異なります。"),
    "wingtip": tri("長而向上彎曲的複合材料翼尖取代 A330ceo 的小型上下翼尖柵，外形受 A350 設計經驗影響。它增加有效展弦比並降低誘導阻力。", "Long, upward-curving composite tips replace the A330ceo's small upper-and-lower fences. Influenced by A350 design experience, they increase effective aspect ratio and reduce induced drag.", "長く上方へ湾曲する複合材翼端がA330ceoの小型上下フェンスを置き換えます。A350の設計経験を取り入れ、有効アスペクト比を高めて誘導抵抗を減らします。"),
    "wing": tri("A330neo 的主翼保留 A330 基本結構位置，但翼展增至約 64 公尺，並更新翼型、整流罩與控制面。更長翼展配合新翼尖改善巡航效率。", "The A330neo wing retains the A330's basic location but grows to roughly 64 metres span with revised aerofoil, fairings and controls. The greater span and new tips improve cruise efficiency.", "A330neoの主翼はA330の基本位置を保ちながら翼幅を約64 mへ拡大し、翼型、フェアリング、操縦面を更新しています。長い翼幅と新翼端が巡航効率を改善します。"),
}

COMMON_MAX = {
    "cockpit": tri(
        "737 MAX 延續 737 的傳統操縱盤與共同型別設計，同時採用四具大型彩色顯示器。這種配置讓已具 737 資格的機組能以差異訓練轉換。",
        "The 737 MAX retains the 737's conventional control yokes and common type philosophy while introducing four large colour displays. The continuity supports transition by already-qualified 737 crews through differences training.",
        "737 MAXは従来型操縦輪と737共通型式の考え方を維持しながら、4面の大型カラー表示器を採用します。既存737乗員は差異訓練で移行できる設計です。"),
    "windshield": tri(
        "駕駛艙外窗維持 737 家族稜角分明、由中央向側面分段排列的輪廓。相較 A320 家族較圓順的窗框，它仍是辨認 Boeing 737 系列的重要正面特徵。",
        "The flight-deck glazing keeps the angular, segmented 737-family outline from the centre panes around to the side windows. Compared with the smoother A320-family framing, it remains a strong frontal Boeing 737 cue.",
        "操縦室窓は中央から側面へ角張った分割配置となる737ファミリーの輪郭を保ちます。より滑らかなA320系の窓枠に対し、正面から737を見分ける重要な特徴です。"),
    "engine": tri(
        "MAX 專用 CFM LEAP-1B 的風扇直徑大於 737NG 的 CFM56，短起落架限制使其仍緊貼翼下前方。鋸齒狀尾緣整流罩（chevron）與較圓的進氣口是主要辨識點。",
        "The MAX-specific CFM LEAP-1B has a larger fan than the 737NG's CFM56 and remains mounted close and forward beneath the wing because of limited ground clearance. Chevron nacelle trailing edges and a rounder inlet are key cues.",
        "MAX専用CFM LEAP-1Bは737NGのCFM56より大径で、地上高の制約から主翼下前方に密接して装着されます。ナセル後縁のシェブロンと丸みのある吸気口が主な識別点です。"),
    "wingtip": tri(
        "Advanced Technology 翼尖小翼由一片向上、另一片向下延伸，形成 MAX 最具代表性的分叉外型。它利用翼尖上下兩側氣流改善效率，不同於 737NG 的單片 blended winglet。",
        "The Advanced Technology winglet splits into an upward and a downward blade, creating the MAX's signature tip. It uses flow on both sides of the tip for efficiency and differs clearly from the 737NG's single blended winglet.",
        "Advanced Technologyウイングレットは上向き・下向きの2枚に分かれ、MAXを象徴する翼端形状を作ります。翼端上下の流れを利用し、737NGの単板ブレンデッド・ウイングレットと明確に異なります。"),
    "wing": tri(
        "MAX 的後掠低翼沿用 737 基本布局，但重新設計翼面、擾流板控制與翼尖區域，以配合新發動機並降低巡航阻力。前緣裝置和後緣襟翼負責起降低速性能。",
        "The MAX keeps the basic 737 low swept-wing arrangement but revises the wing surface, spoiler control and tip region for the new engines and lower cruise drag. Leading-edge devices and trailing-edge flaps provide take-off and landing performance.",
        "MAXは737の低翼後退翼配置を維持しながら、新エンジンと巡航抵抗低減に合わせて翼面、スポイラー制御、翼端部を改設計しています。前縁装置と後縁フラップが離着陸性能を担います。"),
    "gear": tri(
        "為容納較大的 LEAP-1B，MAX 的前起落架比 737NG 加高。主起落架仍向內收進機腹且輪胎外側可見；MAX 10 另採可伸縮連桿式主起落架，以維持較長機身的尾部離地間隙。",
        "To clear the larger LEAP-1B, the MAX nose gear is taller than the 737NG's. The main gear still retracts inward with the tyre sides exposed; the MAX 10 uniquely adds a levered main-gear mechanism to preserve tail clearance for its longer fuselage.",
        "大型LEAP-1Bの地上高確保のため、MAXの前脚は737NGより長くなっています。主脚はタイヤ側面を露出したまま胴体へ格納され、MAX 10のみ長い胴体の尾部クリアランスを守るレバー式主脚機構を備えます。"),
    "vstab": tri("垂直尾翼沿用 737 家族高聳後掠的基本輪廓，根部背鰭平順連接機身。方向舵負責偏航控制；各 MAX 子型尾部外觀大致相同。", "The vertical tail retains the tall swept 737-family outline and a dorsal root blending into the fuselage. The rudder controls yaw; tail appearance is broadly shared across MAX variants.", "垂直尾翼は737系の高い後退形状と胴体へつながるドーサル基部を維持します。方向舵がヨーを制御し、尾部外観はMAX各型で概ね共通です。"),
    "hstab": tri("低置水平尾翼與可調安定面延續 737 傳統布局，控制俯仰與配平。它不是 MAX 子型間的主要辨識點，應搭配機身長度、出口與起落架判斷。", "The low-mounted horizontal tail and trimmable stabilizer continue the traditional 737 arrangement for pitch and trim. It is not a primary MAX-variant cue; use fuselage length, exits and landing gear instead.", "低位置水平尾翼と可動安定板は737伝統配置を継承し、ピッチとトリムを制御します。MAX各型の主要識別点ではなく、胴体長、非常口、降着装置を併用します。"),
}

OVERRIDES = {
    "a319n": {
        "overview": tri("A319neo 是 A320neo 家族的短機身型，結合約 34 公尺機身、兩種新世代引擎與 Sharklet。較少座位配合良好航程，適合需求較薄但航段較長的市場。", "The A319neo is the short-fuselage A320neo-family member, combining an approximately 34-metre body with new-generation engines and Sharklets. Lower capacity and useful range suit thinner, longer sectors.", "A319neoはA320neoファミリーの短胴型で、約34 mの胴体に新世代エンジンとSharkletを組み合わせます。少ない座席数と良好な航続性能により、需要の薄い長距離区間に適します。"),
        "fuselage": tri("A319neo 的窄體機身比 A320neo 短，通常每側配置三個主要客艙門與翼上逃生出口。短胴比例是與 A320／A321neo 最直接的辨識方式。", "The A319neo narrow body is shorter than the A320neo and normally has three principal cabin doors per side plus overwing exits. Its short proportions are the quickest cue against the A320 and A321neo.", "A319neoの単通路胴体はA320neoより短く、通常は片側3か所の主要客室扉と主翼上非常口を備えます。短い胴体比率がA320／A321neoとの最も直接的な識別点です。"),
    },
    "a320n": {
        "overview": tri("A320neo 是 neo 家族的基準型，保留 A320 的六人並排單走道客艙，換裝新世代引擎與 Sharklet。它以相近外廓提供較低油耗、噪音與營運成本。", "The A320neo is the baseline neo variant, retaining the A320's six-abreast single-aisle cabin while adding new-generation engines and Sharklets. It delivers lower fuel burn, noise and operating cost within a familiar envelope.", "A320neoはneoファミリーの基準型で、A320の6席横単通路客室を維持しながら新世代エンジンとSharkletを採用します。同等の外形で燃費、騒音、運航費を低減します。"),
        "fuselage": tri("A320neo 使用約 37.6 公尺長的 A320 窄體機身，典型每側有前後客艙門與兩個翼上逃生出口。長度介於 A319neo 與 A321neo 之間。", "The A320neo uses the approximately 37.6-metre A320 narrow body, typically with forward and aft cabin doors plus two overwing exits per side. Its length sits between the A319neo and A321neo.", "A320neoは全長約37.6 mのA320単通路胴体を使用し、通常は片側に前後の客室扉と2か所の主翼上非常口を備えます。長さはA319neoとA321neoの中間です。"),
    },
    "a321n": {
        "overview": tri("A321neo 是 A320neo 家族的加長高容量型，使用新世代引擎與 Sharklet，並可採 Airbus Cabin Flex 艙門配置。它在單走道市場兼顧較多座位與較長航程。", "The A321neo is the stretched, high-capacity A320neo-family member with new-generation engines, Sharklets and optional Airbus Cabin Flex door arrangements. It combines more seats with longer single-aisle range.", "A321neoはA320neoファミリーの長胴・大容量型で、新世代エンジン、Sharklet、Airbus Cabin Flex扉配置を採用できます。単通路機で多い座席数と長い航続距離を両立します。"),
        "fuselage": tri("約 44.5 公尺的加長窄體機身是 A321neo 的核心特徵。早期配置每側四扇大型客艙門；ACF 配置則調整中後段艙門與翼上出口，應依實機門位辨認。", "The approximately 44.5-metre stretched narrow body defines the A321neo. Early layouts use four large cabin doors per side; ACF layouts relocate or replace mid/aft doors and overwing exits, so door pattern must be read aircraft by aircraft.", "約44.5 mの長胴単通路胴体がA321neoの核心です。初期配置は片側4枚の大型扉、ACF配置は中央・後方扉と主翼上非常口が変更されるため、実機ごとの扉配置確認が必要です。"),
    },
    "a321xlr": {
        "overview": tri("A321XLR 是 A321neo 的超長程衍生型，利用整合式後中央油箱、結構與起落架強化，把單走道飛機延伸到跨洲航線。外觀仍接近 A321neo，辨識通常需結合型號標記與營運資訊。", "The A321XLR is the extra-long-range A321neo derivative. An integrated rear centre tank plus structural and landing-gear changes extend a single-aisle aircraft into intercontinental missions. Externally it remains close to an A321neo, so markings and operator context often matter.", "A321XLRはA321neoの超長距離派生型です。統合式後部中央燃料タンク、構造・脚の強化により単通路機を大陸間路線へ拡張します。外観はA321neoに近く、型式表示や運航情報も識別に必要です。"),
        "fuselage": tri("機身長度與 A321neo 相同，主要差異藏在下部貨艙與後中央油箱區，而非額外拉長。Cabin Flex 艙門配置可依航空公司座椅與逃生需求調整。", "Fuselage length is the same as the A321neo; the major change lies within the lower hold and integrated rear centre tank rather than another stretch. Cabin Flex door arrangements vary with operator seating and evacuation requirements.", "胴体長はA321neoと同じで、主な変更は追加延長ではなく下部貨物室と統合式後部中央燃料タンクにあります。Cabin Flexの扉配置は各社の座席・避難要件で変わります。"),
        "gear": tri("XLR 的起落架與周邊結構針對更高最大起飛重量強化，但仍維持 A321 家族的雙輪前三點式配置。外觀差異不大，不能只靠輪組判斷。", "The XLR landing gear and surrounding structure are reinforced for higher maximum take-off weight while retaining the A321 family's twin-wheel tricycle arrangement. External differences are subtle, so the gear alone is not a reliable identifier.", "XLRの降着装置と周辺構造は高い最大離陸重量に合わせて強化されますが、A321系の各脚2輪式前輪配置を維持します。外観差は小さく、脚だけでは確実に識別できません。"),
    },
    "a338": {
        "overview": tri("A330-800 是較短的 A330neo，結合 A330-200 級機身、重新設計的長翼與 Rolls-Royce Trent 7000。它以較少座位提供長航程，與 -900 最容易由機身長度區分。", "The A330-800 is the shorter A330neo, combining an A330-200-class fuselage with a redesigned long wing and Rolls-Royce Trent 7000 engines. It trades capacity for range and is most easily distinguished from the -900 by fuselage length.", "A330-800は短胴型A330neoで、A330-200級胴体に再設計された長い主翼とRolls-Royce Trent 7000を組み合わせます。座席数を抑えて航続距離を伸ばし、-900とは胴体長で見分けやすい型です。"),
        "fuselage": tri("A330-800 沿用 A330-200 級的短廣體機身與每排八座客艙寬度。相較 A330-900，主翼前後的圓筒段更短，整體比例較緊湊。", "The A330-800 retains the shorter A330-200-class wide body and typical eight-abreast cabin width. Compared with the A330-900, its cylindrical sections ahead of and behind the wing are shorter, giving more compact proportions.", "A330-800はA330-200級の短いワイドボディと標準8席横の客室幅を引き継ぎます。A330-900より主翼前後の円筒部が短く、全体に引き締まった比率です。"),
        "hstab": tri("低置後掠水平尾翼與 A330 家族共通，安裝在後機身兩側並以升降舵和可調安定面控制俯仰。它本身無法可靠區分 -800 與 -900。", "The low swept horizontal tail is common to the A330 family, mounted on either side of the aft fuselage with elevators and a trimmable stabilizer for pitch control. It does not reliably distinguish the -800 from the -900.", "低位置後退水平尾翼はA330ファミリー共通で、後部胴体両側に付き昇降舵と可動安定板でピッチを制御します。これだけでは-800と-900を確実に区別できません。"),
    },
    "a339": {
        "overview": tri("A330-900 是 A330neo 的長機身主力型，以 A330-300 級容量搭配 Trent 7000、新翼與弧形複合材料翼尖。它保留 A330 機身截面並提升航程與效率。", "The A330-900 is the longer, principal A330neo variant, pairing A330-300-class capacity with Trent 7000 engines, a new wing and curved composite tips. It retains the A330 cross-section while improving range and efficiency.", "A330-900はA330neoの長胴主力型で、A330-300級の容量にTrent 7000、新主翼、曲線的な複合材翼端を組み合わせます。A330の胴体断面を維持しつつ航続距離と効率を向上します。"),
        "fuselage": tri("A330-900 使用約 63.7 公尺長的 A330-300 級廣體機身，典型每排八座。長直的客艙圓筒段讓它明顯長於 A330-800。", "The A330-900 uses an approximately 63.7-metre A330-300-class wide body, normally seating eight abreast. Its long straight cabin barrel makes it visibly longer than the A330-800.", "A330-900は全長約63.7 mのA330-300級ワイドボディを使用し、通常は8席横です。長い客室円筒部によりA330-800より明らかに長く見えます。"),
    },
    "a35k": {
        "overview": tri("A350-1000 是 A350 XWB 家族的加長高容量型，配備推力更高的 Trent XWB-97、較長機身與六輪主起落架。它與 A350-900 共享複合材料機體和翼型，但比例與輪組不同。", "The A350-1000 is the stretched, higher-capacity A350 XWB member, using higher-thrust Trent XWB-97 engines, a longer fuselage and six-wheel main bogies. It shares the composite airframe and wing family with the -900 but differs in proportions and landing gear.", "A350-1000はA350 XWBファミリーの長胴・大容量型で、高推力Trent XWB-97、長い胴体、6輪主脚台車を備えます。複合材機体と翼の系統は-900と共通ですが、比率と脚で区別できます。"),
        "fuselage": tri("約 73.8 公尺長的雙走道機身比 A350-900 多出約七公尺，通常保留每側四扇大型客艙門。細長比例與翼後較長的機身段是辨識線索。", "At about 73.8 metres, the twin-aisle fuselage is roughly seven metres longer than the A350-900 and normally retains four large cabin doors per side. Its elongated proportions and longer aft body are useful cues.", "全長約73.8 mの双通路胴体はA350-900より約7 m長く、通常は片側4枚の大型客室扉を維持します。細長い比率と主翼後方の長い胴体が識別点です。"),
        "engine": tri("兩具 Rolls-Royce Trent XWB-97 為 -1000 提供更高推力，風扇直徑與短艙外形仍延續 A350 家族特徵。型號差異主要在額定推力與內部設計，外觀需結合機身和輪組判斷。", "Two Rolls-Royce Trent XWB-97 engines provide the -1000's higher thrust while retaining the A350 family's large-fan nacelle appearance. Rating and internal design differ most, so external identification should combine fuselage and gear cues.", "2基のRolls-Royce Trent XWB-97が-1000向け高推力を供給し、大径ファンのナセル外観はA350系を受け継ぎます。差は主に定格と内部設計のため、外観識別では胴体と脚も併用します。"),
        "gear": tri("A350-1000 的每具主起落架有六個輪胎（三軸），而 A350-900 通常為四輪主架。這是從側面辨別兩型最可靠的特徵之一。", "Each A350-1000 main landing-gear bogie carries six tyres on three axles, whereas the A350-900 normally uses four-wheel bogies. This is one of the most reliable side-view distinctions.", "A350-1000の主脚台車は3軸6輪で、通常4輪台車のA350-900と異なります。側面から両型を見分ける最も確実な特徴の一つです。"),
    },
    "belugaxl": {
        "overview": tri("BelugaXL 是以 A330-200F 為基礎打造的超大型零組件運輸機，用於 Airbus 生產網路。巨大的上部貨艙、低置駕駛艙與鯨魚造型使它無法與普通客機混淆。", "The BelugaXL is an outsized component transport derived from the A330-200F for Airbus's production network. Its enormous upper hold, lowered flight deck and whale-like profile make it unmistakable.", "BelugaXLはA330-200Fを基にAirbus生産網向けに開発された超大型部品輸送機です。巨大な上部貨物室、低い操縦室、クジラ状の外形で通常の旅客機とは容易に区別できます。"),
        "cockpit": tri("駕駛艙位於巨大貨艙地板下方，使機組區不必隨前方貨門一起開啟。主要飛行控制與顯示承襲 A330 家族，有利於訓練與維修共通性。", "The flight deck sits below the oversized cargo floor, so the crew area does not move with the forward cargo door. Principal controls and displays retain A330-family commonality for training and maintenance.", "操縦室は巨大貨物床の下にあり、前方貨物扉とともに動きません。主要な操縦・表示系はA330ファミリーとの共通性を保ち、訓練と整備を容易にします。"),
        "windshield": tri("外窗仍呈 A330 家族的六片分段輪廓，但位置被壓低在巨大貨艙鼻部下方。正面看來，窗帶與機鼻頂部之間的高度差極大。", "The glazing retains the A330 family's segmented six-pane outline but is positioned low beneath the huge cargo nose. Head-on, the large vertical gap between the window belt and crown is distinctive.", "外窓はA330系の分割6枚形状を保ちますが、巨大な貨物ノーズ下に低く配置されます。正面では窓帯と機体頂部の大きな高低差が特徴です。"),
        "fuselage": tri("加大的上部貨艙提供約 2,209 立方公尺容積，前端以大型上掀式貨門裝卸飛機翼段與機身段。下半部仍可看出 A330-200F 的機身基礎。", "The enlarged upper hold provides about 2,209 cubic metres of volume, loaded through a huge upward-opening forward door for wings and fuselage sections. The lower fuselage still reveals its A330-200F foundation.", "拡大上部貨物室は約2,209立方メートルの容積を持ち、翼や胴体区画を大型上開き前方扉から搭載します。下部胴体にはA330-200Fの基礎が残ります。"),
        "engine": tri("BelugaXL 使用兩具 Rolls-Royce Trent 700 渦輪扇，安裝於 A330 型主翼下。它沒有採用 A330neo 的 Trent 7000，因此不能只因 BelugaXL 較新就視為 neo 動力。", "The BelugaXL uses two Rolls-Royce Trent 700 turbofans beneath its A330 wing. It does not use the A330neo's Trent 7000, so its newer service date must not be mistaken for neo propulsion.", "BelugaXLはA330型主翼下に2基のRolls-Royce Trent 700を装備します。A330neoのTrent 7000ではなく、新しい就航時期だけでneo系動力と判断できません。"),
        "wingtip": tri("翼尖採 A330ceo 家族的小型上下翼尖柵，而非 A330neo 的長弧形翼尖。這是辨認其 A330-200F 基礎的重要細節。", "The tips use the A330ceo family's small upper-and-lower wingtip fences rather than the A330neo's long curved tips. This is a useful clue to its A330-200F basis.", "翼端はA330neoの長い曲線翼端ではなく、A330ceo系の小型上下ウイングチップフェンスです。A330-200Fを基礎とする重要な識別点です。"),
        "wing": tri("低置後掠翼源自 A330-200F，承受巨大機身增加的側面積與任務載荷。前緣縫翼、後緣襟翼及擾流板維持大型運輸機的起降與操縱需求。", "The low swept wing derives from the A330-200F and carries the mission loads beneath the much larger side area. Slats, flaps and spoilers provide the required low-speed and control performance.", "低翼後退翼はA330-200F由来で、巨大な側面積と任務荷重を支えます。前縁スラット、後縁フラップ、スポイラーが低速性能と操縦性を担います。"),
        "vstab": tri("垂直尾翼加大以補償巨大貨艙造成的方向安定影響，並保留 Airbus 鯨魚塗裝的尾部輪廓。尾翼面積與高聳比例明顯大於一般 A330。", "The vertical tail is enlarged to offset the directional-stability effects of the enormous cargo body and forms the aft outline of the whale livery. Its area and height are conspicuously greater than on a standard A330.", "巨大貨物胴体による方向安定への影響を補うため垂直尾翼は拡大され、クジラ塗装の後部輪郭を構成します。通常のA330より面積と高さが目立ちます。"),
        "hstab": tri("水平尾翼外端增設垂直端板，協助巨大機身在偏航時維持穩定。這對端板是 BelugaXL 尾部最容易辨認的細節之一。", "Vertical endplates are added at the horizontal-tail tips to help stabilise the huge fuselage in yaw. These fins are among the easiest BelugaXL tail identifiers.", "水平尾翼端には垂直エンドプレートが追加され、巨大胴体のヨー安定を助けます。このフィンはBelugaXL尾部の分かりやすい識別点です。"),
        "gear": tri("前三點式起落架沿用 A330 貨機基礎：雙輪前架與每側四輪主架。寬輪距支撐大型機體，外形不像 A350-1000 的六輪主架。", "The tricycle gear follows the A330 freighter basis: twin nose wheels and four-wheel main bogies on each side. Its wide track supports the large airframe and differs from the A350-1000's six-wheel bogies.", "前輪式降着装置はA330貨物型を基礎とし、前脚2輪、左右各4輪の主脚台車です。広い輪距で大型機体を支え、A350-1000の6輪台車とは異なります。"),
    },
}

MAX_VARIANTS = {
    "b37m": ("737 MAX 7 是 MAX 家族最短的型號，以較少座位換取良好航程與短場彈性。短機身、LEAP-1B 與上下分叉翼尖是主要外觀組合。", "The 737 MAX 7 is the shortest MAX member, trading capacity for range and short-field flexibility. Its short fuselage, LEAP-1B engines and split winglets form the main visual combination.", "737 MAX 7はMAXファミリー最短型で、座席数を抑えて航続距離と短距離滑走路性能を得ています。短い胴体、LEAP-1B、上下分岐翼端が主要な外観特徴です。", "MAX 7 的機身短於 MAX 8，前後艙門之間的窗列較少。它仍使用六人並排的 737 單走道截面。", "The MAX 7 fuselage is shorter than the MAX 8, with fewer window bays between the forward and aft doors. It retains the 737 six-abreast single-aisle cross-section.", "MAX 7の胴体はMAX 8より短く、前後扉間の窓列が少なくなります。737の6席横単通路断面は共通です。"),
    "b38m": ("737 MAX 8 是 MAX 家族的基準主力型，大小接近 737-800，但以 LEAP-1B、分叉翼尖與新座艙系統提升效率。", "The 737 MAX 8 is the baseline and principal MAX variant, similar in size to the 737-800 but using LEAP-1B engines, split winglets and updated flight-deck systems for improved efficiency.", "737 MAX 8はMAXファミリーの基準・主力型で、737-800に近い大きさながらLEAP-1B、分岐翼端、新しい操縦室システムで効率を高めます。", "MAX 8 的機身長度接近 737-800，典型每側有前後大型客艙門與兩個翼上逃生出口。辨識需搭配發動機與翼尖。", "The MAX 8 is close in length to the 737-800, typically with forward and aft cabin doors and two overwing exits per side. Engines and winglets are needed for confident identification.", "MAX 8は737-800に近い胴体長で、通常は片側に前後の大型客室扉と2か所の主翼上非常口があります。確実な識別にはエンジンと翼端も確認します。"),
    "b39m": ("737 MAX 9 是 MAX 8 的加長型，提供更多座位並保留相同 LEAP-1B 與分叉翼尖特徵。長機身與額外艙門／出口配置是辨識重點。", "The 737 MAX 9 is a stretched MAX 8 with more capacity while retaining the same LEAP-1B and split-winglet cues. Its longer fuselage and additional door/exit arrangement are key identifiers.", "737 MAX 9はMAX 8の長胴型で、同じLEAP-1Bと分岐翼端を保ちながら容量を増やします。長い胴体と追加扉・非常口配置が識別点です。", "MAX 9 機身比 MAX 8 長，翼後段比例增加；高密度配置可使用額外中後段出口。與 MAX 10 相比仍稍短。", "The MAX 9 is longer than the MAX 8, especially aft of the wing, and high-density layouts may use an additional mid-aft exit. It remains slightly shorter than the MAX 10.", "MAX 9はMAX 8より長く、特に主翼後方が伸びています。高密度配置では中央後方に追加非常口を備える場合があり、MAX 10よりは短い型です。"),
    "b3xm": ("737 MAX 10 是 MAX 家族最長、容量最大的型號。它在 MAX 9 基礎上再加長，並使用獨特的可伸縮連桿式主起落架維持起飛仰角與尾部間隙。", "The 737 MAX 10 is the longest and highest-capacity MAX. It stretches the MAX 9 further and uniquely uses levered main landing gear to preserve take-off rotation angle and tail clearance.", "737 MAX 10はMAXファミリー最長・最大容量型です。MAX 9をさらに延長し、離陸引き起こし角と尾部間隔を守る独自のレバー式主脚を採用します。", "MAX 10 擁有全系列最長的 737 機身，翼前後圓筒段都更長。艙門與出口配置服務較高載客量，側面比例最為修長。", "The MAX 10 has the longest 737 fuselage, with extended cylindrical sections around the wing. Door and exit arrangements support its higher capacity, giving the most elongated MAX profile.", "MAX 10は737系列最長の胴体を持ち、主翼前後の円筒部が伸びています。高い座席数に対応する扉・非常口配置を持ち、MAXで最も細長い側面比率です。"),
}

for ident, values in MAX_VARIANTS.items():
    OVERRIDES[ident] = {"overview": tri(*values[:3]), "fuselage": tri(*values[3:])}

PART_SPECS = {
    "a319n": {"fuselage": [["全長", "33.84 m"], ["典型載客量", "120–150"]], "engine": [["型號", "LEAP-1A / PW1100G-JM"]], "wing": [["翼展", "35.8 m"]]},
    "a320n": {"fuselage": [["全長", "37.57 m"], ["典型載客量", "150–180"]], "engine": [["型號", "LEAP-1A / PW1100G-JM"]], "wing": [["翼展", "35.8 m"]]},
    "a321n": {"fuselage": [["全長", "44.51 m"], ["典型載客量", "180–220"]], "engine": [["型號", "LEAP-1A / PW1100G-JM"]], "wing": [["翼展", "35.8 m"]]},
    "a321xlr": {"fuselage": [["全長", "44.51 m"], ["核心油箱", "整合式後中央油箱"]], "engine": [["型號", "LEAP-1A / PW1100G-JM"]], "wing": [["翼展", "35.8 m"]], "gear": [["配置", "雙輪前三點式"], ["特徵", "高重量型強化結構"]]},
    "a338": {"fuselage": [["全長", "58.82 m"], ["典型載客量", "220–260"]], "engine": [["型號", "Rolls-Royce Trent 7000"]], "wing": [["翼展", "64.0 m"]]},
    "a339": {"fuselage": [["全長", "63.66 m"], ["典型載客量", "260–300"]], "engine": [["型號", "Rolls-Royce Trent 7000"]], "wing": [["翼展", "64.0 m"]]},
    "a35k": {"fuselage": [["全長", "73.79 m"], ["典型載客量", "350–410"]], "engine": [["型號", "Rolls-Royce Trent XWB-97"]], "gear": [["主起落架", "每側 3 軸 × 6 輪"]]},
    "belugaxl": {"fuselage": [["全長", "63.1 m"], ["貨艙容積", "約 2,209 m³"], ["最大酬載", "51 t"]], "engine": [["型號", "Rolls-Royce Trent 700"]], "wing": [["翼展", "60.3 m"]], "gear": [["主起落架", "每側 4 輪"]]},
    "b37m": {"fuselage": [["全長", "35.56 m"], ["典型載客量", "138–153"]]},
    "b38m": {"fuselage": [["全長", "39.52 m"], ["典型載客量", "162–178"]]},
    "b39m": {"fuselage": [["全長", "42.16 m"], ["典型載客量", "178–193"]]},
    "b3xm": {"fuselage": [["全長", "43.80 m"], ["典型載客量", "188–204"]], "gear": [["主起落架", "每側雙輪、可伸縮連桿式"]]},
}
for ident in MAX_VARIANTS:
    PART_SPECS[ident].update({"cockpit": [["主要顯示器", "4 具大型彩色顯示器"]], "engine": [["型號", "CFM LEAP-1B"]], "wing": [["翼展", "35.9 m"]]})


def main():
    for ident, base_id in BASES.items():
        target_path = ROOT / "data" / f"{ident}.json"
        base = json.loads((ROOT / "data" / f"{base_id}.json").read_text(encoding="utf-8"))
        target = json.loads(target_path.read_text(encoding="utf-8"))
        existing = {part_id: deepcopy(part) for part_id, part in target.get("parts", {}).items()}
        target["partOrder"] = ORDER
        target["parts"] = deepcopy(base["parts"])
        for part_id, part in target["parts"].items():
            old = existing.get(part_id, {})
            part["images"] = old.get("images", [])
            if old.get("fact") and any(old["fact"].values()):
                part["fact"] = old["fact"]
            for field in ("bullets", "specs"):
                if old.get(field):
                    part[field] = old[field]
        shared = (COMMON_MAX if ident in MAX_VARIANTS else
                  COMMON_A320NEO if ident in {"a319n", "a320n", "a321n", "a321xlr"} else
                  COMMON_A330NEO if ident in {"a338", "a339"} else {})
        for part_id, summary in {**shared, **OVERRIDES.get(ident, {})}.items():
            target["parts"][part_id]["summary"] = summary
            target["parts"][part_id]["specs"] = PART_SPECS.get(ident, {}).get(part_id, [])
            old = existing.get(part_id, {})
            if not old.get("fact") or not any(old["fact"].values()):
                target["parts"][part_id]["fact"] = {"zh": "", "en": "", "ja": ""}
            if not old.get("bullets"):
                target["parts"][part_id]["bullets"] = []
        target_path.write_text(json.dumps(target, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for ident in BASES:
        record = json.loads((ROOT / "data" / f"{ident}.json").read_text(encoding="utf-8"))
        assert record["partOrder"] == ORDER and set(record["parts"]) == set(ORDER)
        assert all(set(part["summary"]) == {"zh", "en", "ja"} and all(part["summary"].values()) for part in record["parts"].values())
        assert all(isinstance(part["images"], list) for part in record["parts"].values())
    print(f"Enriched {len(BASES)} aircraft with {len(ORDER)} parts each")


if __name__ == "__main__":
    main()
