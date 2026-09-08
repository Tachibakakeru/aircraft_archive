"""Add ten-part trilingual records to the second commercial-aircraft batch."""

from copy import deepcopy
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
ORDER = ["overview", "cockpit", "windshield", "fuselage", "engine", "wingtip", "wing", "vstab", "hstab", "gear"]
BASES = {
    "b779": "b773", "b78x": "b789", "b763f": "b763", "b77f": "b772",
    "e175": "e170", "e190e2": "e190", "e195e2": "e190",
    "atr72": "atr42", "atr72f": "atr42", "dhc6-400": "q400", "c408": "q400", "l410ng": "q400",
}
RENAME_BASE = {
    "b779": ("777-300", "777-9"), "b78x": ("787-9", "787-10"),
    "b763f": ("767-300", "767-300F"), "b77f": ("777-200", "777 Freighter"),
    "e175": ("E170", "E175"), "e190e2": ("E190", "E190-E2"),
    "e195e2": ("E190", "E195-E2"), "atr72": ("ATR 42", "ATR 72-600"),
    "atr72f": ("ATR 42", "ATR 72-600F"),
}


def t(zh, en, ja):
    return {"zh": zh, "en": en, "ja": ja}


def renamed(value, old, new):
    if isinstance(value, str):
        return value.replace(old, new)
    if isinstance(value, list):
        return [renamed(item, old, new) for item in value]
    if isinstance(value, dict):
        return {key: renamed(item, old, new) for key, item in value.items()}
    return value


def without_media_refs(summary):
    replacements = {
        "zh": (("附圖是", ""), ("這張照片用來", "此配置可"), ("由下方平面照片可", "從下方平面可"),
               ("正面和側面照片可", "從正面和側面可"), ("正面照片可", "從正面可"), ("側面照片可", "從側面可"),
               ("下方照片可", "從下方可"), ("照片中", "實機上"), ("照片可", "可"), ("實照", "實機"), ("照片", "實機"), ("附圖", "")),
        "en": (("The photo shows", ""), ("The image shows", ""), ("the photo", "the aircraft"),
               ("the image", "the aircraft"), ("as pictured", ""), ("pictured", "visible"), ("photo", "view"), ("image", "view")),
        "ja": (("下面写真で", "下面から"), ("正面写真で", "正面から"), ("側面写真で", "側面から"),
               ("写真は", ""), ("写真で", "実機では"), ("写真の", "実機の"), ("写真", "実機"), ("画像", "実機")),
    }
    cleaned = {}
    for lang, text in summary.items():
        for old, new in replacements[lang]:
            text = re.sub(re.escape(old), new, text, flags=re.IGNORECASE)
        cleaned[lang] = text.strip()
        assert cleaned[lang], f"media cleanup removed all {lang} text"
    return cleaned


E2_COMMON = {
    "cockpit": t("E2 採雙人玻璃座艙與 fly-by-wire 飛控，更新的大尺寸顯示器與航電延續 E-Jet 操作邏輯。駕駛艙外觀與第一代相近，但系統與人機介面已現代化。", "The E2 uses a two-crew glass cockpit and fly-by-wire controls. Larger displays and updated avionics retain the E-Jet operating philosophy while modernising the systems and interface.", "E2は2名乗務のグラスコックピットとフライ・バイ・ワイヤを採用します。大型表示器と更新された電子機器はE-Jetの操作思想を保ちながらシステムを近代化しています。"),
    "engine": t("兩具 Pratt & Whitney PW1900G 齒輪傳動渦輪扇安裝於翼下。大型圓形風扇與較長短艙，是 E2 與使用 CF34 的第一代 E-Jet 最明顯差異。", "Two Pratt & Whitney PW1900G geared turbofans are mounted beneath the wing. Their large round fans and longer nacelles are the clearest cues against first-generation E-Jets with CF34 engines.", "2基のPratt & Whitney PW1900Gギヤードターボファンを翼下に装備します。大径の丸いファンと長いナセルが、CF34搭載の初代E-Jetとの最も明確な違いです。"),
    "wing": t("E2 使用重新設計的高展弦比後掠翼，而非單純沿用第一代翼面。翼型、控制面與翼身整流針對較低阻力和新發動機整合最佳化。", "The E2 uses a redesigned high-aspect-ratio swept wing rather than simply retaining the first-generation surface. Aerofoil, controls and fairings are optimised for lower drag and the new engines.", "E2は初代翼をそのまま使わず、再設計した高アスペクト比後退翼を採用します。翼型、操縦面、フェアリングは低抵抗と新エンジン統合に最適化されています。"),
    "wingtip": t("翼尖平順上彎並與新翼融合，沒有獨立直立翼尖小翼。從遠處看，細長翼展和連續曲線有別於第一代 E-Jet 常見的翼尖形式。", "The tip curves upward as an integrated continuation of the new wing rather than a separate upright winglet. Its long span and continuous curve differ from typical first-generation E-Jet tips.", "翼端は独立した直立ウイングレットではなく、新主翼から連続して上方へ湾曲します。長い翼幅と連続曲線が初代E-Jetの翼端と異なります。"),
    "gear": t("前三點式起落架針對 E2 較高重量與大型發動機重新配置，主架向翼根／機身區收納。輪組外觀仍維持支線噴射機常見的雙輪配置。", "The tricycle landing gear is revised for the E2's higher weights and larger engines, with the main units retracting around the wing-root/fuselage area. Twin-wheel units retain a familiar regional-jet appearance.", "前輪式降着装置はE2の高重量と大型エンジンに合わせて改良され、主脚は翼根・胴体付近へ格納されます。各脚2輪の外観はリージョナルジェットらしい構成です。"),
}

