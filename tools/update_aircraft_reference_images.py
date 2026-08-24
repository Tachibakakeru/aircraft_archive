"""Seed real-photo identification references for supported comparison pairs."""

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
    "b773": {
        "overview": "https://commons.wikimedia.org/wiki/File:Boeing_777-300ER,_Geneva_Airport,_Le_Grand-Saconnex_(BL7C0540).jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:Boeing_777-200ER_cockpit.jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:Cockpit_windows_of_an_AA_B773.jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:Boeing_777_nose_from_starboard_side_(2719420855)_(2).jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:B-KPL_Boeing_777_Cathay_Pacific_In_OneWorld_Colours_Nose_(9320566483).jpg",
        "engine": "https://commons.wikimedia.org/wiki/File:Engine_of_Jet_Airways_Boeing_777-300ER.jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:Emirates_77W_wing_view,_July_2015.jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:Emirates_77W_wing_view,_July_2015.jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:View_of_EVA_Air_Boeing_777-300ER_tail.jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:Boeing_777%27s_Tail_(2573279746).jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:B777_Landinggear_(51127441259).jpg",
    },
    "a359": {
        "overview": "https://commons.wikimedia.org/wiki/File:Airbus_A350-941_F-WWCF_MSN002_ILA_Berlin_2016_17.jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:Airbus_A-350_XWB_F-WWYB_cockpit_view.jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:Airbus_A350-941_F-WWCF_MSN002_ILA_Berlin_2016_17.jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:Airbus_A350_cockpit_windows_(14274972354).jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:Airbus_A350-900_(40862885025).jpg",
        "engine": "https://commons.wikimedia.org/wiki/File:Airbus_A350-941_F-WWCF_MSN002_ILA_Berlin_2016_23.jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:Airbus_A-350_XWB_F-WWYB_winglet.jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:Airbus_A350-941_F-WWCF_MSN002_blended_winglet_ILA_Berlin_2016_05.jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:Airbus_A350-941_F-WWCF_MSN002_ILA_Berlin_2016_18.jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:Airbus_A350-941_F-WWCF_MSN002_ILA_Berlin_2016_20.jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:Airbus_A350-941_F-WWCF_MSN002_main_landing_gear_ILA_Berlin_2016_06.jpg",
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
    "b773": {
        "overview": {
            "summary": tr("777-300／300ER 是機身修長的大型雙發廣體客機。常見 777-300ER 可由每側五對大型艙門、六輪主起落架、巨大的 GE90-115B 與水平向外延伸的後掠翼尖辨認。", "The 777-300/300ER is a very long twin-engine wide-body. The common 777-300ER combines five main doors per side, six-wheel main bogies, huge GE90-115Bs and horizontally raked tips.", "777-300／300ERは非常に長い双発ワイドボディ機です。一般的な300ERは片側5枚の大型ドア、6輪主脚、巨大なGE90-115B、水平に伸びるレイクド翼端で識別できます。"),
            "fact": tr("本頁外觀照片以數量最多的 777-300ER 為主；基本型 777-300 的引擎與翼尖可能不同，不能把 GE90-115B 當成所有 777-300 的共同特徵。", "Exterior references emphasize the much more common 777-300ER. The baseline 777-300 may use other engines and lacks some ER-specific cues.", "外観写真は多数派の777-300ERを中心にしています。基本型777-300ではエンジンや翼端が異なる場合があります。"),
            "bullets": [tr("每側五對主艙門，機身明顯比 A350-900 長。", "Five main doors per side and a visibly longer fuselage than the A350-900.", "片側5枚の主ドアで、A350-900より明らかに長い胴体です。"), tr("777-300ER 的 GE90-115B 風扇直徑與機身寬度相比仍非常巨大。", "The 777-300ER's GE90-115B looks exceptionally large even beside its wide fuselage.", "777-300ERのGE90-115Bは太い胴体と比べても非常に大きく見えます。"), tr("六輪主腳與近乎水平的後掠翼尖是強辨識點。", "Six-wheel main bogies and nearly horizontal raked tips are strong cues.", "6輪主脚とほぼ水平のレイクド翼端が強い識別点です。")],
        },
        "cockpit": {
            "summary": tr("777 駕駛艙採傳統駕駛盤與中央操縱柱，六具大型顯示器橫向排列；中央 EICAS 顯示引擎與系統資訊，控制邏輯仍保留典型 Boeing 操作習慣。", "The 777 flight deck uses conventional yokes and control columns with six large displays. Central EICAS screens carry engine and system information in a recognizably Boeing layout.", "777の操縦席は操縦輪とコントロールコラムを備え、6面の大型表示器を横一列に配置します。中央EICASがエンジンとシステム情報を表示します。"),
            "fact": tr("照片為 777-200ER，但主要飛行顯示器、EICAS、駕駛盤與中央基座配置可作 777 家族識別參考。", "The photograph is a 777-200ER, but the displays, EICAS, yokes and centre pedestal are valid 777-family identification references.", "写真は777-200ERですが、表示器、EICAS、操縦輪、中央ペデスタルは777ファミリー共通の参考になります。"),
            "bullets": [tr("兩名飛行員前方都有駕駛盤，不使用 Airbus 式側桿。", "Both pilots have yokes; there are no Airbus-style sidesticks.", "両席に操縦輪があり、Airbus式サイドスティックではありません。"), tr("六面顯示器尺寸一致，中央兩面主要用於 EICAS。", "Six similarly sized displays span the panel, with the centre pair serving EICAS.", "同寸法の6画面が並び、中央2面は主にEICASです。"), tr("油門座與中央基座較高，兩側沒有 A350 的開放式桌板空間。", "The tall throttle pedestal leaves no A350-style open tray-table area in front of the pilots.", "高いスロットル台があり、A350のような正面テーブル空間はありません。")],
        },
        "windshield": {
            "summary": tr("777 的駕駛艙窗沒有 A350 的黑色面罩。兩片正面主風擋寬大而接近梯形，外側窗以明顯折角向後收窄，窗框與白色機鼻蒙皮清楚分離。", "The 777 has no A350-style black mask. Large trapezoidal front panes transition through angular outer panes, with each frame clearly separated from the painted nose skin.", "777にはA350の黒いマスクがありません。大きな台形前面窓から角張った外側窓へつながり、各窓枠が白い機首外板から明確に分かれます。"),
            "fact": tr("777 與 A350 都有多片結構風擋；辨識重點不是窗片數，而是 A350 的黑色連續面罩與 777 分離、角張的窗框。", "Both aircraft use multiple structural panes. The useful cue is the A350's continuous black mask versus the 777's separate angular frames, not pane count.", "両機とも複数の構造窓を使います。枚数ではなく、A350の連続した黒マスクと777の独立した角張る枠を比較します。"),
            "bullets": [tr("正面主風擋較寬，中央接縫近乎垂直。", "Wide forward panes meet at a near-vertical centre seam.", "幅広い前面窓がほぼ垂直の中央継ぎ目で接します。"), tr("外側窗上緣向後下斜，形成明顯多邊形輪廓。", "The outer upper edge slopes aft and down, forming a pronounced polygonal outline.", "外側窓の上端が後方へ下がり、明確な多角形になります。"), tr("窗框未被整片黑色塗裝連成『墨鏡』。", "The frames are not joined by an all-black sunglasses-like surround.", "窓枠は黒い面で一体化したサングラス形状ではありません。")],
        },
        "fuselage": {"summary": tr("777 機身外徑約 6.20 m，客艙通常每排九或十席；777-300 的超長機身每側配置五對主艙門，門間距是遠距辨識的重要線索。", "The 777's fuselage is about 6.20 m wide. The long -300 has five main doors per side, whose spacing is a useful distant cue.", "777の胴体幅は約6.20 mで、長い-300は片側5枚の主ドアを備えます。ドア間隔は遠方識別に有効です。"), "fact": tr("A350-900 每側通常四對主艙門；先數大型艙門，再看主腳輪數，比只比較機身長度可靠。", "The A350-900 normally has four main doors per side. Count doors and main-gear wheels before judging length alone.", "A350-900は通常片側4枚です。胴体長だけでなくドア数と主脚輪数を確認します。"), "bullets": [tr("每側五對大型艙門是 777-300／300ER 的關鍵比例。", "Five large doors per side define the 777-300/300ER proportions.", "片側5枚の大型ドアが777-300／300ERの重要な比率です。"), tr("客艙窗為獨立橢圓窗，不像 787 的大型電子變色窗。", "Cabin windows are conventional individual ovals, unlike the 787's large dimmable windows.", "客室窓は通常の独立楕円窓で、787の大型電子調光窓とは異なります。"), tr("機鼻較圓但窗框有稜角，機尾收束較長。", "The nose is rounded but the glazing is angular, and the aft fuselage tapers over a long distance.", "機首は丸い一方で窓枠は角張り、後部胴体は長く絞られます。")]},
        "engine": {"summary": tr("777-300ER 固定使用 GE90-115B，高旁通比風扇直徑約 3.25 m，短艙巨大而接近完整圓形，是與 A350-900 區分時最醒目的部位之一。", "The 777-300ER exclusively uses the GE90-115B. Its roughly 3.25 m fan and massive near-circular nacelle are among the strongest cues against an A350-900.", "777-300ERはGE90-115B専用で、約3.25 mの巨大なファンとほぼ円形のナセルがA350-900との強い識別点です。"), "fact": tr("基本型 777-300 曾使用 GE90、PW4000 或 Trent 800；看到 GE90-115B 可確認 300ER，但不能反推所有 777-300 都相同。", "Baseline 777-300s could use earlier GE90s, PW4000s or Trent 800s. A GE90-115B confirms a -300ER, not every -300.", "基本型777-300には初期GE90、PW4000、Trent 800もあります。GE90-115Bは300ERの確認点です。"), "bullets": [tr("進氣口直徑巨大，風扇葉片彎曲且數量相對少。", "The inlet is enormous and the fan uses relatively few highly swept blades.", "吸気口が巨大で、強く湾曲した比較的少数のファン翼を使います。"), tr("短艙外形比 A350 的 Trent XWB 更粗壯。", "The nacelle looks bulkier than the A350's Trent XWB installation.", "ナセルはA350のTrent XWBより太く見えます。"), tr("引擎與六輪主腳一起看，能快速確認 777-300ER。", "Pair the engine with the six-wheel main bogie to confirm a 777-300ER.", "エンジンと6輪主脚を組み合わせると300ERを素早く確認できます。")]},
        "wingtip": {"summary": tr("777-300ER 沒有直立小翼，而是把翼尖本身向後、向外延伸成近乎水平的 raked tip。基本型 777-300 的翼尖較短，這是 ER 子型特徵。", "The 777-300ER has no upright winglet; the wing itself extends aft and outward into a nearly horizontal raked tip. The baseline -300 has a shorter tip.", "777-300ERには直立ウイングレットがなく、翼自体が後方・外側へ伸びる水平に近いレイクド翼端です。基本型-300はより短い翼端です。"), "fact": tr("A350 的翼尖明顯向上彎成翼梢裝置；777-300ER 的翼尖主要停留在翼面平面內。", "The A350 tip curves visibly upward, while the 777-300ER tip remains largely in the wing plane.", "A350は翼端が明確に上へ曲がりますが、777-300ERは主に翼面内へ伸びます。"), "bullets": [tr("翼尖向後拉長，沒有高大的直立翼片。", "The tip stretches aft without a tall upright blade.", "翼端は後方へ長く伸び、高い直立翼片がありません。"), tr("由客艙看像尖細的水平刀刃。", "From the cabin it appears as a long, slender horizontal blade.", "客室からは細長い水平の刃のように見えます。"), tr("此特徵應與 GE90-115B、五門機身一起確認。", "Confirm it together with GE90-115Bs and the five-door fuselage.", "GE90-115Bと片側5ドアも合わせて確認します。")]},
        "wing": {"summary": tr("777-300ER 使用大面積、高後掠翼，翼根厚、外翼逐漸變細並接到 raked tip；起飛與降落時可見大型多縫襟翼。", "The 777-300ER has a large swept wing with a thick root, tapered outer panel and raked tip, plus large multi-element flaps.", "777-300ERは厚い翼根から細い外翼とレイクド翼端へ続く大型後退翼で、多重スロットフラップを備えます。"), "fact": tr("777 與 A350 的後掠角接近，不能只看翼面角度；翼尖方向與主腳輪數更可靠。", "The 777 and A350 have similar sweep, so tip geometry and main-gear wheel count are more reliable than sweep alone.", "777とA350の後退角は近いため、翼端形状と主脚輪数の方が有効です。"), "bullets": [tr("外翼長而逐漸變細，末端接水平後掠翼尖。", "The long tapered outer wing ends in a horizontal raked tip.", "長く細くなる外翼が水平のレイクド翼端へ続きます。"), tr("翼根整流罩與六輪主腳輪艙體積很大。", "The root fairing and six-wheel main-gear bay are substantial.", "翼根フェアリングと6輪主脚格納部が大きくなります。"), tr("客艙翼景照片可用沒有直立 winglet 的輪廓判讀。", "Cabin wing views are recognizable by the absence of an upright winglet.", "客室翼景では直立ウイングレットがない輪郭が手掛かりです。")]},
        "vstab": {"summary": tr("777 的垂直尾翼高大、後掠，根部以長背鰭連接後機身；方向舵面積大，以應付大型雙發機單發失效時的偏航力矩。", "The 777's tall swept fin blends into the aft fuselage through a long dorsal fillet and carries a large rudder for engine-out control.", "777の高い後退垂直尾翼は長いドーサルフィンで後部胴体へつながり、大型方向舵を備えます。"), "fact": tr("航空公司塗裝容易吸引注意，但判型仍應看垂尾比例、機身門數與主腳。", "Livery is conspicuous, but identify the type from fin proportions, door count and landing gear.", "塗装は目立ちますが、尾翼比率、ドア数、主脚で機種を確認します。"), "bullets": [tr("垂尾前緣後掠明顯，根部背鰭長。", "The leading edge is strongly swept and the dorsal fillet is long.", "前縁後退が大きく、根元のドーサルフィンが長いです。"), tr("尾翼頂端較平，後緣方向舵接近直線。", "The fin tip is relatively flat and the rudder trailing edge nearly straight.", "尾翼上端は比較的平らで、方向舵後縁はほぼ直線です。"), tr("與 A350 相比，777 後機身與尾翼過渡更厚重。", "The 777's aft-fuselage/fin transition looks heavier than the A350's.", "A350より後部胴体と尾翼のつながりが重厚に見えます。")]},
        "hstab": {"summary": tr("777 的水平尾翼低置、尺寸大且後掠，與長後機身和高垂尾共同形成寬大的尾部輪廓。", "The 777 uses a large low-mounted swept tailplane, producing a broad tail silhouette with the long aft fuselage and tall fin.", "777は大型の低位置後退水平尾翼を備え、長い後部胴体と高い垂直尾翼で幅広い尾部輪郭になります。"), "fact": tr("水平尾翼外形單獨不易區分 777 與 A350；從後方應同時看機身寬度、翼尖與主腳。", "Tailplane shape alone is weak; from the rear also compare fuselage width, wingtips and main gear.", "水平尾翼だけでは判別しにくいため、後方から胴体幅、翼端、主脚も確認します。"), "bullets": [tr("尾翼根部整流罩厚，水平尾翼外展距大。", "The root fairing is thick and the tailplane spans widely.", "付け根フェアリングが厚く、水平尾翼の張り出しが大きいです。"), tr("後緣升降舵分段清楚。", "Segmented elevator surfaces are visible along the trailing edge.", "後縁に分割された昇降舵が見えます。"), tr("以六輪主腳和五門機身作主要交叉確認。", "Use six-wheel bogies and the five-door fuselage as the primary cross-check.", "6輪主脚と片側5ドアを主な照合点にします。")]},
        "gear": {"summary": tr("777-300／300ER 每組主起落架有三根輪軸、六個輪胎，主腳柱高且轉向架很長；前起落架為雙輪。", "Each 777-300/300ER main bogie has three axles and six tyres, creating a long truck beneath the high wide-body.", "777-300／300ERの各主脚は3軸6輪で、長いボギーを形成します。前脚は2輪です。"), "fact": tr("六輪主腳是區分 777-300ER 與四輪主腳 A350-900 最快速、可靠的地面特徵。", "Six-wheel main bogies are one of the fastest, most reliable ground-level cues against the four-wheel A350-900.", "6輪主脚は、4輪のA350-900と見分ける最も速く信頼できる地上識別点です。"), "bullets": [tr("每側主腳三軸六輪，排列明顯比 A350-900 長。", "Three axles and six tyres per side form a much longer bogie than the A350-900's.", "片側3軸6輪で、A350-900より明らかに長いボギーです。"), tr("主腳轉向架落地時會傾斜配合接地。", "The main truck tilts to sequence wheel contact during landing.", "着陸時は主脚ボギーが傾き、車輪が順に接地します。"), tr("搭配五對艙門可排除較短的 777-200。", "Pair it with five doors per side to exclude the shorter 777-200.", "片側5枚のドアと合わせて短い777-200を除外します。")]},
    },
    "a359": {
        "overview": {"summary": tr("A350-900 是複合材料廣體雙發客機，最醒目的外觀是駕駛艙窗周圍的黑色面罩、平順圓潤的機鼻、向上彎曲的翼尖，以及每側四對主艙門。", "The A350-900 is a composite wide-body twin identified by its black cockpit-window mask, smooth rounded nose, upward-curving tips and four main doors per side.", "A350-900は複合材ワイドボディ双発機で、黒い操縦席窓マスク、滑らかな丸い機首、上向きに曲がる翼端、片側4枚の主ドアが特徴です。"), "fact": tr("黑色『墨鏡』最容易看見，但仍應用四輪主腳、四對艙門與彎曲翼尖交叉確認，避免與 A330neo 等其他 Airbus 廣體機混淆。", "The black mask is obvious, but confirm it with four-wheel bogies, four door pairs and curved tips to avoid confusing other Airbus wide-bodies.", "黒いマスクは目立ちますが、4輪主脚、片側4ドア、曲線翼端で他のAirbusワイドボディ機と区別します。"), "bullets": [tr("黑色窗罩將六片駕駛艙窗連成連續面。", "A black surround visually joins the six cockpit panes.", "黒いマスクが6枚の操縦席窓を連続した面に見せます。"), tr("每側四對主艙門，比 777-300ER 少一對。", "Four main doors per side, one fewer than the 777-300ER.", "片側4枚の主ドアで、777-300ERより1枚少ないです。"), tr("翼尖柔和上彎，主腳每側為四輪。", "Tips curve smoothly upward and each main bogie has four wheels.", "翼端は滑らかに上へ曲がり、各主脚は4輪です。")]},
        "cockpit": {"summary": tr("A350 駕駛艙使用側桿與六具大型寬螢幕，飛行員正前方沒有駕駛盤；中央顯示器整合 ECAM、飛行管理與系統頁面。", "The A350 flight deck uses sidesticks and six large widescreen displays, leaving no yoke in front of either pilot. Central screens integrate ECAM, flight-management and system pages.", "A350の操縦席はサイドスティックと6面の大型ワイド画面を使い、両席正面に操縦輪がありません。中央画面がECAMやシステム表示を統合します。"), "fact": tr("A350 與 A380 共用相近的 Airbus 座艙哲學；相較 777，最直觀差異是側桿、桌板與更大的寬螢幕。", "The A350 follows the A380-era Airbus philosophy. Sidesticks, tray tables and larger widescreens distinguish it immediately from a 777.", "A350はA380世代のAirbus思想を採用し、サイドスティック、テーブル、大型ワイド画面が777との明確な違いです。"), "bullets": [tr("左右側桿取代駕駛盤，正面空間可設桌板。", "Sidesticks replace yokes, freeing space for tray tables.", "操縦輪をサイドスティックに置き換え、正面にテーブル空間があります。"), tr("六具大型液晶螢幕比 777 的傳統六屏更寬。", "Six large LCDs are wider than the traditional 777 display set.", "6面の大型LCDは従来型777の画面より横長です。"), tr("中央台與頂板仍保留大量實體旋鈕，並非全觸控。", "The pedestal and overhead retain physical controls; the cockpit is not all-touchscreen.", "中央台とオーバーヘッドには物理操作部が残り、全面タッチ式ではありません。")]},
        "windshield": {"summary": tr("A350 的六片風擋被亮黑色外框連成像『墨鏡』的完整窗罩，外框向兩側拉長並順著圓鼻下緣延伸，是現代客機最鮮明的正面辨識特徵之一。", "The A350's six panes are visually joined by a glossy black sunglasses-like mask that stretches around the rounded nose, one of the clearest modern airliner cues.", "A350の6枚の窓は光沢のある黒いサングラス状マスクで一体化され、丸い機首の両側へ伸びます。現代旅客機で最も明瞭な識別点の一つです。"), "fact": tr("黑色區域主要是外觀與防眩處理，不代表只有一整片玻璃；實際仍是可更換、加熱的多片結構風擋。", "The black surround is not one giant pane; the windshield remains multiple replaceable heated structural panels.", "黒い部分は一枚の巨大ガラスではなく、交換可能な加熱式構造窓が複数並んでいます。"), "bullets": [tr("黑色外框跨過窗片間隔，形成連續面罩。", "The black surround bridges the gaps into one continuous mask.", "黒い外周が窓間をつなぎ、一体のマスクになります。"), tr("正面窗下緣向中央形成柔和下彎弧線。", "The lower edge forms a smooth downward curve toward the centre.", "正面窓の下縁は中央へ向けて滑らかに下がります。"), tr("側窗後端尖細，黑框一路延伸到機身側面。", "The aft side pane tapers sharply and the mask wraps onto the fuselage sides.", "後方側窓は尖り、黒い枠が胴体側面まで回り込みます。")]},
        "fuselage": {"summary": tr("A350 機身外寬約 5.96 m，大量使用碳纖維複合材料。A350-900 每側四對大型主艙門，窗線與黑色駕駛艙面罩之間過渡平順。", "The A350 fuselage is about 5.96 m wide and extensively composite. The -900 has four main doors per side with a smooth transition from cabin windows to the black cockpit mask.", "A350の胴体幅は約5.96 mで複合材を多用します。-900は片側4枚の主ドアを備え、客室窓から黒い操縦席マスクへ滑らかにつながります。"), "fact": tr("777-300ER 每側五對艙門且機身更長；在側面遠景中，數大型艙門通常比估算長度更可靠。", "The 777-300ER has five doors per side and is longer. Counting main doors is usually more reliable than estimating length.", "777-300ERは片側5枚でより長いため、遠景では全長推定より大型ドア数が有効です。"), "bullets": [tr("每側四對主艙門，機翼前兩對、後方兩對。", "Four main doors per side, two ahead of the wing and two aft.", "片側4枚で、主翼前に2枚、後方に2枚あります。"), tr("機身直徑略小於 777，但客艙仍可每排九席。", "The body is slightly narrower than the 777 but still supports nine-abreast seating.", "777よりやや細いものの、客室は9席横並びに対応します。"), tr("複合材料蒙皮使表面接縫與鋁合金機體觀感不同。", "Composite skins produce different panel-joint patterns from aluminium airframes.", "複合材外板はアルミ機体と異なるパネル継ぎ目を見せます。")]},
        "engine": {"summary": tr("A350-900 固定使用 Rolls-Royce Trent XWB-84。短艙圓潤、比例修長，風扇直徑約 3.0 m，雖然巨大但通常比 777-300ER 的 GE90-115B 顯得纖細。", "The A350-900 exclusively uses the Rolls-Royce Trent XWB-84. Its roughly 3.0 m fan sits in a smooth, relatively slender nacelle compared with the 777-300ER's GE90-115B.", "A350-900はRolls-Royce Trent XWB-84専用です。約3.0 mのファンを滑らかで比較的細長いナセルに収め、777-300ERのGE90-115Bより細身に見えます。"), "fact": tr("A350-1000 使用推力更大的 Trent XWB-97，但外觀仍屬同一家族；要區分 -900／-1000 應再看機身長度、艙門與主腳。", "The A350-1000 uses the higher-thrust XWB-97. Separate -900 and -1000 using length, doors and landing gear, not engine appearance alone.", "A350-1000は高推力のXWB-97を使います。-900／-1000はエンジンだけでなく胴体長、ドア、主脚で区別します。"), "bullets": [tr("短艙外形圓滑且較修長，進氣口不像 GE90-115B 那麼粗壯。", "The smooth elongated nacelle looks less bulky than a GE90-115B installation.", "滑らかで長いナセルはGE90-115Bほど太く見えません。"), tr("所有 A350-900 都使用 Trent XWB，沒有多家引擎選項。", "Every A350-900 uses a Trent XWB; there is no competing engine option.", "A350-900はすべてTrent XWBで、他社エンジン選択肢はありません。"), tr("搭配黑色窗罩與上彎翼尖可快速確認 A350。", "Pair it with the black cockpit mask and upturned tips to confirm an A350.", "黒い窓マスクと上向き翼端を合わせてA350を確認します。")]},
        "wingtip": {"summary": tr("A350 的外翼與翼尖連續扭轉、向上彎曲，形成沒有清楚接縫的 blended winglet；輪廓像柔和的長刀向上挑起。", "The A350 outer wing twists and curves continuously upward into a blended winglet with no abrupt joint, resembling a long blade swept upward.", "A350の外翼は連続的にねじれながら上へ曲がり、明確な継ぎ目のないブレンデッド・ウイングレットになります。"), "fact": tr("777-300ER 的 raked tip 主要水平向後延伸；A350 的翼尖則有明顯垂直高度，是遠距最有用的差異之一。", "The 777-300ER raked tip extends mainly aft and horizontally; the A350 tip gains obvious vertical height.", "777-300ERは主に水平後方へ伸び、A350は明確に上方へ高さを持つ点が大きな違いです。"), "bullets": [tr("翼尖由外翼平順上彎，沒有獨立直立小翼接縫。", "The tip rises smoothly from the outer wing without a separate winglet joint.", "外翼から滑らかに上昇し、独立した小翼の継ぎ目がありません。"), tr("外緣向後收尖，視角不同時彎曲程度看起來會改變。", "The trailing outline tapers aft, and apparent curvature changes with viewing angle.", "後方へ細くなり、見る角度で曲がり方が変わって見えます。"), tr("與黑色駕駛艙窗罩一起，是 A350 的代表性外型。", "Together with the black cockpit mask, it defines the A350 silhouette.", "黒い操縦席マスクと並ぶA350の代表的外形です。")]},
        "wing": {"summary": tr("A350 使用高展弦比複合材料機翼，外翼在飛行中會顯著上彎，翼尖連續過渡成 blended winglet；大型襟翼與擾流板沿後緣排列。", "The A350 has a high-aspect-ratio composite wing that flexes visibly in flight and blends continuously into its curved tip, with large flaps and spoilers along the trailing edge.", "A350は高アスペクト比の複合材翼を備え、飛行中に大きくしなり、外翼は曲線翼端へ連続します。後縁には大型フラップとスポイラーがあります。"), "fact": tr("複合材料讓機翼能以受控方式彎曲以降低陣風載荷；看起來柔軟並不代表結構薄弱。", "Composite construction permits controlled flex that helps manage gust loads; visible bending is intentional, not weakness.", "複合材翼のしなりは突風荷重を管理する意図的な設計で、弱さを示すものではありません。"), "bullets": [tr("翼根厚、外翼修長，飛行中上彎幅度明顯。", "A thick root transitions into a slender outer wing with visible in-flight flex.", "厚い翼根から細い外翼へ続き、飛行中の上反りが目立ちます。"), tr("翼尖平順向上彎，不是 777 的水平 raked tip。", "The tip curves upward rather than remaining a horizontal raked extension like the 777's.", "翼端は上へ曲がり、777の水平レイクド翼端とは異なります。"), tr("翼下只有兩具 Trent XWB，位置靠近翼根。", "Two Trent XWBs hang beneath the inner wing.", "2基のTrent XWBが内翼下に配置されます。")]},
        "vstab": {"summary": tr("A350 垂直尾翼以複合材料製成，前緣後掠、頂端向後收尖，根部與後機身的整流過渡較纖細平順。", "The composite A350 fin has a swept leading edge, aft-tapered tip and a relatively slender smooth fairing into the aft fuselage.", "複合材のA350垂直尾翼は後退前縁と後方へ細くなる上端を持ち、後部胴体へ細く滑らかにつながります。"), "fact": tr("垂尾塗裝主要辨識航空公司；區分 777 與 A350 時，黑色窗罩、艙門數與主腳更可靠。", "Tail paint identifies the airline. The cockpit mask, door count and main gear are stronger 777/A350 discriminators.", "尾翼塗装は航空会社の手掛かりです。777／A350判別には窓マスク、ドア数、主脚がより有効です。"), "bullets": [tr("尾翼根部整流罩較長而平滑。", "The fin-root fairing is long and smoothly blended.", "尾翼根元のフェアリングが長く滑らかです。"), tr("頂端向後收尖，方向舵後緣接近直線。", "The tip tapers aft and the rudder trailing edge is nearly straight.", "上端は後方へ細くなり、方向舵後縁はほぼ直線です。"), tr("後機身較 777 顯得細長、表面線條更圓順。", "The aft fuselage appears slimmer and smoother than the 777's.", "後部胴体は777より細長く滑らかに見えます。")]},
        "hstab": {"summary": tr("A350 的水平尾翼低置於後機身兩側，複合材料安定面後掠且翼尖收細，根部整流罩與機身曲面連續。", "The A350's low-mounted composite tailplane is swept and tapered, with root fairings flowing continuously into the aft fuselage.", "A350の低位置複合材水平尾翼は後退・先細形で、付け根フェアリングが後部胴体へ連続します。"), "fact": tr("水平尾翼本身不是可靠的單一判型特徵；應配合上彎翼尖、黑色窗罩與四輪主腳。", "The tailplane is not a reliable standalone cue; combine it with curved tips, the black mask and four-wheel bogies.", "水平尾翼単独は弱い識別点です。曲線翼端、黒マスク、4輪主脚を組み合わせます。"), "bullets": [tr("外形修長，翼尖與後緣收束平順。", "The slender surface tapers smoothly at the tip and trailing edge.", "細長い外形で、翼端と後縁が滑らかに絞られます。"), tr("根部整流罩比 777 的厚重過渡更纖細。", "The root fairing is visually slimmer than the heavier 777 transition.", "付け根は777の重厚な移行部より細く見えます。"), tr("從後方辨識時先看主腳四輪而非只看尾翼。", "From the rear, check the four-wheel main gear before relying on tail shape.", "後方からは尾翼より先に4輪主脚を確認します。")]},
        "gear": {"summary": tr("A350-900 每組主起落架為兩軸四輪，前起落架雙輪；這與 777-300ER 的三軸六輪主腳形成非常清楚的差異。", "Each A350-900 main bogie has two axles and four tyres, versus the 777-300ER's three axles and six tyres.", "A350-900の各主脚は2軸4輪で、777-300ERの3軸6輪と明確に異なります。"), "fact": tr("A350-1000 改用六輪主腳；因此『四輪＝A350』只適用於 A350-900，辨識時要先確認子型與艙門比例。", "The A350-1000 uses six-wheel main gear. Four wheels identify an A350-900, not every A350 variant.", "A350-1000は6輪主脚です。4輪はA350-900の識別点であり、全A350共通ではありません。"), "bullets": [tr("每側主腳兩軸四輪，轉向架明顯短於 777-300ER。", "Two axles and four tyres make a visibly shorter bogie than the 777-300ER's.", "片側2軸4輪で、777-300ERより明らかに短いボギーです。"), tr("主腳艙門與支柱外形較整潔、緊湊。", "The gear doors and strut installation appear relatively compact.", "脚扉と支柱配置は比較的コンパクトです。"), tr("四輪主腳、四對艙門與黑色窗罩三者可快速確認 A350-900。", "Four-wheel bogies, four door pairs and the black mask together confirm an A350-900 quickly.", "4輪主脚、片側4ドア、黒マスクの組み合わせでA350-900を素早く確認できます。")]},
    },
}


CAPTIONS = {
    "overview": tr("實機整體外型參考", "Real-aircraft overall-profile reference", "実機全体外観の参考"),
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
    photo_count = len(CONTENT) * 11
    print(f"Reference-photo data check passed: {len(CONTENT)} aircraft x 10 identification parts / {photo_count} photos.")


if __name__ == "__main__":
    for aircraft in CONTENT:
        update(aircraft)
    check()
