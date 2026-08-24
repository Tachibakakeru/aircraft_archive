"""Seed real-photo identification references for the default 737-800/A320 comparison."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORDER = ["overview", "cockpit", "windshield", "fuselage", "engine", "wingtip", "wing", "vstab", "hstab", "gear"]


def tr(zh: str, en: str, ja: str) -> dict[str, str]:
    return {"zh": zh, "en": en, "ja": ja}


def photo(model: str, part: str, caption: dict[str, str], source: str) -> dict:
    return photo_named(model, f"{part}.jpg", caption, source)


def photo_named(model: str, filename: str, caption: dict[str, str], source: str) -> dict:
    return {
        "src": f"assets/reference/{model}/{filename}",
        "caption": caption,
        "source": source,
    }


SOURCES = {
    "b738": {
        "overview": "https://commons.wikimedia.org/wiki/File:Boeing_737-800_(TC-SNR)_01.jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:The_Flight_Deck_of_the_Boeing_737-800._(2956276002).jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:Front_view_of_boeing_737-800_of_Ryanair_at_Orio_al_Serio_International_Airport,_2006.jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:Cockpit_window_of_Qantas_Boeing_737_(VH-VYE)_taxiing_prior_to_takeoff_at_SYD.jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:Forward_fuselage_of_Virgin_Australia_(VH-YFC)_Boeing_737-81D_at_Sydney_Airport.jpg",
        "engine": "https://commons.wikimedia.org/wiki/File:CFM-56_Lauda_737.jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:Winglet_of_Boeing_737-800.jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:Boeing_737-800_American_Airlines,_clean_and_shiny_wing_%2B_winglet_(4898075792).jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:LN-RCY_Boeing_737-800_Tail_Scheme_(7510635508).jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:Boeing_737-800_Tail_from_Below.jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:737-800_main_gear_bay_(3858029769).jpg",
    },
    "a320": {
        "overview": "https://commons.wikimedia.org/wiki/File:Jetstar_Airbus_A320_VH-XNJ_Perth_2023_(01).jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:Airbus_A320-214_Vueling_EC-HHA_cockpit_(5508849819).jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:Finnair_Airbus_A320_OH-LXB_Budapest_2006_(03).jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:Airbus_A320-200_Airbus_Industries_(AIB)_%22House_colors%22_F-WWBA_-_MSN_001_(10276181983).jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:Aft_door_of_A320.jpg",
        "engine": "https://commons.wikimedia.org/wiki/File:Philippine_Airlines_A320_Engine.jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:F-WWIQ_Airbus_A320_sharklet_ILA_2012_07.jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:The_Sharklet_on_our_newest_Airbus_A320_(8657081970).jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:Vertical_stabilizer_of_A-320.jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:Airbus-H%C3%B6henruder.jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:A320neo_Nose_Landing_Gear.jpg",
    },
}


CONTENT = {
    "b738": {
        "overview": {
            "name": tr("整體外型", "Overall profile", "全体外観"),
            "en": "OVERALL PROFILE",
            "summary": tr(
                "737-800 的機身較窄、離地較低，機鼻略尖，駕駛艙窗框線條較有稜角；CFM56-7B 短艙底部扁平，主起落架收起後仍可看見輪胎胎面。",
                "The 737-800 sits low on a relatively narrow fuselage, with a pointed nose, angular cockpit glazing, flattened CFM56-7B nacelles and exposed main-wheel faces when retracted.",
                "737-800は細めの胴体と低い姿勢、やや尖った機首、角張った操縦席窓、下面が平たいCFM56-7Bナセル、格納後も見える主輪が特徴です。",
            ),
            "fact": tr("辨識時至少同時核對機鼻、引擎短艙與起落架；小翼可能因航空公司改裝而不同。", "Identify it from the nose, nacelles and landing gear together; winglets vary by operator and retrofit.", "機首・ナセル・脚を組み合わせて判別してください。ウイングレットは運航会社や改修で異なります。"),
            "bullets": [
                tr("機腹離地低，主輪收入機腹後胎面外露。", "Low ground clearance; main-wheel faces remain exposed when retracted.", "地上高が低く、格納後も主輪のタイヤ面が露出します。"),
                tr("機鼻與駕駛艙窗較尖、窗框折線較明顯。", "Pointed nose and relatively angular cockpit-window geometry.", "機首が尖り気味で、操縦席窓の輪郭が角張っています。"),
                tr("737NG 常見融合式或 Split Scimitar 小翼，但也可能沒有。", "737NG aircraft may have blended or Split Scimitar winglets, or none.", "737NGにはブレンデッド／スプリット・シミター型、または未装備があります。"),
            ],
        },
        "cockpit": {
            "bullets": [
                tr("正副駕駛前方都有傳統駕駛盤與中央操縱柱。", "Conventional yokes and control columns sit in front of both pilots.", "両席の正面に操縦輪とコントロールコラムがあります。"),
                tr("737NG 典型配置為六具大型顯示器，中央仍保留大量實體旋鈕。", "The 737NG normally has six large displays while retaining many physical controls.", "737NGは通常6面の大型表示器と多数の物理操作部を備えます。"),
                tr("中央座艙可見會隨配平轉動的黑白配平輪。", "Black-and-white manual trim wheels remain prominent on the centre pedestal.", "中央ペデスタルには白黒模様の手動トリムホイールがあります。"),
            ],
        },
        "windshield": {
            "name": tr("駕駛艙外窗", "Cockpit windows", "コックピット窓"),
            "en": "COCKPIT WINDOWS",
            "summary": tr("737-800 的外窗輪廓較有稜角：兩片正面風擋接近直立梯形，外側窗框以明顯折角包向機身側面。正面看時窗帶較窄、中央分隔線較直，側面則可見近似多邊形的側窗。", "The 737-800 glazing is angular: two upright trapezoidal front panes meet a window belt that turns sharply around the nose into polygonal side panes.", "737-800の窓は角張っており、直立気味の台形前面窓から明確な折れ角で多角形の側面窓へつながります。"),
            "fact": tr("客機風擋是加熱、夾層且能承受座艙壓差的結構件；辨識時應看整組窗帶比例，不要只數單一片窗。", "Airliner windshields are heated laminated structural panes. Identify the proportion and outline of the complete window belt rather than counting one pane.", "旅客機の風防は加熱式の積層構造材です。1枚だけでなく窓帯全体の比率と輪郭で判別します。"),
            "bullets": [tr("正面兩片主風擋較扁、中央接縫近乎垂直。", "The two main forward panes look relatively shallow with a near-vertical centre seam.", "正面2枚の主風防は比較的浅く、中央継ぎ目はほぼ垂直です。"), tr("外側窗向機身側面急轉，窗框折角較銳利。", "Outer panes turn sharply onto the fuselage sides with pronounced corners.", "外側窓は胴体側面へ急に回り込み、輪郭の角が明瞭です。"), tr("搭配較尖機鼻與扁平 CFM56-7B 短艙可提高判斷可靠度。", "Cross-check the angular glazing with the pointed nose and flattened CFM56-7B nacelles.", "尖った機首と下面が平たいCFM56-7Bナセルも合わせて確認します。")],
        },
        "fuselage": {
            "bullets": [
                tr("機身外徑約 3.76 m，比 A320 的 3.95 m 窄。", "The 3.76 m fuselage is narrower than the A320's 3.95 m body.", "胴体外径は約3.76 mで、A320の3.95 mより細身です。"),
                tr("典型 737-800 每側有前後主艙門與兩個機翼上方逃生窗。", "A typical 737-800 has forward/aft main doors and two overwing exits per side.", "標準的な737-800は各側に前後ドアと主翼上2か所の非常口があります。"),
                tr("駕駛艙側窗下緣與機鼻輪廓較有折角。", "The cockpit side-window sill and nose contour are comparatively angular.", "操縦席側窓の下端と機首輪郭は比較的角張っています。"),
            ],
        },
        "engine": {
            "bullets": [
                tr("CFM56-7B 進氣口底部明顯扁平，不是完整圓形。", "The CFM56-7B inlet has a visibly flattened lower lip rather than a full circle.", "CFM56-7Bの吸気口下面は明確に平たく、真円ではありません。"),
                tr("附件齒輪箱移到側面，讓短艙能塞進低矮的機翼下方。", "Accessories were moved to the sides so the nacelle fits beneath the low wing.", "低い主翼下に収めるため補機類が側面へ移されています。"),
                tr("737-800 固定使用 CFM56-7B，可把扁平短艙視為強辨識點。", "The 737-800 uses the CFM56-7B; its flattened nacelle is a strong identifier.", "737-800はCFM56-7Bを使用し、平たいナセルが強い識別点です。"),
            ],
        },
        "wingtip": {
            "name": tr("翼尖小翼", "Wingtip device", "翼端装置"),
            "en": "WINGTIP DEVICE",
            "summary": tr("737-800 可見高而向外彎曲的融合式小翼，也可能後續改裝 Split Scimitar 上下分叉小翼；早期或特定營運者也可能沒有小翼。", "A 737-800 may carry tall blended winglets, retrofitted Split Scimitar devices, or no winglet at all.", "737-800には背の高いブレンデッド・ウイングレット、上下に分かれるスプリット・シミター型、または未装備があります。"),
            "fact": tr("翼尖能縮小翼尖渦與誘導阻力，但構型並非唯一機型證據，必須搭配機鼻與引擎判讀。", "Wingtip devices reduce induced drag, but configuration alone is not proof of type; cross-check the nose and engines.", "翼端装置は誘導抗力を減らしますが、それだけで機種は確定できません。機首とエンジンも確認します。"),
            "bullets": [
                tr("融合式小翼由翼端平滑上彎，外形修長。", "Blended winglets curve smoothly upward from the tip.", "ブレンデッド型は翼端から滑らかに上方へ伸びます。"),
                tr("Split Scimitar 構型在翼尖下方另有短小向下翼片。", "Split Scimitar versions add a smaller downward-pointing blade.", "スプリット・シミター型には下向きの小翼片もあります。"),
                tr("不要把小翼當成單一判斷依據。", "Do not use the winglet as the sole identification cue.", "翼端装置だけを識別根拠にしないでください。"),
            ],
        },
        "wing": {"bullets": [tr("後掠約 25°，NG 機翼通常搭配高舉小翼。", "The NG wing is swept about 25 degrees and often carries a tall winglet.", "後退角は約25度で、多くは背の高いウイングレットを備えます。"), tr("翼面比 A320 略大，但僅靠翼形不容易遠距分辨。", "Wing area is slightly larger than the A320's, though planform alone is subtle at distance.", "翼面積はA320よりわずかに大きいものの、遠方では翼形だけの判別は困難です。"), tr("從客艙向外看可搭配扁平引擎短艙確認為 737NG。", "From the cabin, pair the wing view with the flattened nacelle to confirm a 737NG.", "客室からは平たいナセルと合わせて737NGを確認できます。")]},
        "vstab": {"bullets": [tr("尾翼前緣下方有明顯背鰭，平順連到機背。", "A prominent dorsal fin blends the fin's leading edge into the upper fuselage.", "垂直尾翼前縁下には胴体へ連なる大きなドーサルフィンがあります。"), tr("方向舵後緣較筆直，垂尾頂端略向後收尖。", "The rudder trailing edge is straight and the fin tip tapers aft.", "方向舵後縁は直線的で、尾翼上端は後方へ細くなります。"), tr("尾翼塗裝可辨航空公司，不足以單獨判斷機型。", "Tail paint identifies the operator, not necessarily the aircraft type.", "尾翼塗装は運航会社の手掛かりであり、機種の確定材料ではありません。")]},
        "hstab": {"bullets": [tr("水平尾翼低置於機尾兩側，外形後掠。", "Low-mounted swept horizontal stabilizers extend from either side of the tail.", "後退した水平尾翼は胴体尾部の低い位置に付きます。"), tr("由下方可同時觀察外露主輪與尾翼配置。", "A view from below can reveal both the exposed main wheels and tail arrangement.", "下方からは露出主輪と尾翼配置を同時に確認できます。"), tr("水平尾翼不是 737 與 A320 最強的單一辨識點。", "The horizontal tail is not a strong standalone discriminator between 737 and A320.", "水平尾翼だけでは737とA320の判別力は高くありません。")]},
        "gear": {"bullets": [tr("主起落架收起後沒有完整外側艙門，輪胎胎面可從機腹看見。", "The retracted main gear lacks full outer doors, leaving tyre faces visible from below.", "主脚格納時も完全な外扉がなく、機腹からタイヤ面が見えます。"), tr("機身離地較低，前起落架看起來短。", "Low fuselage clearance gives the nose gear a short appearance.", "胴体の地上高が低く、前脚は短く見えます。"), tr("外露主輪是區分 737 與 A320 最可靠的地面特徵之一。", "Exposed main-wheel faces are among the most reliable ground-level 737/A320 cues.", "露出した主輪は737とA320を見分ける有力な地上識別点です。")]},
    },
    "a320": {
        "overview": {
            "name": tr("整體外型", "Overall profile", "全体外観"),
            "en": "OVERALL PROFILE",
            "summary": tr("A320 的機身較寬、離地較高，機鼻輪廓更圓鈍；引擎短艙通常接近圓形，主輪收入有艙門遮蔽。翼尖可能是上下箭形擋板或高大的 Sharklet。", "The A320 has a wider, higher-set fuselage and a rounder nose. Its nacelles are generally circular, retracted gear is covered, and the tips may carry fences or tall Sharklets.", "A320は幅広で地上高が高く、機首は丸みがあります。ナセルは概ね円形で、格納脚は扉に覆われ、翼端はフェンス型またはシャークレット型です。"),
            "fact": tr("先看圓形引擎與較高姿態，再用機鼻、翼尖和起落架艙門交叉確認；A320ceo 與 neo 的引擎大小也不同。", "Start with the round nacelles and taller stance, then cross-check nose, tips and gear doors; A320ceo and neo engine sizes also differ.", "円形ナセルと高い姿勢を起点に、機首・翼端・脚扉を照合します。ceoとneoでもエンジン寸法は異なります。"),
            "bullets": [tr("機身截面較寬，整體姿態比 737 高。", "Wider fuselage and a visibly taller stance than the 737.", "737より胴体が太く、全体の姿勢も高めです。"), tr("機鼻較圓，駕駛艙窗下緣線條較平順。", "Rounder nose with smoother cockpit-window lower contours.", "機首が丸く、操縦席窓下端の輪郭が滑らかです。"), tr("引擎短艙接近圓形，收起的主輪不會像 737 明顯外露。", "Nacelles are close to circular and the retracted main wheels are not exposed like a 737's.", "ナセルは円形に近く、格納主輪は737のように露出しません。")],
        },
        "cockpit": {"bullets": [tr("使用左右側桿，飛行員正前方沒有傳統駕駛盤。", "Sidesticks replace yokes, leaving the area directly in front of each pilot clear.", "操縦輪ではなく左右のサイドスティックを使用します。"), tr("正副駕駛前方可拉出桌板，是 A320 家族顯著座艙特徵。", "Pull-out tray tables sit in front of both pilots, a signature A320-family feature.", "両席正面に引き出し式テーブルがあるのがA320ファミリーの特徴です。"), tr("中央 ECAM 顯示器整合引擎與系統警告資訊。", "Central ECAM displays integrate engine and system warnings.", "中央のECAM表示器がエンジンとシステム警報を統合します。")]},
        "windshield": {
            "name": tr("駕駛艙外窗", "Cockpit windows", "コックピット窓"),
            "en": "COCKPIT WINDOWS",
            "summary": tr("A320 的外窗沿著較圓鈍的機鼻形成較寬、較連續的弧形窗帶。正面主風擋較高大，外側窗向後收尖但上下邊線轉折較平順，從斜側面看整組窗框更像連續包覆機鼻。", "The A320's taller front panes form a broad, continuous window belt around its rounder nose. The outer panes taper aft with smoother upper and lower contours.", "A320は丸い機首を囲む幅広く連続的な窓帯が特徴です。正面窓は高く、外側窓は上下の輪郭を滑らかに保ちながら後方へ細くなります。"),
            "fact": tr("737 與 A320 都不是只靠『窗戶片數』就能分辨；最有用的是正面窗高寬比、外側窗收尖方向，以及窗帶與機鼻曲面的銜接方式。", "Pane count alone does not separate a 737 from an A320. Compare front-pane proportions, outer-pane taper and how the belt follows the nose curvature.", "737とA320は窓の枚数だけでは区別できません。正面窓の縦横比、外側窓の絞り方、機首曲面とのつながりを比較します。"),
            "bullets": [tr("正面主風擋較高，整組窗帶在圓鼻上顯得更寬。", "Main forward panes appear taller and the complete belt looks broader on the rounded nose.", "正面主風防は高く、丸い機首上で窓帯全体が幅広く見えます。"), tr("外側窗向後收尖，窗框上下輪廓比 737 平順。", "Outer panes taper aft with smoother top and bottom contours than on the 737.", "外側窓は後方へ細くなり、上下輪郭は737より滑らかです。"), tr("搭配圓形短艙、較高離地姿態與翼尖構型交叉確認。", "Cross-check with circular nacelles, taller ground stance and the wingtip device.", "円形ナセル、高い地上姿勢、翼端装置も合わせて確認します。")],
        },
        "fuselage": {"bullets": [tr("機身外徑約 3.95 m，比 737 寬約 19 cm。", "The 3.95 m fuselage is about 19 cm wider than the 737's.", "胴体外径は約3.95 mで、737より約19 cm太いです。"), tr("典型 A320 每側有前後主艙門與兩個機翼上方逃生窗。", "A typical A320 has forward/aft main doors and two overwing exits per side.", "標準的なA320は各側に前後ドアと主翼上2か所の非常口があります。"), tr("艙門外形與圓鈍機鼻要搭配引擎、翼尖一起辨識。", "Use door layout and the rounded nose together with engines and wingtips.", "ドア配置と丸い機首を、エンジン・翼端と合わせて判別します。")]},
        "engine": {"bullets": [tr("A320ceo 的 CFM56-5B 或 V2500 短艙底部維持接近圓形。", "A320ceo CFM56-5B or V2500 nacelles remain close to circular underneath.", "A320ceoのCFM56-5B／V2500ナセル下面は円形に近い形です。"), tr("較高的機翼與起落架提供比 737 更多的離地間隙。", "The higher wing and landing gear provide more ground clearance than on a 737.", "高い主翼と脚により737より大きな地上間隔があります。"), tr("neo 的 LEAP-1A／PW1100G 風扇更大，需先分清 ceo 與 neo。", "A320neo LEAP-1A/PW1100G fans are larger, so identify ceo versus neo first.", "neoのLEAP-1A／PW1100Gはさらに大径なので、まずceo／neoを区別します。")]},
        "wingtip": {
            "name": tr("翼尖小翼", "Wingtip device", "翼端装置"),
            "en": "WINGTIP DEVICE",
            "summary": tr("早期 A320 常見上下各一片的小型箭形翼尖擋板；較新的 A320ceo 與 A320neo 則可見高而向外彎的 Sharklet。", "Early A320s often use small upper-and-lower wingtip fences; later A320ceo and A320neo aircraft may carry tall outward-curved Sharklets.", "初期A320は上下に小さな翼端フェンスを備え、後期ceoやneoでは背の高いシャークレットが見られます。"),
            "fact": tr("上下箭形擋板是經典 A320 家族線索；Sharklet 外形與 737 融合式小翼相似，因此必須再看引擎與機鼻。", "Upper/lower fences are a classic A320-family clue. Sharklets resemble 737 blended winglets, so confirm with engines and nose.", "上下フェンスはA320の典型的手掛かりです。シャークレットは737の小翼に似るため、エンジンと機首も確認します。"),
            "bullets": [tr("翼尖擋板同時向上與向下伸出，尺寸較小。", "Classic fences project both above and below the wingtip.", "従来型フェンスは翼端の上下へ小さく伸びます。"), tr("Sharklet 高而後掠，外觀可能與 737 小翼混淆。", "The tall swept Sharklet can be confused with a 737 winglet.", "背の高い後退シャークレットは737の小翼と混同しやすい形です。"), tr("翼尖構型隨出廠年代與改裝狀態改變。", "Tip configuration varies with production date and retrofit status.", "翼端構成は製造時期や改修状況で変わります。")],
        },
        "wing": {"bullets": [tr("後掠約 25°，早期型翼尖可見上下箭形擋板。", "The wing is swept about 25 degrees; early versions show upper/lower tip fences.", "後退角は約25度で、初期型は上下の翼端フェンスが見えます。"), tr("新型 Sharklet 自翼端向上延伸，不能只靠它區分 737。", "Later Sharklets extend upward but cannot alone distinguish an A320 from a 737.", "後期型シャークレットだけでは737との判別はできません。"), tr("從客艙向外看可用圓形引擎短艙與翼尖構型交叉確認。", "From the cabin, cross-check the circular nacelle with the tip device.", "客室からは円形ナセルと翼端装置を組み合わせて確認します。")]},
        "vstab": {"bullets": [tr("複合材料垂直尾翼根部以背鰭平順連接機身。", "The composite fin blends into the fuselage through a dorsal fairing.", "複合材の垂直尾翼はドーサルフェアリングで胴体へ滑らかにつながります。"), tr("垂尾外形本身與其他窄體機相近，需搭配機鼻與引擎。", "Fin shape resembles other narrow-bodies, so pair it with nose and engine cues.", "尾翼形状は他のナローボディ機に似るため、機首とエンジンも確認します。"), tr("尾翼塗裝主要辨識航空公司，不代表機型。", "Tail livery primarily identifies the operator, not the type.", "尾翼塗装は主に運航会社を示し、機種を確定しません。")]},
        "hstab": {"bullets": [tr("水平尾翼低置於機尾，升降舵與安定面皆大量使用複合材料。", "The low-mounted tailplane and elevators make extensive use of composites.", "低位置の水平尾翼と昇降舵には複合材が多用されています。"), tr("翼根整流罩與後機身線條較圓順。", "The tailplane root fairing blends smoothly into the rounded aft fuselage.", "水平尾翼付け根は丸みのある後部胴体へ滑らかにつながります。"), tr("水平尾翼仍屬輔助辨識特徵，不能單獨定型。", "The tailplane is only a supporting cue, not a standalone identifier.", "水平尾翼は補助的な手掛かりで、単独では機種を確定できません。")]},
        "gear": {"bullets": [tr("主起落架收入翼根／機身輪艙後由艙門遮蔽，不留兩塊外露胎面。", "Main gear retracts into covered wing-root/fuselage bays without exposed tyre faces.", "主脚は翼根・胴体の覆われた格納庫へ入り、タイヤ面は露出しません。"), tr("A320 的機身離地與引擎離地間隙通常高於 737NG。", "Fuselage and engine ground clearance are normally greater than on a 737NG.", "胴体とエンジンの地上高は通常737NGより大きいです。"), tr("照片為 A320neo 前起落架，腳架基本布局可作家族參考，不能用於分辨 ceo／neo。", "The photo shows A320neo nose gear; the family layout is useful, but it does not distinguish ceo from neo.", "写真はA320neoの前脚です。ファミリー共通配置の参考にはなりますが、ceo／neo判別には使えません。")]} ,
    },
}


CAPTIONS = {
    "overview": tr("實機側面外型參考", "Real-aircraft side-profile reference", "実機側面外観の参考"),
    "cockpit": tr("實機駕駛艙布局", "Real cockpit layout", "実機コックピット配置"),
    "windshield": tr("實機駕駛艙外窗", "Real cockpit-window geometry", "実機コックピット窓形状"),
    "fuselage": tr("實機機身、舷窗與艙門細節", "Real fuselage, window and door detail", "実機の胴体・窓・ドア詳細"),
    "engine": tr("實機引擎短艙外形", "Real engine-nacelle profile", "実機エンジンナセル外形"),
    "wingtip": tr("實機翼尖裝置外形", "Real wingtip-device profile", "実機翼端装置の外形"),
    "wing": tr("實機主翼平面與外形", "Real wing planform and profile", "実機主翼の平面・外形"),
    "vstab": tr("實機垂直尾翼外形", "Real vertical-tail profile", "実機垂直尾翼の外形"),
    "hstab": tr("實機水平尾翼外形", "Real horizontal-tail profile", "実機水平尾翼の外形"),
    "gear": tr("實機起落架細節", "Real landing-gear detail", "実機着陸装置の詳細"),
}

NAMES = {
    "overview": tr("整體外型", "Overall profile", "全体外観"),
    "cockpit": tr("駕駛艙", "Cockpit", "コックピット"),
    "windshield": tr("駕駛艙外窗", "Cockpit windows", "コックピット窓"),
    "fuselage": tr("機身", "Fuselage", "胴体"),
    "engine": tr("引擎", "Engine", "エンジン"),
    "wingtip": tr("翼尖小翼", "Wingtip device", "翼端装置"),
    "wing": tr("主翼", "Wing", "主翼"),
    "vstab": tr("垂直尾翼", "Vertical stabilizer", "垂直尾翼"),
    "hstab": tr("水平尾翼", "Horizontal stabilizer", "水平尾翼"),
    "gear": tr("起落架", "Landing gear", "着陸装置"),
}


def update(model: str) -> None:
    path = ROOT / "data" / f"{model}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    parts = data.setdefault("parts", {})
    for part_id in ORDER:
        patch = CONTENT[model][part_id]
        part = parts.setdefault(part_id, {})
        part.update(patch)
        part["name"] = NAMES[part_id]
        part.setdefault("specs", [])
        if part_id == "windshield":
            part["images"] = [
                photo_named(model, "window-front.jpg", tr("正面窗型（由實機照片裁切）", "Front window geometry (crop of a real photograph)", "正面窓形状（実機写真から切り出し）"), SOURCES[model]["window_front"]),
                photo_named(model, "window-side.jpg", tr("側面窗型（由實機照片裁切）", "Side window geometry (crop of a real photograph)", "側面窓形状（実機写真から切り出し）"), SOURCES[model]["window_side"]),
            ]
        else:
            part["images"] = [photo(model, part_id, CAPTIONS[part_id], SOURCES[model][part_id])]
    data["partOrder"] = ORDER
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def check() -> None:
    for model in CONTENT:
        data = json.loads((ROOT / "data" / f"{model}.json").read_text(encoding="utf-8"))
        assert data["partOrder"] == ORDER and len(set(data["partOrder"])) == len(ORDER)
        for part_id in ORDER:
            part = data["parts"][part_id]
            assert len(part.get("bullets", [])) >= 3
            for image in part["images"]:
                assert (ROOT / image["src"]).is_file(), image["src"]
                assert image["source"].startswith("https://commons.wikimedia.org/wiki/File:")
                assert all(image["caption"].get(lang) for lang in ("zh", "en", "ja"))
        assert sum(len(data["parts"][part_id]["images"]) for part_id in ORDER) == 11
    print("Reference-photo data check passed: 2 aircraft x 10 identification parts / 22 photos.")


if __name__ == "__main__":
    for aircraft in CONTENT:
        update(aircraft)
    check()