HIGH_WING_COCKPIT = {
    "cockpit": t("雙人座艙以短場與通勤任務為核心，配置現代化顯示器、導航與發動機監控。大型前窗提供進場、未鋪設跑道與地面操作所需視野。", "The two-crew cockpit is arranged around commuter and short-field work, with modern displays, navigation and engine monitoring. Large forward windows support approaches, unpaved-strip and ground operations.", "2名乗務の操縦室は通勤・短距離滑走路任務を中心に、現代的表示、航法、エンジン監視を備えます。大型前窓が進入、未舗装滑走路、地上運用の視界を確保します。"),
    "windshield": t("寬大的多片式駕駛艙外窗兼顧前下方與側向視野，適合低高度、短場及偏遠地區操作。各型窗柱與機鼻比例不同，可配合發動機與起落架辨認。", "Large multi-pane flight-deck glazing provides forward-downward and side visibility for low-level, short-field and remote operations. Pillar and nose proportions vary by type and should be read with engines and landing gear.", "大型の分割操縦室窓は前下方と側方視界を確保し、低高度・短距離・遠隔地運用に適します。窓柱と機首比率は型式ごとに異なり、エンジンや脚と併せて識別します。"),
}

ATR_COMMON = {
    "cockpit": t("ATR 72-600 採雙人玻璃座艙，Thales 航電以五具大型液晶顯示器整合飛行、導航與系統資訊。傳統駕駛盤和中央動力桿保留渦槳機操作布局。", "The ATR 72-600 has a two-crew glass cockpit whose Thales avionics combine flight, navigation and systems information on five large LCDs. Conventional yokes and central power levers retain a familiar turboprop layout.", "ATR 72-600は2名乗務グラスコックピットで、Thales電子機器が5面の大型LCDに飛行・航法・システム情報を統合します。通常操縦輪と中央出力レバーはターボプロップらしい配置です。"),
    "windshield": t("多片式駕駛艙外窗包覆短而圓潤的機鼻，中央風擋較寬、側窗逐步收窄。窗框比例與高翼、T 尾共同構成 ATR 家族輪廓。", "Multi-pane flight-deck glazing wraps around a short rounded nose, with broad centre panes narrowing toward the sides. Its framing works with the high wing and T-tail to form the ATR-family silhouette.", "分割操縦室窓は短く丸い機首を包み、広い中央窓から側面へ細くなります。窓枠、高翼、T尾翼の組合せがATR系シルエットを作ります。"),
    "wingtip": t("高翼末端平緩收尖，標準型沒有高大的直立翼尖小翼；航行燈整合在翼尖。ATR 72 的辨識重點是長直高翼，而非獨立 winglet。", "The high wing tapers to simple tips without tall upright winglets in the standard configuration, with navigation lights at the ends. The long straight high wing, not a separate winglet, is the main ATR 72 cue.", "高翼は単純に細くなる翼端を持ち、標準仕様に大型直立ウイングレットはありません。航法灯を端部に備え、独立翼端板より長い直線高翼がATR 72の特徴です。"),
    "vstab": t("後掠單垂尾由短尾錐上方升起，頂端承載水平尾翼；大型方向舵在單發狀況下提供偏航控制。高垂尾是 ATR 的鮮明側面特徵。", "A swept single fin rises above the short tail cone and carries the horizontal tail at its tip. A large rudder provides yaw authority after an engine failure, making the tall fin a strong ATR side-view cue.", "後退した単一垂直尾翼が短い尾部から立ち上がり、頂部に水平尾翼を載せます。大型方向舵が片発時のヨーを制御し、高い垂尾はATRの明確な側面特徴です。"),
    "hstab": t("水平尾翼位於垂尾頂端形成真正 T 尾，讓尾翼遠離高翼與螺旋槳尾流。左右升降舵控制俯仰，外形與低置尾翼支線機明顯不同。", "The horizontal tail sits atop the fin as a true T-tail, keeping it away from high-wing and propeller wake. Elevators control pitch, and the silhouette differs clearly from regional aircraft with low tailplanes.", "水平尾翼は垂尾頂部の真正T尾翼で、高翼とプロペラ後流から離れます。左右昇降舵がピッチを制御し、低位置尾翼の地域機と明確に異なります。"),
    "gear": t("可收放前三點式起落架由雙輪前架與左右雙輪主架組成；主架收進機腹兩側突出整流罩，而非發動機短艙。此輪艙位置是 ATR 的重要正面辨識點。", "Retractable tricycle gear uses twin nose wheels and twin-wheel main units. The mains stow in projecting fuselage-side fairings rather than the engine nacelles, an important head-on ATR cue.", "格納式前輪脚は前脚2輪と左右各2輪主脚で、主脚はエンジンナセルではなく胴体側面の張り出しフェアリングへ収まります。正面からの重要なATR識別点です。"),
}

OVERRIDES = {
    "b779": {
        "overview": t("777-9 是 777X 家族的大型客機，以加長機身、全新複合材料機翼、可折疊翼尖與 GE9X 為核心。它保留 777 雙發寬體布局，但翼尖與發動機能立即區別於 777-300ER。", "The 777-9 is the large 777X passenger model, built around a stretched fuselage, new composite wing, folding tips and GE9X engines. It retains the twin-engine 777 layout but is readily separated from the 777-300ER by its tips and engines.", "777-9は長胴、全新複合材主翼、折り畳み翼端、GE9Xを核とする大型777X旅客型です。777の双発ワイドボディ配置を保ちつつ、翼端とエンジンで777-300ERと容易に区別できます。"),
        "fuselage": t("約 76.7 公尺的機身使 777-9 成為 777 家族最長型之一，維持寬大的雙走道截面與每側四扇主要客艙門。細長比例和長翼共同形成外觀。", "At about 76.7 metres, the 777-9 has one of the longest 777 fuselages, retaining the broad twin-aisle cross-section and four principal cabin doors per side. Its elongated body works visually with the long wing.", "全長約76.7 mで777系列最長級の胴体を持ち、幅広い双通路断面と片側4枚の主要客室扉を維持します。長い胴体と主翼が独特の比率を作ります。"),
        "engine": t("兩具 GE9X 是目前最大級民航渦輪扇之一，具有巨大風扇、複合材料葉片與鋸齒狀短艙尾緣。其直徑和圓潤進氣口遠大於早期 777 的 GE90。", "Two GE9X engines rank among the largest civil turbofans, with huge fans, composite blades and chevron nacelle trailing edges. Their diameter and rounded inlets exceed those of earlier 777 GE90 installations.", "2基のGE9Xは最大級の民間ターボファンで、巨大ファン、複合材ブレード、シェブロン付きナセル後縁を備えます。直径と丸い吸気口は従来777のGE90を上回ります。"),
        "wingtip": t("地面滑行時翼尖可向上折疊，使展開約 71.8 公尺的長翼能使用既有 777 等級登機門；起飛前必須展平並鎖定。折疊鉸鏈是 777X 的關鍵辨識點。", "The tips fold upward on the ground so the roughly 71.8-metre-span wing can use existing 777-class gates; they must extend and lock before take-off. The hinge is a defining 777X cue.", "地上では翼端を上方へ折り畳み、展開時約71.8 mの主翼を既存777級ゲートへ収めます。離陸前に展開・固定し、ヒンジ部が777Xの決定的識別点です。"),
        "wing": t("全新高展弦比複合材料機翼具有更長翼展與明顯上反／彎曲，並整合折疊翼尖。它不是 777-300ER 金屬翼的簡單延長，而是 777X 效率提升核心。", "The new high-aspect-ratio composite wing has greater span, visible flex and integrated folding tips. It is not a simple extension of the 777-300ER metal wing but a core source of 777X efficiency.", "新しい高アスペクト比複合材主翼は長い翼幅、目立つたわみ、折り畳み翼端を統合します。777-300ER金属翼の単純延長ではなく、777X効率向上の核心です。"),
        "gear": t("大型前三點式起落架使用雙輪前架與每側六輪主架，輪組布局延續 777 家族以分散高重量。777-9 的主架另配合加長機身與起飛姿態控制。", "The large tricycle gear uses twin nose wheels and six-wheel main bogies on each side, continuing the 777 approach to distributing high weight. The 777-9 gear also supports rotation management for its long fuselage.", "大型前輪式降着装置は前脚2輪、左右各6輪主脚台車で高重量を分散する777方式を継承します。777-9では長胴の離陸姿勢管理にも対応します。"),
    },
    "b78x": {
        "overview": t("787-10 是 Dreamliner 家族最長、容量最大的型號，與 787-9 共享複合材料機身、彎曲翼尖和兩種高旁通比引擎。主要辨識點是主翼前後更長的機身，而非新的翼形。", "The 787-10 is the longest and highest-capacity Dreamliner, sharing the composite fuselage, curved tips and two engine choices with the 787-9. Its principal cue is the longer body around the same wing.", "787-10はDreamliner最長・最大容量型で、787-9と複合材胴体、曲線翼端、2種のエンジンを共有します。主な識別点は新しい翼ではなく、同じ翼の前後に伸びた胴体です。"),
        "fuselage": t("約 68.3 公尺長的複合材料機身比 787-9 再延長約 5.5 公尺，仍保留大型電致變色客艙窗與每側四扇主要客艙門。較長翼後機身段最易辨認。", "The approximately 68.3-metre composite fuselage is about 5.5 metres longer than the 787-9, retaining large electrochromic windows and four principal cabin doors per side. The extended aft body is the clearest cue.", "全長約68.3 mの複合材胴体は787-9より約5.5 m長く、大型電子調光窓と片側4枚の主要扉を維持します。長い主翼後方胴体が最も分かりやすい特徴です。"),
    },
    "b763f": {
        "overview": t("767-300F 是原廠生產的中型雙發廣體貨機，以 767-300ER 尺寸為基礎並設大型主甲板貨門。無客艙窗的長直機身、CF6 引擎與傳統翼尖形成典型外觀。", "The 767-300F is a factory-built medium twin-engine wide-body freighter based on 767-300ER dimensions, with a large main-deck cargo door. Its windowless body, CF6 engines and conventional tips form the classic profile.", "767-300Fは767-300ER寸法を基礎に大型主甲板貨物扉を備える新造中型双発貨物機です。窓のない長い胴体、CF6、通常翼端が典型的外観です。"),
        "fuselage": t("約 54.9 公尺長的廣體機身具有平整強化貨艙地板，主甲板左前方設大型貨門，可裝載標準貨盤與貨櫃。封閉窗列與貨門輪廓可區分客機。", "The approximately 54.9-metre wide body has a reinforced flat main deck and a large forward-left cargo door for standard pallets and containers. Blank window rows and the cargo-door outline distinguish it from passenger aircraft.", "全長約54.9 mのワイドボディは強化された平坦主甲板と左前方大型貨物扉を持ち、標準パレットとコンテナを搭載します。閉じた窓列と貨物扉輪郭が旅客型との識別点です。"),
        "engine": t("原廠 767-300F 使用兩具 General Electric CF6-80C2 高旁通比渦輪扇。短艙位於低翼下方，圓形進氣口與傳統尾噴口不同於新世代鋸齒短艙。", "Factory 767-300Fs use two General Electric CF6-80C2 high-bypass turbofans beneath the low wing. Round inlets and conventional exhaust nacelles differ from newer chevron-edged designs.", "新造767-300Fは低翼下に2基のGeneral Electric CF6-80C2高バイパス比ターボファンを装備します。丸い吸気口と通常排気ナセルは新世代シェブロン型と異なります。"),
        "wingtip": t("原廠貨機以傳統尖細翼尖交付，沒有 767 客機改裝常見的高大 blended winglet；部分營運商改裝狀態應依個別飛機確認。", "Factory freighters were delivered with conventional tapered tips rather than the tall blended winglets seen on some passenger 767 retrofits; individual aftermarket fits must be checked aircraft by aircraft.", "新造貨物型は通常の細い翼端で納入され、旅客767改修機で見られる大型ブレンデッド・ウイングレットは標準ではありません。後付け状態は個体ごとに確認します。"),
    },
    "b77f": {
        "overview": t("777 Freighter 以 777-200LR 機體與 777-300ER 級機翼、起落架為基礎，是長程大型雙發貨機。無窗貨艙、左側主甲板貨門與 GE90-110B1L 是主要特徵。", "The 777 Freighter combines a 777-200LR-based body with 777-300ER-class wing and landing gear as a long-range heavy twin freighter. A windowless hold, left main-deck cargo door and GE90-110B1L define it.", "777 Freighterは777-200LR系胴体に777-300ER級の翼と脚を組み合わせる長距離大型双発貨物機です。無窓貨物室、左主甲板貨物扉、GE90-110B1Lが特徴です。"),
        "fuselage": t("約 63.7 公尺的機身沒有客艙窗列，主甲板左後方設大型貨門，強化地板可承載約 102 噸最大酬載。機身長度接近 777-200，而非較長的 -300。", "The approximately 63.7-metre fuselage lacks passenger-window rows and carries a large aft-left main-deck cargo door. A reinforced floor supports roughly 102 tonnes maximum payload; body length is 777-200-like, not -300-like.", "全長約63.7 mの胴体には客室窓列がなく、左後方に大型主甲板貨物扉があります。強化床は最大約102 tを支え、胴体長は長い-300ではなく777-200系です。"),
        "engine": t("777F 由兩具 GE90-110B1L 提供動力，尺寸與推力屬大型 GE90 後期型。寬大進氣口和扭曲複合材料風扇葉片是近看辨識特徵。", "The 777F is powered by two GE90-110B1L engines from the large later GE90 family. Their huge inlets and swept composite fan blades are close-range identifiers.", "777Fは大型後期GE90系列のGE90-110B1Lを2基搭載します。巨大な吸気口と後退した複合材ファンブレードが近距離識別点です。"),
        "wingtip": t("翼尖採平順向後延伸的 raked tip，而非直立翼尖小翼。這套 64.8 公尺翼展的長翼源自 777-200LR／-300ER 級設計。", "The wing ends in smoothly swept raked tips rather than upright winglets. This 64.8-metre-span wing comes from the 777-200LR/-300ER design standard.", "翼端は直立ウイングレットではなく滑らかに後退するレイクド・チップです。翼幅64.8 mの翼は777-200LR／-300ER級設計に由来します。"),
        "wing": t("777F 使用 777-200LR／-300ER 級長展弦翼，翼展約 64.8 公尺，具前緣縫翼、後緣多縫襟翼與大型擾流板，以支撐高重量貨運起降。", "The 777F uses the long 777-200LR/-300ER-standard wing, spanning about 64.8 metres with slats, multi-element flaps and large spoilers for heavy freighter operation.", "777Fは777-200LR／-300ER級の長い主翼を使用し、翼幅約64.8 m、前縁スラット、多要素フラップ、大型スポイラーで重量貨物運航を支えます。"),
    },
    "e175": {
        "overview": t("E175 是第一代 E-Jet 的 70 至 80 席級主力型，較 E170 加長但保留四人並排客艙、翼下 CF34 與低置尾翼。它常見於北美支線航空市場。", "The E175 is the principal 70-to-80-seat first-generation E-Jet, stretched from the E170 while retaining the four-abreast cabin, underwing CF34 engines and low tail. It is especially common in North American regional service.", "E175は初代E-Jetの70～80席級主力型で、E170を延長しながら4席横客室、翼下CF34、低位置尾翼を維持します。北米リージョナル運航で特に一般的です。"),
        "fuselage": t("約 31.7 公尺長的窄體機身比 E170 稍長，客艙維持每排四座、無中間座位。每側前後主要艙門與翼上出口形成 E-Jet 典型配置。", "The approximately 31.7-metre narrow body is slightly longer than the E170 while keeping four-abreast seating without middle seats. Forward and aft doors plus overwing exits form the familiar E-Jet arrangement.", "全長約31.7 mの単通路胴体はE170より少し長く、中央席のない4席横を維持します。前後扉と主翼上非常口がE-Jetの典型配置です。"),
    },
    "e190e2": {
        **E2_COMMON,
        "overview": t("E190-E2 是第二代 E-Jet 的中型型號，以新翼、PW1900G 與更新 fly-by-wire 系統取代第一代 E190 的主要氣動與動力配置。", "The E190-E2 is the mid-size second-generation E-Jet, replacing the first E190's principal aerodynamic and propulsion arrangement with a new wing, PW1900G engines and updated fly-by-wire.", "E190-E2は第2世代E-Jetの中型で、新主翼、PW1900G、更新されたフライ・バイ・ワイヤにより初代E190の主要空力・動力構成を刷新します。"),
        "fuselage": t("約 36.2 公尺長的四人並排機身維持 E190 級容量，圓整機鼻與低置尾翼延續家族外觀。相較 E195-E2，它的翼前後圓筒段較短。", "The approximately 36.2-metre four-abreast fuselage retains E190-class capacity and the family's rounded nose and low tail. Its body sections around the wing are shorter than the E195-E2's.", "全長約36.2 mの4席横胴体はE190級容量と家族共通の丸い機首・低位置尾翼を維持します。E195-E2より主翼前後の胴体区間が短い型です。"),
    },
    "e195e2": {
        **E2_COMMON,
        "overview": t("E195-E2 是 E2 家族最長、容量最大的型號，使用 PW1900G 與專屬較長翼展。它的載客量接近小型主線窄體機，但仍保留四人並排客艙。", "The E195-E2 is the longest and highest-capacity E2, using PW1900G engines and its own longer-span wing. Capacity approaches small mainline narrow-bodies while retaining a four-abreast cabin.", "E195-E2はE2最長・最大容量型で、PW1900Gと専用の長い主翼を採用します。小型幹線単通路機に近い容量ながら4席横客室を維持します。"),
        "fuselage": t("約 41.5 公尺機身明顯長於 E190-E2，仍採四人並排、無中間座位配置。主翼前後的長窗列與修長比例是兩型最直接差異。", "The approximately 41.5-metre fuselage is visibly longer than the E190-E2 while retaining four-abreast seating without middle seats. Long window runs around the wing provide the clearest distinction.", "全長約41.5 mでE190-E2より明らかに長く、中央席のない4席横を維持します。主翼前後の長い窓列と細長い比率が最も直接的な違いです。"),
    },
    "atr72": {
        **ATR_COMMON,
        "overview": t("ATR 72-600 是 ATR 家族的加長高容量渦槳支線機，以高翼、雙 PW127XT-M、六葉螺旋槳與 T 尾為特徵。與 ATR 42 相比，機身及翼展更長。", "The ATR 72-600 is the stretched, higher-capacity ATR turboprop, identified by its high wing, two PW127XT-M engines, six-blade propellers and T-tail. It is longer and wider-spanned than the ATR 42.", "ATR 72-600はATR系の長胴・大容量ターボプロップで、高翼、2基のPW127XT-M、6枚プロペラ、T尾翼が特徴です。ATR 42より胴体と翼幅が長い型です。"),
        "fuselage": t("約 27.2 公尺的加長機身通常容納 68 至 78 名乘客，截面維持每排四座。前後艙門位置與長窗列可協助區分較短的 ATR 42。", "The approximately 27.2-metre stretched fuselage normally carries 68 to 78 passengers in a four-abreast cabin. Door positions and the longer window run help distinguish it from the shorter ATR 42.", "全長約27.2 mの長胴は通常68～78名を4席横で収容します。扉位置と長い窓列が短いATR 42との識別に役立ちます。"),
        "engine": t("兩具 Pratt & Whitney Canada PW127XT-M 驅動六葉低噪音螺旋槳。渦槳在較短航段以較低速度換取良好燃油效率與短場性能。", "Two Pratt & Whitney Canada PW127XT-M engines drive six-blade low-noise propellers. Turboprop propulsion trades speed for fuel efficiency and short-field performance on shorter sectors.", "2基のPratt & Whitney Canada PW127XT-Mが6枚低騒音プロペラを駆動します。ターボプロップは短距離区間で速度と引き換えに燃費と短距離性能を得ます。"),
        "wing": t("約 27.1 公尺的高翼跨越機身上方，讓螺旋槳與發動機保持良好離地高度；大型襟翼支援支線機場低速操作。翼展大於 ATR 42。", "The roughly 27.1-metre high wing crosses above the fuselage, keeping engines and propellers clear of the ground. Large flaps support low-speed regional-airport work, and span exceeds the ATR 42's.", "約27.1 mの高翼は胴体上を通り、エンジンとプロペラの地上高を確保します。大型フラップが地方空港の低速運用を支え、翼幅はATR 42より長くなります。"),
    },
    "atr72f": {
        **ATR_COMMON,
        "overview": t("ATR 72-600F 是原廠新造的專用貨機，不是封窗客機改裝型。它保留 ATR 72 高翼與 T 尾，同時加入大型主甲板貨門及貨運專用地板。", "The ATR 72-600F is a factory-built dedicated freighter, not a window-plugged passenger conversion. It retains the ATR 72 high wing and T-tail while adding a large main-deck cargo door and freight floor.", "ATR 72-600Fは客席窓を塞いだ改造機ではなく、新造専用貨物型です。ATR 72の高翼とT尾翼を保ち、大型主甲板貨物扉と貨物床を追加します。"),
        "fuselage": t("機身側面沒有連續客艙窗，左前方的大型貨門可裝載貨盤與 ULD；另設機組門。矩形貨門和封閉側壁是與 ATR 72-600 客機最清楚差異。", "The fuselage lacks a continuous passenger-window row and has a large forward-left door for pallets and ULDs plus a separate crew door. The rectangular cargo door and blank sidewalls clearly separate it from the passenger ATR 72-600.", "胴体に連続客室窓列はなく、左前方にパレット・ULD用大型扉と別の乗員扉があります。矩形貨物扉と無窓側壁が旅客ATR 72-600との明確な違いです。"),
        "engine": t("兩具 PW127M 渦槳驅動六葉螺旋槳，安裝在高翼前緣。動力與低速效率適合高頻短程貨運及較短跑道。", "Two PW127M turboprops drive six-blade propellers from nacelles on the high wing. Their low-speed efficiency suits frequent short cargo sectors and shorter runways.", "高翼前縁の2基のPW127Mが6枚プロペラを駆動します。低速効率は高頻度短距離貨物便と短い滑走路に適します。"),
        "wing": t("與客運 ATR 72-600 共用約 27.1 公尺高翼和高升力裝置，螺旋槳具有充足離地高度。貨機任務不改變基本翼面輪廓。", "It shares the passenger ATR 72-600's roughly 27.1-metre high wing and high-lift devices, with ample propeller clearance. The freight mission does not alter the basic wing outline.", "旅客ATR 72-600と約27.1 mの高翼・高揚力装置を共有し、十分なプロペラ地上高を持ちます。貨物任務でも基本翼形は変わりません。"),
    },
    "dhc6-400": {
        **HIGH_WING_COCKPIT,
        "overview": t("DHC-6 Twin Otter Series 400 是 19 席級高翼雙發短場多用途機，可換裝輪式、浮筒或雪橇。固定起落架、翼支柱與方正機身是代表特徵。", "The DHC-6 Twin Otter Series 400 is a 19-seat high-wing twin-engine STOL utility aircraft available on wheels, floats or skis. Fixed gear, wing struts and a boxy fuselage define it.", "DHC-6 Twin Otter Series 400は19席級高翼双発STOL多用途機で、車輪、フロート、スキーに対応します。固定脚、翼支柱、箱形胴体が代表的特徴です。"),
        "fuselage": t("近矩形截面的非加壓機身便於載客、貨運、跳傘與醫療任務快速改裝，右側大型雙扇門提供寬敞裝卸口。Series 400 最多搭載 19 名乘客。", "The near-rectangular unpressurised fuselage converts readily among passenger, cargo, parachute and medical missions. A large double door on the right eases loading, and Series 400 seats up to 19 passengers.", "矩形に近い非与圧胴体は旅客、貨物、降下、医療任務へ容易に転換でき、右側大型二枚扉が積み降ろしを助けます。Series 400は最大19名です。"),
        "engine": t("兩具 PT6A-34 渦槳裝於高翼，採三葉可逆槳距螺旋槳。大直徑螺旋槳與低速推力是 Twin Otter 短距起降能力的重要來源。", "Two PT6A-34 turboprops on the high wing drive three-blade reversible-pitch propellers. Large propellers and strong low-speed thrust are central to Twin Otter STOL performance.", "高翼の2基のPT6A-34が3枚可逆ピッチプロペラを駆動します。大径プロペラと強い低速推力がTwin OtterのSTOL性能を支えます。"),
        "wingtip": t("翼尖簡潔圓鈍，沒有民航噴射機式翼尖小翼；Series 400 可見航行燈與燈罩。辨識重點應放在長直高翼和翼支柱。", "The tips are simple and rounded without airliner-style winglets; navigation-light fairings may be visible. Identification relies more on the long straight high wing and its struts.", "翼端は簡潔な丸形で旅客ジェット式ウイングレットはなく、航法灯カバーが見られます。長い直線高翼と支柱の方が主要識別点です。"),
        "wing": t("長直高翼以支柱連接下機身，提供低翼載與良好低速升力。全翼展約 19.8 公尺，搭配襟翼讓飛機能在偏遠短跑道操作。", "A long straight high wing is braced to the lower fuselage, providing low wing loading and strong low-speed lift. Its roughly 19.8-metre span and flaps support remote short-strip operation.", "長い直線高翼は下部胴体へ支柱で結ばれ、低翼面荷重と良好な低速揚力を生みます。約19.8 mの翼幅とフラップが遠隔短滑走路運用を支えます。"),
        "vstab": t("單片垂直尾翼與大型方向舵位於傳統尾段，面積充足以應對單發失效時的不對稱推力。外形不像 ATR／Q400 的 T 尾。", "A single vertical fin and large rudder sit in a conventional tail and provide authority against asymmetric thrust after an engine failure. The arrangement is not a T-tail like the ATR or Q400.", "単一垂直尾翼と大型方向舵を通常尾部に置き、片発停止時の非対称推力へ対応します。ATRやQ400のT尾翼とは異なります。"),
        "hstab": t("水平尾翼裝在後機身低處，並以小支柱加固。低置尾翼與高翼形成 Twin Otter 很容易辨認的傳統布局。", "The horizontal tail is mounted low on the aft fuselage and supported by small braces. Its low tailplane and high wing create the Twin Otter's recognisable conventional arrangement.", "水平尾翼は後部胴体低位置に付き、小支柱で補強されます。低い尾翼と高翼の組合せがTwin Otterらしい通常配置です。"),
        "gear": t("起落架不收納；陸基型使用固定前三點式輪架，也可更換大型浮筒、兩棲浮筒或雪橇。外露輪架簡化維修並適合粗糙場地。", "The gear does not retract. Landplanes use fixed tricycle wheels, while large floats, amphibious floats or skis can be fitted. Exposed gear simplifies maintenance and suits rough fields.", "脚は格納されず、陸上型は固定前輪式、ほかに大型フロート、水陸両用フロート、スキーを装着できます。露出脚は整備を簡略化し荒地に適します。"),
    },
    "c408": {
        **HIGH_WING_COCKPIT,
        "overview": t("Cessna 408 SkyCourier 是 19 席或三個 LD3 貨櫃級的高翼雙發通勤運輸機，從設計初期即兼顧客運與貨運。固定起落架、巨大貨門與無翼支柱高翼是外觀重點。", "The Cessna 408 SkyCourier is a high-wing twin commuter for 19 passengers or three LD3 containers, designed from the outset for passenger and freight work. Fixed gear, a huge cargo door and an unbraced high wing define it.", "Cessna 408 SkyCourierは19名またはLD3コンテナ3個を運ぶ高翼双発コミューターで、当初から旅客・貨物双方を想定しています。固定脚、大型貨物扉、支柱なし高翼が特徴です。"),
        "fuselage": t("方正非加壓機身提供平整貨艙截面，貨運型左側大型門可直接裝卸 LD3；客運型可設 19 席與大型側門。高機頂與垂直側壁強調實用性。", "The boxy unpressurised fuselage provides a regular cargo section. A large left door accepts LD3 containers on freighters, while passenger layouts carry 19 seats with a large side door. Tall, vertical sidewalls emphasise utility.", "箱形非与圧胴体は規則的な貨物断面を持ち、貨物型左側大型扉からLD3を直接搭載できます。旅客型は19席と大型側扉を備え、高い機体と垂直側壁が実用性を示します。"),
        "engine": t("兩具 PT6A-65SC 驅動四葉 McCauley 螺旋槳，短艙位於高翼前緣。反推與低速推力協助縮短落地滑跑並提升貨運機場適應性。", "Two PT6A-65SC engines drive four-blade McCauley propellers from nacelles on the high wing. Reverse thrust and low-speed pull shorten landing roll and support cargo-airfield operations.", "高翼ナセルの2基のPT6A-65SCが4枚McCauleyプロペラを駆動します。逆推力と低速推力が着陸滑走を短縮し貨物空港への適応性を高めます。"),
        "wingtip": t("懸臂高翼末端略為上翹且無獨立翼尖小翼，燈具整合於翼尖。與 Twin Otter 相比，SkyCourier 沒有外部翼支柱。", "The cantilever high wing ends in a mildly swept/upturned tip without a separate winglet, with lights integrated at the end. Unlike the Twin Otter, the SkyCourier has no external wing struts.", "片持ち高翼は独立ウイングレットなしの緩い後退・上反翼端で灯火を統合します。Twin Otterと異なり外部翼支柱がありません。"),
        "wing": t("約 22 公尺的懸臂高翼讓發動機與螺旋槳遠離地面，並提供大型襟翼以支援短場操作。無支柱設計使貨門與機身側面保持暢通。", "The roughly 22-metre cantilever high wing keeps engines and propellers clear of the ground and uses large flaps for short-field performance. Its strutless design leaves the cargo door and fuselage sides unobstructed.", "約22 mの片持ち高翼はエンジンとプロペラの地上高を確保し、大型フラップで短距離性能を得ます。支柱がなく貨物扉と胴体側面を妨げません。"),
        "vstab": t("高大的單垂尾與方向舵控制雙發不對稱推力，前緣以圓滑背鰭連接機身。尾翼位於水平尾翼中央上方，但並非 T 尾。", "A tall single fin and rudder control asymmetric twin-engine thrust, with a smooth dorsal transition into the fuselage. The fin rises above the centrally mounted tailplane but does not form a T-tail.", "高い単一垂直尾翼と方向舵が双発の非対称推力を制御し、前縁は滑らかなドーサル部で胴体へつながります。水平尾翼上に伸びますがT尾翼ではありません。"),
        "hstab": t("水平尾翼裝在後機身中段，位置高於 Twin Otter 的低置尾翼但低於 T 尾頂端。傳統升降舵提供俯仰控制。", "The horizontal tail mounts midway up the aft fuselage, higher than the Twin Otter's low tailplane but below a T-tail position. Conventional elevators provide pitch control.", "水平尾翼は後部胴体中段に付き、Twin Otterの低位置尾翼より高くT尾翼頂部より低い位置です。通常の昇降舵でピッチを制御します。"),
        "gear": t("固定前三點式起落架採低壓輪胎與堅固支柱，不設收納艙門。這降低重量與維護複雜度，適合高頻貨運和條件較差跑道。", "Fixed tricycle landing gear uses robust struts and tyres without retraction doors. This reduces weight and maintenance complexity for frequent freight work and less-prepared runways.", "固定前輪式降着装置は頑丈な支柱とタイヤを使い格納扉を持ちません。重量と整備複雑性を抑え、高頻度貨物運航と条件の悪い滑走路に適します。"),
    },
    "l410ng": {
        **HIGH_WING_COCKPIT,
        "overview": t("L 410 NG 是 L 410 家族的現代化 19 席高翼雙發通勤機，換裝 H85-200、五葉螺旋槳、新翼與玻璃座艙。短場、非鋪裝跑道能力仍是設計核心。", "The L 410 NG is the modernised 19-seat high-wing twin commuter, adding H85-200 engines, five-blade propellers, a new wing and glass cockpit while retaining short and unpaved-strip capability.", "L 410 NGはL 410系を近代化した19席高翼双発コミューターで、H85-200、5枚プロペラ、新主翼、グラスコックピットを採用し短距離・未舗装滑走路能力を維持します。"),
        "fuselage": t("非加壓機身容納最多 19 名乘客，可快速改為貨運、救護或特殊任務；後段大型側門便於裝卸。NG 延長機鼻行李艙並更新內裝與系統。", "The unpressurised fuselage carries up to 19 passengers and converts to freight, medical or special missions through a large aft side door. The NG adds an extended nose baggage compartment and updated systems.", "非与圧胴体は最大19名を収容し、後部大型側扉から貨物、医療、特殊任務へ転換できます。NGは延長機首手荷物室と更新された内装・システムを備えます。"),
        "engine": t("兩具 GE Aerospace H85-200 渦槳驅動五葉 AV 725 螺旋槳，具電子控制與反推能力。五葉槳和較流線短艙是 NG 相較舊型 L 410 的辨識點。", "Two GE Aerospace H85-200 turboprops drive five-blade AV 725 propellers with electronic control and reverse. Five blades and streamlined nacelles distinguish the NG from older L 410 variants.", "2基のGE Aerospace H85-200が電子制御・逆推力付き5枚AV 725プロペラを駆動します。5枚プロペラと流線形ナセルが旧L 410との識別点です。"),
        "wingtip": t("新設計高翼採乾淨圓順翼尖，燃油整合於翼內，不再依賴舊型常見的大型翼尖油箱。翼尖燈具形成小型整流外殼。", "The redesigned high wing has clean rounded tips and carries fuel internally rather than relying on the prominent tip tanks seen on many older L 410s. Tip lights form small fairings.", "再設計高翼は滑らかな丸形翼端と翼内燃料を採用し、旧L 410で目立つ大型翼端タンクに依存しません。翼端灯が小型フェアリングを形成します。"),
        "wing": t("約 20 公尺的新高翼增加燃油容量並改善巡航效率，同時保留大型高升力裝置和良好螺旋槳離地間隙。機翼無 Twin Otter 式外部支柱。", "The roughly 20-metre new high wing increases fuel capacity and cruise efficiency while retaining strong high-lift devices and propeller clearance. It lacks Twin Otter-style external bracing.", "約20 mの新高翼は燃料容量と巡航効率を高め、大型高揚力装置とプロペラ地上高を維持します。Twin Otter式外部支柱はありません。"),
        "vstab": t("單垂尾與大方向舵提供短場低速及單發狀況所需方向控制，前緣以背鰭連接機身。尾翼是傳統配置而非 T 尾。", "A single fin and large rudder provide directional authority at short-field speeds and after an engine failure, with a dorsal transition into the fuselage. The tail is conventional rather than T-shaped.", "単一垂直尾翼と大型方向舵が短距離低速時と片発時の方向制御を担い、ドーサル部で胴体へつながります。T尾翼ではなく通常配置です。"),
        "hstab": t("水平尾翼安裝於後機身中低位置，配合傳統升降舵控制俯仰。相較 ATR 72 的 T 尾，L 410 NG 尾翼位置明顯較低。", "The horizontal tail mounts low-to-mid on the aft fuselage with conventional elevators. It sits visibly lower than the ATR 72's T-tail and is a useful silhouette cue.", "水平尾翼は後部胴体の中低位置に付き通常昇降舵を備えます。ATR 72のT尾翼より明らかに低く、シルエット識別に有効です。"),
        "gear": t("可收放前三點式起落架適合未鋪裝跑道，主輪向發動機短艙／翼根區收納。相較固定腳 Twin Otter 與 SkyCourier，這是重要辨識差異。", "Retractable tricycle gear is designed for unpaved strips, with the main wheels stowing around the nacelle/wing-root area. Retraction distinguishes it from fixed-gear Twin Otter and SkyCourier aircraft.", "格納式前輪脚は未舗装滑走路向けで、主輪をナセル・翼根付近へ収めます。固定脚のTwin OtterやSkyCourierとの重要な違いです。"),
    },
}


SPECS = {
    "b779": {"fuselage": [["全長", "76.72 m"]], "engine": [["型號", "GE9X"]], "wing": [["翼展", "71.8 m（展開）"]], "gear": [["主起落架", "每側 6 輪"]]},
    "b78x": {"fuselage": [["全長", "68.28 m"], ["典型載客量", "約 336"]]},
    "b763f": {"fuselage": [["全長", "54.94 m"], ["最大酬載", "約 52.5 t"]], "engine": [["型號", "CF6-80C2"]]},
    "b77f": {"fuselage": [["全長", "63.73 m"], ["最大酬載", "約 102 t"]], "engine": [["型號", "GE90-110B1L"]], "wing": [["翼展", "64.8 m"]]},
    "e175": {"fuselage": [["全長", "31.68 m"], ["典型載客量", "76–88"]]},
    "e190e2": {"fuselage": [["全長", "36.24 m"]], "engine": [["型號", "PW1900G"]], "wing": [["翼展", "33.72 m"]]},
    "e195e2": {"fuselage": [["全長", "41.50 m"]], "engine": [["型號", "PW1900G"]], "wing": [["翼展", "35.12 m"]]},
    "atr72": {"fuselage": [["全長", "27.17 m"], ["典型載客量", "68–78"]], "engine": [["型號", "PW127XT-M"]], "wing": [["翼展", "27.05 m"]]},
    "atr72f": {"fuselage": [["全長", "27.17 m"], ["最大酬載", "約 9.2 t"]], "engine": [["型號", "PW127M"]], "wing": [["翼展", "27.05 m"]]},
    "dhc6-400": {"fuselage": [["最大載客量", "19"]], "engine": [["型號", "PT6A-34"]], "wing": [["翼展", "19.81 m"]], "gear": [["配置", "固定輪式／浮筒／雪橇"]]},
    "c408": {"fuselage": [["容量", "19 人／3 個 LD3"]], "engine": [["型號", "PT6A-65SC"]], "wing": [["翼展", "22.02 m"]], "gear": [["配置", "固定前三點式"]]},
    "l410ng": {"fuselage": [["最大載客量", "19"]], "engine": [["型號", "H85-200"]], "wing": [["翼展", "20.0 m"]], "gear": [["配置", "可收放前三點式"]]},
}


def main():
    for ident, base_id in BASES.items():
        path = ROOT / "data" / f"{ident}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        base = json.loads((ROOT / "data" / f"{base_id}.json").read_text(encoding="utf-8"))
        existing = {part_id: deepcopy(part) for part_id, part in data.get("parts", {}).items()}
        data["partOrder"] = ORDER
        data["parts"] = deepcopy(base["parts"])
        if ident in RENAME_BASE:
            data["parts"] = renamed(data["parts"], *RENAME_BASE[ident])
        for part_id, part in data["parts"].items():
            part["summary"] = without_media_refs(part["summary"])
            old = existing.get(part_id, {})
            part["images"] = old.get("images", [])
            part["specs"] = []
            part["fact"] = {"zh": "", "en": "", "ja": ""}
            part["bullets"] = []
            if old.get("fact") and any(old["fact"].values()):
                part["fact"] = old["fact"]
            for field in ("bullets", "specs"):
                if old.get(field):
                    part[field] = old[field]
        for part_id, summary in OVERRIDES[ident].items():
            part = data["parts"][part_id]
            part["summary"] = summary
            part["specs"] = SPECS.get(ident, {}).get(part_id, [])
            old = existing.get(part_id, {})
            if not old.get("fact") or not any(old["fact"].values()):
                part["fact"] = {"zh": "", "en": "", "ja": ""}
            if not old.get("bullets"):
                part["bullets"] = []
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for ident in BASES:
        data = json.loads((ROOT / "data" / f"{ident}.json").read_text(encoding="utf-8"))
        assert data["partOrder"] == ORDER and set(data["parts"]) == set(ORDER)
        assert all(isinstance(p["summary"], dict) and all(p["summary"].get(lang) for lang in ("zh", "en", "ja")) for p in data["parts"].values())
        assert all(isinstance(p["images"], list) for p in data["parts"].values())
    print(f"Enriched {len(BASES)} aircraft with {len(ORDER)} parts each")


if __name__ == "__main__":
    main()
