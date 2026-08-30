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


def identify(summary: tuple[str, str, str], fact: tuple[str, str, str], bullets: list[tuple[str, str, str]]) -> dict:
    return {"summary": tr(*summary), "fact": tr(*fact), "bullets": [tr(*bullet) for bullet in bullets]}


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
    "b789": {
        "overview": "https://commons.wikimedia.org/wiki/File:Qantas_Boeing_787_VH-ZNM_Perth_2026_(01).jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:Boeing_787-8_N787BA_cockpit.jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:Front_view_of_ANA_Boeing_787-8_JA834A_at_Taipei_Songshan_Airport_20150101.jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:Cockpit_windows_of_a_Boeing_787_(3).jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:VN-A819_Boeing_787-9_Bamboo_Airways_LHR_23.3.22.jpg",
        "engine": "https://commons.wikimedia.org/wiki/File:Boeing_787_engine_chevrons.jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:Wingtip_device_of_Boeing_787_(1).jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:Boeing_787_Dreamliner_wing_view.jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:Vertical_tail_of_B787_(1).jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:Horizontal_stabilizer_of_B787_(1).jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:Air_India_Boeing_787_Dreamliner_N1008S_PAS_2013_06_main_landing_gear.jpg",
    },
    "a333": {
        "overview": "https://commons.wikimedia.org/wiki/File:AirAsia_X_Airbus_A330_9M-XXQ_Perth_2024_(02).jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:Airbus_A330-302_Iberia_EC-LYF_cockpit_(10983484845).jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:Airbus_A330_Front_View.jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:Airbus_A330-343X,_China_Eastern_Airlines_JP7548435.jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:Airbus_A330-300_(Air_Canada)_333.jpg",
        "engine": "https://commons.wikimedia.org/wiki/File:Rolls-Royce_Trent_700_viewed_from_boarding_gangway.jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:Wingtip_device_on_a_China_Eastern_Airlines_Airbus_A330-343.jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:02-JUL-2022_-_QR184_VIE-DOH_(A330-300_-_A7-AEO)_(04).jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:Airbus_A330_tail_Leitwerk.jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:China_Eastern_Airbus_A330-300_B-6095_lining_up_at_Taipei_Songshan_April_2026_3.jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:Landing_gear_on_a_Malaysian_Airlines_Airbus_A330-300.jpg",
    },
    "b748": {
        "overview": "https://commons.wikimedia.org/wiki/File:Lufthansa_Boeing_747-8i_at_San_Francisco_September_2023.jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:Boeing_747-8I_flight_deck_Beltyukov.jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:Lufthansa_Boeing_747-8_20180513_3722.jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:Boeing_747_cockpit_window_from_outside.jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:Boeing_747-8_Baden-W%C3%BCrttemberg.jpg",
        "engine": "https://commons.wikimedia.org/wiki/File:General_Electric_GEnx_on_747-8I_prototype.jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:2015_10_01_LH_Boeing_747_8_D_ABYT@EDDF_left_wingtip.jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:2015_10_01_LH_Boeing_747_8_D_ABYT@EDDF_left_wing.jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:Boeing_747-8_of_Korean_Air_at_Los_Angeles_International_Airport.jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:Boeing_747-8F_N5017Q_inflight.jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:Boeing_747-8I_landing_gear.jpg",
    },
    "a380": {
        "overview": "https://commons.wikimedia.org/wiki/File:Emirates_Airbus_A380_A6-EOG_Perth_2024_(01).jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:Airbus_A380_cockpit.jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:A380-front.JPG",
        "window_side": "https://commons.wikimedia.org/wiki/File:Airbus_A380_front_side.jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:Airbus_A380_front_side.jpg",
        "engine": "https://commons.wikimedia.org/wiki/File:A380_Engines.jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:British_Airways_Airbus_A380-841_F-WWSK_PAS_2013_10_Wingtip_device.jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:A380_Wing.jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:A380_Tail.jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:A380-tail.JPG",
        "gear": "https://commons.wikimedia.org/wiki/File:British_Airways_Airbus_A380-841_F-WWSK_PAS_2013_08_main_landing_gear.jpg",
    },
    "b752": {
        "overview": "https://commons.wikimedia.org/wiki/File:Icelandair_Boeing_757_TF-ISR_Milan_Malpensa_2024_(01).jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:Boeing_757-200_flight_deck.jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:Face_to_Face_with_Delta_(N616DL)_(8331933080).jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:The_front_end_of_a_757_(2710024227).jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:American_Airlines_B757-200_forward_fuselage_view_in_hangar.jpg",
        "engine": "https://commons.wikimedia.org/wiki/File:British_Airways_B757_Heathrow_Airport_jet_engine_intake.jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:Boeing_757_winglet_(4269906229).jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:Onboard_the_Boeing_757_(3390330324).jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:Boeing_757-200_-_Icelandair_(tail).jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:Icelandair_tail_at_Oslo.jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:Ba_b757-200_g-bpei_closeup_arp.jpg",
    },
    "a321": {
        "overview": "https://commons.wikimedia.org/wiki/File:Finnair_Airbus_A321_OH-LZF_Oslo_Gardermoen_2024_(01).jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:Airbus_A321_cockpit_-_G-EUXG_British_Airways.jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:Delta_A321_at_Airbus_Mobile.jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:Finnair_Airbus_A321_OH-LZF_Oslo_Gardermoen_2024_(02).jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:Airbus_A321-211,_N827Q_-_open_doors.jpg",
        "engine": "https://commons.wikimedia.org/wiki/File:Airbus_A321-231,_Middle_East_Airlines_(MEA)_JP6762964.jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:Wingtip_device_of_Airbus_A-321-200.JPG",
        "wing": "https://commons.wikimedia.org/wiki/File:Airbus_A321_wingtip_fence.jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:TC-JRN_Airbus_A321_Turkish_Airlines_Tail_(8633650011).jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:TransAsia_Airways_Airbus_A321-231_B-22612_Departing_from_Taipei_Songshan_Airport_20151003f.jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:Port_side_main_landing_gear_of_Finnair_Airbus_A321_OH-LZA.jpg",
    },
    "b763": {
        "overview": "https://commons.wikimedia.org/wiki/File:Hawaiian_Airlines_(N592HA)_Boeing_767-300ER_at_Sydney_Airport.jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:AeroMexico_Boeing_767-300ER_cockpit.jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:Boeing_767-300ER_(Japan_Airlines)_02.jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:Hawaiian_Airlines_(N592HA)_Boeing_767-300ER_at_Sydney_Airport.jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:Boeing_767-300ER_United_Airlines_N656UA.jpg",
        "engine": "https://commons.wikimedia.org/wiki/File:Air_Canada_Boeing_767-300ER_with_CF6-80_engines.jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:ALL_NIPPON_BOEING_767-300_WINGLETS_AT_NARITA_AIRPORT_TOKYO_JAPAN_JUNE_2012_(7456802526).jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:Boeing_767-323ER_spoilers_on_descent_to_POS,_AAL_1167,_11-29-12.jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:ET-ALO_at_ADD.jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:Ba_b767-300_g-bnwa_planform_arp.jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:American_Airlines_B767-300ER_main_landing_gear.jpg",
    },
    "a332": {
        "overview": "https://commons.wikimedia.org/wiki/File:Airbus_A330-200_Hainan_AL_(CHH)_F-WWYJ_-_MSN_1168_-_Will_be_B-6520_(5413679264).jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:13-08-06-Cockpit-d-alpa-a330-200.jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:Face_to_face_(F-OONE)_(14771492742).jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:KLM_Airbus_A330-200_PH-AOI_nose_section_(3186787311).jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:KLM_Airbus_A330-200_PH-AOI_nose_section_(3186787311).jpg",
        "engine": "https://commons.wikimedia.org/wiki/File:Pratt_%26_Whitney_PW4000_turbofan_with_open_cowling.jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:%E7%BF%BC%E5%B0%96%E5%B0%8F%E7%BF%BC02.JPG",
        "wing": "https://commons.wikimedia.org/wiki/File:Window_and_wing_inflight.jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:KLM_Airbus_A330-200_PH-AOC_tail_(6924834528).jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:Cyprus_airways_a330-200_5b-dbs_arp.jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:VH-SSA_%27Outback%27_Airbus_A330-223_Strategic_Airlines_(7107083943).jpg",
    },
    "b744": {
        "overview": "https://commons.wikimedia.org/wiki/File:Air_New_Zealand_747-400_sideview.jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:Boeing_747-400_cockpit.jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:Boeing_747_Jumbo_front_cockpit_windows.jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:KLM_Boeing_747-400_PH-BFI_nose_section_(10205055606).jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:KLM_Boeing_747-400_PH-BFI_nose_section_(10205055606).jpg",
        "engine": "https://commons.wikimedia.org/wiki/File:Rolls_Royce_Trent_jet_engine,_Qantas_747-400_(5381505855).jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:Winglet_and_nav_light_arp.jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:Elal_747-400_wing.jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:KLM_Boeing_747-400_PH-BFT_tail_(6972557066).jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:Ba_b747-400_g-bnle_arp.jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:Boeing_747_main_landing_gear.jpg",
    },
    "a346": {
        "overview": "https://commons.wikimedia.org/wiki/File:Etihad_Airways_Airbus_A340-600_SYD_Gilbert-1.jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:A340-642_flight_deck.jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:A340-600_(13024845015).jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:G-VSHY_Airbus_A340-642_(cn_383)_Virgin_Atlantic_Airways._(6100631197).jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:G-VSHY_Airbus_A340-642_(cn_383)_Virgin_Atlantic_Airways._(6100631197).jpg",
        "engine": "https://commons.wikimedia.org/wiki/File:Iberia_A340-600_Rolls-Royce_Trent_500_engines.jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:Airbus_A340-600_Wing.JPG",
        "wing": "https://commons.wikimedia.org/wiki/File:A340-600_clean-wing_bottom_plan-view.jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:Airbus_A340-600_Tail_assembly_(8459395384).jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:G-VBUG_Airbus_A346_Virgin_Atlantic_Tail_(13891670573).jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:Thai_airways_a340-600_hs-tna_takeoff_arp.jpg",
    },
    "b717": {
        "overview": "https://commons.wikimedia.org/wiki/File:Boeing_717,_N483HA,_Hawaiian_Airlines.jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:N938AT_Boeing_717_flight_deck.jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:Boeing_717_MD95,_Hawaiian,_Honolulu,_nose-on_(4389641139)_(3).jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:N937AT_Boeing_717_Air_Tran_Nose_(7438725424).jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:N937AT_Boeing_717_Air_Tran_Nose_(7438725424).jpg",
        "engine": "https://commons.wikimedia.org/wiki/File:Boeing_717_MD95,_Hawaiian,_left_port_tail_and_engine,_at_gate_(4389633539)_(3).jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:11-APR-2022_-_HA284_LIH-HNL_(B717-200_-_N488HA)_(02).jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:Boeing_717_(1).jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:EC-MGT_717_Volotea_tailfin_VGO.jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:Air_Tran_Boeing_717_aka_MD-95_-_note_tail_surrface_anhedral_-_frame_1049_(4906658072)_(2).jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:QantasLink_B717-231_(VH-NXO)_departing_Perth_Airport.jpg",
    },
    "cs100": {
        "overview": "https://commons.wikimedia.org/wiki/File:ITA_Airways_A220-100_EI-HLE_2024-06-15_Munich_Airport_p02.jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:Bombardier_CS100_(23463394635).jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:Bombardier_CS100_(23463413085).jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:Swiss,_HB-JBC,_Bombardier_CS100_(31383514146).jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:Swiss,_HB-JBC,_Bombardier_CS100_(31383514146).jpg",
        "engine": "https://commons.wikimedia.org/wiki/File:Bombardier_CS100_at_Brussels_Airport_(25272589779).jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:Cabin_window_view_of_Swissair_aircraft_wings_(24482756908).jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:ITA_Airways,_I-ADVA,_Airbus_A220-100_(54007495525)_at_Milan_Linate.jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:Swiss,_HB-JBI,_Airbus_A220-100_(49580114558).jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:Swiss_International_Airlines_HB-JBH_BOMBARDIER_CS100_A220-100_(Ank_Kumar,_Infosys_Limited)_05.jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:Bombardier_CS100_(23437223616).jpg",
    },
    "b737": {
        "overview": "https://commons.wikimedia.org/wiki/File:Southwest_Boeing_737-700_N947WN_BWI_MD1.jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:Cockpit-737-700-by-RalfR.jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:B-5265_Boeing_737-79P_China_Eastern_Airlines_Lining_Up_for_Take_Off_-_Head_On_(8613160786).jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:KLM_Boeing_737-700_PH-BGF_cockpit_closeup_(3517238451).jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:Southwest_Boeing_737-700_N947WN_BWI_MD1.jpg",
        "engine": "https://commons.wikimedia.org/wiki/File:Virgin_Blue_Boeing_737-700_SYD_Spijkers.jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:Boeing_737-700_Southwest_winglet,_and_headquarters,_Love_Field_(2717214038)_(3).jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:Southwest_Starboard_Wing_(33198022825).jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:Boeing_737-700_PH-BGP_of_KLM_Tail_(12291134464).jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:Boeing_737-700,_Southwest,_winglets,_from_below_(6190651480).jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:VH-VBY_%27Virginia_Blue%27_Boeing_737-7FE_Virgin_Blue_(9046044503).jpg",
    },
    "a319": {
        "overview": "https://commons.wikimedia.org/wiki/File:Ba_a319-100_g-euog_arp.jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:Airbus-319-cockpit.jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:G-EZGM_easyJet_Airbus_A319-111_-_cn_4778_head-on_taxiing.JPG",
        "window_side": "https://commons.wikimedia.org/wiki/File:Ba_a319-100_g-euog_arp.jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:Hamburg_Airport_easyJet_Airbus_A319-111_G-EZAO_(DSC08652).jpg",
        "engine": "https://commons.wikimedia.org/wiki/File:Hamburg_Airport_easyJet_Airbus_A319-111_G-EZAO_(DSC08652).jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:Airbus_A319_wintip.jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:A319_Port_Wing_(40736437962).jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:Germanwings_Airbus_A319-112_D-AKNP_STR_2016_01.jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:Adria_Airways_Airbus_A319_(S5-AAR)_@CDG,_2015-06-25.jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:QantasLink_Airbus_A319_VH-8NP_Perth_2025_(02).jpg",
    },
    "b736": {
        "overview": "https://commons.wikimedia.org/wiki/File:Boeing_737-600_(6778274137).jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:Cockpit-737-700-by-RalfR.jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:SAS_Boeing_737-600_parked_at_Kiruna_Airport_(DSCF0852).jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:Boeing_737-600_(6778274137).jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:Boeing_737-600_(6778274137).jpg",
        "engine": "https://commons.wikimedia.org/wiki/File:Boeing_737-600_(6778274137).jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:SAS_Boeing_737-600_parked_at_Kiruna_Airport_(DSCF0852).jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:SAS_Boeing_737-600_parked_at_Kiruna_Airport_(DSCF0852).jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:Boeing_737-600_(6778274137).jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:Boeing_737-600_(6778274137).jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:Boeing_737-600_(6778274137).jpg",
    },
    "a318": {
        "overview": "https://commons.wikimedia.org/wiki/File:Airbus_A318-111_(F-GUGJ)_01.jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:Airbus_A318_Cockpit_(8605111142).jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:Airbus_A318_aterrizando_pista_20L_en_SDU_(8781193831).jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:Airbus_A318-111_(F-GUGJ)_01.jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:Airbus_A318-122_(8360157259).jpg",
        "engine": "https://commons.wikimedia.org/wiki/File:Airbus_A318-122_(8360157259).jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:Airbus_A318-122_(8360157259).jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:Airbus_A318-122_(8360157259).jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:Airbus_A318-122_(8360157259).jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:Airbus_A318-122_(8360157259).jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:Airbus_A318_Landing_Gear_(8604009277).jpg",
    },
    "b772": {
        "overview": "https://commons.wikimedia.org/wiki/File:United_Boeing_777-200_N77019_MD1.jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:Boeing_777-200ER_cockpit.jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:Boeing_777-200_(Japan_Airlines)_JA704J_(3220615977).jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:United_Boeing_777-200_N77019_MD1.jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:United_Boeing_777-200_N77019_MD1.jpg",
        "engine": "https://commons.wikimedia.org/wiki/File:United_Boeing_777-200_N77019_MD1.jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:United_Airlines_-_N772UA_-_Boeing_777-200_-_San_Francisco_International_Airport-0406.jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:United_Airlines_-_N772UA_-_Boeing_777-200_-_San_Francisco_International_Airport-0406.jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:United_Boeing_777-200_N77019_MD1.jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:United_Boeing_777-200_N77019_MD1.jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:Boeing_777-200_center,_aft,_fuselage,_wing_root_fairing,_main_gear_and_doors,_etc._(2719420955)_(3).jpg",
    },
    "a343": {
        "overview": "https://commons.wikimedia.org/wiki/File:South_African_Airways_Airbus_A340-313_ZS-SXE_MUC_2015_06.jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:A340-300_cockpit_(8459431964).jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:South_African_Airways_Airbus_A340-313_ZS-SXE_MUC_2015_02.jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:Airbus_A340-313X,_Virgin_Atlantic_Airways_JP359341.jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:South_African_Airways_Airbus_A340-313_ZS-SXE_MUC_2015_06.jpg",
        "engine": "https://commons.wikimedia.org/wiki/File:South_African_Airways_Airbus_A340-313_ZS-SXE_MUC_2015_06.jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:BLADE,_ILA_2018,_Sch%C3%B6nefeld_(1X7A5551).jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:BLADE,_ILA_2018,_Sch%C3%B6nefeld_(1X7A5551).jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:South_African_Airways_Airbus_A340-313_ZS-SXE_MUC_2015_06.jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:South_African_Airways_Airbus_A340-313_ZS-SXE_MUC_2015_06.jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:South_African_Airways_Airbus_A340-313_ZS-SXE_MUC_2015_02.jpg",
    },
    "beluga": {
        "overview": "https://commons.wikimedia.org/wiki/File:Airbus_Beluga_Airbus_A300B4-608ST_F-GSTA_(28858044414).jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:Airbus_A300_panel.jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:Airbus_A300-600ST_Beluga_F-GSTB_44675.jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:Airbus_A300-600ST_Beluga_F-GSTA.jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:Airbus_Beluga_A300-600ST_open.jpeg",
        "engine": "https://commons.wikimedia.org/wiki/File:Airbus_A300-600ST_Beluga_F-GSTA.jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:Airbus_A300-600ST_Beluga_1_(1).jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:Airbus_A300-600ST_Beluga_1_(1).jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:Airbus_A300-600ST_Beluga_1_(1).jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:Airbus_A300-600ST_Beluga_1_(1).jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:Airbus_A300-600ST_Beluga_F-GSTB_44675.jpg",
    },
    "dreamlifter": {
        "overview": "https://commons.wikimedia.org/wiki/File:Boeing_Dreamlifter_Landing.jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:Boeing_747-400_cockpit.jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:Boeing_Dreamlifter_Landing.jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:Boeing_747-400LCF_Dreamlifter.jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:747_400LCF_DREAM_LIFTER.jpg",
        "engine": "https://commons.wikimedia.org/wiki/File:Boeing_Dreamlifter_Landing.jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:Boeing_747-400LCF_Dreamlifter.jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:Boeing_Dreamlifter_Landing.jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:Boeing_747-409(LCF)_Dreamlifter,_N249BA_-_PAE_(21348697683).jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:Boeing_747-409(LCF)_Dreamlifter,_N249BA_-_PAE_(21348697683).jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:Boeing_Dreamlifter_Landing.jpg",
    },
    "crj900": {
        "overview": "https://commons.wikimedia.org/wiki/File:Air_Canada_Express_Bombardier_CRJ-900_C-FJFZ_BWI_MD1.jpg",
        "cockpit": "https://commons.wikimedia.org/wiki/File:Bombardier-crj-900-cockpit-by-RalfR.jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:THE_CRJ-900_head_on_(2436749543).jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:Air_Canada_Express_Bombardier_CRJ-900_C-FJFZ_BWI_MD1.jpg",
        "fuselage": "https://commons.wikimedia.org/wiki/File:Air_Canada_Express_Bombardier_CRJ-900_C-FJFZ_BWI_MD1.jpg",
        "engine": "https://commons.wikimedia.org/wiki/File:Air_Canada_Express_Bombardier_CRJ-900_C-FJFZ_BWI_MD1.jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:Air_Canada_Express_Bombardier_CRJ-900_C-FJFZ_BWI_MD1.jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:Lufthansa_Regional_Bombardier_CRJ-900LR_D-ACKK_MUC_2015_01.jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:Air_Canada_Express_Bombardier_CRJ-900_C-FJFZ_BWI_MD1.jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:On_nice_looking_tail_(2813033694).jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:Lufthansa_Regional_Bombardier_CRJ-900LR_D-ACKK_MUC_2015_01.jpg",
    },
    "e190": {
        "overview": "https://commons.wikimedia.org/wiki/File:Finnair_Embraer_190_OH-LKP_at_HEL_05JUN2015.JPG",
        "cockpit": "https://commons.wikimedia.org/wiki/File:Cabine_do_Embraer_190.jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:PH-EZX_KLM_Cityhopper_Embraer_ERJ-190STD_(ERJ-190-100)_-_cn_19000545_taxiing_front_view_13july2013_pic1.JPG",
        "window_side": "https://commons.wikimedia.org/wiki/File:Finnair_Embraer_190_OH-LKP_at_HEL_05JUN2015.JPG",
        "fuselage": "https://commons.wikimedia.org/wiki/File:Finnair_Embraer_190_OH-LKP_at_HEL_05JUN2015.JPG",
        "engine": "https://commons.wikimedia.org/wiki/File:Embraer_E190_engine_in-flight.jpg",
        "wingtip": "https://commons.wikimedia.org/wiki/File:Embraer_E190_wingtip.jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:Embraer_E190_wing.jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:LV-CDY_Embraer_190_Austral_Tail_(8164021706).jpg",
        "hstab": "https://commons.wikimedia.org/wiki/File:LV-CDY_Embraer_190_Austral_Tail_(8164021706).jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:PH-EZX_KLM_Cityhopper_Embraer_ERJ-190STD_(ERJ-190-100)_-_cn_19000545_taxiing_front_view_13july2013_pic1.JPG",
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
    "b789": {
        "overview": {"summary": tr("787-9 是中大型複合材料廣體雙發客機，可由圓滑機鼻、大型駕駛艙窗、鋸齒狀引擎短艙後緣、明顯上彎的高展弦比主翼與水平後掠翼尖辨認。", "The 787-9 is a composite wide-body twin identified by its smooth nose, large cockpit glazing, serrated nacelle trailing edges, highly flexible wing and horizontal raked tips.", "787-9は複合材ワイドボディ双発機で、滑らかな機首、大型操縦席窓、ナセル後縁のシェブロン、大きくしなる主翼、水平レイクド翼端が特徴です。"), "fact": tr("辨識 787 時，鋸齒短艙與無直立小翼的彎曲主翼比航空公司塗裝更可靠；787-8、-9、-10 仍需再用機身長度與門距區分。", "Chevrons and a flexed wing without upright winglets are stronger 787 cues than livery; separate the -8, -9 and -10 by length and door spacing.", "787の識別には塗装よりシェブロンと直立小翼のない柔軟な主翼が有効で、-8／-9／-10は全長とドア間隔で区別します。"), "bullets": [tr("四對主艙門，機身比 787-8 長、比 787-10 短。", "Four main doors per side; longer than the 787-8 and shorter than the 787-10.", "片側4枚の主ドアで、787-8より長く787-10より短い胴体です。"), tr("引擎短艙後緣有明顯鋸齒狀 chevrons。", "Distinct chevrons surround the nacelle trailing edge.", "エンジンナセル後縁に明確なシェブロンがあります。"), tr("主翼飛行中上彎明顯，翼尖向後延伸而不直立。", "The wing flexes strongly in flight and ends in a swept, non-upright tip.", "飛行中の主翼しなりが大きく、翼端は直立せず後方へ伸びます。")]},
        "cockpit": {"summary": tr("787 駕駛艙保留 Boeing 傳統駕駛盤，但採大型橫向液晶螢幕、雙 HUD 與高度整合的 EICAS／飛行管理顯示，視覺上比 A330ceo 的上一代面板更開闊。", "The 787 retains Boeing yokes but uses large landscape displays, dual HUDs and integrated EICAS/flight-management pages, giving a more open appearance than the earlier A330ceo panel.", "787はBoeing式操縦輪を残しつつ、大型横長画面、デュアルHUD、統合EICAS／飛行管理表示を採用し、A330ceoより開放的に見えます。"), "fact": tr("最直接的 787／A330 座艙差異是駕駛盤對側桿；HUD 與螢幕世代可輔助，但航空公司選配會造成差異。", "The clearest 787/A330 cockpit cue is yoke versus sidestick; HUD and display fit are secondary because options vary.", "最も明確な差は操縦輪とサイドスティックです。HUDや画面構成は運航会社の仕様差があります。"), "bullets": [tr("正副駕駛前方都有駕駛盤與中央操縱柱。", "Both pilots have yokes and control columns.", "両席の正面に操縦輪とコントロールコラムがあります。"), tr("大型橫向顯示器整合 PFD、導航與 EICAS。", "Large landscape displays integrate flight, navigation and EICAS information.", "大型横長画面が飛行、航法、EICAS情報を統合します。"), tr("擋風玻璃前可見 HUD 組件，是常見 787 座艙線索。", "HUD units ahead of the windscreen are a common 787 flight-deck cue.", "風防前のHUD装置は787でよく見られる手掛かりです。")]},
        "windshield": {"summary": tr("787 的駕駛艙窗面積大，兩片正面風擋寬而較直立，外側窗向後下方收尖；窗帶與圓滑機鼻融合，但沒有 A350 式整片黑色面罩。", "The 787 has large, upright forward panes and outer panes tapering aft and down. The glazing blends into the smooth nose without an A350-style full black mask.", "787は大型で直立気味の前面窓と、後下方へ細くなる側面窓を持ちます。滑らかな機首に馴染みますがA350の全面黒マスクはありません。"), "fact": tr("787 與 A330 都有六片主要駕駛艙窗；不要只數窗片，應比較 787 更大的窗面、較圓的機鼻與外側窗收尖角度。", "Both 787 and A330 use six principal cockpit panes; compare the 787's larger glass area, rounder nose and outer-pane taper instead of counting panes.", "787とA330はいずれも主要窓が6枚です。枚数ではなく787の大きな窓面、丸い機首、側窓の絞り方を見ます。"), "bullets": [tr("正面主風擋寬大，中央接縫近乎垂直。", "Wide forward panes meet at a near-vertical centre seam.", "幅広い前面窓がほぼ垂直の中央継ぎ目で接します。"), tr("外側窗後端尖細並向下收束。", "The aft side panes taper to a pointed, downward-swept end.", "外側窓後端は尖り、下向きに絞られます。"), tr("搭配鋸齒短艙與 raked tip 可排除 A330。", "Cross-check chevron nacelles and raked tips to exclude an A330.", "シェブロンナセルとレイクド翼端を合わせてA330を除外します。")]},
        "fuselage": {"summary": tr("787-9 機身大量使用碳纖維複合材料，每側四對主艙門；客艙窗比傳統廣體機更高大，並使用電子變色玻璃而非機械遮光板。", "The composite 787-9 has four main doors per side and unusually large cabin windows with electrochromic dimming instead of mechanical shades.", "複合材の787-9は片側4枚の主ドアを備え、従来機より大型の電子調光式客室窓を採用します。"), "fact": tr("787 與 A330-300 都可能有四對主艙門，因此舷窗尺寸、機鼻、引擎 chevrons 與翼尖比單純數門更重要。", "Both 787 and A330-300 can have four main doors per side, so window size, nose, chevrons and wingtips matter more than door count alone.", "787とA330-300はいずれも片側4ドアのため、窓寸法、機首、シェブロン、翼端を重視します。"), "bullets": [tr("大型客艙窗縱向較高，窗角圓滑。", "Cabin windows are noticeably tall with rounded corners.", "客室窓は縦に大きく、角が丸い形です。"), tr("電子變色窗通常看不到傳統上下拉式遮光板。", "Electrochromic windows normally lack pull-down shades.", "電子調光窓には通常の上下式シェードがありません。"), tr("四對艙門的間距可協助區分 787-8、-9、-10。", "Spacing between the four door pairs helps separate 787 variants.", "4枚のドア間隔が787各型の区別に役立ちます。")]},
        "engine": {"summary": tr("787-9 可使用 General Electric GEnx-1B 或 Rolls-Royce Trent 1000；兩者短艙後緣都有鋸齒狀 chevrons，用來混合噴流並降低噪音。", "The 787-9 can use GEnx-1B or Trent 1000 engines; both installations feature serrated nacelle chevrons that mix the jet flow and reduce noise.", "787-9はGEnx-1BまたはTrent 1000を使用し、どちらも噴流混合と騒音低減のためナセル後縁にシェブロンを備えます。"), "fact": tr("A330ceo 的 CF6、PW4000 或 Trent 700 短艙後緣平滑；看到整圈鋸齒是辨識 787 最可靠的近距特徵之一。", "A330ceo CF6, PW4000 and Trent 700 nacelles have smooth trailing edges; a full chevron ring is one of the strongest close-range 787 cues.", "A330ceoのCF6、PW4000、Trent 700は後縁が滑らかで、全周シェブロンは787の強い近距離識別点です。"), "bullets": [tr("短艙後緣呈規則三角鋸齒。", "Regular triangular chevrons ring the nacelle trailing edge.", "ナセル後縁を規則的な三角シェブロンが囲みます。"), tr("GEnx 與 Trent 1000 外觀不同，但都保留 787 chevrons。", "GEnx and Trent 1000 differ visually, but both retain 787 chevrons.", "GEnxとTrent 1000は外観が異なりますが、双方にシェブロンがあります。"), tr("短艙尺寸大，進氣口接近完整圓形。", "The large inlet is close to circular.", "大型の吸気口はほぼ円形です。")]},
        "wingtip": {"summary": tr("787 沒有直立翼尖小翼；高展弦比主翼在外翼連續上彎後，末端向後拉長形成水平為主的 raked tip。", "The 787 has no upright winglet. Its high-aspect-ratio wing flexes upward and finishes in an aft-stretched, primarily horizontal raked tip.", "787には直立ウイングレットがなく、高アスペクト比翼が上へしなり、後方へ長い水平レイクド翼端になります。"), "fact": tr("A330ceo 的三角形直立翼尖擋板很醒目；即使遠距只看輪廓，『直立三角板』與『後掠尖翼』通常已能快速區分。", "The A330ceo's upright triangular fence is conspicuous; its silhouette alone often separates it from the 787's swept pointed tip.", "A330ceoの直立三角フェンスは目立ち、787の後退した尖り翼端との輪郭差で遠方からも区別できます。"), "bullets": [tr("翼尖沿翼面向後收尖，不形成直立板。", "The tip tapers aft in the wing plane without an upright blade.", "翼面内で後方へ細くなり、直立板を作りません。"), tr("飛行中外翼上彎會讓翼尖看似抬高。", "In-flight wing flex makes the tip appear elevated.", "飛行中のしなりで翼端が高く見えます。"), tr("與 A330 的短小三角翼尖擋板形成強烈對比。", "It contrasts strongly with the A330's small triangular wingtip fence.", "A330の小さな三角翼端フェンスと強く対照します。")]},
        "wing": {"summary": tr("787 的複合材料主翼展弦比高、翼尖細長，飛行中可見顯著彈性上彎；後緣採先進襟翼與擾流板配置。", "The 787's composite high-aspect-ratio wing is slender and visibly flexes upward in flight, with advanced flaps and spoilers along the trailing edge.", "787の複合材高アスペクト比翼は細長く、飛行中に大きく上へしなります。後縁には先進的なフラップとスポイラーがあります。"), "fact": tr("大幅上彎是受控彈性設計，可降低陣風載荷；A330 機翼也會彎曲，但外翼比例與直立翼尖擋板更傳統。", "The large bend is controlled elasticity that manages gust loads. A330 wings also flex, but have a more conventional outer wing and upright fence.", "大きなしなりは突風荷重を抑える意図的な設計です。A330も曲がりますが、外翼と直立フェンスはより従来型です。"), "bullets": [tr("翼根厚、外翼細長，飛行中弧度明顯。", "A thick root transitions to a slender outer wing with obvious in-flight curvature.", "厚い翼根から細い外翼へ続き、飛行中の曲線が明瞭です。"), tr("翼尖為 raked tip，沒有 A330ceo 的直立三角板。", "The raked tip lacks the A330ceo's upright triangular fence.", "レイクド翼端にはA330ceoの直立三角板がありません。"), tr("客艙窗外常可看到翼面大幅上下彈性位移。", "Cabin views often reveal substantial elastic wing movement.", "客室から翼の大きな弾性変位が見られます。")]},
        "vstab": {"summary": tr("787 垂直尾翼以複合材料製成，前緣後掠、頂端向後收尖，根部整流罩平順連接機背。", "The composite 787 fin has a swept leading edge, aft-tapered tip and smooth dorsal fairing into the upper fuselage.", "787の複合材垂直尾翼は後退前縁、後方へ細くなる上端、滑らかなドーサルフェアリングを持ちます。"), "fact": tr("垂尾外形不是區分 787 與 A330 的首要線索；優先看引擎 chevrons、翼尖與客艙窗。", "Fin shape is not the primary 787/A330 cue; prioritize nacelle chevrons, wingtips and cabin windows.", "垂直尾翼は主要識別点ではなく、シェブロン、翼端、客室窓を優先します。"), "bullets": [tr("前緣後掠明顯，頂端圓滑收尖。", "The leading edge is strongly swept and the tip tapers smoothly.", "前縁後退が大きく、上端は滑らかに細くなります。"), tr("根部背鰭與後機身表面過渡平順。", "The dorsal root blends smoothly into the aft fuselage.", "根元は後部胴体へ滑らかにつながります。"), tr("尾翼塗裝只適合辨識航空公司。", "Tail livery identifies the operator, not the type by itself.", "尾翼塗装は運航会社の識別用で、機種単独判定には使えません。")]},
        "hstab": {"summary": tr("787 的水平尾翼低置且後掠，複合材料表面與細長後機身平順融合；外形簡潔、翼尖收束較尖。", "The low-mounted swept composite tailplane blends into the slender aft fuselage and tapers cleanly toward pointed tips.", "787の低位置後退複合材水平尾翼は細い後部胴体へ滑らかにつながり、翼端へきれいに細くなります。"), "fact": tr("水平尾翼單獨難以區分 787 與 A330；側後方觀察時應同時確認翼尖裝置與引擎後緣。", "Tailplane shape alone is weak; from aft-quarter views also check the wingtip device and nacelle trailing edge.", "水平尾翼単独では弱いため、後斜めから翼端装置とナセル後縁も確認します。"), "bullets": [tr("尾翼後掠且翼尖收細。", "The swept surface tapers toward a narrow tip.", "後退面が細い翼端へ収束します。"), tr("根部整流罩順著複合材料後機身延伸。", "The root fairing follows the composite aft fuselage smoothly.", "付け根フェアリングが複合材後部胴体へ滑らかに続きます。"), tr("需以 chevrons 與 raked tip 交叉確認。", "Confirm with chevrons and the raked wingtip.", "シェブロンとレイクド翼端で照合します。")]},
        "gear": {"summary": tr("787-9 每組主起落架為兩軸四輪、前起落架雙輪；主腳轉向架落地時帶有傾角，收入翼身整流區。", "Each 787-9 main bogie has two axles and four tyres. The truck tilts for touchdown and retracts into the wing-body fairing.", "787-9の各主脚は2軸4輪で、接地用の傾きを持ち、翼胴フェアリング内へ格納されます。"), "fact": tr("A330-300 同樣是四輪主腳，因此輪數不能區分兩者；必須改看機鼻、翼尖與引擎短艙後緣。", "The A330-300 also has four-wheel bogies, so wheel count does not separate them; use the nose, wingtips and nacelle trailing edges.", "A330-300も4輪主脚のため輪数では区別できません。機首、翼端、ナセル後縁を確認します。"), "bullets": [tr("每側兩軸四輪，前腳雙輪。", "Two axles and four tyres per main bogie, with twin nose wheels.", "各主脚は2軸4輪、前脚は2輪です。"), tr("主腳轉向架具有明顯接地傾角。", "The main truck shows a pronounced touchdown tilt.", "主脚ボギーに明確な接地傾斜があります。"), tr("輪數與 A330 相同，不能作單一判型依據。", "Wheel count matches the A330 and is not a standalone identifier.", "輪数はA330と同じで、単独の識別点にはなりません。")]},
    },
    "a333": {
        "overview": {"summary": tr("A330-300 是傳統鋁合金廣體雙發客機，外觀重點是 Airbus 經典圓鈍機鼻、較小的駕駛艙窗、平滑引擎短艙後緣，以及翼尖直立的三角形擋板。", "The A330-300 is a conventional aluminium wide-body twin, identified by the classic rounded Airbus nose, smaller cockpit glazing, smooth nacelle trailing edges and upright triangular wingtip fences.", "A330-300は従来型アルミ合金ワイドボディ双発機で、丸いAirbus機首、小さめの操縦席窓、滑らかなナセル後縁、直立三角翼端フェンスが特徴です。"), "fact": tr("A330-300 與 787-9 都常見四對主艙門和四輪主腳；最有效的差異是 A330 的直立翼尖擋板對 787 的 raked tip，以及平滑短艙對鋸齒短艙。", "Both often have four door pairs and four-wheel bogies. The strongest cues are A330 upright fences versus 787 raked tips, and smooth versus chevron nacelles.", "両機とも片側4ドア・4輪主脚が多く、A330の直立フェンス対787のレイクド翼端、滑らかなナセル対シェブロンが最有効です。"), "bullets": [tr("每側四對主艙門，機身比例修長。", "Four main doors per side on a long fuselage.", "長い胴体に片側4枚の主ドアがあります。"), tr("翼尖有小型直立三角形擋板。", "Small upright triangular fences sit at the wingtips.", "翼端に小型の直立三角フェンスがあります。"), tr("引擎短艙後緣平滑，沒有 787 chevrons。", "Nacelle trailing edges are smooth, without 787 chevrons.", "ナセル後縁は滑らかで787のシェブロンがありません。")]},
        "cockpit": {"summary": tr("A330ceo 駕駛艙採 Airbus 側桿、飛行員正前方桌板與六具較傳統的顯示器；中央 ECAM 顯示引擎與系統狀態。", "The A330ceo flight deck uses Airbus sidesticks, tray tables ahead of the pilots and six earlier-generation displays, with central ECAM screens for engines and systems.", "A330ceoの操縦席はAirbus式サイドスティック、正面テーブル、6面の従来型表示器を備え、中央ECAMがエンジンとシステムを表示します。"), "fact": tr("與 787 相比，最直觀差異是沒有駕駛盤；A330neo 可換裝更新顯示器，因此螢幕外觀需視子型與改裝狀態判讀。", "The clearest difference from a 787 is the absence of yokes. A330neo and upgrades may use newer displays, so screen appearance depends on variant and retrofit.", "787との最明確な差は操縦輪がないことです。A330neoや改修機は新型画面を使うため表示器外観は仕様で変わります。"), "bullets": [tr("側桿位於左右側壁，正面沒有駕駛盤。", "Sidesticks sit at the sidewalls, leaving no yoke ahead of either pilot.", "サイドスティックは側壁にあり、正面に操縦輪がありません。"), tr("正副駕駛前方設有可拉出桌板。", "Pull-out tray tables sit in front of both pilots.", "両席正面に引き出し式テーブルがあります。"), tr("中央兩具 ECAM 顯示器呈上下排列。", "Two central ECAM displays are arranged vertically.", "中央2面のECAM表示器は上下配置です。")]},
        "windshield": {"summary": tr("A330 的駕駛艙窗保留經典 Airbus 六片式輪廓：正面主風擋較窄高，外側窗沿圓鈍機鼻向後延伸，窗框彼此分開且沒有 787 那種更大面積的玻璃感。", "The A330 retains the classic six-pane Airbus outline: relatively tall narrow front panes and separate outer panes wrapping around the rounded nose, with less glass area than the 787.", "A330は古典的なAirbus六枚窓で、比較的縦長の前面窓と丸い機首へ回り込む独立側窓を持ち、787ほど大きなガラス面には見えません。"), "fact": tr("A330 與 A340 共用相近機鼻與窗型；引擎數可立即排除四發 A340，再用翼尖與短艙區分 787。", "A330 and A340 share similar nose glazing. Engine count excludes the four-engine A340, then wingtips and nacelles separate a 787.", "A330とA340は似た機首窓を共有します。4発のA340をエンジン数で除外し、翼端とナセルで787と区別します。"), "bullets": [tr("正面主風擋較縱長，中央接縫清楚。", "Forward panes look relatively tall with a clear centre seam.", "前面窓は比較的縦長で中央継ぎ目が明瞭です。"), tr("外側窗框沿機鼻側面形成明顯折線。", "Outer frames form a clear angular line along the nose side.", "外側窓枠が機首側面に明確な折れ線を作ります。"), tr("窗面積通常比 787 小，機鼻下緣更接近傳統 Airbus 曲線。", "The glass area is smaller than the 787's and the lower nose follows a classic Airbus curve.", "窓面積は787より小さく、機首下面は従来のAirbus曲線です。")]},
        "fuselage": {"summary": tr("A330-300 機身外寬約 5.64 m，以鋁合金半硬殼結構為主；每側四對大型主艙門，客艙窗是較小的傳統橢圓窗並配機械遮光板。", "The A330-300's roughly 5.64 m aluminium fuselage has four main doors per side and smaller conventional oval cabin windows with mechanical shades.", "A330-300の胴体幅は約5.64 mで主にアルミ半モノコック構造です。片側4ドアと小型の従来型楕円客室窓を備えます。"), "fact": tr("與 787-9 相比，A330 客艙窗較小且面板接縫更像傳統鋁合金機身；但遠距仍應搭配翼尖與引擎確認。", "Compared with the 787-9, A330 windows are smaller and aluminium panel joints more conventional; at distance confirm with wingtips and engines.", "787-9より客室窓が小さく、アルミ外板の継ぎ目が従来型です。遠方では翼端とエンジンも確認します。"), "bullets": [tr("四對主艙門與 787-9 相同，不能只靠門數。", "Four door pairs match the 787-9, so door count alone is insufficient.", "片側4ドアは787-9と同じで、ドア数だけでは不十分です。"), tr("客艙窗較小，通常有傳統遮光板。", "Cabin windows are smaller and normally use pull-down shades.", "客室窓は小さく、通常は従来型シェードがあります。"), tr("鋁合金外板可見較規則的蒙皮與鉚接分區。", "Aluminium skin shows more conventional panel and fastener zones.", "アルミ外板には従来型のパネル・締結区画が見えます。")]},
        "engine": {"summary": tr("A330-300 可選 GE CF6-80E1、Pratt & Whitney PW4000 或 Rolls-Royce Trent 700；三種短艙外觀不同，但後緣都比 787 的 chevrons 平滑。", "The A330-300 can use GE CF6-80E1, PW4000 or Rolls-Royce Trent 700 engines. Their nacelles differ, but all have smoother trailing edges than 787 chevrons.", "A330-300はCF6-80E1、PW4000、Trent 700を選択でき、外観は異なりますが後縁はいずれも787のシェブロンより滑らかです。"), "fact": tr("不能只靠引擎品牌辨識 A330，因為同一子型有三種選項；最穩定的家族線索是『無鋸齒短艙＋直立翼尖擋板』。", "Engine brand alone cannot identify an A330 because three options exist; the stable family combination is smooth nacelles plus upright tip fences.", "同型に3種のエンジンがあるためブランドだけでは判別できず、滑らかなナセルと直立翼端フェンスの組合せが安定した手掛かりです。"), "bullets": [tr("短艙後緣平滑，沒有一圈三角鋸齒。", "The nacelle trailing edge is smooth without a ring of triangular teeth.", "ナセル後縁は滑らかで三角シェブロンがありません。"), tr("Trent 700、CF6、PW4000 的進氣口與整流罩細節不同。", "Trent 700, CF6 and PW4000 installations differ in inlet and fairing details.", "Trent 700、CF6、PW4000で吸気口とフェアリング詳細が異なります。"), tr("照片為 A330-300 上的 Trent 700。", "The reference photograph shows a Trent 700 on an A330-300.", "参考写真はA330-300のTrent 700です。")]},
        "wingtip": {"summary": tr("A330ceo 翼尖裝有短小、近三角形的直立擋板，向上伸出並略向外傾；與 787 向後延伸的水平 raked tip 很容易區分。", "The A330ceo uses a short upright, roughly triangular wingtip fence, slightly canted outward and easily separated from the 787's aft-extending raked tip.", "A330ceoは短い直立三角翼端フェンスを備え、やや外傾します。787の後方へ伸びるレイクド翼端と容易に区別できます。"), "fact": tr("此特徵適用 A330ceo；A330neo 改用更大型、彎曲的翼尖裝置，不能把兩代 A330 混為一談。", "This cue applies to A330ceo aircraft. The A330neo uses larger curved tips, so do not mix the two generations.", "この特徴はA330ceoに適用されます。A330neoは大型曲線翼端を使うため世代を混同しないでください。"), "bullets": [tr("翼尖有明顯直立高度，外形短而三角。", "The tip has obvious vertical height and a short triangular profile.", "翼端には明確な高さがあり、短い三角形です。"), tr("不像 787 翼尖沿翼面向後拉長。", "It does not stretch aft in the wing plane like a 787 tip.", "787のように翼面内で後方へ長く伸びません。"), tr("同時確認平滑引擎後緣可快速辨識 A330ceo。", "A smooth nacelle trailing edge confirms the A330ceo quickly.", "滑らかなナセル後縁も合わせるとA330ceoを素早く確認できます。")]},
        "wing": {"summary": tr("A330ceo 使用傳統後掠低翼，翼根厚、外翼逐漸收窄，末端接直立三角翼尖擋板；飛行中會彎曲但輪廓通常不如 787 誇張。", "The A330ceo has a conventional swept low wing with a thick root, tapered outer panel and upright triangular fence. It flexes in flight but usually looks less dramatic than the 787.", "A330ceoは厚い翼根から細い外翼へ続く従来型後退低翼で、末端に直立三角フェンスがあります。飛行中もしなりますが787ほど強調されません。"), "fact": tr("A330 與 A340 共用基本機翼家族；看到同類翼尖但有四具引擎時即為 A340，而非 A330。", "A330 and A340 share a basic wing family; four engines beneath a similar wing identify an A340, not an A330.", "A330とA340は基本翼を共有し、同様の翼端で4発ならA340です。"), "bullets": [tr("外翼線條較傳統，末端接短小直立擋板。", "The conventional outer wing ends in a short upright fence.", "従来型外翼の末端に短い直立フェンスがあります。"), tr("後緣配置大型雙縫襟翼與擾流板。", "Large multi-element flaps and spoilers line the trailing edge.", "後縁に大型多要素フラップとスポイラーがあります。"), tr("飛行中上彎程度通常比 787 視覺上較小。", "Visible in-flight flex is usually less pronounced than on a 787.", "飛行中の見かけのしなりは通常787より小さめです。")]},
        "vstab": {"summary": tr("A330-300 垂直尾翼高大、前緣後掠，根部以長背鰭連接機身；整體比例與 A340 家族相近。", "The A330-300 has a tall swept fin with a long dorsal root fairing, sharing broad proportions with the A340 family.", "A330-300は高い後退垂直尾翼と長いドーサル根元を持ち、A340ファミリーと近い比率です。"), "fact": tr("垂尾塗裝只能辨識航空公司；區分 787 時仍應優先看翼尖與引擎後緣。", "Tail livery identifies the airline; wingtips and nacelle trailing edges remain stronger cues against a 787.", "尾翼塗装は航空会社を示すだけで、787との区別には翼端とナセル後縁を優先します。"), "bullets": [tr("高大尾翼前緣後掠，頂端較平直。", "The tall fin has a swept leading edge and a relatively squared tip.", "高い尾翼は後退前縁と比較的平らな上端を持ちます。"), tr("根部背鰭長，與機背過渡明顯。", "A long dorsal fillet creates a clear transition into the upper fuselage.", "長いドーサルフィレットが機背へ明確につながります。"), tr("照片為 A330-300 尾部，可直接觀察垂尾比例。", "The reference shows an A330-300 tail and its fin proportions directly.", "参考写真はA330-300尾部で垂直尾翼比率を直接確認できます。")]},
        "hstab": {"summary": tr("A330／A340 家族的水平尾翼低置、後掠且翼根厚，後緣升降舵分段清楚；外形比 787 的複合材料尾翼更接近傳統 Airbus 設計。", "The A330/A340 family uses a low-mounted swept tailplane with a thick root and clearly segmented elevators, following a more conventional Airbus form than the 787.", "A330／A340ファミリーの水平尾翼は低位置・後退・厚い翼根を持ち、分割昇降舵が明瞭で、787より従来型Airbus形状です。"), "fact": tr("後方實機照片可觀察左右水平尾翼的安裝高度與後掠角；但水平尾翼仍只是輔助線索，不能單獨定型。", "The rear aircraft view shows tailplane height and sweep, but tailplane shape remains only a supporting identification cue.", "実機後方写真では水平尾翼の取付高さと後退角を確認できますが、形状は補助的手掛かりに限られます。"), "bullets": [tr("後掠平面形由厚翼根向外逐漸收尖。", "The swept planform tapers from a thick root toward the tip.", "厚い翼根から翼端へ細くなる後退平面形です。"), tr("升降舵沿後緣分段配置。", "Segmented elevators run along the trailing edge.", "後縁に分割昇降舵があります。"), tr("應搭配直立翼尖擋板與平滑短艙確認 A330。", "Confirm an A330 using upright tip fences and smooth nacelles.", "直立翼端フェンスと滑らかなナセルでA330を確認します。")]},
        "gear": {"summary": tr("A330-300 每組主起落架為兩軸四輪，前起落架雙輪；主腳向內收入翼身整流區，配置與 787-9 的輪數相同。", "Each A330-300 main bogie has two axles and four tyres, retracting inward into the wing-body fairing; its wheel count matches the 787-9.", "A330-300の各主脚は2軸4輪で翼胴フェアリングへ内側格納され、輪数は787-9と同じです。"), "fact": tr("四輪主腳無法區分 A330 與 787；照片應用來理解結構，判型仍回到翼尖、窗型與引擎後緣。", "Four-wheel bogies do not separate A330 and 787. Use the photograph for structure, then identify by wingtips, glazing and nacelle trailing edges.", "4輪主脚ではA330と787を区別できません。構造理解に使い、翼端、窓、ナセル後縁で判別します。"), "bullets": [tr("每側兩軸四輪，前腳雙輪。", "Two axles and four tyres per main bogie, with twin nose wheels.", "各主脚は2軸4輪、前脚は2輪です。"), tr("主腳柱與轉向架適合廣體機高重量起降。", "The strut and bogie support wide-body operating weights.", "主脚柱とボギーがワイドボディ機の重量を支えます。"), tr("輪數與 787 相同，不能單獨作辨識點。", "Wheel count matches the 787 and cannot identify the type alone.", "輪数は787と同じで単独識別には使えません。")]},
    },
    "b748": {
        "overview": identify(
            ("747-8 的最強外型線索是機鼻後方隆起的短上層甲板、四具引擎與細長機身。客運型 747-8I 長約 76.3 m，機翼末端向後延伸而不直立。", "The 747-8 is defined by its short upper-deck hump behind the nose, four engines and long slender fuselage. The 747-8I is about 76.3 m long and uses aft-extending tips rather than upright winglets.", "747-8は機首後方の短い上部デッキの隆起、4発エンジン、細長い胴体が特徴です。747-8Iは全長約76.3 mで、翼端は直立せず後方へ伸びます。"),
            ("遠距辨識時先找『駝峰』；A380 雖也是四發巨型客機，但其上層甲板延伸至整個機身，輪廓完全不同。", "At distance, find the hump first. The A380 is also a giant quadjet, but its upper deck runs the full fuselage length.", "遠方ではまず「こぶ」を探します。A380も巨大4発機ですが、上部デッキは胴体全長に続きます。"),
            [("上層甲板只集中在前機身，形成經典 747 隆起。", "The upper deck is concentrated over the forward fuselage, forming the classic 747 hump.", "上部デッキは前部胴体に集中し、747特有の隆起を作ります。"), ("四具 GEnx-2B 引擎的短艙後緣有鋸齒。", "All four GEnx-2B nacelles have chevron trailing edges.", "4基のGEnx-2Bナセル後縁にシェブロンがあります。"), ("翼尖沿翼面向後拉長，不是 A380 的上下翼尖擋板。", "The tips stretch aft in the wing plane, unlike the A380's upper/lower fences.", "翼端は翼面内で後方へ伸び、A380の上下フェンスとは異なります。")],
        ),
        "cockpit": identify(
            ("747-8 駕駛艙保留 Boeing 傳統駕駛盤與中央操縱柱，並以大型彩色顯示器呈現 PFD、導航與 EICAS 資訊；油門座控制四具引擎。", "The 747-8 flight deck retains Boeing yokes and control columns, with large colour displays for flight, navigation and EICAS information and a four-engine throttle quadrant.", "747-8の操縦席はBoeing式操縦輪とコントロールコラムを残し、大型カラー画面に飛行・航法・EICAS情報を表示し、4発用スロットルを備えます。"),
            ("與 A380 最快的座艙差異是 747-8 有駕駛盤；A380 使用左右側桿，飛行員正前方沒有操縱輪。", "The quickest cockpit distinction is the yoke: the 747-8 has one, while the A380 uses sidesticks.", "最も速い違いは操縦輪です。747-8には操縦輪があり、A380はサイドスティックを使います。"),
            [("兩席前方皆有大型駕駛盤。", "Large yokes sit directly ahead of both pilots.", "両席の正面に大型操縦輪があります。"), ("中央油門座有四支引擎推力桿。", "Four thrust levers occupy the centre pedestal.", "中央ペデスタルに4本の推力レバーがあります。"), ("座艙位置在隆起上層甲板前端，視線高度明顯較高。", "The cockpit sits at the front of the raised upper deck, giving a notably high eye position.", "操縦席は隆起した上部デッキ前端にあり、視点が非常に高い位置です。")],
        ),
        "windshield": identify(
            ("747 的駕駛艙窗高置於上層甲板，正面兩片主風擋寬大，外側另有狹長窗片沿隆起機鼻向後包覆；整組窗帶與下方主甲板距離很大。", "The 747 cockpit glazing sits high on the upper deck. Two broad front panes are flanked by narrow side panes wrapping around the raised nose, far above the main deck.", "747の操縦席窓は上部デッキの高い位置にあり、幅広い前面2枚と細長い側面窓が隆起した機首を囲み、主デッキから大きく離れています。"),
            ("側窗照片為 747 家族實機；747-8 延續相同的高置六片式窗帶，判讀時應同時確認前機身駝峰。", "The side-window photograph is a 747-family reference. The 747-8 retains the same high-set six-pane arrangement; confirm it with the hump.", "側面写真は747ファミリーの参考です。747-8も同じ高位置の6枚窓を継承するため、こぶと合わせて確認します。"),
            [("正面主風擋下緣形成明顯向下折角。", "The lower edges of the main panes form pronounced downward angles.", "主風防下端には明瞭な下向きの折れ角があります。"), ("外側窗片窄而近垂直，與 A380 較平順的窗帶不同。", "Narrow, near-vertical outer panes differ from the smoother A380 belt.", "細く直立気味の外側窓はA380の滑らかな窓帯と異なります。"), ("窗戶位於主甲板舷窗列上方很高的位置。", "The cockpit windows sit conspicuously above the main-deck cabin-window row.", "操縦席窓は主デッキ客室窓列より著しく高い位置です。")],
        ),
        "fuselage": identify(
            ("747-8I 的上層甲板僅覆蓋前機身，主甲板則貫穿全長；側面可見上下兩排舷窗只在前段重疊，之後恢復單排。", "On the 747-8I, the upper deck covers only the forward fuselage. Two window rows overlap near the front, then the aircraft continues with a single main-deck row.", "747-8Iの上部デッキは前部だけを覆い、前方では上下2列の窓が重なりますが、その後は主デッキ1列になります。"),
            ("這個『局部雙層』輪廓是區分 A380 全長雙層機身最可靠的特徵；貨運型 747-8F 的上層甲板更短。", "This partial double-deck profile is the most reliable contrast with the full-length double-deck A380. The 747-8F hump is shorter still.", "この部分的二階建て輪郭は全長二階建てA380との最も確実な違いです。747-8Fのこぶはさらに短いです。"),
            [("前機身有上下兩排舷窗，後機身只剩主甲板窗列。", "Two window rows appear forward, but only the main-deck row continues aft.", "前部は上下2列、後部は主デッキ1列だけです。"), ("客運型上層甲板隆起比 747-400 更長。", "The passenger upper-deck hump is longer than on the 747-400.", "旅客型の上部デッキ隆起は747-400より長くなっています。"), ("機身較 A380 窄，外觀更修長。", "The fuselage is narrower than the A380's and looks more slender.", "胴体はA380より細く、より長細く見えます。")],
        ),
        "engine": identify(
            ("747-8 固定使用四具 General Electric GEnx-2B67 高旁通比渦扇；短艙尾緣與核心整流罩具有鋸齒狀 chevrons，是與舊型 747 及 A380 的強辨識差異。", "The 747-8 exclusively uses four GEnx-2B67 high-bypass turbofans. Chevron nacelle and core-fairing edges distinguish it from older 747s and the A380.", "747-8は4基のGEnx-2B67高バイパス比ターボファンのみを使用し、ナセルとコアカウル後縁のシェブロンが旧型747やA380との強い違いです。"),
            ("鋸齒可讓冷熱氣流較平順混合以降低噴流噪音；它不是單純裝飾，也不是 A380 引擎的標準外型。", "The chevrons promote smoother hot/cold stream mixing to reduce jet noise; they are functional and not standard on A380 engines.", "シェブロンは冷熱流を滑らかに混合してジェット騒音を減らす機能部品で、A380エンジンの標準形状ではありません。"),
            [("四具引擎全部為 GEnx-2B 系列。", "All four engines are from the GEnx-2B family.", "4基すべてGEnx-2B系列です。"), ("短艙後緣可見一圈明顯三角鋸齒。", "A clear ring of triangular chevrons marks the nacelle trailing edge.", "ナセル後縁に三角形のシェブロンが並びます。"), ("A380 可用 Trent 900 或 GP7200，短艙後緣較平滑。", "The A380 uses Trent 900 or GP7200 engines with smoother nacelle edges.", "A380はTrent 900またはGP7200を使い、ナセル後縁はより滑らかです。")],
        ),
        "wingtip": identify(
            ("747-8 採用加長、向後收尖的 raked wingtip，翼尖幾乎維持在主翼平面內，沒有 747-400 常見的直立小翼。", "The 747-8 uses an extended, aft-tapering raked wingtip that stays largely in the wing plane, with no 747-400-style upright winglet.", "747-8は後方へ細長く伸びるレイクド翼端を採用し、翼面内にほぼ収まり、747-400型の直立ウイングレットはありません。"),
            ("看到 747 駝峰卻沒有直立小翼、而是長而水平的翼尖，通常就是 747-8；A380 則有上下方向的翼尖擋板。", "A 747 hump combined with long horizontal tips rather than upright winglets strongly indicates a 747-8; the A380 uses upper/lower fences.", "747のこぶと、直立小翼ではなく長い水平翼端の組合せは747-8の強い手掛かりです。A380は上下フェンスです。"),
            [("翼尖沿後掠方向平順拉長。", "The tip extends smoothly aft with the sweep.", "翼端は後退方向へ滑らかに伸びます。"), ("沒有明顯向上的垂直小翼。", "There is no prominent upright winglet.", "目立つ直立ウイングレットはありません。"), ("與 GEnx 鋸齒短艙一起使用可快速排除 747-400。", "Pair it with GEnx chevrons to exclude the 747-400 quickly.", "GEnxシェブロンと組み合わせれば747-400を素早く除外できます。")],
        ),
        "wing": identify(
            ("747-8 使用重新設計的大型後掠翼，翼展約 68.4 m；翼根厚、外翼長而逐漸收尖，飛行時會上彎並連到 raked tip。", "The 747-8 has a redesigned swept wing spanning about 68.4 m, with a thick root, long tapered outer panel, visible flight flex and raked tips.", "747-8は翼幅約68.4 mの再設計後退翼を持ち、厚い翼根、長く細くなる外翼、飛行時のたわみ、レイクド翼端が特徴です。"),
            ("A380 翼展約 79.75 m、翼弦與翼面積都更巨大；即使兩者都是四發，A380 的機翼視覺尺度仍更寬厚。", "The A380 spans about 79.75 m with much greater chord and area, so its wing looks broader even though both aircraft have four engines.", "A380は翼幅約79.75 mで翼弦・面積も大きく、同じ4発でも主翼がより幅広く見えます。"),
            [("四具引擎平均掛在左右主翼下方。", "Four engines are distributed beneath the two wings.", "4基のエンジンが左右主翼下に配置されます。"), ("外翼末端沿翼面向後收尖。", "The outer wing tapers aft into the raked tip.", "外翼は後方へ細くなりレイクド翼端へ続きます。"), ("翼展小於 A380，但機身更長。", "Its span is smaller than the A380's even though the fuselage is longer.", "翼幅はA380より小さい一方、胴体はより長いです。")],
        ),
        "vstab": identify(
            ("747-8 的垂直尾翼高而後掠，從較窄的後機身上方升起；與 A380 寬厚、面積巨大的垂尾相比，外形更修長。", "The 747-8 has a tall swept fin rising from a relatively narrow aft fuselage. It looks slimmer than the A380's very broad, high-area fin.", "747-8の垂直尾翼は細い後部胴体から立ち上がる高い後退形で、A380の幅広く大面積な尾翼より細長く見えます。"),
            ("垂尾塗裝主要辨識航空公司；判別機型仍需搭配駝峰、翼尖與引擎。", "Tail paint identifies the airline; type identification still depends on the hump, tips and engines.", "尾翼塗装は航空会社の手掛かりであり、機種はこぶ、翼端、エンジンも合わせて判断します。"),
            [("前緣後掠，頂端向後收尖。", "The leading edge is swept and the tip tapers aft.", "前縁は後退し、上端は後方へ細くなります。"), ("根部與狹長後機身平順連接。", "The root blends into the slender aft fuselage.", "根元は細長い後部胴体へ滑らかにつながります。"), ("比例不像 A380 垂尾那樣寬厚巨大。", "Its proportions are not as broad and massive as the A380 fin.", "A380の尾翼ほど幅広く巨大ではありません。")],
        ),
        "hstab": identify(
            ("747-8 的水平尾翼低置於機尾、後掠且向外收尖；從斜後方或空中照片可見它與狹長後機身形成較輕巧的尾部輪廓。", "The 747-8 uses low-mounted swept tailplanes that taper outward, producing a comparatively slender tail silhouette around the narrow aft fuselage.", "747-8の水平尾翼は低位置・後退・外方へ細くなる形で、細い後部胴体と比較的軽快な尾部輪郭を作ります。"),
            ("水平尾翼本身不是最強辨識點；應以 747 駝峰與 GEnx 鋸齒短艙先定型，再用尾翼比例確認。", "The tailplane alone is weak evidence. Identify the hump and GEnx chevrons first, then use tail proportions as confirmation.", "水平尾翼単独の識別力は低く、まずこぶとGEnxシェブロンで判別し、尾翼比率で確認します。"),
            [("安裝位置低於垂尾根部。", "The tailplanes mount low beneath the fin root.", "水平尾翼は垂直尾翼根元より低く付きます。"), ("平面形後掠並向翼尖明顯收窄。", "The swept planform narrows strongly toward the tips.", "後退平面形は翼端へ大きく細くなります。"), ("A380 的水平尾翼面積與根部厚度視覺上更大。", "The A380 tailplanes look larger in area and root thickness.", "A380の水平尾翼は面積と翼根厚がより大きく見えます。")],
        ),
        "gear": identify(
            ("747-8 有四組四輪主起落架轉向架：左右翼下各一組、機身下各一組，加上雙輪前腳，全機共 18 個輪胎。", "The 747-8 has four four-wheel main bogies—one wing and one body bogie per side—plus twin nose wheels, for 18 tyres total.", "747-8は左右それぞれ翼脚1組と胴体脚1組の計4組・各4輪主脚に前脚2輪を加え、合計18輪です。"),
            ("A380 有 22 個輪胎：兩組四輪翼腳加兩組六輪機身腳。只要看清機身腳每組是四輪還是六輪，就能快速區分。", "The A380 has 22 tyres: two four-wheel wing bogies and two six-wheel body bogies. Counting body-bogie wheels separates them quickly.", "A380は翼脚2組各4輪、胴体脚2組各6輪で計22輪です。胴体脚が4輪か6輪かを見れば素早く区別できます。"),
            [("四組主腳各有四輪。", "All four main bogies carry four tyres each.", "4組の主脚はすべて各4輪です。"), ("機身中央兩組主腳可轉向以減少轉彎輪胎側滑。", "The body bogies steer to reduce tyre scrub in turns.", "胴体脚は旋回時のタイヤ横滑りを減らすため操向します。"), ("總輪數 18，少於 A380 的 22。", "Total tyre count is 18, versus 22 on the A380.", "総輪数は18輪で、A380の22輪より少ないです。")],
        ),
    },
    "a380": {
        "overview": identify(
            ("A380 是全長雙層、四發、超大型廣體客機。機身粗短而高，兩層客艙窗列幾乎從機鼻延伸到機尾，機翼與垂尾尺度都非常巨大。", "The A380 is a full-length double-deck, four-engine very-large wide-body. Its deep fuselage carries two cabin-window rows almost nose to tail, with an enormous wing and fin.", "A380は全長二階建て・4発の超大型ワイドボディ機です。太く高い胴体に2列の客室窓がほぼ機首から機尾まで続き、主翼と尾翼も巨大です。"),
            ("與 747-8 相比，不要只數四具引擎；A380 沒有前段駝峰，而是整個機身都維持雙層高度。", "Do not rely only on four engines. Unlike the 747-8 hump, the A380 maintains double-deck height along almost the entire fuselage.", "4発だけで判断せず、747-8の前部こぶと違い、A380はほぼ胴体全長で二階建て高さを維持します。"),
            [("上下兩排客艙窗一路延伸到後機身。", "Two cabin-window rows continue far into the aft fuselage.", "上下2列の客室窓が後部胴体まで続きます。"), ("機鼻圓鈍、機身截面非常高大。", "The nose is rounded and the fuselage cross-section is exceptionally deep.", "機首は丸く、胴体断面は非常に高大です。"), ("翼展約 79.75 m，明顯大於 747-8。", "The roughly 79.75 m span is substantially greater than the 747-8's.", "翼幅は約79.75 mで747-8を大きく上回ります。")],
        ),
        "cockpit": identify(
            ("A380 駕駛艙採 Airbus 側桿、正面桌板、大型整合顯示器與中央 ECAM；兩側另有可操作電子飛行包與系統介面的鍵盤／游標設備。", "The A380 flight deck uses Airbus sidesticks, forward tray tables, large integrated displays and central ECAM, with keyboard/cursor interfaces for electronic flight and system functions.", "A380の操縦席はAirbus式サイドスティック、正面テーブル、大型統合表示器、中央ECAMを備え、電子飛行・システム操作用キーボード／カーソル装置もあります。"),
            ("與 747-8 相比，飛行員正前方沒有駕駛盤；四具引擎仍由中央四支推力桿控制。", "Unlike the 747-8, there are no yokes ahead of the pilots, although four central thrust levers still command the four engines.", "747-8と違い正面に操縦輪はありませんが、4発は中央の4本の推力レバーで操作します。"),
            [("左右側桿位於座椅外側。", "Sidesticks sit outboard of the pilot seats.", "サイドスティックは各席外側にあります。"), ("正面空間可配置桌板與大型顯示器。", "The clear forward area accommodates tray tables and large displays.", "正面空間にテーブルと大型表示器を配置できます。"), ("中央推力桿共有四支，對應四具引擎。", "Four centre thrust levers correspond to the four engines.", "中央の4本の推力レバーが4基のエンジンに対応します。")],
        ),
        "windshield": identify(
            ("A380 駕駛艙窗位於圓鈍機鼻中段，正面主風擋較寬平，外側窗沿機鼻平順向後收窄；窗帶下方緊接下層客艙，而不是位於獨立駝峰頂端。", "The A380 glazing sits midway up the rounded nose. Broad, shallow front panes taper smoothly into side panes, above the lower-deck cabin rather than atop a separate hump.", "A380の操縦席窓は丸い機首中段にあり、幅広く浅い前面窓から側面窓へ滑らかに細くなり、独立したこぶの頂上ではありません。"),
            ("正面看時 A380 窗帶像貼在巨大圓鼻中央；747 的窗戶則更高、更有折角，且下方還有明顯主甲板距離。", "Head-on, the A380 belt sits across the centre of a huge round nose. The 747 belt is higher and more angular, with a larger gap to the main deck.", "正面ではA380の窓帯が巨大な丸い機首中央に付きます。747はより高く角張り、主デッキとの間隔も大きいです。"),
            [("主風擋外形較扁寬，中央接縫短。", "The main panes are broad and shallow with a short centre seam.", "主風防は幅広く浅く、中央継ぎ目は短めです。"), ("外側窗與圓鼻曲面銜接較平順。", "Outer panes blend smoothly around the round nose.", "外側窓は丸い機首曲面へ滑らかにつながります。"), ("窗戶高度低於最上層客艙窗列，不形成 747 式駝峰。", "The cockpit is below the uppermost cabin row and creates no 747-style hump.", "操縦席は最上部客室窓列より低く、747型のこぶを作りません。")],
        ),
        "fuselage": identify(
            ("A380 的主甲板與上層甲板都幾乎貫穿全機，側面可見兩排連續舷窗與上下層大型艙門；機身外寬約 7.14 m，垂直截面尤其高。", "Both A380 decks run almost the full aircraft length, producing two continuous window rows and doors on both levels. The fuselage is about 7.14 m wide and exceptionally deep.", "A380は両デッキがほぼ全長に続き、上下2列の連続窓と両階の大型ドアを備えます。胴体幅は約7.14 mで高さも非常に大きいです。"),
            ("747-8 只有前段是雙層；A380 的後段仍保留上下兩排窗，這是側面辨識最可靠差異。", "Only the front of a 747-8 is double-deck. The A380 retains two window rows aft, making this the most reliable side-view distinction.", "747-8は前部だけ二階建てですが、A380は後部まで2列窓が続くため、側面で最も確実な違いです。"),
            [("上層甲板舷窗延伸至機翼後方與機尾附近。", "Upper-deck windows continue behind the wing toward the tail.", "上部デッキ窓は主翼後方から機尾近くまで続きます。"), ("上、下層都有對應的大型逃生艙門。", "Large emergency doors serve both upper and lower decks.", "上下両デッキに大型非常口があります。"), ("機身截面比 747 更寬、更高、更圓厚。", "The body is wider, taller and fuller than the 747's.", "胴体は747より幅広く、高く、丸みがあります。")],
        ),
        "engine": identify(
            ("A380 可選四具 Rolls-Royce Trent 900 或 Engine Alliance GP7200 高旁通比渦扇；兩者短艙皆巨大，但後緣整體較平滑，沒有 747-8 GEnx 的完整鋸齒圈。", "The A380 uses four Rolls-Royce Trent 900 or Engine Alliance GP7200 turbofans. Both have huge nacelles with generally smoother trailing edges than 747-8 GEnx chevrons.", "A380は4基のTrent 900またはGP7200を使用します。巨大なナセルですが、747-8 GEnxのような一周シェブロンはなく後縁は概ね滑らかです。"),
            ("部分 A380 外側引擎沒有反推裝置；只有兩具內側引擎提供反推，以減輕重量並避免外側引擎在跑道邊緣吸入異物。", "Only the two inboard A380 engines have thrust reversers, reducing weight and limiting debris ingestion near runway edges.", "A380は内側2基だけに逆推力装置を備え、重量を減らし、滑走路端に近い外側エンジンの異物吸入を抑えます。"),
            [("可搭載 Trent 900 或 GP7200，不是單一引擎型。", "It may carry Trent 900s or GP7200s rather than one exclusive engine type.", "Trent 900またはGP7200を搭載します。"), ("只有內側兩具引擎具反推。", "Only the two inboard engines provide reverse thrust.", "逆推力は内側2基だけです。"), ("短艙後緣比 747-8 的 GEnx chevrons 平滑。", "Nacelle trailing edges are smoother than 747-8 GEnx chevrons.", "ナセル後縁は747-8 GEnxシェブロンより滑らかです。")],
        ),
        "wingtip": identify(
            ("A380 翼尖使用小型上下翼尖擋板：上方翼片較高、下方翼片較短，形成明顯垂直輪廓；它不是 747-8 那種水平向後延伸的 raked tip。", "The A380 uses small upper-and-lower wingtip fences, with a taller upper blade and shorter lower blade, unlike the 747-8's horizontal raked tip.", "A380は上側が高く下側が短い上下翼端フェンスを使い、747-8の水平レイクド翼端とは異なります。"),
            ("A380plus 曾展示高大新翼梢概念，但量產營運中的標準 A380 仍以小型上下擋板為主。", "A taller A380plus winglet was demonstrated, but standard production A380s in service retain the small upper/lower fences.", "A380plusでは大型翼端案が示されましたが、量産運航A380は標準の小型上下フェンスです。"),
            [("翼尖同時向上與向下伸出。", "The tip projects both above and below the wing.", "翼端は上方と下方の両方へ伸びます。"), ("整體尺寸小於多數現代大型 Sharklet。", "The device is smaller than most modern large Sharklets.", "多くの現代大型シャークレットより小型です。"), ("與全長雙層機身一起，是 A380 強辨識組合。", "Together with the full double deck, it is a strong A380 cue.", "全長二階建て胴体と組み合わせると強いA380識別点です。")],
        ),
        "wing": identify(
            ("A380 的大型後掠翼展約 79.75 m，翼根厚且翼弦極寬，以承載最大起飛重量超過 500 噸的機體；四具引擎分布在寬大的主翼下。", "The A380's huge swept wing spans about 79.75 m, with a thick root and very broad chord sized for an aircraft exceeding 500 tonnes at maximum takeoff weight.", "A380の巨大後退翼は翼幅約79.75 m、厚い翼根と非常に広い翼弦を持ち、最大離陸重量500トン超の機体を支えます。"),
            ("A380 翼尖受到 80 m 機場設施限制而控制在約 79.75 m；747-8 翼展較小、外翼更修長並採 raked tip。", "The A380 span was kept near 79.75 m to fit the 80 m airport box. The 747-8 is narrower and uses longer-looking raked outer tips.", "A380は空港の80 mボックスに合わせ翼幅約79.75 mに抑えられ、747-8はより狭く細長いレイクド外翼です。"),
            [("翼根與翼弦非常寬厚。", "The root and chord are exceptionally broad and thick.", "翼根と翼弦が非常に幅広く厚いです。"), ("四具引擎間距大，外側引擎靠近跑道邊緣。", "The four engines are widely spaced, with outer engines near runway edges.", "4基の間隔が広く、外側エンジンは滑走路端に近づきます。"), ("翼尖接小型上下擋板，不是水平 raked tip。", "The tip ends in upper/lower fences rather than a horizontal raked extension.", "翼端は水平レイクドではなく上下フェンスです。")],
        ),
        "vstab": identify(
            ("A380 的垂直尾翼非常高大且面積寬廣，用來穩定巨大的高側面積機身；根部厚、方向舵分段，外觀比 747-8 更寬厚。", "The A380 fin is exceptionally tall and broad to stabilize its huge side area. It has a thick root and segmented rudder and looks broader than the 747-8 fin.", "A380の垂直尾翼は巨大な側面積を安定させるため非常に高く幅広く、厚い根元と分割方向舵を持ち、747-8より幅広く見えます。"),
            ("A380 垂尾高度接近八層樓，地面近看非常誇張；但遠距仍要以全長雙層機身與翼尖擋板確認。", "The A380 tail is extraordinarily tall at ground level, but at distance confirm it with the full double deck and wingtip fences.", "A380の尾翼は地上で非常に巨大ですが、遠方では全長二階建て胴体と翼端フェンスで確認します。"),
            [("垂尾根部寬厚，與高大後機身連接。", "A broad thick root blends into the deep aft fuselage.", "幅広く厚い根元が高い後部胴体へつながります。"), ("方向舵為分段設計。", "The rudder is divided into segments.", "方向舵は分割構造です。"), ("整體面積與寬度大於 747-8 垂尾。", "Overall area and breadth exceed those of the 747-8 fin.", "全体面積と幅は747-8垂直尾翼を上回ります。")],
        ),
        "hstab": identify(
            ("A380 的水平尾翼低置於後機身，翼根厚、面積巨大且後掠；從側後方可見它在寬厚機尾兩側形成很大的水平面。", "The A380's low-mounted tailplanes are thick-rooted, very large and swept, forming broad horizontal surfaces around the deep aft fuselage.", "A380の水平尾翼は後部胴体の低い位置に付き、厚い翼根、大面積、後退形を持ち、高い機尾の両側に広い水平面を作ります。"),
            ("A380 尾翼照片可同時看出垂尾、水平尾翼與雙層後機身比例；747-8 的後機身較窄、尾翼輪廓更修長。", "The A380 tail view shows the fin, tailplane and double-deck aft-body proportions together; the 747-8 aft fuselage is slimmer.", "A380尾部写真では垂直尾翼、水平尾翼、二階建て後部胴体の比率を同時に確認でき、747-8後部はより細身です。"),
            [("水平尾翼根部厚、面積大。", "The tailplane has a thick root and large area.", "水平尾翼は厚い翼根と大面積を持ちます。"), ("安裝位置低於巨大垂尾根部。", "It mounts low beneath the enormous fin root.", "巨大な垂直尾翼根元より低く取り付きます。"), ("與高大的全長雙層後機身形成寬厚尾部。", "It creates a broad tail around the deep full-double-deck aft body.", "高い全長二階建て後部胴体と幅広い尾部を作ります。")],
        ),
        "gear": identify(
            ("A380 有兩組四輪翼下主腳與兩組六輪機身主腳，再加雙輪前腳，共 22 個輪胎；六輪機身腳是與 747-8 四輪機身腳的直接差異。", "The A380 has two four-wheel wing bogies, two six-wheel body bogies and twin nose wheels, totaling 22 tyres. Six-wheel body bogies directly distinguish it from the 747-8.", "A380は翼脚2組各4輪、胴体脚2組各6輪、前脚2輪で計22輪です。胴体脚6輪が747-8の4輪胴体脚との直接的な違いです。"),
            ("四組主腳共同分散巨大重量；機身主腳可轉向，讓這架超大型客機在滑行轉彎時降低輪胎側滑。", "Four main bogies distribute the immense weight, and steerable body bogies reduce tyre scrub during taxi turns.", "4組の主脚が巨大な重量を分散し、操向可能な胴体脚が地上旋回時のタイヤ横滑りを減らします。"),
            [("每側翼下主腳為四輪。", "Each wing bogie carries four tyres.", "各翼脚は4輪です。"), ("每側機身主腳為三軸六輪。", "Each body bogie has three axles and six tyres.", "各胴体脚は3軸6輪です。"), ("總輪數 22，多於 747-8 的 18。", "Total tyre count is 22, versus 18 on the 747-8.", "総輪数は22輪で、747-8の18輪より多いです。")],
        ),
    },
    "b752": {
        "overview": identify(
            ("757-200 是修長、離地較高的單走道雙發客機；機鼻尖長、駕駛艙窗較方正，主翼與尾翼相對機身都顯得寬大。", "The 757-200 is a long, high-sitting narrow-body twin with a pointed nose, fairly rectangular cockpit glazing and large wings and tail surfaces for its fuselage width.", "757-200は細長く地上高の高い単通路双発機で、尖った機首、比較的四角い操縦席窓、胴体幅に対して大きな主翼と尾翼が特徴です。"),
            ("757 與 A321 長度接近，但 757 的起落架更高、機鼻更尖、主翼與引擎更大；三項一起看比只看機身長度可靠。", "The 757 and A321 are similar in length, but the 757 stands taller and has a sharper nose, larger wing and larger engines. Use those cues together.", "757とA321は全長が近いものの、757は脚が高く、機首が鋭く、主翼とエンジンが大きいため、複数の特徴を組み合わせます。"),
            [("機身外寬約 3.76 m，外觀細長。", "The roughly 3.76 m fuselage looks notably slender.", "胴体外径は約3.76 mで細長く見えます。"), ("機腹與引擎離地高度明顯高於 737 與 A321。", "The belly and engines sit visibly higher than those of a 737 or A321.", "胴体下面とエンジンの地上高は737やA321より明らかに高めです。"), ("原廠可無小翼，後期常見大型改裝翼梢小翼。", "Original aircraft may have plain tips; many later received large retrofit winglets.", "原型は翼端装置なしの場合があり、後年に大型ウイングレットを改修装着した機体も多くあります。")],
        ),
        "cockpit": identify(
            ("757 駕駛艙採傳統 Boeing 駕駛盤與中央操縱柱，早期機多為六具 CRT 顯示器；布局與 767 高度共通。", "The 757 flight deck uses Boeing yokes and control columns with six CRT-era displays on many aircraft, and shares a strongly common layout with the 767.", "757の操縦席はBoeing式操縦輪とコントロールコラムを使い、多くは6面のCRT世代表示器を備え、767と高い共通性があります。"),
            ("757 與 767 具有共同型別資格；辨識 A321 時最直觀差異是正前方駕駛盤，而 Airbus 使用側桿與桌板。", "The 757 and 767 share a type rating. Against an A321, the clearest cue is the yoke directly ahead of each pilot versus Airbus sidesticks and tray tables.", "757と767は共通型式資格を持ちます。A321との最明確な差は、正面の操縦輪に対しAirbusはサイドスティックとテーブルを使う点です。"),
            [("正副駕駛前方都有駕駛盤。", "A yoke is positioned in front of each pilot.", "両席の正面に操縦輪があります。"), ("中央顯示與實體控制布局屬 1980 年代 Boeing 世代。", "The central displays and physical-control layout reflect 1980s Boeing design.", "中央表示器と物理操作部は1980年代Boeing世代の設計です。"), ("推力桿位於中央操縱台，沒有 Airbus 式側桿。", "Thrust levers sit on the centre pedestal; there are no Airbus-style sidesticks.", "推力レバーは中央ペデスタルにあり、Airbus式サイドスティックはありません。")],
        ),
        "windshield": identify(
            ("757 的正面主風擋較寬、接近矩形，中央接縫近乎垂直；外側窗大而方，配合尖長且略下垂的機鼻形成獨特表情。", "The 757 has broad, nearly rectangular forward panes with a near-vertical centre seam and large square side panes above a long pointed, slightly drooped nose.", "757は幅広くほぼ長方形の前面窓、垂直に近い中央継ぎ目、大きな四角い側面窓を持ち、長く少し下がった機首と組み合わさります。"),
            ("757 與 767 的窗型很接近；區分時再看機身寬度、起落架輪組與整體比例，不能只靠風擋。", "757 and 767 glazing is very similar. Use fuselage width, landing-gear bogies and overall proportions as additional checks.", "757と767の窓形状は非常に似るため、胴体幅、脚ボギー、全体比率も確認します。"),
            [("兩片主風擋寬而平，中央接縫直。", "The two main panes are broad and flat with a straight centre seam.", "2枚の主風防は幅広く平らで、中央継ぎ目は直線的です。"), ("側窗輪廓大而方正，窗框折角明顯。", "Large square side panes have pronounced frame corners.", "大きく四角い側面窓には明確な角があります。"), ("尖長機鼻與高起落架是必要的交叉確認。", "Cross-check with the long pointed nose and tall landing gear.", "長く尖った機首と高い脚で照合します。")],
        ),
        "fuselage": identify(
            ("757-200 機身長約 47.32 m、外寬約 3.76 m，形成高長寬比外觀；客艙門與翼上逃生口配置會依航空公司與認證布局不同。", "The 757-200 is about 47.32 m long but only about 3.76 m wide, giving it a high fineness ratio. Door and overwing-exit layouts vary by operator and certification configuration.", "757-200は全長約47.32 m、胴体幅約3.76 mで非常に細長く、ドアと翼上非常口の配置は運航会社・認証仕様で異なります。"),
            ("不要用門數單獨判型：757-200 有不同出口配置，改裝貨機也會封閉客艙窗並增加大型貨艙門。", "Do not identify it by door count alone: 757-200 exit layouts vary, while freighter conversions blank cabin windows and add a large cargo door.", "ドア数だけで判別しないでください。757-200は出口配置が複数あり、貨物改造機は窓を塞ぎ大型貨物扉を追加します。"),
            [("機身比 A321 更長且更窄。", "The body is longer and narrower than the A321's.", "胴体はA321より長く細身です。"), ("前段艙門與窗列位於較高的機身位置。", "Forward doors and cabin windows sit noticeably high above the ground.", "前方ドアと客室窓は地上から高い位置にあります。"), ("客運型、貨運改裝型的外部開口差異很大。", "Passenger and converted-freighter openings differ substantially.", "旅客型と貨物改造型では外部開口が大きく異なります。")],
        ),
        "engine": identify(
            ("757-200 可搭載 Rolls-Royce RB211-535 或 Pratt & Whitney PW2000；兩者都是大型高旁通渦扇，短艙尺寸相對窄機身非常醒目。", "The 757-200 uses either Rolls-Royce RB211-535 or Pratt & Whitney PW2000 turbofans, both notably large relative to the narrow fuselage.", "757-200はRB211-535またはPW2000を搭載し、細い胴体に対して大きな高バイパス比ターボファンが目立ちます。"),
            ("照片為 RB211 進氣口；PW2000 的整流罩細節不同，所以應先辨認『大型圓形短艙＋高離地』，再判斷引擎子型。", "The reference shows an RB211 inlet. PW2000 details differ, so first identify the large round nacelle and high ground clearance, then determine engine type.", "参考写真はRB211吸気口です。PW2000は細部が異なるため、まず大型円形ナセルと高い地上高を確認し、その後エンジン型を判別します。"),
            [("短艙比 A321ceo 的 CFM56／V2500 更大。", "The nacelle is larger than an A321ceo CFM56 or V2500 installation.", "ナセルはA321ceoのCFM56／V2500より大型です。"), ("進氣口接近完整圓形，沒有 737NG 的扁平底部。", "The inlet is nearly circular, without the flattened 737NG lower lip.", "吸気口はほぼ真円で、737NGのような平たい下面はありません。"), ("RB211 與 PW2000 的風扇、整流罩接縫不可混為一談。", "RB211 and PW2000 fan and cowling details should not be conflated.", "RB211とPW2000のファン・カウル細部を混同しないでください。")],
        ),
        "wingtip": identify(
            ("757 原始翼尖是簡單後掠尖端；許多 757-200 後來加裝 Aviation Partners Boeing 融合式小翼，少數再改成 Split Scimitar。", "The original 757 has a plain swept tip. Many 757-200s later received Aviation Partners Boeing blended winglets, and a smaller number gained Split Scimitar upgrades.", "757の原型翼端は単純な後退端ですが、多くの757-200がAPBブレンデッド・ウイングレットを後付けし、一部はSplit Scimitarへ改修されました。"),
            ("有沒有小翼不能決定是否為 757；照片顯示的是改裝融合式小翼，不是所有 757 的原廠共同特徵。", "Winglet presence does not determine whether an aircraft is a 757. The photo shows a retrofit blended winglet, not a universal factory feature.", "ウイングレットの有無だけでは757を判定できません。写真は後付けブレンデッド型で、全機共通の原型特徴ではありません。"),
            [("融合式小翼高大、根部曲線平順。", "The blended winglet is tall with a smooth curved root.", "ブレンデッド型は高く、根元が滑らかに湾曲します。"), ("未改裝機保留平直後掠翼尖。", "Unmodified aircraft retain a plain swept tip.", "未改修機は単純な後退翼端です。"), ("A321ceo 常見小型上下翼尖擋板，輪廓完全不同。", "A321ceos commonly use small upper/lower fences with a very different outline.", "A321ceoで一般的な上下小型フェンスとは輪郭が大きく異なります。")],
        ),
        "wing": identify(
            ("757 主翼面積約 185.25 m²，翼弦與展弦比都比 A321 更大；後緣有大型多段襟翼，支援高重量下的短場性能。", "The 757 wing covers about 185.25 m² and is larger in chord and span than the A321 wing, with substantial multi-element trailing-edge flaps for heavy-weight field performance.", "757の主翼面積は約185.25 m²でA321より翼弦・翼幅とも大きく、大型多要素フラップで高重量時の離着陸性能を確保します。"),
            ("翼尖改裝會改變總翼展；判讀資料時要分清原始翼尖與後裝小翼版本。", "Retrofit winglets change total span, so specifications must distinguish original and modified configurations.", "後付けウイングレットで全幅が変わるため、原型と改修仕様を区別して諸元を読みます。"),
            [("翼根厚、外翼細長且後掠。", "The thick root transitions into a long swept outer wing.", "厚い翼根から細長い後退外翼へ続きます。"), ("大型雙縫襟翼與擾流板占據長後緣。", "Large double-slotted flaps and spoilers occupy much of the trailing edge.", "大型二重隙間フラップとスポイラーが長い後縁を占めます。"), ("整體翼面明顯大於 A321。", "The overall wing is visibly larger than the A321's.", "主翼全体はA321より明らかに大きいです。")],
        ),
        "vstab": identify(
            ("757 垂直尾翼高大、前緣後掠，根部以長背鰭平順接入細長後機身；方向舵面積也大。", "The 757 has a tall swept fin with a long dorsal root fairing blending into the slender aft fuselage and a large rudder area.", "757は高い後退垂直尾翼、細長い後部胴体へ続く長いドーサル根元、大面積の方向舵を備えます。"),
            ("垂尾塗裝只能辨識航空公司；區分 A321 時要再看尾翼相對機身的高度、機鼻與主起落架輪數。", "Tail paint identifies the operator, not the type. Against an A321, also check fin-to-fuselage scale, nose form and main-wheel count.", "尾翼塗装は会社を示すだけです。A321との区別には尾翼比率、機首、主輪数も確認します。"),
            [("垂尾相對窄機身顯得非常高。", "The fin looks exceptionally tall over the narrow fuselage.", "細い胴体に対して垂直尾翼が非常に高く見えます。"), ("前緣後掠、頂端較平直。", "Its leading edge is swept and the tip comparatively squared.", "前縁は後退し、上端は比較的平らです。"), ("根部背鰭沿機背向前延伸。", "A dorsal fillet extends forward along the upper fuselage.", "根元フィレットが機背に沿って前方へ伸びます。")],
        ),
        "hstab": identify(
            ("757 的低置水平尾翼面積大、後掠明顯，安裝在細長後機身兩側；相對 A321 看起來更寬、更有翼面感。", "The 757's low-mounted tailplanes are large and strongly swept on either side of the slender aft fuselage, appearing broader than those of an A321.", "757の低位置水平尾翼は大面積で後退が強く、細い後部胴体の両側に付き、A321より幅広く見えます。"),
            ("757 與 A321 都是傳統低置尾翼，單看一小段水平尾翼不夠；側後方需同時看垂尾、機身寬度與主翼。", "Both types use conventional low tailplanes, so a partial view is insufficient. From aft-quarter angles include the fin, fuselage width and main wing.", "両機とも通常の低位置尾翼のため、一部だけでは不十分です。後斜めでは垂直尾翼、胴体幅、主翼も見ます。"),
            [("翼根整流罩較長，沿後機身延伸。", "A long root fairing runs along the aft fuselage.", "長い翼根フェアリングが後部胴体に沿います。"), ("外形後掠且逐漸收尖。", "The swept planform tapers toward the tips.", "後退平面形が翼端へ細くなります。"), ("面積與展幅視覺上大於 A321 尾翼。", "Its apparent area and span exceed the A321 tailplane's.", "見かけの面積と幅はA321より大きいです。")],
        ),
        "gear": identify(
            ("757-200 每側主起落架是兩軸四輪轉向架，前起落架雙輪；較長的主腳讓大型引擎與機身保持離地間隙。", "Each 757-200 main bogie has two axles and four tyres, plus twin nose wheels. Long struts provide clearance for the large engines and fuselage.", "757-200の各主脚は2軸4輪、前脚は2輪で、長い脚柱が大型エンジンと胴体の地上間隔を確保します。"),
            ("這是與標準 A321 最直接差異之一：A321 每側主腳通常只有單軸雙輪。", "This is one of the clearest differences from a standard A321, whose main gear normally has a single axle and two tyres per side.", "標準A321の各主脚は通常1軸2輪であり、最も明確な違いの一つです。"),
            [("每側主腳四輪，呈前後兩軸。", "Four tyres on each main bogie are arranged on two axles.", "各主脚は前後2軸の4輪です。"), ("主腳與前腳都比 A321 更高。", "Both main and nose gear stand taller than the A321's.", "主脚・前脚ともA321より高く立ちます。"), ("照片可同時看到四輪主腳與大型水平尾翼。", "The reference view shows the four-wheel bogie and large tailplane together.", "参考写真では4輪主脚と大型水平尾翼を同時に確認できます。")],
        ),
    },
    "a321": {
        "overview": identify(
            ("A321 是 A320 家族加長型單走道雙發客機；機身長而離地較低，機鼻圓鈍、駕駛艙窗帶呈典型 Airbus 折線，主翼相對機身較小。", "The A321 is the stretched A320-family narrow-body twin: long but low-sitting, with a rounded nose, classic angular Airbus glazing and a wing that looks relatively small against the fuselage.", "A321はA320ファミリーの胴体延長型で、長く低い姿勢、丸い機首、典型的なAirbus窓帯、胴体に対して小さく見える主翼が特徴です。"),
            ("與 757-200 相比，A321 機身較短寬、起落架較低、引擎較小；A321ceo 與 neo 的引擎與翼尖又會不同。", "Compared with a 757-200, the A321 is shorter and wider, sits lower and has smaller engines. Engine and wingtip appearance also differs between ceo and neo generations.", "757-200より短く幅広く、姿勢が低く、エンジンも小型です。A321ceoとneoではエンジンと翼端も異なります。"),
            [("機身外寬約 3.95 m，比 757 寬。", "The roughly 3.95 m fuselage is wider than the 757's.", "胴体外径は約3.95 mで757より太いです。"), ("傳統 A321ceo 常見四對全尺寸艙門。", "Traditional A321ceos commonly show four pairs of full-size doors.", "従来型A321ceoでは片側4枚の大型ドアが一般的です。"), ("較短起落架讓機身與引擎靠近地面。", "Shorter landing gear keeps the body and engines closer to the ground.", "短い脚により胴体とエンジンが地面に近くなります。")],
        ),
        "cockpit": identify(
            ("A321 與 A320 家族共用 Airbus 駕駛艙哲學：左右側桿、正面折疊桌板、六具顯示器與中央上下排列的 ECAM。", "The A321 shares the A320-family Airbus flight deck: sidesticks, forward tray tables, six displays and vertically arranged central ECAM screens.", "A321はA320ファミリー共通のAirbus操縦席で、サイドスティック、正面テーブル、6面表示器、上下配置の中央ECAMを備えます。"),
            ("與 757 相比，飛行員正前方沒有駕駛盤；A321ceo 的舊式 LCD／CRT 外觀也可能因航電升級而不同。", "Unlike the 757 there are no yokes ahead of the pilots. Display appearance on A321ceos may vary with avionics upgrades.", "757と違い正面に操縦輪はありません。A321ceoの表示器外観は改修状況で異なる場合があります。"),
            [("側桿位於左右側壁。", "Sidesticks are mounted on the sidewalls.", "サイドスティックは左右側壁にあります。"), ("正面沒有操縱柱，可配置桌板。", "No control column blocks the forward tray-table area.", "正面に操縦柱がなく、テーブルを配置できます。"), ("中央兩具 ECAM 顯示器監控引擎與系統。", "Two central ECAM screens monitor engines and systems.", "中央2面のECAMがエンジンとシステムを監視します。")],
        ),
        "windshield": identify(
            ("A321 採 A320 家族六片式駕駛艙窗：正面兩片主風擋呈斜邊梯形，外側窗沿圓鈍機鼻向後收尖，整組窗帶比 757 更有折線感。", "The A321 uses the A320-family six-pane glazing: two trapezoidal forward panes and outer panes tapering aft around a rounded nose, producing a more kinked belt than the 757.", "A321はA320ファミリーの六枚窓で、台形の前面2枚と丸い機首に沿って後方へ細くなる外側窓からなり、757より折れ線的です。"),
            ("A319、A320、A321 的機鼻與窗型幾乎相同，不能靠駕駛艙窗區分家族子型；必須看機身長度與出口配置。", "A319, A320 and A321 noses and glazing are nearly identical. Use fuselage length and exit layout to distinguish family members.", "A319・A320・A321の機首窓はほぼ同じため、胴体長と出口配置で子型を区別します。"),
            [("主風擋帶斜邊，中央接縫較短。", "Forward panes have slanted edges and a relatively short centre seam.", "前面窓は斜辺を持ち、中央継ぎ目は比較的短めです。"), ("外側窗向後上方收尖。", "Outer panes taper aft and upward.", "外側窓は後上方へ細くなります。"), ("圓鈍機鼻與低地上姿態可排除 757。", "The rounded nose and low stance help exclude a 757.", "丸い機首と低い姿勢で757を除外できます。")],
        ),
        "fuselage": identify(
            ("A321ceo 機身長約 44.51 m、外寬約 3.95 m；傳統配置每側常見四個全尺寸艙門，窗列與門距是辨認加長機身的重要線索。", "The A321ceo is about 44.51 m long and 3.95 m wide. Traditional layouts commonly have four full-size doors per side, whose spacing highlights the stretched fuselage.", "A321ceoは全長約44.51 m、胴体幅約3.95 mで、従来配置では片側4枚の大型ドアが延長胴体を示します。"),
            ("A321neo 的 Airbus Cabin Flex 可取消部分中段大型門、改用翼上逃生口；因此門數與位置必須配合世代判讀。", "A321neo Airbus Cabin Flex can remove some mid-cabin full-size doors and add overwing exits, so door layout must be interpreted by generation.", "A321neoのAirbus Cabin Flexでは一部中央大型ドアを廃止し翼上非常口を追加できるため、世代と合わせて判断します。"),
            [("傳統 A321ceo 每側四個大型矩形艙門。", "A traditional A321ceo has four large rectangular doors per side.", "従来型A321ceoは片側4枚の大型長方形ドアです。"), ("機身比 757 寬，但總長略短。", "The fuselage is wider but slightly shorter than the 757's.", "胴体は757より太い一方、全長は少し短めです。"), ("ACF／LR／XLR 的出口配置不能套用 ceo 判法。", "ACF, LR and XLR exit layouts should not be judged by ceo rules.", "ACF／LR／XLRの出口配置にceoの判別法をそのまま適用できません。")],
        ),
        "engine": identify(
            ("A321ceo 可搭載 CFM56-5B 或 IAE V2500；兩者都比 757 的 RB211／PW2000 小，短艙也更靠近地面。", "The A321ceo uses CFM56-5B or IAE V2500 engines, both smaller and closer to the ground than the 757's RB211 or PW2000 installations.", "A321ceoはCFM56-5BまたはV2500を搭載し、757のRB211／PW2000より小さく地面に近い位置にあります。"),
            ("照片為搭載 V2500 的 A321；A321neo 改用更大的 LEAP-1A 或 PW1100G，外觀不可混同。", "The reference shows a V2500-powered A321. A321neos use larger LEAP-1A or PW1100G engines and should not be visually conflated.", "参考写真はV2500搭載A321です。A321neoは大型LEAP-1AまたはPW1100Gを使うため混同しないでください。"),
            [("ceo 引擎短艙直徑小於 757。", "Ceo nacelles are smaller in diameter than the 757's.", "ceoのナセル径は757より小さいです。"), ("CFM56 與 V2500 的進氣口、排氣錐細節不同。", "CFM56 and V2500 inlet and exhaust details differ.", "CFM56とV2500では吸気口・排気部の細部が異なります。"), ("neo 大型引擎會讓離地間隙看起來更小。", "Larger neo engines make ground clearance look tighter.", "neoの大型エンジンは地上間隔をさらに小さく見せます。")],
        ),
        "wingtip": identify(
            ("早期 A321ceo 使用小型上下翼尖擋板，像短小的垂直箭頭；較晚 ceo 與 neo 可使用高大的 Sharklet。", "Early A321ceos use small upper-and-lower wingtip fences like short vertical arrows; later ceos and neos may use tall Sharklets.", "初期A321ceoは小さな上下翼端フェンスを使い、後期ceoとneoは大型Sharkletを装備できます。"),
            ("參考照片顯示傳統上下翼尖擋板；辨識時不要把 Sharklet 當成所有 A321 的共同特徵。", "The reference shows the traditional upper/lower fence. Do not treat a Sharklet as universal to every A321.", "参考写真は従来の上下フェンスです。Sharkletを全A321共通の特徴としないでください。"),
            [("上方翼片較大、下方翼片較小。", "The upper blade is larger and the lower blade smaller.", "上側ブレードが大きく、下側は小型です。"), ("輪廓比 757 改裝融合式小翼短很多。", "It is far shorter than a retrofit 757 blended winglet.", "757の後付けブレンデッド型よりはるかに短いです。"), ("Sharklet 世代外觀高大，需再看機身與引擎。", "Sharklet-equipped aircraft require fuselage and engine cross-checks.", "Sharklet装備機は胴体とエンジンも照合します。")],
        ),
        "wing": identify(
            ("A321ceo 與 A320 共用基本主翼，翼面積約 122.6 m²；相對加長機身看起來較小，外翼末端接翼尖擋板或 Sharklet。", "The A321ceo shares the basic A320 wing of about 122.6 m². Against the stretched fuselage it looks relatively small and ends in fences or Sharklets.", "A321ceoはA320と基本主翼を共有し、面積は約122.6 m²です。延長胴体に対して小さく見え、翼端はフェンスまたはSharkletです。"),
            ("A321neo 與 A321XLR 有結構、增升與油箱相關改進，但外觀辨識仍應先確認翼尖、引擎與出口配置。", "A321neo and A321XLR incorporate structural, high-lift and fuel-system changes, but visual identification still starts with tips, engines and exits.", "A321neo／XLRには構造・高揚力・燃料系改良がありますが、外観判別は翼端、エンジン、出口配置から始めます。"),
            [("主翼面積與展幅小於 757。", "Wing area and span are smaller than the 757's.", "主翼面積と翼幅は757より小さいです。"), ("後緣配置單縫襟翼與多片擾流板。", "Single-slotted flaps and multiple spoilers line the trailing edge.", "後縁に単隙間フラップと複数スポイラーがあります。"), ("外翼相對短，讓加長機身比例更突出。", "The relatively short outer wing emphasizes the stretched fuselage.", "比較的短い外翼が延長胴体を強調します。")],
        ),
        "vstab": identify(
            ("A321 垂直尾翼與 A320 家族相近，前緣後掠、頂端略平，根部以短背鰭連接後機身；相對 757 的尾翼較小。", "The A321 fin follows the A320-family form: swept leading edge, slightly squared tip and a short dorsal root fairing, smaller relative to the airframe than the 757 fin.", "A321の垂直尾翼はA320ファミリー共通で、後退前縁、やや平らな上端、短い根元フィレットを持ち、757より相対的に小型です。"),
            ("A319、A320、A321 的垂尾非常相似，不能用尾翼單獨分辨；必須看機身長度與艙門／逃生口。", "A319, A320 and A321 fins are very similar. Distinguish them by fuselage length and door/exit layout, not the fin alone.", "A319・A320・A321の垂直尾翼は非常に似るため、胴体長とドア／非常口で区別します。"),
            [("垂尾高度與面積小於 757。", "The fin is lower and smaller than the 757's.", "垂直尾翼は757より低く小型です。"), ("根部背鰭較短，後機身較粗。", "The dorsal fillet is shorter and the aft fuselage fuller.", "根元フィレットは短く、後部胴体は太めです。"), ("尾部輔助動力單元排氣口位於尖端。", "The APU exhaust sits at the pointed tailcone.", "APU排気口は尖ったテールコーン先端にあります。")],
        ),
        "hstab": identify(
            ("A321 的水平尾翼低置於尾錐兩側，面積與展幅比 757 小；正後方可見短而略後掠的平面與圓潤後機身。", "The A321's low-mounted tailplanes are smaller in area and span than the 757's. From directly aft they appear short and swept beside a fuller tailcone.", "A321の低位置水平尾翼は757より面積・幅が小さく、真後ろから短い後退面と丸い後部胴体が見えます。"),
            ("兩型都是傳統尾翼，不應只靠安裝位置；最有效的是比較水平尾翼尺度與主起落架輪組。", "Both use conventional tailplanes, so mounting position alone is weak. Compare tailplane scale and main-gear wheel arrangement.", "両機とも通常配置のため取付位置だけでは弱く、水平尾翼の大きさと主脚輪組を比較します。"),
            [("水平尾翼從尾錐較低位置向兩側伸出。", "The tailplanes project from a low position on the tailcone.", "水平尾翼は尾錐の低い位置から左右へ伸びます。"), ("展幅與面積明顯小於 757。", "Span and area are visibly smaller than the 757's.", "翼幅と面積は757より明らかに小さいです。"), ("正後方可同時確認雙輪主腳與圓形機身截面。", "An aft view also reveals twin-wheel main gear and the rounded fuselage section.", "後方から2輪主脚と丸い胴体断面も確認できます。")],
        ),
        "gear": identify(
            ("標準 A321 每側主起落架為單軸雙輪，前起落架也是雙輪；短腳柱讓機身與引擎靠近地面。", "A standard A321 has a single axle with two tyres on each main gear and twin nose wheels. Short struts keep the fuselage and engines close to the ground.", "標準A321は各主脚1軸2輪、前脚2輪で、短い脚柱により胴体とエンジンが地面に近くなります。"),
            ("與 757 每側四輪主腳相比，A321 的雙輪主腳是近距離最可靠差異之一。", "Against the 757's four-wheel bogie per side, the A321's twin-wheel main gear is one of the strongest close-range identifiers.", "757の各側4輪ボギーに対し、A321の2輪主脚は近距離で最も強い識別点の一つです。"),
            [("每側主腳只有兩個輪胎。", "Each main leg carries only two tyres.", "各主脚は2輪だけです。"), ("主腳柱短，收進翼身整流罩。", "The short main leg retracts into the wing-body fairing.", "短い主脚柱は翼胴フェアリングへ格納されます。"), ("輪數、地上高度都明顯少於 757。", "Wheel count and ground clearance are both lower than the 757's.", "輪数と地上高はいずれも757より小さいです。")],
        ),
    },
    "b763": {
        "overview": identify(
            ("767-300 是窄體感明顯的雙走道雙發客機：機身修長、機鼻較尖、主翼與引擎尺度都小於 A330-200；原始翼尖平直，部分 -300ER 後來加裝高大融合式小翼。", "The 767-300 is a visibly slender twin-aisle twinjet with a pointed nose and smaller wing and engines than the A330-200. Original tips are plain, while some -300ERs received tall blended winglets.", "767-300は細身の双通路双発機で、尖った機首とA330-200より小さい主翼・エンジンが特徴です。原型は通常翼端ですが、一部-300ERは大型ブレンデッド・ウイングレットを装備します。"),
            ("最可靠的遠距離組合是『窄長機身＋較尖機鼻＋較小主翼』；若有高大小翼仍要確認機身寬度，不能直接判成 737 或 757。", "The strongest long-range combination is a narrow long body, pointed nose and relatively small wing. A tall winglet alone does not distinguish it from a 737 or 757.", "遠距離では細長い胴体、尖った機首、比較的小さい主翼の組合せが有効です。大型ウイングレットだけで737や757と判断できません。"),
            [("全長約 54.94 m，機身外寬約 5.03 m。", "Length is about 54.94 m and fuselage width about 5.03 m.", "全長約54.94 m、胴体外幅約5.03 mです。"), ("機鼻與尾錐都比 A330-200 更細長。", "Both nose and tailcone are slimmer than the A330-200's.", "機首と尾部はいずれもA330-200より細長いです。"), ("翼尖可能是原始平直型或後裝融合式小翼。", "Tips may be original plain tips or retrofit blended winglets.", "翼端は原型または後付けブレンデッド型があります。")],
        ),
        "cockpit": identify(
            ("767 駕駛艙採 Boeing 駕駛盤與中央操縱柱，典型布局有六具 CRT／液晶顯示器、中央 EICAS 與傳統模式控制面板；後期改裝機的螢幕可能更現代。", "The 767 flight deck uses Boeing yokes and control columns, typically with six CRT/LCD displays, central EICAS and a conventional mode-control panel; retrofit aircraft may have newer screens.", "767の操縦席はBoeing式操縦輪とコントロールコラム、通常6面のCRT／LCD、中央EICAS、従来型モード制御盤を備え、改修機は新型画面の場合があります。"),
            ("對比 A330 最直接的是駕駛員正前方的駕駛盤；顯示器新舊不能單獨判型，因 767 與 A330 都有航電升級。", "The clearest contrast with the A330 is the yoke ahead of each pilot. Display generation alone is unreliable because both types have avionics upgrades.", "A330との最明確な差は各操縦席正面の操縦輪です。両型とも改修例があるため画面世代だけでは判別できません。"),
            [("正副駕駛前方均有駕駛盤與操縱柱。", "A yoke and control column sit ahead of each pilot.", "両席正面に操縦輪とコントロールコラムがあります。"), ("中央 EICAS 顯示引擎與警告資訊。", "Central EICAS displays show engine and alert information.", "中央EICASがエンジンと警報情報を表示します。"), ("中央推力台與大量實體旋鈕呈現 1980 年代 Boeing 風格。", "The throttle pedestal and physical controls reflect 1980s Boeing design.", "スロットル台と多数の物理操作部は1980年代Boeing設計です。")],
        ),
        "windshield": identify(
            ("767 使用六片式駕駛艙窗，正面兩片風擋較直立，外側窗帶形成明顯折角；配合較尖且略下垂的機鼻，正面輪廓比 A330 更窄。", "The 767 uses six cockpit panes with upright front windscreens and an angular outer belt. Combined with its pointed, slightly drooped nose, the frontal outline is narrower than the A330's.", "767は6枚窓で、直立気味の前面窓と角張った外側窓帯を持ちます。尖ってやや下がる機首と組み合わさり、A330より正面輪郭が狭く見えます。"),
            ("757 與 767 的窗型與機鼻語彙相近；需要再用機身寬度、主翼與引擎尺度區分，不能只數窗片。", "The 757 and 767 share similar window and nose styling; use fuselage width, wing and engine scale rather than pane count alone.", "757と767は窓・機首形状が近いため、窓枚数だけでなく胴体幅、主翼、エンジン寸法で区別します。"),
            [("中央接縫長，正面風擋輪廓偏方正。", "The centre seam is long and the forward panes look relatively square.", "中央継ぎ目が長く、前面窓は比較的四角く見えます。"), ("側窗向後收尖，但窗帶整體較窄。", "Side panes taper aft within a relatively narrow window belt.", "側窓は後方へ細くなり、窓帯全体は比較的狭いです。"), ("尖細機鼻是與 A330 圓鈍機鼻的重要差異。", "The slender pointed nose is a key contrast with the rounded A330 nose.", "細く尖った機首が丸いA330との重要な差です。")],
        ),
        "fuselage": identify(
            ("767-300 機身外寬約 5.03 m，典型經濟艙為 2-3-2；側面看起來比 A330-200 窄長。客艙門與翼上出口配置會依航空公司及認證方案不同。", "The 767-300 fuselage is about 5.03 m wide and typically seats 2-3-2 in economy, giving a narrower, longer look than the A330-200. Door and overwing-exit layouts vary by operator and certification configuration.", "767-300の胴体幅は約5.03 m、エコノミーは通常2-3-2で、A330-200より細長く見えます。ドアと翼上非常口配置は仕様で異なります。"),
            ("門數不是可靠的單一判據；辨識時同時比較機身直徑、前後門間距、機鼻與翼尖。", "Door count is not a reliable single cue; compare fuselage diameter, door spacing, nose and wingtips together.", "ドア数だけでは不十分で、胴体径、ドア間隔、機首、翼端を合わせて判断します。"),
            [("機身直徑明顯小於 A330。", "The fuselage diameter is visibly smaller than the A330's.", "胴体径はA330より明らかに小さいです。"), ("舷窗列沿修長機身延伸，翼身整流罩較緊湊。", "The window row runs along a slender body with a compact wing-body fairing.", "細長い胴体に窓列が続き、翼胴フェアリングは小型です。"), ("客貨型與不同出口方案會改變艙門外觀。", "Passenger, freighter and exit configurations alter door appearance.", "旅客型・貨物型・出口仕様によりドア外観が変わります。")],
        ),
        "engine": identify(
            ("767-300／-300ER 可搭載 GE CF6-80C2、Pratt & Whitney PW4000 或 Rolls-Royce RB211-524；短艙直徑與推力級通常小於 A330-200 的同世代引擎。", "The 767-300/-300ER can use GE CF6-80C2, Pratt & Whitney PW4000 or Rolls-Royce RB211-524 engines. Their nacelles and thrust class are generally smaller than contemporary A330-200 installations.", "767-300／-300ERはCF6-80C2、PW4000、RB211-524を装備でき、ナセル径と推力級は同世代A330-200より一般に小さめです。"),
            ("兩型都可能掛 CF6 或 PW4000，所以不能只看製造商；應比較短艙相對機身的尺寸、翼尖與機鼻。", "Both types may carry CF6 or PW4000 engines, so manufacturer alone is insufficient; compare nacelle-to-body scale, wingtips and nose.", "両型ともCF6やPW4000を搭載し得るため、メーカーだけでなく胴体に対するナセル寸法、翼端、機首を比較します。"),
            [("CF6-80C2 短艙相對窄小，後緣平滑。", "The CF6-80C2 nacelle is relatively compact with a smooth trailing edge.", "CF6-80C2ナセルは比較的小型で後縁は滑らかです。"), ("RB211 安裝可由不同的進氣口與排氣段辨認。", "RB211 installations have different inlet and exhaust details.", "RB211装備は吸気口と排気部の形状が異なります。"), ("所有傳統選項都沒有 787 式鋸齒短艙。", "None of the traditional options has 787-style chevrons.", "いずれも787式シェブロンはありません。")],
        ),
        "wingtip": identify(
            ("767 原始主翼只有簡單後掠翼尖；部分 767-300ER 後裝 Aviation Partners Boeing 高大融合式小翼。兩種外觀都存在，不能把小翼視為全系列標配。", "The original 767 has a simple swept tip, while some 767-300ERs received tall Aviation Partners Boeing blended winglets. Both configurations remain valid.", "767原型は単純な後退翼端で、一部767-300ERはAPB大型ブレンデッド・ウイングレットを後付けしました。両形態が存在します。"),
            ("有小翼時，其高度與平滑彎曲輪廓遠大於 A330ceo 的短小直立三角翼梢。", "When fitted, the tall smoothly curved winglet is much larger than the short upright triangular A330ceo tip device.", "装備時は高く滑らかな曲面で、A330ceoの短い直立三角翼端よりはるかに大きいです。"),
            [("原始翼尖沒有直立擋板。", "Original tips have no upright fence.", "原型翼端に直立フェンスはありません。"), ("後裝小翼高大並向上平滑彎曲。", "Retrofit winglets are tall and curve smoothly upward.", "後付け型は高く滑らかに上方へ曲がります。"), ("判型前先確認是否為改裝機。", "Establish whether the aircraft is retrofitted before identifying it.", "改修機かどうかを確認してから判別します。")],
        ),
        "wing": identify(
            ("767-300 原始翼展約 47.57 m，主翼後掠且面積小於 A330；翼根與翼身整流罩較緊湊，後裝小翼機翼展會增加。", "The original 767-300 spans about 47.57 m. Its swept wing is smaller than the A330's, with a more compact root and fairing; retrofit winglets increase span.", "767-300の原型翼幅は約47.57 mで、A330より小さく、翼根とフェアリングも小型です。後付け小翼で翼幅は増えます。"),
            ("由上方或下方看，767 的機翼相對窄機身仍很寬，但絕對展幅及翼面積都小於 A330-200。", "In plan view the wing is broad against the narrow fuselage, yet absolute span and area remain smaller than the A330-200's.", "平面では細い胴体に対して広く見えますが、絶対的な翼幅と面積はA330-200より小さいです。"),
            [("主翼後掠，翼尖原始為簡單收尖。", "The swept wing originally ends in a simple tapered tip.", "後退主翼は原型では単純に細く終わります。"), ("翼上有多片擾流板與雙縫襟翼。", "Multiple spoilers and double-slotted flaps occupy the upper and trailing wing.", "翼上に複数スポイラー、後縁に二重隙間フラップがあります。"), ("翼身整流罩比 A330 更短小。", "The wing-body fairing is shorter and smaller than the A330's.", "翼胴フェアリングはA330より短く小型です。")],
        ),
        "vstab": identify(
            ("767 垂直尾翼前緣大幅後掠、頂端略方，根部背鰭不長；尾錐細長，整體尾部比 A330-200 更纖細。", "The 767 fin has a strongly swept leading edge, a slightly squared tip and a modest dorsal fillet. Its long narrow tailcone makes the empennage look slimmer than the A330-200's.", "767の垂直尾翼は強い後退前縁、やや角形の上端、小さめの背びれを持ち、細長い尾部でA330-200より軽快に見えます。"),
            ("尾翼塗裝無法判定機型；應用尾錐粗細、翼尖與機身直徑交叉確認。", "Tail livery does not identify the type; cross-check tailcone width, wingtips and fuselage diameter.", "尾翼塗装では判型できず、尾部の太さ、翼端、胴体径を照合します。"),
            [("尾翼前緣後掠明顯，根部過渡較短。", "The leading edge is strongly swept with a short root transition.", "前縁後退が強く、根元の移行部は短めです。"), ("細尾錐末端可見 APU 排氣口。", "The slender tailcone ends at the APU exhaust.", "細い尾部先端にAPU排気口があります。"), ("相對窄機身，垂尾顯得高而薄。", "Against the narrow fuselage the fin looks tall and thin.", "細い胴体に対して垂直尾翼は高く薄く見えます。")],
        ),
        "hstab": identify(
            ("767 的低置水平尾翼後掠且向外收尖；由下方平面照片可同時比較其展幅、升降舵分段與細長尾錐。", "The 767's low-mounted tailplane is swept and tapered. An underside planform view reveals its span, segmented elevators and slender tailcone together.", "767の低位置水平尾翼は後退して翼端へ細くなり、下面写真で翼幅、分割昇降舵、細い尾部を同時に確認できます。"),
            ("水平尾翼外形只能作輔助；兩型都是傳統低置布局，應優先看翼尖與機身直徑。", "Tailplane shape is secondary because both aircraft use conventional low-mounted layouts; prioritize wingtips and fuselage diameter.", "両型とも通常の低位置配置のため水平尾翼は補助情報で、翼端と胴体径を優先します。"),
            [("後掠平面由厚翼根向外快速收尖。", "The swept planform tapers quickly from a thick root.", "厚い翼根から外側へ急速に細くなります。"), ("升降舵沿後緣分段配置。", "Segmented elevators line the trailing edge.", "後縁に分割昇降舵があります。"), ("下方全機照片能同時觀察主翼與尾翼比例。", "The underside view shows wing and tail proportions together.", "下面全景で主翼と尾翼の比率を同時に確認できます。")],
        ),
        "gear": identify(
            ("767-300 每側主起落架為兩軸四輪轉向架，前起落架雙輪；這與 A330-200 相同，因此輪胎數不能區分兩型。", "Each 767-300 main gear has a two-axle four-wheel bogie and the nose gear has two wheels. The A330-200 uses the same counts, so wheel number does not separate them.", "767-300の各主脚は2軸4輪、前脚は2輪で、A330-200も同じため輪数では区別できません。"),
            ("近距離應比較較窄的輪距、支柱與艙門形狀，並回看機身寬度；不要把『四輪主腳』誤認成 777。", "At close range compare narrower track, strut and door geometry, then check fuselage width; four-wheel bogies do not imply a 777.", "近距離では狭い輪距、脚柱、扉形状と胴体幅を確認し、4輪主脚だけで777と判断しないでください。"),
            [("每側主腳四輪，前腳雙輪。", "Four tyres sit on each main bogie with twin nose wheels.", "各主脚4輪、前脚2輪です。"), ("主腳收進翼根附近的輪艙。", "The main gear retracts into bays near the wing root.", "主脚は翼根付近の格納庫へ収まります。"), ("機身與輪距都比 A330 窄。", "Both fuselage and gear track are narrower than the A330's.", "胴体と脚間隔はいずれもA330より狭いです。")],
        ),
    },
    "a332": {
        "overview": identify(
            ("A330-200 是短機身長程廣體雙發客機，圓鈍 Airbus 機鼻、寬機身、大展弦比主翼與短小直立三角翼梢，是對比 767-300 的主要外觀線索。", "The A330-200 is a short-fuselage long-range wide-body twin, identified against the 767-300 by its rounded Airbus nose, wider body, large high-aspect-ratio wing and small upright triangular tip devices.", "A330-200は短胴長距離ワイドボディ双発機で、丸いAirbus機首、太い胴体、大型高アスペクト比主翼、小型直立三角翼端が767-300との主要差です。"),
            ("A330-200 比 767-300 更長也更寬，但機身相對主翼看起來較短粗；A330-300 又比 -200 長，不能只靠家族特徵判子型。", "The A330-200 is longer and wider than the 767-300 yet looks shorter and fuller relative to its wing. The A330-300 is longer again, so family cues alone do not identify the variant.", "A330-200は767-300より長く太い一方、主翼に対して短く太く見えます。A330-300はさらに長いため、家族特徴だけで子型は判別できません。"),
            [("全長約 58.82 m，機身外寬約 5.64 m。", "Length is about 58.82 m and fuselage width about 5.64 m.", "全長約58.82 m、胴体外幅約5.64 mです。"), ("圓鈍機鼻與寬大機身比 767 更厚實。", "The rounded nose and wide body look fuller than the 767.", "丸い機首と太い胴体は767より量感があります。"), ("A330ceo 翼尖有短小直立三角翼梢。", "A330ceos carry small upright triangular tip devices.", "A330ceo翼端には小型直立三角翼端があります。")],
        ),
        "cockpit": identify(
            ("A330-200 駕駛艙採 Airbus 側桿、正面桌板、六具顯示器與中央上下排列 ECAM；正副駕駛前方沒有駕駛盤與操縱柱。", "The A330-200 flight deck uses Airbus sidesticks, forward tray tables, six displays and vertically stacked central ECAM screens, with no yokes or control columns ahead of the pilots.", "A330-200の操縦席はAirbus式サイドスティック、正面テーブル、6面表示器、上下配置ECAMを備え、正面に操縦輪や柱はありません。"),
            ("與 767 相比，側桿對駕駛盤是最直觀差異；螢幕可能因改裝而更新，但基本操縱哲學不變。", "Against the 767, sidesticks versus yokes are the clearest cue. Screens may be upgraded, but the control philosophy remains.", "767との最明確な差はサイドスティック対操縦輪です。画面は改修されても操縦思想は変わりません。"),
            [("側桿位於左右側壁。", "Sidesticks are mounted on the sidewalls.", "サイドスティックは左右側壁にあります。"), ("飛行員正前方可使用折疊桌板。", "Tray tables occupy the unobstructed space ahead of the pilots.", "操縦席正面の空間に折り畳みテーブルがあります。"), ("中央 ECAM 顯示引擎與系統狀態。", "Central ECAM screens show engine and system status.", "中央ECAMがエンジンとシステム状態を表示します。")],
        ),
        "windshield": identify(
            ("A330 使用經典 Airbus 六片式窗帶：正面兩片風擋呈斜邊梯形，外側窗沿圓鈍機鼻向後包覆，正面輪廓比 767 更寬。", "The A330 uses the classic six-pane Airbus belt: two trapezoidal front windscreens and outer panes wrapping around a rounded nose, producing a wider frontal outline than the 767.", "A330は古典的なAirbus六枚窓で、台形の前面2枚と丸い機首へ回り込む外側窓により、767より正面輪郭が広く見えます。"),
            ("A330-200 與 -300 的窗型幾乎相同，需用機身長度與垂尾比例判子型；窗片數也不能單獨排除 767。", "A330-200 and -300 glazing is nearly identical; use fuselage length and fin proportions for the variant. Pane count alone also does not exclude a 767.", "A330-200と-300の窓形状はほぼ同じで、胴体長と垂尾比率で子型を判断します。窓枚数だけでは767も除外できません。"),
            [("圓鼻使窗帶向兩側平滑展開。", "The rounded nose lets the window belt spread smoothly sideways.", "丸い機首に沿って窓帯が両側へ滑らかに広がります。"), ("主風擋斜邊明顯，中央接縫較短。", "The front panes have obvious slanted edges and a shorter centre seam.", "前面窓の斜辺が明瞭で中央継ぎ目は短めです。"), ("整組玻璃相對機身看起來更寬低。", "The glazing appears wider and lower relative to the fuselage.", "窓全体は胴体に対して幅広く低く見えます。")],
        ),
        "fuselage": identify(
            ("A330-200 機身外寬約 5.64 m，經濟艙典型為 2-4-2；短於 A330-300，但仍比 767-300 更粗、更長，翼身整流罩也更大。", "The A330-200 fuselage is about 5.64 m wide and typically seats 2-4-2 in economy. It is shorter than the A330-300 but wider and longer than the 767-300, with a larger wing-body fairing.", "A330-200の胴体幅は約5.64 m、エコノミーは通常2-4-2です。A330-300より短い一方、767-300より太く長く、翼胴フェアリングも大型です。"),
            ("A330-200 常見每側四個大型主艙門，但門與窗配置仍會依客艙方案變化；應以機身比例與尾翼交叉判讀。", "Four large main doors per side are common, but cabin configuration can alter door and window details; cross-check body proportions and tail.", "片側4枚の大型ドアが一般的ですが、客室仕様で細部が変わるため胴体比率と尾翼も確認します。"),
            [("寬機身讓窗列與艙門看起來較矮。", "The wide body makes windows and doors look proportionally shorter.", "太い胴体により窓とドアは相対的に低く見えます。"), ("翼身整流罩寬大且向後延伸。", "The broad wing-body fairing extends well aft.", "大型翼胴フェアリングが後方へ長く伸びます。"), ("較短機身搭配大翼，比例不同於 A330-300。", "The short fuselage and large wing differ in proportion from the A330-300.", "短い胴体と大きな主翼の比率はA330-300と異なります。")],
        ),
        "engine": identify(
            ("A330-200 可搭載 GE CF6-80E1、Pratt & Whitney PW4000 或 Rolls-Royce Trent 700；三種短艙外觀不同，但整體尺寸通常大於 767 的對應引擎。", "The A330-200 can use GE CF6-80E1, Pratt & Whitney PW4000 or Rolls-Royce Trent 700 engines. Their nacelles differ, but are generally larger than corresponding 767 installations.", "A330-200はCF6-80E1、PW4000、Trent 700を選択でき、形状は異なりますが767用より一般に大型です。"),
            ("參考照片是 A330-223 的 PW4000 開罩狀態；引擎品牌與 767 有重疊，不能單靠風扇或商標判型。", "The reference shows an open-cowling PW4000 on an A330-223. Engine brands overlap with the 767, so fan or branding alone is insufficient.", "参考写真はA330-223のPW4000開放状態です。767とメーカーが重なるため、ファンやロゴだけでは判別できません。"),
            [("短艙直徑相對 767 更大。", "Nacelle diameter is larger relative to the 767's.", "ナセル径は767より大きいです。"), ("三種引擎的進氣口、整流罩與排氣段不同。", "The three options differ in inlet, cowling and exhaust details.", "3種類で吸気口、カウリング、排気部が異なります。"), ("短艙後緣平滑，沒有 787 式鋸齒。", "Nacelle trailing edges are smooth without 787-style chevrons.", "ナセル後縁は滑らかで787式シェブロンはありません。")],
        ),
        "wingtip": identify(
            ("A330ceo 翼尖有短小直立三角翼梢，前緣後掠、頂端收尖；與 767 原始平直翼尖或高大後裝小翼都很不同。", "The A330ceo has a short upright triangular tip device with a swept leading edge and tapered top, unlike either the 767's plain tip or tall retrofit winglet.", "A330ceoは前縁が後退し上端が細くなる短い直立三角翼端を持ち、767の通常翼端や大型後付け小翼と明確に異なります。"),
            ("A330neo 改用 A350 風格大型彎曲翼尖，不能套用 ceo 判法；本條目針對 A330-200ceo。", "A330neos use larger A350-inspired curved tips, so this ceo cue does not apply; this entry covers the A330-200ceo.", "A330neoはA350風大型曲線翼端を使うため、このceo判別法は適用できません。本項はA330-200ceoです。"),
            [("三角翼梢自翼端向上伸出並逐漸收尖。", "The triangular device rises from the tip and tapers upward.", "三角翼端は翼端から上へ伸びて細くなります。"), ("輪廓遠小於 767 融合式小翼。", "The profile is far smaller than a 767 blended winglet.", "767ブレンデッド・ウイングレットよりはるかに小型です。"), ("所有 A330ceo 家族都可見相近翼尖語彙。", "A similar tip vocabulary appears across the A330ceo family.", "A330ceoファミリーで同様の翼端形状が見られます。")],
        ),
        "wing": identify(
            ("A330ceo 主翼展約 60.3 m，展弦比高、翼根厚且翼身整流罩寬大；相較 767-300 的 47.57 m 原始翼展，遠距離就能看出更大的翼面。", "The A330ceo spans about 60.3 m, with a high-aspect-ratio wing, thick root and broad fairing. Its wing is visibly larger than the original 47.57 m-span 767-300 wing.", "A330ceoの翼幅は約60.3 mで、高アスペクト比、厚い翼根、大型フェアリングを持ち、原型翼幅47.57 mの767-300より明らかに大型です。"),
            ("A330-200 與 -300 共用基本主翼；判子型仍要看機身長度與 -200 較大的垂直尾翼。", "The A330-200 and -300 share the basic wing; identify the variant using fuselage length and the -200's larger fin.", "A330-200と-300は基本主翼を共有するため、胴体長と-200の大型垂尾で子型を判断します。"),
            [("主翼長而後掠，外翼末端接直立三角翼梢。", "The long swept wing ends in an upright triangular tip device.", "長い後退主翼の端に直立三角翼端があります。"), ("翼根厚、翼身整流罩寬大。", "The root is thick and the wing-body fairing broad.", "翼根が厚く翼胴フェアリングも大型です。"), ("多片擾流板與大型襟翼佔據後緣。", "Multiple spoilers and large flaps occupy the wing and trailing edge.", "複数スポイラーと大型フラップが翼後縁を占めます。")],
        ),
        "vstab": identify(
            ("A330-200 因機身較短、尾力臂較小，使用比 A330-300 更大的垂直尾翼；高大後掠尾翼與厚實根部是辨認 -200 的重要家族內線索。", "Because its shorter fuselage gives less tail moment arm, the A330-200 uses a larger vertical fin than the A330-300. The tall swept fin and substantial root are useful within-family cues.", "A330-200は短い胴体で尾部モーメントアームが小さいため、A330-300より大型の垂直尾翼を使い、高い後退尾翼と厚い根元が子型識別に役立ちます。"),
            ("對比 767，A330 尾部建立在更粗的機身與更寬的背鰭過渡上；尾翼塗裝仍不能取代形狀判讀。", "Against the 767, the A330 tail rises from a fuller fuselage and broader dorsal transition; livery still cannot replace shape cues.", "767に比べ太い胴体と広い背びれ移行部から尾翼が立ち上がります。塗装だけでは判別できません。"),
            [("-200 垂尾比例高大，面積大於 -300。", "The -200 fin is proportionally tall and larger than the -300's.", "-200の垂尾は相対的に高く、-300より大きいです。"), ("根部過渡寬厚，連接較粗後機身。", "A broad thick root blends into the fuller aft fuselage.", "幅広く厚い根元が太い後部胴体へつながります。"), ("尾錐末端為 APU 排氣口。", "The tailcone ends at the APU exhaust.", "尾部先端にAPU排気口があります。")],
        ),
        "hstab": identify(
            ("A330-200 的低置水平尾翼面積與展幅都大於 767，後掠翼面從厚翼根向外收尖；全機下方照片可直接比較尾翼與寬機身比例。", "The A330-200's low-mounted tailplane is larger in area and span than the 767's, tapering from a thick swept root. An underside view shows its scale against the wide fuselage.", "A330-200の低位置水平尾翼は767より面積・幅が大きく、厚い後退翼根から細くなります。下面写真で太い胴体との比率を確認できます。"),
            ("水平尾翼本身不是主要判據；兩型布局相同，應配合翼尖、機身寬度與垂尾比例。", "Tailplane shape alone is secondary because both types share the layout; combine it with wingtips, fuselage width and fin proportion.", "両型とも同配置のため水平尾翼単独は補助的で、翼端、胴体幅、垂尾比率と組み合わせます。"),
            [("水平尾翼從粗壯尾錐兩側伸出。", "The tailplanes project from either side of a broad tailcone.", "太い尾部の両側から水平尾翼が伸びます。"), ("翼根厚、外段後掠並收尖。", "The root is thick and the swept outer panel tapers.", "翼根が厚く、外側は後退して細くなります。"), ("與大垂尾組成較厚重的尾部輪廓。", "Together with the large fin it forms a fuller empennage.", "大型垂尾とともに厚みある尾部輪郭を作ります。")],
        ),
        "gear": identify(
            ("A330-200 每側主起落架為兩軸四輪轉向架，前起落架雙輪；主腳向內收進寬大的翼身整流罩。", "Each A330-200 main gear has a two-axle four-wheel bogie and the nose gear has two wheels; the main units retract inward into the broad wing-body fairing.", "A330-200の各主脚は2軸4輪、前脚は2輪で、主脚は内側へ大型翼胴フェアリング内に格納されます。"),
            ("輪數與 767-300 完全相同；應比較 A330 較寬輪距、粗機身、較大型主翼與不同的支柱／艙門形狀。", "Wheel counts exactly match the 767-300. Use the A330's wider track, fuller body, larger wing and different strut/door geometry.", "輪数は767-300と同じため、A330の広い脚間隔、太い胴体、大型主翼、脚柱・扉形状を比較します。"),
            [("每側主腳四輪，前腳雙輪。", "Four tyres sit on each main bogie with twin nose wheels.", "各主脚4輪、前脚2輪です。"), ("主腳輪距與支柱尺度大於 767。", "Main-gear track and strut scale are greater than the 767's.", "主脚間隔と脚柱寸法は767より大きいです。"), ("輪艙位於寬大的翼身整流罩內。", "The gear bays sit within the broad wing-body fairing.", "脚格納庫は大型翼胴フェアリング内にあります。")],
        ),
    },
}

CONTENT.update({
    "beluga": {
        "overview": identify(
            ("A300-600ST Beluga 以 A300-600 為基礎，把上半機身擴成鯨魚般的超大貨艙；低置駕駛艙、雙發與前開式貨艙門是最醒目的組合。", "The A300-600ST Beluga combines an A300-600 lower airframe with a whale-like upper cargo hold; its low cockpit, twin engines and upward-opening nose door form the key silhouette.", "A300-600ST BelugaはA300-600の下部機体に巨大な上部貨物室を組み合わせ、低い操縦席、双発、上開き機首貨物扉が特徴です。"),
            ("BelugaST 可載約 47 噸，貨艙容積約 1,400 m³，主要任務是運送機翼與機身段等超大型空中巴士零組件。", "The BelugaST carries about 47 tonnes in roughly 1,400 m³, principally moving oversized Airbus wings and fuselage sections.", "BelugaSTは約47トン、約1,400 m³の貨物室を持ち、主にエアバスの翼や胴体区画を輸送します。"),
            [("機長 56.15 m、翼展 44.84 m。", "Length 56.15 m; span 44.84 m.", "全長56.15 m、全幅44.84 mです。"), ("駕駛艙位於貨艙地板下方。", "The cockpit sits below the cargo floor.", "操縦席は貨物床より下にあります。"), ("前端貨艙門向上開啟，不必拆離駕駛艙。", "The forward cargo door opens upward without disconnecting the cockpit.", "前部貨物扉は操縦席を切り離さず上方へ開きます。")],
        ),
        "cockpit": identify(
            ("BelugaST 沿用 A300-600 世代駕駛艙：傳統駕駛盤、早期 EFIS 顯示器與大量實體開關；照片為同家族 A300 的代表配置。", "The BelugaST retains the A300-600-generation flight deck with conventional yokes, early EFIS displays and numerous physical controls; the photo shows the shared A300-family layout.", "BelugaSTは操縦輪、初期EFIS、多数の物理操作部を持つA300-600世代の操縦席を継承します。写真は同系A300の代表配置です。"),
            ("座艙被下移到主貨艙地板以下，裝卸時貨艙鼻門可在駕駛艙上方開啟，這是它與一般鼻門貨機最大的操作差異。", "Placing the cockpit below the main-deck floor lets the cargo nose open above it during loading, unlike conventional nose-door freighters.", "操縦席を主貨物床より下に置くため、一般的な機首扉貨物機と違い、その上で機首扉を開けられます。"),
            [("正副駕駛均使用傳統駕駛盤。", "Both pilots use conventional yokes.", "両操縦席に従来型操縦輪があります。"), ("儀表風格屬 A300-600 的類比／早期玻璃化過渡世代。", "Instrumentation reflects the A300-600 analogue-to-early-glass transition.", "A300-600のアナログから初期グラス化への移行期の計器です。"), ("駕駛艙照片應視為 A300 家族布局參考。", "Treat the cockpit photograph as an A300-family layout reference.", "操縦席写真はA300ファミリー配置の参考です。")],
        ),
        "windshield": identify(
            ("Beluga 的六片式 A300 駕駛艙窗位於巨大貨艙隆起下方，正面看像一條很低的窄窗帶；側面窗則緊貼機鼻下半部。", "The Beluga's six-pane A300 glazing forms a narrow low-set band beneath the huge cargo bulge, with the side panes tucked into the lower nose.", "BelugaのA300系6枚窓は巨大な貨物室膨らみの下に低く細い窓帯を作り、側面窓も機首下部にあります。"),
            ("不要只看窗片輪廓：『窗帶極低、上方是無窗的大型圓頂貨艙』才是 Beluga 最可靠的正面識別點。", "Do not rely on pane shape alone: the extremely low window band beneath a windowless domed cargo body is the strongest frontal cue.", "窓形だけでなく、窓のない巨大なドーム状貨物室の下に窓帯が極端に低い点が最重要です。"),
            [("兩片主風擋位於機鼻中線兩側。", "Two main windshields flank the nose centreline.", "2枚の主風防が機首中心線を挟みます。"), ("外側斜窗向後連到側窗。", "Angled outer panes lead into the side windows.", "斜めの外側窓が側面窓へ続きます。"), ("貨艙隆起遠高於窗帶。", "The cargo bulge towers above the glazing.", "貨物室の膨らみは窓帯よりはるかに高いです。")],
        ),
        "fuselage": identify(
            ("Beluga 的上部貨艙最大約 7.1 m 寬、6.7 m 高，可容納長達約 30 m 的超大型貨物；前方整片貨艙門向上掀開。", "The Beluga's upper hold reaches about 7.1 m wide and 6.7 m high for outsized loads up to roughly 30 m long; the entire forward cargo shell hinges upward.", "上部貨物室は最大約7.1 m幅、6.7 m高で約30 mの大型貨物を収容し、前部外殻全体が上へ開きます。"),
            ("Beluga 從機首裝載；Dreamlifter 則把後機身整段向側面旋開。看到開門位置即可快速區分兩者。", "The Beluga loads through the nose, whereas the Dreamlifter swings its aft fuselage sideways; the door location quickly separates them.", "Belugaは機首から積載し、Dreamlifterは後部胴体を横へ旋回させます。扉位置で素早く区別できます。"),
            [("貨艙容積約 1,400 m³。", "Cargo volume is about 1,400 m³.", "貨物容積は約1,400 m³です。"), ("載重約 47,000 kg。", "Payload is about 47,000 kg.", "搭載量は約47,000 kgです。"), ("下半機身仍保留 A300-600 基本結構。", "The lower fuselage retains the basic A300-600 structure.", "下部胴体はA300-600の基本構造を保ちます。")],
        ),
        "engine": identify(
            ("BelugaST 使用兩具 GE CF6-80C2A8 高旁通比渦扇，分別吊掛在左右主翼下；圓形短艙與雙發布局來自 A300-600。", "The BelugaST uses two GE CF6-80C2A8 high-bypass turbofans, one beneath each A300-600-derived wing.", "BelugaSTはA300-600由来の主翼下にGE CF6-80C2A8高バイパス比ターボファンを各1基装備します。"),
            ("Dreamlifter 有四具 PW4062A；遠距離辨識時，雙發 Beluga 與四發 Dreamlifter 幾乎不會混淆。", "The Dreamlifter has four PW4062A engines, making the twin-versus-four-engine distinction decisive at range.", "DreamlifterはPW4062Aを4基装備するため、双発と4発の違いが遠距離でも決定的です。"),
            [("左右主翼各一具引擎。", "One engine is mounted under each wing.", "左右主翼下に各1基です。"), ("短艙為傳統圓形進氣口。", "The nacelle has a conventional round inlet.", "ナセル吸気口は通常の円形です。"), ("推力級約 26 噸。", "Each engine is in roughly the 26-tonne-thrust class.", "各エンジンは約26トン推力級です。")],
        ),
        "wingtip": identify(
            ("BelugaST 保留 A300-600 的簡潔翼尖，沒有大型垂直小翼；從後方可見翼尖只以小幅上翹／端部整形收尾。", "The BelugaST retains the A300-600's plain tip without a large vertical winglet, ending in only a modest tip fairing.", "BelugaSTは大型垂直ウイングレットのないA300-600の簡潔な翼端を保ちます。"),
            ("照片中靠近尾部的小型直立片是水平尾翼端部輔助垂直翼，不是主翼翼尖小翼。", "The small upright surfaces near the tail are auxiliary tailplane finlets, not main-wing winglets.", "尾部近くの小さな直立面は水平尾翼端の補助フィンで、主翼ウイングレットではありません。"),
            [("主翼端沒有高聳翼尖小翼。", "No tall winglet rises from the main-wing tip.", "主翼端に高いウイングレットはありません。"), ("翼尖輪廓薄而平順。", "The tip profile is thin and clean.", "翼端形状は薄く簡潔です。"), ("應與尾翼端部小翼分開辨認。", "Do not confuse it with the tailplane finlets.", "水平尾翼端フィンと混同しないでください。")],
        ),
        "wing": identify(
            ("BelugaST 主翼源自 A300-600，翼展 44.84 m，後掠主翼下各掛一具 CF6；機身巨大後，主翼視覺上顯得相對短小。", "The BelugaST uses the A300-600-derived 44.84 m swept wing with one CF6 beneath each side; the huge fuselage makes the wing look relatively compact.", "BelugaSTはA300-600由来の翼幅44.84 m後退翼を使い、巨大な胴体のため翼が相対的に小さく見えます。"),
            ("Dreamlifter 的 747 翼展達 64.44 m 且有四具引擎；比較翼展與引擎數量可立即判別。", "The Dreamlifter spans 64.44 m and carries four engines, so span and engine count separate the pair immediately.", "Dreamlifterは翼幅64.44 m・4発で、翼幅とエンジン数からすぐ区別できます。"),
            [("後掠低翼配置。", "Swept low-wing arrangement.", "後退した低翼配置です。"), ("翼展 44.84 m。", "Wingspan is 44.84 m.", "翼幅は44.84 mです。"), ("高升力裝置沿後緣展開。", "High-lift devices occupy much of the trailing edge.", "後縁の広い範囲に高揚力装置があります。")],
        ),
        "vstab": identify(
            ("Beluga 的垂尾經放大與強化，根部前方有醒目的三角形背鰭，用來補償巨大上機身帶來的方向穩定影響。", "The Beluga has an enlarged reinforced fin with a conspicuous triangular dorsal extension to restore directional stability behind the huge upper fuselage.", "Belugaの垂直尾翼は大型化・強化され、巨大な上部胴体による方向安定低下を補う三角形背びれがあります。"),
            ("高大的垂尾、寬背鰭與水平尾翼端小翼共同構成 Beluga 特有的尾部輪廓。", "The tall fin, broad dorsal extension and tailplane finlets together create the Beluga's distinctive tail silhouette.", "高い垂尾、幅広い背びれ、水平尾翼端フィンがBeluga独特の尾部輪郭を作ります。"),
            [("垂尾根部背鰭向前延伸。", "A dorsal extension runs forward from the fin root.", "垂尾根元の背びれが前方へ伸びます。"), ("尾翼相對機身高度很高。", "The fin is tall relative to the fuselage.", "胴体に対して垂尾が高いです。"), ("方向舵後緣近乎筆直。", "The rudder trailing edge is nearly straight.", "方向舵後縁はほぼ直線です。")],
        ),
        "hstab": identify(
            ("Beluga 的水平尾翼經強化，左右端部各加裝一片直立輔助垂尾；從正後方看形成非常特殊的三垂直面配置。", "The Beluga's reinforced tailplane carries an auxiliary vertical finlet at each tip, creating a distinctive three-vertical-surface rear view.", "強化された水平尾翼の両端に補助垂直フィンが付き、後方から3枚の垂直面に見えます。"),
            ("端部小翼是為改善巨大機身遮蔽氣流時的方向穩定性，不是減少主翼誘導阻力的翼尖小翼。", "These finlets improve directional stability in flow disturbed by the huge fuselage; they are not drag-reducing main-wing devices.", "端部フィンは巨大胴体後流での方向安定を補い、主翼の抗力低減用装置ではありません。"),
            [("左右水平尾翼端各一片直立小翼。", "One vertical finlet stands at each tailplane tip.", "左右水平尾翼端に各1枚の垂直フィンがあります。"), ("水平尾翼低置於垂尾根部。", "The tailplane mounts low at the fin root.", "水平尾翼は垂尾根元の低位置です。"), ("這是 Beluga 最強的後方識別點。", "This is the strongest rear identification cue.", "Belugaを後方から識別する最強の特徴です。")],
        ),
        "gear": identify(
            ("Beluga 沿用 A300-600 起落架：前腳雙輪，左右主腳各四輪，合計 10 輪；主腳位於翼根下方。", "The Beluga retains A300-600 landing gear: twin nose wheels and four wheels on each main bogie, ten wheels in total.", "BelugaはA300-600の脚を継承し、前脚2輪、左右主脚各4輪の合計10輪です。"),
            ("Dreamlifter 沿用 747 的 18 輪配置並有四組主起落架；主腳組數是地面辨識兩者的直接方法。", "The Dreamlifter retains the 747's 18-wheel arrangement with four main bogies; bogie count is a direct ground-identification cue.", "Dreamlifterは4組主脚を持つ747の18輪配置で、主脚組数が地上識別に有効です。"),
            [("前腳為單支柱雙輪。", "The nose unit has twin wheels on one strut.", "前脚は単支柱2輪です。"), ("每側主腳為四輪轉向架。", "Each main bogie carries four wheels.", "左右主脚は各4輪ボギーです。"), ("總輪數為 10 輪。", "Total wheel count is ten.", "総輪数は10輪です。")],
        ),
    },
    "dreamlifter": {
        "overview": identify(
            ("747-400 Dreamlifter 是由 747-400 客機改裝的 LCF：保留四發、上層駕駛艙與 747 主翼，但上半機身膨大成巨型貨艙，尾部可整段向側面旋開。", "The 747-400 Dreamlifter is a converted 747-400 LCF retaining four engines, the upper-deck cockpit and 747 wing beneath a huge cargo body whose tail swings sideways.", "747-400 Dreamlifterは747-400旅客機改造LCFで、4発・上層操縦席・747主翼を残し、巨大貨物胴体と横開き尾部を備えます。"),
            ("四架 Dreamlifter 專門運送 787 大型組件；貨艙約 1,840 m³，容量約為 747-400F 的三倍。", "Four Dreamlifters move major 787 assemblies; the roughly 1,840 m³ hold offers about three times the volume of a 747-400F.", "4機のDreamlifterが787大型部品を輸送し、約1,840 m³の貨物室は747-400Fの約3倍です。"),
            [("機長 71.68 m、翼展 64.44 m。", "Length 71.68 m; span 64.44 m.", "全長71.68 m、全幅64.44 mです。"), ("ICAO 機型代碼為 BLCF。", "Its ICAO type designator is BLCF.", "ICAO機種コードはBLCFです。"), ("四架皆由既有 747-400 改裝。", "All four aircraft were converted from existing 747-400s.", "全4機が既存747-400から改造されました。")],
        ),
        "cockpit": identify(
            ("Dreamlifter 保留 747-400 駕駛艙：雙駕駛盤、六具主要 CRT／顯示器與寬大的中央控制台；照片為 747-400 家族代表配置。", "The Dreamlifter retains the 747-400 flight deck with dual yokes, six principal CRT/display units and a broad centre pedestal; the photo shows the shared 747-400-family layout.", "Dreamlifterは双操縦輪、主要6面表示器、幅広い中央ペデスタルを持つ747-400操縦席を継承します。写真は同型ファミリー配置です。"),
            ("它不像 Beluga 把駕駛艙移到貨艙下方；駕駛艙仍在 747 上層甲板前端，因此正面窗帶位置很高。", "Unlike the Beluga, its cockpit was not lowered beneath the hold; it remains at the front of the 747 upper deck, placing the windows high above the nose.", "Belugaと違って操縦席は貨物室下へ移されず、747上層前部に残るため窓位置が高いです。"),
            [("正副駕駛各有大型駕駛盤。", "Each pilot has a large control yoke.", "両席に大型操縦輪があります。"), ("747-400 以六具主要電子顯示器為核心。", "Six primary electronic displays define the 747-400 panel.", "747-400計器盤は主要6面電子表示器が中心です。"), ("駕駛艙照片應視為 747-400 家族布局參考。", "Treat the cockpit photograph as a 747-400-family layout reference.", "操縦席写真は747-400ファミリー配置の参考です。")],
        ),
        "windshield": identify(
            ("Dreamlifter 的駕駛艙窗位於 747 上層甲板最前端，窗帶高高壓在機鼻上方；側面可同時看到上層窗與下層機鼻貨艙外殼。", "The Dreamlifter's cockpit glazing sits at the front of the 747 upper deck, high above the nose; side views show the elevated window band over the lower nose shell.", "操縦席窓は747上層前端で機首より高く、側面では高い窓帯と下部機首外殻を同時に確認できます。"),
            ("Beluga 的窗帶位於貨艙隆起下方低處；Dreamlifter 則位於機鼻上方高處。兩者的窗帶高度關係正好相反。", "The Beluga's windows sit low beneath its cargo bulge; the Dreamlifter's sit high above the nose—the opposite vertical relationship.", "Belugaは貨物膨らみ下の低位置、Dreamlifterは機首上の高位置で、窓帯の上下関係が逆です。"),
            [("正面風擋位於短上層甲板前端。", "Forward panes cap the short upper deck.", "正面風防は短い上層甲板前端です。"), ("側窗高於主甲板艙門與下層窗列。", "Side panes sit above the main-deck door and lower window row.", "側窓は主甲板扉と下層窓列より高いです。"), ("搭配四具引擎即可排除 Beluga。", "Four engines immediately rule out the Beluga.", "4発と組み合わせればBelugaではありません。")],
        ),
        "fuselage": identify(
            ("Dreamlifter 貨艙容積約 1,840 m³，內部截面約 6.3 × 6.9 m、可用長度約 30 m；整個後機身由鉸鏈向左側旋開裝卸。", "The Dreamlifter offers about 1,840 m³ with an approximately 6.3 × 6.9 m cross-section and 30 m usable length; the aft fuselage hinges open sideways for loading.", "貨物室は約1,840 m³、断面約6.3 × 6.9 m、長さ約30 mで、後部胴体全体が横へ開きます。"),
            ("它運送 787 機翼與機身段等大體積、相對不重的組件，因此追求的是容積而非傳統貨機的最大重量。", "It carries bulky, relatively light 787 wings and fuselage sections, prioritising volume rather than conventional freighter payload mass.", "787の翼や胴体区画など大型で比較的軽い部品を運び、通常貨物機の重量より容積を重視します。"),
            [("尾部側開門是最重要結構特徵。", "The swing-tail door is the defining structure.", "横開き尾部が最大の構造特徴です。"), ("上半機身從駕駛艙後方一路巨大隆起。", "The upper fuselage swells dramatically behind the cockpit.", "操縦席後方から上部胴体が大きく膨らみます。"), ("下層貨艙仍可裝載一般貨物。", "The lower hold can still carry conventional cargo.", "下部貨物室には通常貨物も積載できます。")],
        ),
        "engine": identify(
            ("四架 Dreamlifter 均使用四具 Pratt & Whitney PW4062／PW4062A 高旁通比渦扇，兩具一組掛在每側 747-400 主翼下。", "All four Dreamlifters use four Pratt & Whitney PW4062/PW4062A high-bypass turbofans, two beneath each 747-400 wing.", "4機のDreamlifterはいずれもPratt & Whitney PW4062／PW4062Aを4基、各翼下に2基ずつ装備します。"),
            ("資料不能沿用採 GE 或 Rolls-Royce 引擎的其他 747-400；Dreamlifter 實際四架皆為 Pratt & Whitney 動力。", "Do not inherit engine data from GE- or Rolls-Royce-powered 747-400s; every Dreamlifter is Pratt & Whitney-powered.", "GEやRolls-Royce搭載747-400の情報を流用せず、Dreamlifter全機はPratt & Whitney仕様です。"),
            [("四具引擎、每側兩具。", "Four engines, two per wing.", "4発で各翼2基です。"), ("型號為 PW4062／PW4062A。", "The type is PW4062/PW4062A.", "型式はPW4062／PW4062Aです。"), ("圓形短艙保留 747-400 比例。", "Round nacelles retain 747-400 proportions.", "円形ナセルは747-400の比率です。")],
        ),
        "wingtip": identify(
            ("Dreamlifter 改裝時拆除了一般 747-400 高聳的翼尖小翼，主翼以平直、略帶端部整形的翼尖收尾。", "The Dreamlifter conversion removed the standard 747-400's tall winglets, leaving clean, nearly flat tips with simple fairing.", "Dreamlifter改造では通常747-400の高いウイングレットを撤去し、簡潔でほぼ平らな翼端になりました。"),
            ("『747-400 外型卻沒有垂直翼尖小翼』是辨識 Dreamlifter 的重要輔助特徵；但部分 747-400D 也無小翼，仍須看巨型貨艙。", "A 747-400-like aircraft without vertical winglets supports Dreamlifter identification, though some 747-400Ds also lack them; confirm the giant cargo body.", "747-400形で垂直ウイングレットがない点は手掛かりですが、747-400Dも未装備なので巨大貨物胴体を確認します。"),
            [("沒有一般 747-400 的高式翼尖小翼。", "No standard 747-400 tall winglet.", "通常747-400の高いウイングレットはありません。"), ("翼尖輪廓接近平直。", "The tip remains nearly flat.", "翼端はほぼ平らです。"), ("應搭配膨大機身與四發判讀。", "Confirm with the swollen body and four engines.", "巨大胴体と4発も合わせて確認します。")],
        ),
        "wing": identify(
            ("Dreamlifter 保留 747-400 的 64.44 m 後掠主翼與四發配置；巨大貨艙讓機翼看起來較低且較薄。", "The Dreamlifter retains the 747-400's 64.44 m swept four-engine wing, which appears low and thin beneath the enormous cargo body.", "Dreamlifterは747-400の翼幅64.44 m後退4発翼を保ち、巨大貨物胴体の下で低く薄く見えます。"),
            ("Beluga 只有兩具引擎且翼展 44.84 m；從正後方或下方看主翼與引擎配置即可快速區分。", "The Beluga has only two engines and a 44.84 m span; rear or underside views separate the pair quickly.", "Belugaは双発・翼幅44.84 mで、後方や下面から主翼とエンジン配置を見ればすぐ区別できます。"),
            [("每側翼下有兩具引擎。", "Two engines hang beneath each wing.", "各翼下に2基のエンジンがあります。"), ("後掠角與 747-400 基本相同。", "Sweep is essentially that of the 747-400.", "後退角は基本的に747-400と同じです。"), ("大型襟翼支援重型低速起降。", "Large flaps support heavy low-speed operations.", "大型フラップが重量機の低速運用を支えます。")],
        ),
        "vstab": identify(
            ("Dreamlifter 保留大型 747 垂直尾翼，尾翼本體並未像貨艙般膨大；相對巨型後機身，垂尾視覺上顯得窄而高。", "The Dreamlifter retains the large 747 vertical fin; because the cargo body is greatly enlarged, the fin appears relatively narrow and tall.", "Dreamlifterは747の大型垂直尾翼を残し、巨大化した貨物胴体に対して細く高く見えます。"),
            ("從正後方可同時看到中央垂尾、四具引擎與圓鼓的貨艙截面，這組輪廓與 Beluga 的尾端輔助小翼完全不同。", "From aft, the single centre fin, four engines and bulbous cargo cross-section contrast sharply with the Beluga's auxiliary tail finlets.", "後方からの中央垂尾1枚、4発、丸い貨物断面は、Belugaの補助尾翼端フィンと明確に異なります。"),
            [("單一中央垂直尾翼。", "A single central vertical fin.", "中央垂直尾翼は1枚です。"), ("沒有 Beluga 的水平尾翼端部小翼。", "No Beluga-style tailplane finlets.", "Beluga型の水平尾翼端フィンはありません。"), ("尾根前方緊接巨大貨艙尾段。", "The fin root meets the enlarged aft cargo shell.", "垂尾根元は巨大な後部貨物外殻へ接続します。")],
        ),
        "hstab": identify(
            ("Dreamlifter 水平尾翼保留 747 低置後掠布局，與後機身共同位於可旋開的尾段；裝卸時整個尾段向側面移開。", "The Dreamlifter retains the 747's low swept tailplanes, attached to the aft section that swings sideways during loading.", "水平尾翼は747の低位置後退配置を保ち、積載時に横へ旋回する後部区画に付いています。"),
            ("尾門的鉸鏈、鎖定與重新對準精度是 Dreamlifter 結構核心；關閉後仍需恢復完整飛行載荷路徑。", "Hinging, locking and precise realignment of the tail are structural essentials because the closed section must restore the full flight-load path.", "尾部のヒンジ、ロック、精密再結合は、閉鎖後に飛行荷重経路を戻すため重要です。"),
            [("水平尾翼低置於機尾兩側。", "Tailplanes mount low on both sides.", "水平尾翼は機尾両側の低位置です。"), ("沒有端部輔助垂直翼。", "There are no auxiliary vertical tip fins.", "端部補助垂直フィンはありません。"), ("尾段可隨貨艙門整體旋開。", "The entire tail section swings with the cargo door.", "尾部区画全体が貨物扉とともに旋回します。")],
        ),
        "gear": identify(
            ("Dreamlifter 沿用 747-400 的 18 輪起落架：前腳雙輪，翼下與機身下共有四組四輪主轉向架，用來分散巨大重量。", "The Dreamlifter retains the 747-400's 18-wheel gear: twin nose wheels plus four four-wheel main bogies beneath the wings and fuselage.", "Dreamlifterは747-400の18輪脚を継承し、前脚2輪と翼下・胴体下の4組4輪主脚で重量を分散します。"),
            ("最大起飛重量約 364,235 kg；四組主腳與 18 輪配置遠多於 Beluga 的兩組主腳、10 輪。", "Maximum takeoff weight is about 364,235 kg; four main bogies and 18 wheels greatly exceed the Beluga's two bogies and ten wheels.", "最大離陸重量は約364,235 kgで、4組主脚・18輪はBelugaの2組・10輪より大幅に多いです。"),
            [("前腳為雙輪。", "The nose gear has twin wheels.", "前脚は2輪です。"), ("兩組翼腳加兩組機身腳。", "Two wing bogies are supplemented by two body bogies.", "翼脚2組に胴体脚2組を加えます。"), ("總輪數為 18 輪。", "Total wheel count is eighteen.", "総輪数は18輪です。")],
        ),
    },
})


CONTENT.update({
    "b744": {
        "overview": identify(
            ("747-400 以機首上方延伸的上層甲板『駝峰』、四具引擎與大型垂直翼尖小翼最容易辨認；全長約 70.67 m、翼展約 64.44 m。", "The 747-400 is most readily identified by its extended upper-deck hump, four engines and tall vertical winglets. It is about 70.67 m long with a 64.44 m span.", "747-400は延長された上部デッキのこぶ、4発エンジン、大型垂直ウイングレットが最も明確で、全長約70.67 m、翼幅約64.44 mです。"),
            ("對比 A340-600，747-400 機身較短粗、駕駛艙位置更高且有雙層前機身；A340-600 則是沒有駝峰的超長單層機身。", "Against the A340-600, the 747-400 is shorter and bulkier, with a high cockpit and double-deck forward fuselage; the A340-600 has an exceptionally long single-deck profile.", "A340-600に比べ747-400は短く太く、操縦席が高い二階建て前部胴体を持ちます。A340-600はこぶのない超長い単層胴体です。"),
            [("上層甲板窗列從機首後方延伸至主翼前。", "The upper-deck window row extends aft toward the wing.", "上部デッキ窓列が機首後方から主翼手前まで続きます。"), ("四具引擎吊掛於大後掠翼下。", "Four engines hang below a strongly swept wing.", "強い後退主翼下に4基のエンジンがあります。"), ("多數遠程型有直立翼尖小翼；747-400D 例外。", "Most long-range versions have upright winglets; the 747-400D is an exception.", "長距離型の多くは直立ウイングレットを持ち、747-400Dは例外です。")],
        ),
        "cockpit": identify(
            ("747-400 是首款採兩人制玻璃駕駛艙的 747，保留 Boeing 駕駛盤與中央操縱柱，典型配置有六具大型 CRT、EICAS 與四發推力桿。", "The 747-400 introduced a two-crew glass flight deck to the 747 family, retaining Boeing yokes and control columns with six large CRTs, EICAS and four thrust levers.", "747-400は747初の2名乗務グラスコックピットで、Boeing式操縦輪、6面大型CRT、EICAS、4本のスラストレバーを備えます。"),
            ("與 A340-600 的側桿與桌板相比，駕駛盤和四支推力桿是最直觀差異；螢幕改裝狀態則可能不同。", "Yokes and four thrust levers are the clearest contrast with the A340-600's sidesticks and tray tables; display retrofits may vary.", "A340-600のサイドスティックとテーブルに対し、操縦輪と4本のスラストレバーが最も明確です。画面は改修で異なる場合があります。"),
            [("正副駕駛前方均有大型駕駛盤。", "A large yoke sits ahead of each pilot.", "両操縦席正面に大型操縦輪があります。"), ("中央 EICAS 監控四具引擎與系統。", "Central EICAS screens monitor four engines and aircraft systems.", "中央EICASが4発エンジンと機体システムを監視します。"), ("高置座艙源自上層甲板機首位置。", "The flight deck sits high in the forward upper deck.", "操縦席は前方上部デッキの高い位置にあります。")],
        ),
        "windshield": identify(
            ("747-400 的六片駕駛艙窗位於機鼻上方高處，正面窗較直立、外側窗沿上層甲板向後折轉；下方仍可看到圓鈍主甲板機鼻。", "The 747-400's six cockpit panes sit high above the nose. Upright front panes turn aft along the upper deck while the rounded main-deck nose remains below.", "747-400の6枚窓は機首上方の高い位置にあり、直立気味の前面窓から上部デッキ側面へ折れ、下には丸い主デッキ機首が見えます。"),
            ("高置窗帶加上窗下方的大面積機鼻，是任何 A340 都沒有的特徵；即使只看到前半機身也很可靠。", "The high window belt and large expanse of nose below it are absent from every A340 and remain reliable even in a cropped forward view.", "高い窓帯とその下の大きな機首面はA340にはなく、前部だけでも信頼できる識別点です。"),
            [("窗帶位於上層甲板，離主甲板艙門很高。", "The glazing is on the upper deck, high above main-deck doors.", "窓帯は上部デッキにあり、主デッキ扉より高い位置です。"), ("正面風擋較方正，中央接縫近垂直。", "Forward panes are fairly square with a near-vertical centre seam.", "前面窓は比較的四角く中央継ぎ目はほぼ垂直です。"), ("側窗後方緊接上層甲板舷窗。", "Upper-deck cabin windows continue immediately aft of the side panes.", "側窓後方に上部デッキ客室窓が続きます。")],
        ),
        "fuselage": identify(
            ("747-400 機身外寬約 6.5 m，前段為局部雙層：主甲板上方的加長上層甲板形成明顯駝峰，典型主甲板經濟艙為 3-4-3。", "The 747-400 fuselage is about 6.5 m wide and partially double-decked. Its stretched upper deck forms the hump above a main deck typically arranged 3-4-3 in economy.", "747-400の胴体幅は約6.5 mで前部が部分二階建てです。延長上部デッキがこぶを作り、主デッキのエコノミーは通常3-4-3です。"),
            ("747-400 客機上層甲板比早期 747 明顯更長；貨機通常保留短駝峰，不能把所有 747-400 外型視為完全相同。", "Passenger 747-400s have a much longer upper deck than early 747s; freighters generally retain the short hump, so not every 747-400 has the same side profile.", "旅客型747-400の上部デッキは初期747より長く、貨物型は通常短いこぶのため、全機が同じ側面形ではありません。"),
            [("上下兩排窗只出現在前機身。", "Two window rows appear only on the forward fuselage.", "前部胴体だけに上下2列の窓があります。"), ("主甲板直徑與艙門尺度大於 A340。", "Main-deck diameter and doors are larger than the A340's.", "主デッキ胴体径と扉はA340より大きいです。"), ("前段駝峰向主翼前方平滑下降。", "The forward hump blends down ahead of the wing.", "前部のこぶは主翼手前で滑らかに低くなります。")],
        ),
        "engine": identify(
            ("747-400 可選 GE CF6-80C2、Pratt & Whitney PW4000 或 Rolls-Royce RB211-524；四具短艙分置於主翼下，後緣皆為傳統平滑輪廓。", "The 747-400 could use GE CF6-80C2, Pratt & Whitney PW4000 or Rolls-Royce RB211-524 engines. Four conventional smooth-edged nacelles sit beneath the wing.", "747-400はCF6-80C2、PW4000、RB211-524を選択でき、4基の従来型滑らかなナセルが主翼下にあります。"),
            ("參考照片標題雖寫 Trent，實際機型分類與短艙是 Qantas 747-400 的 Rolls-Royce RB211；辨識時應看短艙形狀而非檔名。", "Although the source title says Trent, the Qantas 747-400 installation is a Rolls-Royce RB211; identify the nacelle from the aircraft and shape rather than the filename.", "出典名はTrentですが、Qantas 747-400の搭載機はRolls-Royce RB211です。ファイル名ではなく機体とナセル形状で判断します。"),
            [("四具引擎是與雙發 747 後繼機的根本差異。", "Four engines fundamentally separate it from later twinjets.", "4発であることが後継双発機との根本的な差です。"), ("不同引擎的進氣口、整流罩與排氣段不同。", "Inlet, cowling and exhaust details vary by engine option.", "エンジン選択で吸気口、カウリング、排気部が異なります。"), ("沒有 747-8 GEnx 的鋸齒狀短艙後緣。", "It lacks the serrated GEnx nacelle edges of the 747-8.", "747-8のGEnxにある鋸歯状ナセル後縁はありません。")],
        ),
        "wingtip": identify(
            ("長程 747-400 的翼尖先向外延伸，再接一片高而近乎垂直的梯形小翼；這是區分 747-400 與早期 747、747-8 的重要線索。", "Long-range 747-400 wings have a tip extension capped by a tall near-vertical trapezoidal winglet, a key distinction from early 747s and the raked-tip 747-8.", "長距離747-400は翼端延長部に高いほぼ垂直の台形ウイングレットを持ち、初期747やレイクド翼端の747-8と区別できます。"),
            ("日本國內線 747-400D 為了高頻起降取消翼尖小翼；看到沒有小翼的 747 仍需核對上層甲板與子型。", "The high-cycle domestic 747-400D omitted winglets; a winglet-free 747 therefore still requires upper-deck and variant checks.", "高頻度国内線用747-400Dはウイングレットを省略したため、未装備747でも上部デッキと型式確認が必要です。"),
            [("小翼高大、直立，頂端略向後收。", "The winglet is tall, upright and tapers slightly aft.", "ウイングレットは高く直立し上端が後方へ細くなります。"), ("翼尖仍有明顯水平延伸段。", "A visible horizontal tip extension precedes the winglet.", "ウイングレット手前に水平翼端延長があります。"), ("747-8 則使用水平延伸的斜削翼尖。", "The 747-8 instead uses a horizontally extended raked tip.", "747-8は水平に延びるレイクド翼端です。")],
        ),
        "wing": identify(
            ("747-400 主翼翼展約 64.44 m，後掠角大、翼根厚，四具引擎與複雜的前後緣增升裝置沿翼面配置。", "The 747-400 wing spans about 64.44 m, with strong sweep, a thick root, four engines and extensive leading- and trailing-edge high-lift devices.", "747-400の主翼幅は約64.44 mで、強い後退角、厚い翼根、4発エンジン、大規模な前後縁高揚力装置を持ちます。"),
            ("翼展與 A340-600 接近，不能單看寬度；747 的翼根接在更粗機身上，外翼末端通常有高大直立小翼。", "Span is close to the A340-600's, so width alone is insufficient. The 747 wing joins a much broader fuselage and usually ends in a tall upright winglet.", "翼幅はA340-600に近いため幅だけでは不十分で、より太い胴体への翼根と高い直立ウイングレットを確認します。"),
            [("每側主翼下各有兩具引擎。", "Two engines hang beneath each wing.", "各主翼下に2基ずつエンジンがあります。"), ("外翼後掠並接翼尖延伸與小翼。", "The swept outer panel ends in a tip extension and winglet.", "後退外翼は翼端延長とウイングレットへ続きます。"), ("大面積襟翼與擾流板支援重型機低速飛行。", "Large flaps and spoilers support the heavy aircraft at low speed.", "大型フラップとスポイラーが重量機の低速飛行を支えます。")],
        ),
        "vstab": identify(
            ("747-400 垂直尾翼高大、前緣大幅後掠，根部建立在寬厚後機身上；相對駝峰機鼻，尾部輪廓仍是傳統單垂尾。", "The 747-400 has a large strongly swept fin rooted in a broad aft fuselage; despite the forward hump, the rear remains a conventional single-fin empennage.", "747-400の垂直尾翼は大型で前縁後退が強く、太い後部胴体に接続します。前部のこぶとは対照的に通常の単垂尾です。"),
            ("塗裝常讓垂尾看起來更顯眼，但真正可比較的是粗尾錐、較寬根部與 747 特有前機身。", "Livery makes the fin prominent, but the useful cues are the broad root, thick tailcone and unmistakable 747 forward fuselage.", "塗装よりも幅広い根元、太い尾部、747特有の前部胴体を比較します。"),
            [("前緣後掠明顯，頂端近方形。", "The leading edge is strongly swept and the tip nearly square.", "前縁後退が強く上端はほぼ角形です。"), ("根部與寬大的後機身平滑融合。", "The root blends into the broad aft fuselage.", "根元は幅広い後部胴体へ滑らかにつながります。"), ("尾錐末端可見 APU 排氣口。", "The tailcone ends at the APU exhaust.", "テールコーン先端にAPU排気口があります。")],
        ),
        "hstab": identify(
            ("747-400 的低置水平尾翼後掠且面積大，從粗壯尾錐兩側向外收尖；下方全機照片可同時看見尾翼、四發與多組主起落架。", "The 747-400's large low-mounted tailplanes sweep and taper from a broad tailcone. An underside view also reveals four engines and multiple main-gear bogies.", "747-400の大型低位置水平尾翼は太い尾部から後退し細くなり、下面写真では4発と複数主脚も同時に確認できます。"),
            ("A340-600 也是傳統低置水平尾翼，因此安裝位置本身無法判型；應比較尾錐粗細與前機身。", "The A340-600 also has a conventional low tailplane, so mounting position alone is not diagnostic; compare tailcone thickness and forward fuselage.", "A340-600も通常の低位置尾翼のため、取付位置だけでなく尾部の太さと前部胴体を比較します。"),
            [("尾翼展幅大，翼根非常厚。", "The tailplane is broad with a very thick root.", "水平尾翼は大きく翼根が非常に厚いです。"), ("後緣由多段升降舵構成。", "The trailing edge contains segmented elevators.", "後縁は分割された昇降舵で構成されます。"), ("與 747 粗機身形成厚重尾部比例。", "It forms a massive empennage with the wide 747 fuselage.", "太い747胴体と大型尾部を形成します。")],
        ),
        "gear": identify(
            ("747-400 共 18 輪：前起落架雙輪，四組主起落架各四輪；兩組位於翼下、兩組位於機身下方。", "The 747-400 has 18 wheels: twin nose wheels and four four-wheel main bogies, two wing-mounted and two body-mounted.", "747-400は計18輪で、前脚2輪、主脚4組各4輪（翼下2組・胴体下2組）です。"),
            ("A340-600 只有三組四輪主腳、共 14 輪；近距離數主轉向架組數，是兩者最可靠差異之一。", "The A340-600 has only three four-wheel main bogies and 14 wheels total. Counting main bogie groups is one of the strongest close-range differences.", "A340-600は4輪主脚3組、計14輪です。主脚ボギー数は近距離で最も確実な差の一つです。"),
            [("左右翼下各一組四輪主腳。", "One four-wheel bogie sits beneath each wing.", "左右主翼下に各1組4輪主脚があります。"), ("機身中央另有左右兩組四輪主腳。", "Two additional four-wheel bogies sit beneath the fuselage.", "胴体下にさらに左右2組の4輪主脚があります。"), ("全部放下時可見四組主轉向架並列。", "All four main bogies are visible when the gear is extended.", "脚下げ時に4組の主ボギーが並びます。")],
        ),
    },
    "a346": {
        "overview": identify(
            ("A340-600 是極修長的單層四發廣體客機，全長約 75.36 m、翼展約 63.45 m；沒有 747 駝峰，四具 Trent 500 與中置主起落架是核心特徵。", "The A340-600 is an exceptionally long single-deck four-engine widebody, about 75.36 m long with a 63.45 m span. It lacks the 747 hump and is defined by four Trent 500s and a centre main gear.", "A340-600は全長約75.36 m、翼幅約63.45 mの非常に長い単層4発ワイドボディで、747のこぶがなく、4基のTrent 500と中央主脚が特徴です。"),
            ("它比 747-400 更長但機身更窄，側面像一支非常長的鉛筆；辨識時把『無駝峰長機身＋四發＋中央主腳』一起確認。", "It is longer but narrower than the 747-400, giving a pencil-like side profile. Confirm the hump-free long body, four engines and centre gear together.", "747-400より長く細いため鉛筆のように見え、こぶのない長胴体、4発、中央主脚を組み合わせて確認します。"),
            [("全機只有一排客艙窗，沒有上層甲板。", "A single cabin-window row runs the full fuselage with no upper deck.", "上部デッキはなく客室窓列は1列です。"), ("四具 Trent 500 均勻分布於主翼下。", "Four Trent 500s are spaced beneath the wing.", "4基のTrent 500が主翼下に配置されます。"), ("超長機身前後伸出主翼很遠。", "The extremely long fuselage extends far ahead of and behind the wing.", "超長胴体が主翼の前後へ大きく伸びます。")],
        ),
        "cockpit": identify(
            ("A340-600 駕駛艙延續 Airbus 側桿與桌板設計，採六具顯示器、中央 ECAM 與四發推力桿；飛行員正前方沒有駕駛盤。", "The A340-600 flight deck follows Airbus sidestick and tray-table design with six displays, central ECAM and four thrust levers; no yokes sit ahead of the pilots.", "A340-600の操縦席はAirbus式サイドスティックとテーブル、6面表示器、中央ECAM、4本のスラストレバーを持ち、正面に操縦輪はありません。"),
            ("A330 與 A340 家族座艙高度共通化，內部單靠面板很難判子型；四支推力桿與引擎頁面才顯示四發身分。", "A330 and A340 cockpits are highly common, so the panel alone rarely identifies the variant; four thrust levers and four-engine system pages reveal the A340.", "A330とA340の操縦席は共通性が高く、4本のスラストレバーと4発用表示でA340と確認します。"),
            [("側桿位於左右側壁。", "Sidesticks are mounted on the sidewalls.", "サイドスティックは左右側壁にあります。"), ("正前方桌板取代 Boeing 駕駛盤。", "Tray tables replace Boeing-style yokes ahead of the pilots.", "正面はBoeing式操縦輪ではなくテーブルです。"), ("中央台有四支引擎推力桿。", "Four engine thrust levers occupy the centre pedestal.", "中央台に4本のエンジンスラストレバーがあります。")],
        ),
        "windshield": identify(
            ("A340-600 使用經典 Airbus 六片窗帶，正面風擋呈斜邊梯形，外側窗沿圓鈍機鼻平滑包向側面；位置接近單層機身中心線。", "The A340-600 uses classic Airbus six-pane glazing: slanted trapezoidal front windscreens flow around a rounded nose into the side panes at normal single-deck height.", "A340-600はAirbus伝統の6枚窓で、斜辺台形の前面窓が丸い機首に沿って側面へ滑らかにつながり、単層胴体の通常高さにあります。"),
            ("與 747-400 最大差異不是窗片數，而是窗帶高度：A340 下方只有一般圓鼻，747 窗下還有巨大的主甲板機鼻。", "Pane count is less important than height: below the A340 glazing is a normal rounded nose, while the 747 has a vast main-deck nose beneath its high cockpit.", "747-400との差は枚数より高さで、A340窓下は通常の丸い機首、747は高い操縦席下に大きな主デッキ機首があります。"),
            [("中央接縫短，主風擋向外上方傾斜。", "The centre seam is short and the main panes slope outward and upward.", "中央継ぎ目は短く主窓は外上方へ傾きます。"), ("外側窗帶沿圓鼻平順包覆。", "Outer panes wrap smoothly around the rounded nose.", "外側窓帯が丸い機首を滑らかに包みます。"), ("窗後直接接單排客艙舷窗。", "A single cabin-window row continues aft.", "後方には1列の客室窓が続きます。")],
        ),
        "fuselage": identify(
            ("A340-600 機身外寬約 5.64 m，典型經濟艙為 2-4-2；全長 75.36 m 曾使它成為世界最長客機，側面呈極細長的單層輪廓。", "The A340-600 fuselage is about 5.64 m wide, typically 2-4-2 in economy, and its 75.36 m length once made it the world's longest airliner, producing an extremely slender single-deck profile.", "A340-600の胴体幅は約5.64 m、エコノミーは通常2-4-2で、全長75.36 mによりかつて世界最長の旅客機となった非常に細長い単層形です。"),
            ("與較短 A340-500 共用基本翼與尾部語彙；辨識 -600 應看主翼前後特別長的機身和更多艙門間距。", "It shares basic wing and tail styling with the shorter A340-500; identify the -600 by the exceptionally long fuselage ahead of and behind the wing and wider door spacing.", "短いA340-500と主翼・尾部形状を共有するため、主翼前後の極端な胴体長とドア間隔で-600を判別します。"),
            [("全長比 747-400 約長 4.7 m。", "It is roughly 4.7 m longer than the 747-400.", "747-400より約4.7 m長いです。"), ("只有單排窗，沒有雙層駝峰。", "There is one window row and no double-deck hump.", "窓列は1列で二階建てのこぶはありません。"), ("翼身整流罩位於超長機身中段。", "The wing-body fairing sits near the middle of the very long body.", "翼胴フェアリングは超長胴体の中央付近です。")],
        ),
        "engine": identify(
            ("A340-600／-500 只使用 Rolls-Royce Trent 500 系列，四具引擎短艙較圓、後緣平滑；不像早期 A340-200／-300 的小型 CFM56。", "The A340-500/-600 exclusively uses Rolls-Royce Trent 500 engines. Its four rounded smooth-edged nacelles are much larger than the CFM56s on early A340-200/-300s.", "A340-500／-600はRolls-Royce Trent 500専用で、4基の丸い滑らかなナセルは初期A340-200／-300のCFM56より大型です。"),
            ("與 747-400 不同，A340-600 沒有三種引擎選項；看到四具尺寸一致的 Trent 500 配超長 Airbus 機身，即可快速縮小範圍。", "Unlike the 747-400, the A340-600 has no alternative engine families. Four identical Trent 500s beneath the long Airbus fuselage strongly narrow identification.", "747-400と異なり代替エンジンはなく、超長Airbus胴体下の4基Trent 500が強い識別点です。"),
            [("四具引擎均為 Trent 500 家族。", "All four engines belong to the Trent 500 family.", "4基すべてTrent 500系です。"), ("短艙圓潤，後緣沒有鋸齒。", "Nacelles are rounded with smooth trailing edges.", "ナセルは丸く後縁に鋸歯はありません。"), ("尺寸明顯大於 A340-300 的 CFM56。", "They are visibly larger than A340-300 CFM56 nacelles.", "A340-300のCFM56より明らかに大型です。")],
        ),
        "wingtip": identify(
            ("A340-600 主翼末端有小型直立三角翼梢，輪廓由翼端向上收尖；它比 747-400 的高大梯形小翼更短、更像翼尖延伸的一部分。", "The A340-600 ends in a small upright triangular tip device that tapers upward. It is much shorter than the 747-400's tall trapezoidal winglet and looks integrated with the tip.", "A340-600は上方へ細くなる小型直立三角翼端を持ち、747-400の高い台形ウイングレットより短く翼端と一体的です。"),
            ("A340-500／-600 翼尖與 A330ceo／A340 家族有相近 Airbus 語彙；必須再用四發與超長機身確認。", "The A340-500/-600 tip shares Airbus family styling with A330ceos and other A340s; confirm four engines and the very long fuselage.", "A330ceoや他A340と似たAirbus翼端形状のため、4発と超長胴体を追加確認します。"),
            [("翼梢短小並近乎垂直。", "The tip device is short and nearly vertical.", "翼端装置は短くほぼ垂直です。"), ("頂端向後收尖，不是高大梯形板。", "It tapers aft rather than forming a tall trapezoidal blade.", "上端は後方へ細く、高い台形板ではありません。"), ("與 747-400 小翼高度差異明顯。", "Its height is clearly less than the 747-400 winglet's.", "747-400ウイングレットより明らかに低いです。")],
        ),
        "wing": identify(
            ("A340-600 主翼翼展約 63.45 m，與 747-400 接近；翼下四具 Trent 500、外翼小型直立翼梢及細長機身比例形成獨特平面輪廓。", "The A340-600 spans about 63.45 m, close to the 747-400. Four Trent 500s, small upright tips and a very slender fuselage define its planform.", "A340-600の翼幅は約63.45 mで747-400に近く、4基Trent 500、小型直立翼端、細長い胴体が独特の平面形を作ります。"),
            ("下方看時，翼展相近但 A340 機身遠比 747 窄長；主翼後方還能看到四輪中置主腳艙區域。", "From below, similar span contrasts with a much narrower and longer fuselage than the 747; the four-wheel centre-gear bay is also visible aft of the wing centre.", "下面では翼幅が近い一方、A340胴体は747より細長く、主翼中央後方に4輪中央脚格納部も見えます。"),
            [("每側兩具引擎間距均勻。", "Two engines are evenly spaced beneath each wing.", "各主翼下の2基エンジンは均等に配置されます。"), ("翼根厚並與大型翼身整流罩連接。", "A thick root joins a substantial wing-body fairing.", "厚い翼根が大型翼胴フェアリングへつながります。"), ("外翼末端為短小直立三角翼梢。", "The outer wing ends in a short upright triangular tip.", "外翼端は短い直立三角翼端です。")],
        ),
        "vstab": identify(
            ("A340-600 的垂直尾翼高大後掠，根部以寬背鰭接入較細後機身；配合極長機身，垂尾看起來比 747-400 更纖細。", "The A340-600 has a tall swept fin with a broad dorsal root blending into a relatively narrow aft fuselage. Against the very long body it looks slimmer than the 747-400 fin.", "A340-600の垂直尾翼は高く後退し、広い背びれ根元が比較的細い後部胴体へつながり、747-400より細身に見えます。"),
            ("A340-500 與 -600 尾翼相近，不能單靠垂尾判子型；需看機身長度與中置主腳。", "A340-500 and -600 fins are similar, so variant identification requires fuselage length and centre-gear configuration.", "A340-500と-600の垂尾は似るため、胴体長と中央主脚で子型を確認します。"),
            [("前緣後掠，頂端略方。", "The leading edge is swept and the tip slightly squared.", "前縁は後退し上端はやや角形です。"), ("根部背鰭沿後機身向前延伸。", "The dorsal fillet extends forward along the aft fuselage.", "根元背びれが後部胴体に沿って前方へ伸びます。"), ("尾錐細於 747，末端為 APU 排氣口。", "The tailcone is slimmer than the 747's and ends at the APU exhaust.", "尾部は747より細く先端にAPU排気口があります。")],
        ),
        "hstab": identify(
            ("A340-600 的低置水平尾翼從細長尾錐兩側伸出，後掠並向外收尖；相對超長機身看起來比 747 的水平尾翼輕巧。", "The A340-600's low-mounted tailplanes sweep and taper from a slender tailcone. Against the exceptionally long fuselage they appear lighter than the 747's tailplanes.", "A340-600の低位置水平尾翼は細い尾部から後退し細くなり、超長胴体に対して747より軽快に見えます。"),
            ("兩者都是傳統尾翼布局，水平尾翼只能作輔助；前機身有無駝峰與主腳組數更可靠。", "Both use conventional tail layouts, so the tailplane is secondary; the forward hump and number of main bogies are more reliable.", "両機とも通常尾翼のため補助的で、前部こぶの有無と主脚ボギー数の方が確実です。"),
            [("尾翼後掠且翼尖收細。", "The tailplane is swept and tapers at the tip.", "水平尾翼は後退し翼端で細くなります。"), ("翼根接在較窄的後機身。", "The root joins a relatively narrow aft fuselage.", "翼根は比較的細い後部胴体に接続します。"), ("尾部整體比例比 747 修長。", "The overall empennage proportion is more slender than the 747's.", "尾部全体は747より細長い比率です。")],
        ),
        "gear": identify(
            ("A340-600 共 14 輪：前腳雙輪，左右翼下主腳各四輪，機身中線另有一組四輪主腳；中置四輪是 -500／-600 的重要特徵。", "The A340-600 has 14 wheels: twin nose wheels, four-wheel wing gears on each side and one four-wheel centreline body gear. The four-wheel centre gear is a key -500/-600 cue.", "A340-600は計14輪で、前脚2輪、左右翼下主脚各4輪、胴体中央主脚4輪です。4輪中央脚は-500／-600の重要特徴です。"),
            ("早期 A340-200／-300 的中置主腳為雙輪；747-400 則有兩組機身主腳、四組主轉向架，因此不能只看到中央輪就判 747。", "Earlier A340-200/-300s use a twin-wheel centre gear, while the 747-400 has two body gears and four main bogies. A centre gear alone does not imply a 747.", "初期A340-200／-300の中央脚は2輪、747-400は胴体脚2組・主ボギー4組です。中央輪だけで747とは判断できません。"),
            [("左右翼下各一組四輪主腳。", "One four-wheel main bogie sits beneath each wing.", "左右主翼下に各1組4輪主脚があります。"), ("機身中線只有一組四輪主腳。", "Only one four-wheel bogie sits on the fuselage centreline.", "胴体中心線には4輪主脚が1組だけです。"), ("三組主轉向架對比 747 的四組。", "Three main bogies contrast with the 747's four.", "主ボギー3組で747の4組と異なります。")],
        ),
    },
})


def clone_variant(source: str, replacements: tuple[tuple[str, str], ...]) -> dict:
    def replace(value):
        if isinstance(value, str):
            for old, new in replacements:
                value = value.replace(old, new)
            return value
        if isinstance(value, list):
            return [replace(item) for item in value]
        if isinstance(value, dict):
            return {key: replace(item) for key, item in value.items()}
        return value
    return replace(CONTENT[source])


CONTENT["b736"] = clone_variant("b738", (("737-800", "737-600"), ("A320", "A318")))
CONTENT["b736"].update({
    "overview": identify(
        ("737-600 是 737 Next Generation 家族最短的量產型，全長 31.24 m；短粗比例、低矮機身、扁平 CFM56-7B 短艙與收起後外露的主輪是主要輪廓。", "The 737-600 is the shortest production 737 Next Generation, 31.24 m long. Its stubby proportions, low stance, flattened CFM56-7B nacelles and exposed retracted main wheels define it.", "737-600は全長31.24 mで737 Next Generation最短の量産型です。短い胴体、低い姿勢、下面が平たいCFM56-7Bナセル、格納後も露出する主輪が特徴です。"),
        ("它只比 A318 短約 20 cm，肉眼不能靠全長分辨；機鼻、引擎底部、翼尖與主輪收納方式更可靠。", "It is only about 20 cm shorter than the A318, so length alone is unreliable; nose, nacelle underside, wingtips and gear stowage work better.", "A318より約20 cm短いだけなので全長だけでは判別できません。機首、ナセル下面、翼端、脚格納方式を見ます。"),
        [("737NG 家族中機身最短。", "Shortest fuselage in the 737NG family.", "737NGファミリー最短胴です。"), ("低矮姿態與扁平短艙很醒目。", "Low stance and flat nacelles stand out.", "低い姿勢と平たいナセルが目立ちます。"), ("主輪收起後仍可看見胎面。", "Main tyre faces remain visible when retracted.", "格納後も主輪面が見えます。")],
    ),
    "cockpit": identify(
        ("737-600 使用 737NG 共通的傳統駕駛盤玻璃座艙：正副駕駛前方各有駕駛盤，中央有油門、黑白配平輪與大量實體開關。", "The 737-600 uses the common 737NG yoke-equipped glass cockpit, with a yoke before each pilot, central throttles, black-and-white trim wheels and many physical controls.", "737-600は737NG共通の操縦輪式グラスコックピットで、各席の操縦輪、中央スロットル、白黒トリムホイール、多数の物理スイッチがあります。"),
        ("本頁座艙照片取自共通布局的 737-700；駕駛艙本身無法可靠區分 -600 與其他 NG 子型，但可立即與側桿式 A318 分開。", "The photo shows the common layout in a 737-700. The cockpit cannot reliably distinguish a -600 from other NG variants, but it immediately separates the sidestick A318.", "写真は共通配置の737-700です。操縦席だけで-600と他NGを区別できませんが、サイドスティック式A318とはすぐ区別できます。"),
        [("正副駕駛前方都有傳統駕駛盤。", "A conventional yoke sits before each pilot.", "両席正面に通常の操縦輪があります。"), ("中央保留大型配平輪。", "Large trim wheels remain on the centre pedestal.", "中央ペデスタルに大型トリムホイールがあります。"), ("大量實體旋鈕包圍玻璃顯示器。", "Many physical controls surround the glass displays.", "グラス表示器を多数の物理操作器が囲みます。")],
    ),
    "fuselage": identify(
        ("737-600 保留 737 的窄機身與每排六座截面，典型每側有前後主艙門及一個翼上逃生出口；翼前、翼後都只有很短的窗列。", "The 737-600 retains the narrow six-abreast 737 body, typically with forward/aft main doors and one overwing exit per side; window runs ahead of and behind the wing are very short.", "737-600は737共通の横6席狭胴で、通常は各側に前後ドアと翼上出口1か所を持ち、翼前後の窓列が非常に短いです。"),
        ("出口數與 A318 相近，因此真正的子型線索是極短窗列及 737 較窄、較低的機身截面。", "Exit count is similar to the A318; the stronger subtype cues are the very short window runs and the 737's narrower, lower body.", "出口数はA318と似ています。非常に短い窓列と、737の細く低い胴体がより強い手掛かりです。"),
        [("每側前後各一扇主艙門。", "One main door sits at each end per side.", "各側前後に主ドア1枚ずつです。"), ("典型每側一個翼上出口。", "Typically one overwing exit per side.", "通常は各側翼上出口1か所です。"), ("翼前與翼後窗列都很短。", "Window runs before and after the wing are short.", "翼前後の窓列が短いです。")],
    ),
    "engine": identify(
        ("737-600 固定使用 CFM56-7B 高旁通比渦輪扇；因 737 機身離地低，附件移至側面，使進氣口下緣呈扁平的非圓形輪廓。", "The 737-600 exclusively uses CFM56-7B turbofans. Low ground clearance moves accessories to the sides, producing the characteristic flattened inlet underside.", "737-600はCFM56-7Bのみを使用し、低い地上高に合わせて補機を側面へ移したため吸気口下面が平たい形です。"),
        ("A318 的 CFM56-5B 或 PW6000 短艙底部更圓、位置更高；近距離只看引擎就能有效區分兩型。", "The A318's CFM56-5B or PW6000 nacelles are rounder underneath and sit higher, making engine shape a strong close-range discriminator.", "A318のCFM56-5B／PW6000ナセルは下面がより丸く高い位置にあり、近距離では強い識別点です。"),
        [("只使用 CFM56-7B 系列。", "Only CFM56-7B engines are used.", "CFM56-7Bのみを使用します。"), ("進氣口底部明顯扁平。", "The inlet underside is visibly flattened.", "吸気口下面が明確に平たいです。"), ("引擎離地間隙小於 A318。", "Engine ground clearance is lower than the A318's.", "エンジン地上間隔はA318より小さいです。")],
    ),
    "wingtip": identify(
        ("737-600 基本型採傳統平直翼尖；Boeing 文件另列有 737-600W 翼尖小翼構型，但實際機隊多數仍以無翼尖小翼外觀最具代表性。", "The basic 737-600 has plain tips. Boeing documentation also lists a 737-600W winglet configuration, but the plain-tip appearance is more representative of the fleet.", "737-600基本型は通常翼端です。Boeing資料には737-600Wウイングレット型もありますが、実機では通常翼端が代表的です。"),
        ("看到無小翼的 737NG 且機身異常短，是 737-600 的強線索；不能只用無小翼排除其他早期 NG。", "A very short plain-tip 737NG strongly suggests a -600, but plain tips alone do not exclude early examples of other NG variants.", "小翼なしで極端に短い737NGは-600の強い手掛かりですが、通常翼端だけでは他の初期NGを除外できません。"),
        [("代表性外觀是平直翼尖。", "Plain tips are the representative appearance.", "通常翼端が代表的です。"), ("少數／文件構型可見翼尖小翼。", "Winglet-equipped/documented configurations exist.", "ウイングレット構成も存在します。"), ("必須搭配極短機身判讀。", "Confirm with the very short fuselage.", "極端に短い胴体と合わせて判定します。")],
    ),
    "wing": identify(
        ("737-600 使用 737NG 基本後掠主翼，基本翼展約 34.32 m；主翼相對 31.24 m 的極短機身顯得寬大，後緣配置襟翼、擾流板與副翼。", "The 737-600 uses the basic swept 737NG wing with an approximately 34.32 m span. It looks broad against the 31.24 m fuselage and carries flaps, spoilers and ailerons along the trailing edge.", "737-600は基本翼幅約34.32 mの737NG後退翼を使い、31.24 mの短胴に対して大きく見え、後縁にフラップ、スポイラー、補助翼があります。"),
        ("A318 翼展約 34.10 m，幾乎相同；737-600 應靠平直翼尖、低掛扁平短艙及短窄機身判讀，而不是靠翼展。", "The A318 span is about 34.10 m, nearly identical. Identify the 737-600 through plain tips, low flattened nacelles and its short narrow body rather than span.", "A318の翼幅約34.10 mとほぼ同じため、通常翼端、低い平たいナセル、短く細い胴体で判定します。"),
        [("基本翼展約 34.32 m。", "Basic span is about 34.32 m.", "基本翼幅は約34.32 mです。"), ("相對短機身顯得主翼很寬。", "The wing looks broad against the short body.", "短胴に対して主翼が広く見えます。"), ("低掛扁平短艙是客艙視角線索。", "Low flat nacelles are a cabin-view cue.", "低い平型ナセルが客室視点の手掛かりです。")],
    ),
    "vstab": identify(
        ("737-600 垂直尾翼具有 737NG 典型的前伸背鰭、後掠前緣與較直的方向舵後緣；放在最短 NG 機身上顯得比例很高。", "The 737-600 fin has the typical 737NG forward dorsal fillet, swept leading edge and relatively straight rudder trailing edge; it looks tall on the shortest NG body.", "737-600垂尾は737NG典型の前方へ伸びる背びれ、後退前縁、比較的直線的な方向舵後縁を持ち、最短NG胴体上で高く見えます。"),
        ("A318 的垂尾為短胴穩定性而進一步加高，輪廓與根部過渡也更像 Airbus；尾翼高度應搭配機鼻與引擎一起判斷。", "The A318 fin is further enlarged for short-body stability and has a different Airbus root blend. Use fin height together with nose and nacelle cues.", "A318垂尾は短胴安定性のためさらに高く、Airbusらしい根元形状です。垂尾高は機首・ナセルと合わせて見ます。"),
        [("前緣下方有長背鰭。", "A long dorsal fillet extends forward.", "前縁下に長い背びれがあります。"), ("方向舵後緣接近直線。", "The rudder trailing edge is nearly straight.", "方向舵後縁はほぼ直線です。"), ("短機身使垂尾比例偏高。", "The short body makes the fin look tall.", "短胴で垂尾が高く見えます。")],
    ),
    "hstab": identify(
        ("737-600 水平尾翼低置於尾錐兩側，後掠並向外收尖；外形與其他 737NG 共通，單看此部位無法確認 -600。", "The 737-600 has low-mounted swept tapered tailplanes shared with other 737NG variants, so this part alone cannot confirm a -600.", "737-600水平尾翼は尾部両側の低位置にある後退・先細形で他737NGと共通し、単独では-600を確認できません。"),
        ("737-600 與 A318 都採傳統低置水平尾翼；配合 737 外露主輪與 A318 高垂尾，判斷才可靠。", "Both use conventional low tailplanes; combine this view with the 737's exposed mains and the A318's tall fin.", "両機とも通常の低位置水平尾翼なので、737の露出主輪とA318の高い垂尾を併用します。"),
        [("水平尾翼低置且後掠。", "Tailplanes are low-mounted and swept.", "水平尾翼は低位置・後退形です。"), ("輪廓與其他 737NG 共通。", "The outline is common across the 737NG family.", "輪郭は737NGファミリー共通です。"), ("需搭配起落架與垂尾判讀。", "Use it with landing-gear and fin cues.", "脚と垂尾の特徴も合わせて見ます。")],
    ),
    "gear": identify(
        ("737-600 前腳雙輪，左右主腳各單軸雙輪；主腳向內收起後沒有完整外側艙門，輪胎胎面仍直接暴露在機腹。", "The 737-600 has twin nose wheels and a two-wheel main unit per side. The mains retract inward without full outer doors, leaving tyre faces exposed beneath the belly.", "737-600は前脚2輪、左右主脚各2輪で、完全な外扉なしに内側へ格納され、タイヤ面が機腹に露出します。"),
        ("A318 的總輪數同樣為六輪，但主輪收起後由艙門遮蔽；因此輪數無用，外露胎面才是最可靠差異。", "The A318 also totals six wheels, but doors cover its retracted mains. Wheel count is useless; exposed tyre faces are the reliable difference.", "A318も合計6輪ですが格納主輪は扉で覆われます。輪数ではなく露出タイヤ面が確実な差です。"),
        [("前腳與每側主腳均為雙輪。", "Nose and each main unit use twin wheels.", "前脚と左右主脚は各2輪です。"), ("收起後主輪胎面外露。", "Main tyre faces remain exposed when retracted.", "格納後も主輪面が露出します。"), ("機身離地姿態低於 A318。", "The fuselage sits lower than the A318's.", "胴体地上高はA318より低いです。")],
    ),
})

CONTENT["a318"] = clone_variant("a320", (("A320", "A318"), ("737-800", "737-600")))
CONTENT["a318"].update({
    "overview": identify(
        ("A318 是 A320 家族最短的量產型，全長約 31.44 m、翼展 34.10 m；短粗機身、圓鼻、圓形短艙、上下翼尖擋板與特別加高的垂尾構成輪廓。", "The A318 is the shortest production A320-family member, about 31.44 m long with a 34.10 m span. Its stubby body, round nose and nacelles, upper/lower tip fences and unusually tall fin define it.", "A318は全長約31.44 m、翼幅34.10 mでA320ファミリー最短の量産型です。短い胴体、丸い機首とナセル、上下翼端フェンス、特に高い垂尾が特徴です。"),
        ("它與 737-600 幾乎等長；A318 的機身更寬、離地更高、主輪收起後有艙門遮蔽，垂尾也因短胴穩定需求而明顯加高。", "It is almost the same length as the 737-600. The A318 is wider and higher, covers its retracted mains with doors, and has a visibly enlarged fin for short-body directional stability.", "737-600とほぼ同じ長さですが、A318は太く高く、格納主輪が扉で覆われ、短胴の方向安定性のため垂尾が明確に大型化されています。"),
        [("A320 家族最短量產型。", "Shortest production A320-family member.", "A320ファミリー最短量産型です。"), ("上下翼尖擋板是標準外觀。", "Upper/lower tip fences are standard.", "上下翼端フェンスが標準です。"), ("垂尾比例比 A319／A320 更高。", "The fin is proportionally taller than on A319/A320.", "垂尾はA319／A320より相対的に高いです。")],
    ),
    "cockpit": identify(
        ("A318 與 A319、A320、A321 共用側桿式玻璃座艙：飛行員正前方沒有駕駛盤，中央上下排列兩具 ECAM 顯示器。", "The A318 shares the A319/A320/A321 sidestick glass cockpit: no yokes ahead of the pilots and two central stacked ECAM displays.", "A318はA319／A320／A321共通のサイドスティック式グラスコックピットで、正面に操縦輪がなく中央に上下2面ECAMがあります。"),
        ("家族座艙高度共通，內部照片通常無法辨識 A318 子型；但側桿與桌板可立即排除有駕駛盤的 737-600。", "Family cockpit commonality makes the A318 subtype hard to identify inside, but sidesticks and tray tables immediately exclude the yoke-equipped 737-600.", "共通性が高く機内だけでA318を特定しにくい一方、サイドスティックとテーブルで操縦輪付き737-600を除外できます。"),
        [("側桿位於兩名駕駛外側。", "Sidesticks sit outboard of both pilots.", "サイドスティックは両席外側です。"), ("正前方設有可收折桌板。", "Folding tray tables sit ahead of the pilots.", "正面に折り畳みテーブルがあります。"), ("中央 ECAM 上下排列。", "Central ECAM displays are stacked.", "中央ECAMは上下配置です。")],
    ),
    "fuselage": identify(
        ("A318 保留 A320 家族約 3.95 m 寬的每排六座機身，但縮短至約 31.44 m；典型每側有前後主艙門及一個翼上逃生出口。", "The A318 retains the A320 family's roughly 3.95 m-wide six-abreast body but shortens it to about 31.44 m; typically each side has forward/aft main doors and one overwing exit.", "A318はA320ファミリー共通の幅約3.95 m・横6席胴体を約31.44 mまで短縮し、通常各側に前後ドアと翼上出口1か所を持ちます。"),
        ("它的翼前、翼後窗列都比 A319 更短；與等長 737-600 相比，機身截面更寬、離地姿態更高。", "Its window runs ahead of and behind the wing are shorter than the A319's. Against the similarly long 737-600, its body is wider and sits higher.", "翼前後の窓列はA319より短く、ほぼ同長の737-600より胴体が太く高い位置にあります。"),
        [("每側前後各一扇主艙門。", "One main door sits at each end per side.", "各側前後に主ドア1枚ずつです。"), ("典型每側一個翼上出口。", "Typically one overwing exit per side.", "通常は各側翼上出口1か所です。"), ("寬機身截面配極短窗列。", "A wide body section is paired with short window runs.", "太い胴体断面と短い窓列の組合せです。")],
    ),
    "engine": identify(
        ("A318 可裝 CFM56-5B8／5B9 系列或 Pratt & Whitney PW6000（PW6122A）；兩者底部都比 737-600 的 CFM56-7B 更圓，離地間隙也較大。", "The A318 uses CFM56-5B8/-5B9 variants or the Pratt & Whitney PW6000 (PW6122A). Both are rounder underneath and sit higher than the 737-600's CFM56-7B.", "A318はCFM56-5B8／5B9系またはPratt & Whitney PW6000（PW6122A）を使用し、737-600のCFM56-7Bより下面が丸く地上間隔も大きいです。"),
        ("PW6000 短艙外形與 CFM56-5B 不同，因此判斷 A318 時應先確認圓形進氣口，再用極短機身與高垂尾確認子型。", "PW6000 and CFM56-5B nacelles differ, so first identify the round inlet, then use the very short body and tall fin to confirm an A318.", "PW6000とCFM56-5Bでナセル形状が異なるため、まず丸い吸気口を見て、極短胴と高い垂尾でA318を確認します。"),
        [("可見 CFM56-5B 或 PW6000。", "CFM56-5B or PW6000 engines may appear.", "CFM56-5BまたはPW6000を装備します。"), ("進氣口底部接近圓形。", "The inlet underside is nearly circular.", "吸気口下面は円形に近いです。"), ("離地間隙大於 737-600。", "Ground clearance exceeds the 737-600's.", "地上間隔は737-600より大きいです。")],
    ),
    "wingtip": identify(
        ("量產 A318 使用經典 A320 家族上下翼尖擋板：翼尖同時有向上與向下的小片，而不是高大的 Sharklet。", "Production A318s use classic A320-family upper-and-lower tip fences rather than tall Sharklets.", "量産A318は高いSharkletではなく、A320ファミリー従来型の上下翼端フェンスを使います。"),
        ("上下雙向擋板配上極短機身與高垂尾，是從遠處辨識 A318 的實用組合。", "Upper/lower fences combined with a very short body and tall fin form a practical distant A318 cue.", "上下フェンス、極短胴、高い垂尾の組合せが遠距離でのA318識別に有効です。"),
        [("翼尖上、下各伸出一片。", "One fence projects above and below the tip.", "翼端の上と下へ各1枚伸びます。"), ("量產機沒有常見 Sharklet 構型。", "Production aircraft lack the common Sharklet configuration.", "量産機に一般的なSharklet構成はありません。"), ("配合高垂尾確認 A318。", "Combine it with the tall fin to confirm A318.", "高い垂尾と合わせてA318を確認します。")],
    ),
    "wing": identify(
        ("A318 沿用 A320 家族基本主翼，翼展 34.10 m；相對極短機身，主翼顯得格外寬大，後緣仍有多段襟翼與擾流板。", "The A318 retains the basic A320-family wing with a 34.10 m span. Against its very short body the wing looks unusually broad, with multi-section flaps and spoilers on the trailing edge.", "A318は翼幅34.10 mのA320ファミリー共通主翼を使い、極短胴に対して翼が大きく見え、後縁に多段フラップとスポイラーがあります。"),
        ("737-600 基本翼展約 34.32 m，尺寸幾乎相同；應看 A318 上下翼尖擋板與圓形短艙，而非只看翼展。", "The basic 737-600 span is about 34.32 m, nearly identical; use the A318's upper/lower fences and round nacelles rather than span alone.", "737-600基本型の翼幅約34.32 mとほぼ同じなので、翼幅ではなくA318の上下フェンスと丸いナセルを見ます。"),
        [("主翼與 A320 家族高度共通。", "The wing is highly common with the A320 family.", "主翼はA320ファミリーと高い共通性があります。"), ("相對短機身顯得翼幅很大。", "The span looks large against the short body.", "短胴に対して翼幅が大きく見えます。"), ("上下翼尖擋板是近距離線索。", "Upper/lower tip fences are a close-range cue.", "上下翼端フェンスが近距離の手掛かりです。")],
    ),
    "vstab": identify(
        ("A318 因機身最短、方向力臂較小，採用比 A319／A320 更高的垂直尾翼；高大後掠尾翼在短機身上形成非常醒目的比例。", "Because its shortest fuselage provides less yaw moment arm, the A318 uses a taller vertical fin than the A319/A320; the tall swept fin is conspicuous on the short body.", "A318は最短胴でヨー方向の腕が短いためA319／A320より高い垂尾を採用し、短い胴体上で非常に目立ちます。"),
        ("這是區分 A318 與 A319 最重要的外部線索之一；737-600 雖也短，但垂尾根部與機鼻、短艙外形不同。", "This is one of the strongest external cues separating an A318 from an A319. The 737-600 is also short, but its fin root, nose and nacelles differ.", "A319との識別で最重要の外部特徴の一つです。737-600も短胴ですが、垂尾根元、機首、ナセル形状が異なります。"),
        [("垂尾高於其他早期 A320 家族成員。", "The fin is taller than on other early A320-family members.", "他の初期A320ファミリーより垂尾が高いです。"), ("短機身讓尾翼比例非常突出。", "The short body makes the fin proportion striking.", "短胴で垂尾比率が際立ちます。"), ("根部寬而平順接入後機身。", "Its broad root blends smoothly into the aft body.", "幅広い根元が後部胴体へ滑らかにつながります。")],
    ),
    "hstab": identify(
        ("A318 水平尾翼低置於尾錐兩側，後掠並向外收窄，基本輪廓與 A320 家族共通；在短機身上看起來比例較寬。", "The A318 has low-mounted swept tapered tailplanes sharing the basic A320-family form; they look relatively broad on the short fuselage.", "A318水平尾翼は尾部両側の低位置にある後退・先細形でA320ファミリー共通ですが、短胴上では相対的に広く見えます。"),
        ("737-600 也有相似低置尾翼，單看此部位不足以辨識；A318 的高垂尾、圓形短艙與有艙門主輪更可靠。", "The 737-600 has a similar low tailplane, so this part alone is insufficient. The A318's tall fin, round nacelles and covered mains are stronger cues.", "737-600も似た低位置尾翼のため単独判定はできず、A318の高い垂尾、丸いナセル、覆われる主輪が有効です。"),
        [("水平尾翼低置且後掠。", "Tailplanes are low-mounted and swept.", "水平尾翼は低位置・後退形です。"), ("與 A320 家族基本輪廓共通。", "The basic outline is shared with the A320 family.", "基本輪郭はA320ファミリー共通です。"), ("應搭配高垂尾與引擎判讀。", "Use it with the tall fin and engine cues.", "高い垂尾とエンジン特徴を併用します。")],
    ),
    "gear": identify(
        ("A318 前腳雙輪，左右主腳各單軸雙輪；主腳向內收入翼身整流區，艙門會遮蔽輪胎，地面姿態也比 737-600 高。", "The A318 has twin nose wheels and a two-wheel main unit per side. The mains retract inward behind doors, and the aircraft sits higher than the 737-600.", "A318は前脚2輪、左右主脚各2輪で、内側へ格納され扉に覆われ、737-600より高い姿勢です。"),
        ("兩型總輪數都是六輪；不要數輪子，應看 A318 較長的腳柱與完整主輪艙門，對比 737 的外露胎面。", "Both total six wheels. Do not count wheels; compare the A318's taller struts and full main doors with the 737's exposed tyre faces.", "両機とも合計6輪です。輪数ではなくA318の長い脚柱・完全な主脚扉と、737の露出タイヤ面を比較します。"),
        [("前腳與每側主腳均為雙輪。", "Nose and each main unit use twin wheels.", "前脚と左右主脚は各2輪です。"), ("收起主輪由艙門遮蔽。", "Doors cover the retracted main wheels.", "格納主輪は扉で覆われます。"), ("腳柱與離地高度高於 737-600。", "Struts and ground clearance exceed the 737-600's.", "脚柱と地上高は737-600より大きいです。")],
    ),
})

CONTENT["b772"] = {
    "overview": identify(
        ("777-200／200ER 是第一代 777 長程雙發廣體客機，全長約 63.7 m、翼展 60.9 m；兩具大直徑引擎、寬大圓機身與六輪主腳是主要輪廓。", "The 777-200/200ER is the original long-range 777 twin, about 63.7 m long with a 60.9 m span. Two large engines, a broad round body and six-wheel main bogies define it.", "777-200／200ERは全長約63.7 m、翼幅60.9 mの初代777長距離双発機です。大型エンジン2基、太い胴体、6輪主脚が特徴です。"),
        ("A340-300 幾乎同長、同翼展；最快的區分方式是先數引擎，再看 777 沒有中置主腳。", "The A340-300 is almost identical in length and span. Count engines first, then note that the 777 has no centre main gear.", "A340-300とは全長・翼幅がほぼ同じです。まずエンジン数、次に777には中央主脚がない点を見ます。"),
        [("翼下只有兩具大型引擎。", "Only two large underwing engines.", "主翼下は大型エンジン2基です。"), ("左右主腳各為三軸六輪。", "Each main bogie has three axles and six tyres.", "左右主脚は各3軸6輪です。"), ("機腹沒有 A340-300 的中置主腳。", "No A340-300-style centre gear.", "A340-300型の中央主脚がありません。")],
    ),
    "cockpit": identify(
        ("777 駕駛艙以傳統駕駛盤、六具大型顯示器與中央 EICAS 為核心，油門與控制台集中在兩席之間。", "The 777 flight deck centres on conventional yokes, six large displays and central EICAS screens, with throttles and controls on the centre pedestal.", "777操縦席は操縦輪、6面大型表示器、中央EICASを中心に、スロットル類を中央ペデスタルへ配置します。"),
        ("A340-300 採 Airbus 側桿、正面桌板與 ECAM；駕駛盤是否存在是座艙內最直接的廠牌線索。", "The A340-300 uses Airbus sidesticks, forward tray tables and ECAM. The presence or absence of yokes is the quickest cockpit cue.", "A340-300はサイドスティック、正面テーブル、ECAMを採用し、操縦輪の有無が最速の識別点です。"),
        [("正副駕駛前方都有駕駛盤。", "A yoke sits before each pilot.", "両席正面に操縦輪があります。"), ("中央兩面主要顯示 EICAS。", "The centre pair primarily serves EICAS.", "中央2面は主にEICASです。"), ("中央基座高，沒有 Airbus 式桌板。", "The tall pedestal leaves no Airbus-style tray table.", "高い中央台がありAirbus式テーブルはありません。")],
    ),
    "windshield": identify(
        ("777 的兩片正面風擋寬大，外側窗以明顯折角向後收窄，窗框輪廓較粗且多邊形感強。", "The 777 has broad forward panes and clearly angular outer panes that taper aft, producing a heavy polygonal frame.", "777は幅広い前面窓と、後方へ絞られる角張った外側窓を持ち、太い多角形枠に見えます。"),
        ("A340-300 的 Airbus 窗帶較扁平、轉折較柔和；正面與側面照片應一起比較，不能只數窗片。", "The A340-300's Airbus glazing looks flatter with softer transitions. Compare front and side views rather than pane count alone.", "A340-300の窓帯はより平たく滑らかです。枚数だけでなく正面・側面を併用します。"),
        [("正面窗寬大且中央接縫近垂直。", "Wide front panes meet at a near-vertical seam.", "幅広い前面窓がほぼ垂直に接します。"), ("外側窗上緣向後下斜。", "Outer-pane upper edges slope aft and down.", "外側窓上端は後方へ下がります。"), ("窗框沒有連續黑色面罩。", "Frames remain separate without a black mask.", "連続した黒マスクはありません。")],
    ),
    "fuselage": identify(
        ("777 機身外寬約 6.20 m，777-200 典型每側四扇主艙門；圓形寬機身、橢圓舷窗與長尾錐構成 Boeing 廣體輪廓。", "The 777 body is about 6.20 m wide and a typical 777-200 has four main doors per side, with oval windows and a long aft taper.", "777の胴体幅は約6.20 mで、777-200は通常片側4枚の主ドア、楕円窓、長い後部絞りを持ちます。"),
        ("A340-300 機身約 5.64 m 寬；兩者都常見每側四門，因此門數必須配合引擎與主腳判讀。", "The A340-300 body is about 5.64 m wide. Both commonly show four doors per side, so combine door count with engines and gear.", "A340-300の胴体幅は約5.64 mです。両機とも片側4ドアが多く、エンジンと脚も併用します。"),
        [("典型每側四扇主艙門。", "Typically four main doors per side.", "通常は片側4枚の主ドアです。"), ("機身比 A340-300 更寬。", "The body is wider than the A340-300's.", "胴体はA340-300より太いです。"), ("客艙窗為獨立橢圓形。", "Cabin windows are individual ovals.", "客室窓は独立した楕円形です。")],
    ),
    "engine": identify(
        ("777-200／200ER 可配 PW4000、Rolls-Royce Trent 800 或早期 GE90；無論型號，兩具短艙都明顯大於 A340-300 的四具 CFM56-5C。", "The 777-200/200ER could use PW4000s, Trent 800s or early GE90s. In every case its two nacelles are much larger than the A340-300's four CFM56-5Cs.", "777-200／200ERはPW4000、Trent 800、初期GE90を選択でき、いずれもA340-300のCFM56-5C 4基より大きなナセルです。"),
        ("照片中的 United 777-200 使用 PW4000 系列；不能把它當成所有 777-200 的唯一引擎外形。", "The photographed United 777-200 uses PW4000-series engines; that nacelle is not universal to every 777-200.", "写真のUnited 777-200はPW4000系列で、全777-200共通の外形ではありません。"),
        [("總數固定為兩具。", "There are always two engines.", "エンジンは常に2基です。"), ("短艙直徑遠大於 A340-300。", "Nacelles are far larger than the A340-300's.", "ナセル径はA340-300より大幅に大きいです。"), ("三種引擎選項會改變細部外形。", "Three engine options change the detail shape.", "3種の選択で細部形状が変わります。")],
    ),
    "wingtip": identify(
        ("一般 777-200／200ER 使用簡潔、近乎水平的傳統翼尖，沒有直立 winglet；後來的 777-200LR 才採明顯延長的 raked tip。", "Standard 777-200/200ER aircraft use plain near-horizontal tips without upright winglets; the later 777-200LR introduced prominent raked tips.", "通常の777-200／200ERは直立小翼のない水平に近い通常翼端で、後の777-200LRが長いレイクド翼端を採用します。"),
        ("A340-300 翼尖可見向上、向下伸出的短翼尖擋板；這比兩者近似的翼展更容易辨認。", "The A340-300 carries short upper/lower wingtip fences, a better cue than their nearly identical spans.", "A340-300には上下へ伸びる短い翼端フェンスがあり、ほぼ同じ翼幅より有効な手掛かりです。"),
        [("沒有高大的直立小翼。", "No tall upright winglet.", "高い直立小翼はありません。"), ("標準型翼尖主要留在翼面平面。", "The standard tip stays largely in the wing plane.", "通常翼端は主に翼面内です。"), ("不要與 777-200LR 的延長翼尖混淆。", "Do not confuse it with the -200LR raked tip.", "-200LRの延長翼端と混同しません。")],
    ),
    "wing": identify(
        ("777-200 的後掠主翼翼展約 60.9 m，翼下各掛一具大型引擎；厚翼根、長外翼與大型多段襟翼很醒目。", "The 777-200's swept wing spans about 60.9 m and carries one large engine per side, with a thick root, long outer panels and large multi-element flaps.", "777-200の後退翼は翼幅約60.9 mで片側1基の大型エンジン、厚い翼根、長い外翼、大型多重フラップを持ちます。"),
        ("A340-300 翼展約 60.3 m，尺寸幾乎相同；翼下是兩具還是四具引擎才是決定性差異。", "The A340-300 span is about 60.3 m, almost identical. Two versus four underwing engines is decisive.", "A340-300の翼幅約60.3 mとほぼ同じで、翼下2基か4基かが決定的です。"),
        [("每側翼下只有一具引擎。", "One engine hangs beneath each wing.", "各主翼下は1基です。"), ("翼根厚且外翼長。", "The root is thick and the outer wing long.", "翼根は厚く外翼が長いです。"), ("後緣配置大型多段襟翼。", "Large multi-element flaps line the trailing edge.", "後縁に大型多重フラップがあります。")],
    ),
    "vstab": identify(
        ("777 的垂直尾翼高大後掠，以長背鰭接入粗壯後機身，方向舵面積也很大。", "The 777's tall swept fin blends into its broad aft body through a long dorsal fillet and carries a large rudder.", "777の高い後退垂尾は長い背びれで太い後部胴体へつながり、大型方向舵を備えます。"),
        ("A340-300 尾部通常顯得較細；垂尾只能作輔助，仍應先看引擎與中置主腳。", "The A340-300 tail usually looks slimmer. The fin is secondary; engines and centre gear remain stronger cues.", "A340-300の尾部はより細く見えます。垂尾は補助で、エンジンと中央脚を優先します。"),
        [("前緣後掠且根部背鰭長。", "Strong sweep and a long dorsal fillet.", "前縁後退が大きく背びれが長いです。"), ("頂端較平，方向舵後緣近直線。", "The tip is fairly flat and rudder edge straight.", "上端は比較的平らで方向舵後縁は直線的です。"), ("粗壯尾身是輔助比例線索。", "The broad tail body is a supporting cue.", "太い尾部胴体が補助線索です。")],
    ),
    "hstab": identify(
        ("777 使用大型低置後掠水平尾翼，厚實翼根與寬機身相接，形成寬大的尾部輪廓。", "The 777 uses large low-mounted swept tailplanes with thick roots joining the wide aft body.", "777は大型の低位置後退水平尾翼を持ち、厚い翼根が太い後部胴体へ接続します。"),
        ("A340-300 也是傳統低置尾翼，單看水平尾翼很難定型；應配合翼下引擎數與翼尖。", "The A340-300 also has conventional low tailplanes, so use engine count and wingtips rather than this feature alone.", "A340-300も通常の低位置尾翼で、単独ではなくエンジン数と翼端を併用します。"),
        [("水平尾翼尺寸大且後掠。", "Large, swept tailplanes.", "大型で後退した水平尾翼です。"), ("翼根整流罩厚實。", "The root fairing is substantial.", "翼根フェアリングが厚いです。"), ("此部位只適合交叉確認。", "Use this only as a cross-check.", "この部位は照合用です。")],
    ),
    "gear": identify(
        ("777-200 前腳雙輪，左右主腳各有三根輪軸、六個輪胎，總輪數 14；主腳轉向架修長，機腹沒有中置主腳。", "The 777-200 has twin nose wheels and two three-axle, six-tyre main bogies: 14 wheels total, with no centre main gear.", "777-200は前脚2輪、左右主脚各3軸6輪の計14輪で、中央主脚はありません。"),
        ("A340-300 總輪數 12：左右主腳各四輪，另有一組中線雙輪；從地面或機腹看最容易區分。", "The A340-300 totals 12 wheels: four on each wing gear plus a centreline twin. This is decisive from ground or belly views.", "A340-300は左右主脚各4輪と中央2輪の計12輪で、地上・腹面から決定的に区別できます。"),
        [("每側主腳三軸六輪。", "Three axles and six tyres per main bogie.", "各主脚は3軸6輪です。"), ("全機共 14 輪。", "Fourteen wheels in total.", "全機計14輪です。"), ("沒有機身中線主腳。", "No centreline body gear.", "胴体中央脚がありません。")],
    ),
}

CONTENT["a343"] = {
    "overview": identify(
        ("A340-300 是四發長程廣體客機，全長約 63.69 m、翼展約 60.3 m；四具細長 CFM56-5C、小型翼尖擋板與中置主腳是關鍵。", "The A340-300 is a four-engine long-range wide-body, about 63.69 m long with a 60.3 m span. Four slim CFM56-5Cs, small tip fences and centre gear are key cues.", "A340-300は全長約63.69 m、翼幅約60.3 mの4発長距離機で、細いCFM56-5C 4基、小型翼端フェンス、中央脚が特徴です。"),
        ("它與 777-200 幾乎同長同寬展，但四發與機腹中線雙輪讓兩者一眼可分。", "It nearly matches the 777-200 in length and span, but four engines and a centreline twin-wheel gear separate them immediately.", "777-200と全長・翼幅がほぼ同じですが、4発と中央2輪脚で即座に区別できます。"),
        [("翼下共有四具引擎。", "Four engines beneath the wings.", "主翼下に4基あります。"), ("翼尖有短小上下擋板。", "Small upper/lower tip fences.", "翼端に小型上下フェンスがあります。"), ("機腹中線另有雙輪主腳。", "A twin-wheel centre gear sits under the fuselage.", "胴体中央に2輪主脚があります。")],
    ),
    "cockpit": identify(
        ("A340-300 與 A330 共用 Airbus 側桿玻璃座艙，飛行員正前方沒有駕駛盤，中央 ECAM 顯示引擎與系統資訊。", "The A340-300 shares the Airbus sidestick glass cockpit with the A330: no yokes ahead of the pilots and central ECAM system displays.", "A340-300はA330と共通のサイドスティック式グラスコックピットで、正面に操縦輪がなく中央ECAMがあります。"),
        ("四發狀態會反映在引擎顯示與油門桿配置；與 777 相比，側桿和桌板仍是最直觀差異。", "Four-engine indications and throttle controls reflect the powerplant count; sidesticks and tray tables remain the clearest contrast with the 777.", "4発表示とスロットル構成があり、777との差はサイドスティックとテーブルが最明確です。"),
        [("側桿位於兩名駕駛外側。", "Sidesticks sit outboard of both pilots.", "サイドスティックは両席外側です。"), ("正前方有桌板而非駕駛盤。", "Tray tables replace forward yokes.", "正面は操縦輪でなくテーブルです。"), ("中央 ECAM 顯示四發系統。", "Central ECAM covers the four-engine systems.", "中央ECAMが4発システムを表示します。")],
    ),
    "windshield": identify(
        ("A340-300 採 A330／A340 共通六片式窗帶，正面窗較扁平，外側窗沿圓鼻平順向後收窄。", "The A340-300 uses the common A330/A340 six-pane glazing: flatter forward panes and outer panes tapering smoothly around the rounded nose.", "A340-300はA330／A340共通の6枚窓で、前面窓は平たく外側窓が丸い機首に沿って滑らかに細くなります。"),
        ("777 的窗框更粗、更角張；兩型都沒有 A350 式黑色面罩，因此應比較窗框幾何而非顏色。", "The 777's frames are heavier and more angular. Neither has an A350-style black mask, so compare geometry rather than colour.", "777の枠は太く角張ります。両機ともA350型黒マスクがないため色でなく形状を比較します。"),
        [("正面窗帶較扁平。", "The forward glazing looks flatter.", "正面窓帯はより平たく見えます。"), ("外側窗轉折較柔和。", "Outer-pane transitions are smoother.", "外側窓の変化が滑らかです。"), ("窗框與 A330 家族共通。", "The frame is shared with the A330 family.", "窓枠はA330系と共通です。")],
    ),
    "fuselage": identify(
        ("A340-300 使用 A330／A340 共通約 5.64 m 寬機身，典型每側四扇主艙門，圓鼻與長直窗列形成修長輪廓。", "The A340-300 uses the roughly 5.64 m-wide A330/A340 fuselage, typically with four main doors per side, a rounded nose and long straight window belt.", "A340-300は幅約5.64 mのA330／A340共通胴体で、通常片側4枚の主ドア、丸い機首、長い窓列を持ちます。"),
        ("777-200 也常見每側四門，但機身約寬 56 cm；門數相同時，應回到引擎數與主腳。", "The 777-200 also commonly has four doors per side but is about 56 cm wider; engines and gear are more useful than door count.", "777-200も片側4ドアが多い一方で約56 cm太く、ドア数よりエンジンと脚が有効です。"),
        [("典型每側四扇主艙門。", "Typically four main doors per side.", "通常片側4枚の主ドアです。"), ("機身截面與 A330 共通。", "The fuselage section is shared with the A330.", "胴体断面はA330と共通です。"), ("比 777 機身更窄。", "The body is narrower than the 777's.", "胴体は777より細いです。")],
    ),
    "engine": identify(
        ("A340-300 固定使用四具 CFM56-5C，高旁通比短艙直徑相對機身顯得小，兩具分布在每側主翼下。", "The A340-300 exclusively uses four CFM56-5Cs. Their high-bypass nacelles look relatively small beside the wide body, with two under each wing.", "A340-300はCFM56-5C 4基専用で、広い胴体に対してナセルが小さく、各主翼下に2基配置されます。"),
        ("777-200 的兩具 PW4000、Trent 800 或 GE90 都明顯更大；引擎數與直徑是最穩定的外觀差異。", "The 777-200's two PW4000, Trent 800 or GE90 engines are visibly larger. Count and diameter are the most stable cues.", "777-200のPW4000、Trent 800、GE90はいずれも大きく、数と直径が最安定した差です。"),
        [("每側主翼下兩具，共四具。", "Two per wing, four total.", "各主翼下2基、計4基です。"), ("只使用 CFM56-5C 系列。", "Only CFM56-5C engines are used.", "CFM56-5Cのみを使用します。"), ("短艙比 777 小而細長。", "Nacelles are smaller and slimmer than the 777's.", "ナセルは777より小さく細長いです。")],
    ),
    "wingtip": identify(
        ("A340-300 經典翼尖有短小的上下翼尖擋板，向上部分略高、向下部分較短，沒有大型融合式 winglet。", "The classic A340-300 tip has small upper and lower fences, with a taller upper blade and shorter lower blade rather than a large blended winglet.", "A340-300の典型翼端は上側がやや高い小型上下フェンスで、大型ブレンデッドウイングレットではありません。"),
        ("標準 777-200 翼尖近乎水平且沒有上下擋板；從客艙翼景即可快速區分。", "A standard 777-200 has a near-horizontal plain tip without upper/lower fences, making cabin wing views useful.", "標準777-200は上下フェンスのない水平に近い翼端で、客室翼景から区別できます。"),
        [("上、下各有短小擋板。", "Small fences project above and below.", "上下に小型フェンスがあります。"), ("尺寸遠小於現代 Sharklet。", "Much smaller than a modern Sharklet.", "現代Sharkletより大幅に小型です。"), ("是 A330／早期 A340 家族線索。", "A cue shared with early A330/A340 aircraft.", "初期A330／A340共通の手掛かりです。")],
    ),
    "wing": identify(
        ("A340-300 後掠主翼翼展約 60.3 m，每側掛兩具 CFM56；外翼接小型翼尖擋板，後緣有大型襟翼與擾流板。", "The A340-300's swept wing spans about 60.3 m, carries two CFM56s per side and ends in small tip fences, with large flaps and spoilers aft.", "A340-300の後退翼は翼幅約60.3 mで各側CFM56 2基、小型翼端フェンス、大型フラップとスポイラーを備えます。"),
        ("777-200 翼展約 60.9 m，幾乎相同；主翼判讀應看每側一具還是兩具引擎，而非估算翼展。", "The 777-200 span is about 60.9 m, nearly identical. Count one versus two engines per wing instead of estimating span.", "777-200の翼幅約60.9 mとほぼ同じで、翼幅より片側1基か2基かを見ます。"),
        [("每側翼下掛兩具引擎。", "Two engines hang beneath each wing.", "各主翼下に2基あります。"), ("外翼末端接小型擋板。", "Small fences finish the outer wing.", "外翼端に小型フェンスがあります。"), ("翼展與 777-200 幾乎相同。", "Span nearly matches the 777-200.", "翼幅は777-200とほぼ同じです。")],
    ),
    "vstab": identify(
        ("A340-300 的垂直尾翼高大後掠，根部以 Airbus 式平順背鰭接入較細的後機身，外形與 A330 高度共通。", "The A340-300's tall swept fin blends through a smooth Airbus-style dorsal root into a slimmer aft body and is highly common with the A330.", "A340-300の高い後退垂尾はAirbusらしい滑らかな根元で細い後部胴体へ接続し、A330と高い共通性があります。"),
        ("僅靠尾翼很難把 A340 與 A330 分開；四具引擎和中置主腳才是 A340-300 的主要確認點。", "The fin alone cannot reliably separate an A340 from an A330; four engines and centre gear confirm the A340-300.", "尾翼だけではA330と区別できず、4発と中央脚がA340-300の主確認点です。"),
        [("垂尾高大且前緣後掠。", "Tall fin with a swept leading edge.", "高く前縁後退した垂尾です。"), ("根部過渡平順。", "The root transition is smooth.", "根元のつながりが滑らかです。"), ("外形與 A330 相近。", "The outline closely resembles the A330's.", "外形はA330に近いです。")],
    ),
    "hstab": identify(
        ("A340-300 採低置後掠水平尾翼，從細長尾錐向外收尖，與 A330 共用相近的傳統尾部布局。", "The A340-300 uses low-mounted swept tailplanes tapering from a slender tailcone in a conventional layout shared closely with the A330.", "A340-300は細い尾部から伸びる低位置後退水平尾翼で、A330と近い通常尾部配置です。"),
        ("777-200 也是低置尾翼，水平尾翼本身不是強線索；應搭配較窄機身、四發與中置主腳。", "The 777-200 also uses low tailplanes, so combine this with the narrower body, four engines and centre gear.", "777-200も低位置尾翼のため、細い胴体、4発、中央脚を併用します。"),
        [("低置、後掠且向外收尖。", "Low-mounted, swept and tapered.", "低位置・後退・先細形です。"), ("尾錐比例較細長。", "The tailcone looks relatively slender.", "尾部は比較的細長いです。"), ("單獨不能區分 A330。", "It cannot alone separate an A330.", "単独ではA330と区別できません。")],
    ),
    "gear": identify(
        ("A340-300 前腳雙輪、左右翼下主腳各四輪，機身中線另有一組雙輪主腳，總輪數 12。", "The A340-300 has twin nose wheels, four-wheel wing gears on each side and a twin-wheel centreline gear: 12 wheels total.", "A340-300は前脚2輪、左右翼下主脚各4輪、中央主脚2輪の計12輪です。"),
        ("中置雙輪可把 -300 與雙發 A330 分開，也與 A340-500／-600 的四輪中置主腳不同；777 則沒有中央主腳。", "The twin centre gear separates it from the twin-engine A330 and differs from the four-wheel centre gear on A340-500/-600; the 777 has none.", "中央2輪は双発A330と区別し、A340-500／-600の中央4輪とも異なり、777には中央脚がありません。"),
        [("左右翼下主腳各四輪。", "Four wheels on each wing main gear.", "左右翼下主脚は各4輪です。"), ("機身中線主腳為雙輪。", "The centreline body gear has two wheels.", "胴体中央脚は2輪です。"), ("全機總輪數為 12。", "Twelve wheels in total.", "全機計12輪です。")],
    ),
}

CONTENT.update({
    "b717": {
        "overview": identify(
            ("Boeing 717-200 是約百座級短程單走道客機，全長約 37.8 m、翼展約 28.4 m；兩具引擎置於後機身，水平尾翼架在垂直尾翼頂端，形成醒目的 T 型尾翼。", "The Boeing 717-200 is a roughly 100-seat short-haul single-aisle jet, about 37.8 m long with a 28.4 m span. Its two engines sit on the aft fuselage and its tailplane crowns the fin in a distinct T-tail.", "Boeing 717-200は約100席の短距離単通路機で、全長約37.8 m、翼幅約28.4 mです。2基のエンジンを後部胴体に置き、水平尾翼を垂尾頂部に載せたT字尾翼が特徴です。"),
            ("717 源自 McDonnell Douglas MD-95／DC-9 家族，並非與 737 共用構型；對比 A220-100 時，先看引擎位置與尾翼即可快速分辨。", "The 717 originated as the McDonnell Douglas MD-95 in the DC-9 lineage rather than sharing the 737 layout. Against an A220-100, engine position and tail arrangement identify it immediately.", "717はMcDonnell Douglas MD-95／DC-9系譜で、737と同じ構成ではありません。A220-100との比較ではエンジン位置と尾翼で素早く判別できます。"),
            [("尾置雙發使主翼下方完全沒有引擎短艙。", "Rear-mounted engines leave the wing undersides free of nacelles.", "尾部エンジンのため主翼下にナセルがありません。"), ("T 型尾翼高而明顯，水平尾翼位於垂尾頂端。", "The high T-tail places the tailplane at the top of the fin.", "高いT字尾翼で水平尾翼は垂尾頂部にあります。"), ("機身比 A220-100 更長，但翼展明顯更窄。", "It is longer than the A220-100 but has a substantially narrower span.", "A220-100より長い一方、翼幅は大幅に狭いです。")],
        ),
        "cockpit": identify(
            ("717 駕駛艙保留傳統駕駛盤與中央操縱柱，採六具電子顯示器與中央引擎／系統顯示；座艙布局是 MD-90 技術的進一步現代化。", "The 717 flight deck retains conventional yokes and control columns, with six electronic displays and central engine/system indications, evolving the MD-90 cockpit concept.", "717の操縦席は従来型操縦輪とコラムを残し、6面電子表示器と中央エンジン／システム表示を備え、MD-90の設計を発展させています。"),
            ("A220 也不是典型 A320 座艙：它有側桿但採五具大型橫向螢幕。對比時看 717 的駕駛盤與較多直立顯示器最直接。", "The A220 is not an A320-style cockpit either: it uses sidesticks and five wide displays. The 717's yokes and more numerous portrait-oriented screens are the clearest contrast.", "A220もA320型そのものではなく、サイドスティックと5面大型横長画面を使います。717の操縦輪と多数の縦長画面が明確な差です。"),
            [("正副駕駛前方各有一具駕駛盤。", "A yoke sits directly ahead of each pilot.", "両操縦席正面に操縦輪があります。"), ("中央台只有兩支引擎推力桿。", "Two engine thrust levers occupy the centre pedestal.", "中央台には2本の推力レバーがあります。"), ("面板保留大量實體旋鈕與按鍵。", "The panel retains numerous physical knobs and switches.", "パネルには多数の物理ノブとスイッチがあります。")],
        ),
        "windshield": identify(
            ("717 的駕駛艙窗延續 DC-9 家族的稜角輪廓：正面主風擋較方正，外側窗由狹長梯形向後折入機身側面，窗帶位於圓鈍機鼻上方。", "The 717 retains the angular DC-9-family glazing: fairly square main windscreens lead into narrow trapezoidal side panes above a rounded nose.", "717はDC-9系の角張った窓形状を継承し、比較的四角い主風防から細長い台形側窓へ続き、丸い機首上部に配置されます。"),
            ("A220 的主風擋更寬、外側窗更圓滑且整組窗帶帶有現代弧線；兩型都應看窗框比例與機鼻，而不是只數窗片。", "The A220 has broader front panes and more rounded outer glazing with a modern continuous contour. Compare proportions and nose shape rather than merely counting panes.", "A220は前面窓が広く外側窓も丸みがあり、現代的な連続輪郭です。枚数だけでなく窓枠比率と機首形状を見ます。"),
            [("中央兩片主風擋接近直立方形。", "The two centre windscreens are close to upright rectangles.", "中央2枚の主風防は直立した四角形に近いです。"), ("側窗框折角清楚，帶有 DC-9 家族特徵。", "Distinct corners in the side glazing reflect the DC-9 lineage.", "側窓の折れ角にDC-9系の特徴があります。"), ("圓鈍機鼻比 A220 更短、更接近半球形。", "The rounded nose is shorter and more hemispherical than the A220's.", "丸い機首はA220より短く半球状に見えます。")],
        ),
        "fuselage": identify(
            ("717 使用約 3.34 m 寬的 DC-9 家族機身，客艙典型為 2-3 座位；前後主要艙門分布簡單，機身後段被兩具引擎與進氣口占據。", "The 717 uses the roughly 3.34 m-wide DC-9-family fuselage with typical 2-3 seating. Its simple door layout gives way aft to two engine installations and their inlets.", "717は幅約3.34 mのDC-9系胴体で、客室は通常2-3配列です。単純なドア配置の後方は2基エンジンと吸気口が占めます。"),
            ("它雖比 A220-100 長約 2.8 m，翼展卻短約 6.7 m；側面辨識時可利用長筒狀機身、尾置引擎與高 T 尾的組合。", "Although about 2.8 m longer than the A220-100, its span is roughly 6.7 m shorter. The long tube, rear engines and tall T-tail work together as a side-view signature.", "A220-100より約2.8 m長い一方、翼幅は約6.7 m短く、長い筒状胴体、尾部エンジン、高いT字尾翼が側面の特徴です。"),
            [("客艙窗細小且排列密集。", "Small cabin windows form a closely spaced row.", "小型客室窓が密に並びます。"), ("前艙門後方直到主翼前有長直機身段。", "A long straight fuselage section runs from the forward door toward the wing.", "前扉から主翼前まで長い直線的胴体が続きます。"), ("後機身兩側直接承載引擎短艙。", "The aft fuselage directly carries both engine nacelles.", "後部胴体両側がエンジンナセルを直接支えます。")],
        ),
        "engine": identify(
            ("717 只使用兩具 Rolls-Royce BR715 高旁通比渦扇，安裝在後機身兩側；短艙進氣口位置高，與主翼完全分離。", "The 717 exclusively uses two Rolls-Royce BR715 high-bypass turbofans mounted on the aft fuselage. Their inlets sit high and are completely separate from the wing.", "717はRolls-Royce BR715高バイパスターボファン2基のみを後部胴体両側に搭載し、吸気口は高く主翼と完全に離れています。"),
            ("A220-100 的 PW1500G 尺寸更大且吊掛翼下；即使看不到尾翼，只看引擎位置也幾乎不會混淆。", "The A220-100's larger PW1500Gs hang beneath the wing. Engine location alone nearly eliminates confusion even when the tail is hidden.", "A220-100の大型PW1500Gは主翼下にあり、尾翼が見えなくてもエンジン位置だけでほぼ区別できます。"),
            [("每側一具 BR715 緊貼後機身。", "One BR715 hugs each side of the aft fuselage.", "後部胴体両側にBR715が1基ずつ密着します。"), ("短艙尾端位於 T 尾下方。", "Nacelle exhausts sit beneath the T-tail.", "ナセル排気部はT字尾翼の下にあります。"), ("主翼下沒有任何引擎吊架。", "There are no engine pylons beneath the wing.", "主翼下にエンジンパイロンはありません。")],
        ),
        "wingtip": identify(
            ("717 原始主翼採簡單後掠翼尖，沒有高大翼尖小翼；從客艙向外看，翼尖低矮而平直，只留下導航燈與小型整流外形。", "The 717's original wing ends in a simple swept tip without a tall winglet. From the cabin the tip stays low and plain, carrying only navigation lights and small fairings.", "717の主翼端は高いウイングレットのない単純な後退翼端で、客室からは低く平らに見え、航法灯と小型整流部だけがあります。"),
            ("A220 的翼尖則向上彎成明顯的融合式小翼；這是遠距離區分兩者的第二強線索，僅次於引擎與尾翼布局。", "The A220 tip rises into a distinct blended winglet. After engine and tail layout, this is the next strongest long-range cue.", "A220は翼端が上方へ曲がる明確なブレンデッド・ウイングレットを持ち、エンジンと尾翼に次ぐ遠距離識別点です。"),
            [("翼尖不向上形成大型板狀結構。", "The tip does not rise into a large blade-like device.", "翼端は大型板状に立ち上がりません。"), ("翼展短，翼尖離機身相對近。", "The short span keeps the tip relatively close to the fuselage.", "翼幅が短く翼端は胴体に比較的近いです。"), ("簡單翼尖應與尾置引擎一起確認。", "Confirm the plain tip together with rear-mounted engines.", "単純翼端は尾部エンジンと合わせて確認します。")],
        ),
        "wing": identify(
            ("717 主翼翼展約 28.4 m，面積緊湊、後掠角中等，主翼本身不承載引擎；全機下方可清楚看到乾淨翼面與尾置雙發。", "The 717 wing spans about 28.4 m, with a compact area and moderate sweep. It carries no engines, leaving a clean planform that contrasts with the aft-mounted pair.", "717の主翼幅は約28.4 mで、コンパクトな面積と中程度の後退角を持ち、エンジンを搭載しないため翼面がすっきりしています。"),
            ("A220-100 的 35.1 m 翼展甚至略大於自身 35.0 m 機長；717 則是機長明顯大於翼展，平面比例差異很大。", "The A220-100's 35.1 m span slightly exceeds its 35.0 m length, while the 717 is clearly longer than its span, creating very different planform proportions.", "A220-100は翼幅35.1 mが全長35.0 mをわずかに上回りますが、717は全長が翼幅より明らかに長く、平面比率が大きく異なります。"),
            [("主翼下方沒有引擎或大型吊架。", "No engines or large pylons hang beneath the wing.", "主翼下にエンジンや大型パイロンがありません。"), ("翼根與窄機身交界簡潔。", "The root joins the narrow fuselage with a compact fairing.", "翼根は細い胴体へコンパクトに接続します。"), ("後緣由襟翼、副翼與擾流板構成。", "Flaps, ailerons and spoilers occupy the trailing region.", "後縁にはフラップ、補助翼、スポイラーがあります。")],
        ),
        "vstab": identify(
            ("717 垂直尾翼高而後掠，頂端直接承載整片水平尾翼；引擎進氣口就在垂尾根部前方兩側，形成典型 DC-9 家族尾部。", "The 717's tall swept fin directly carries the complete horizontal tail. Engine inlets flank the fuselage just ahead of its root, creating the classic DC-9-family empennage.", "717の高い後退垂尾は頂部に水平尾翼全体を載せ、根元前方両側にエンジン吸気口がある典型的DC-9系尾部です。"),
            ("A220 的水平尾翼低置於後機身，垂尾頂端沒有橫向翼面；從後方只需看水平尾翼高度即可快速分辨。", "The A220's tailplane is mounted low on the aft fuselage, leaving the fin tip clear. Tailplane height separates the two immediately from behind.", "A220の水平尾翼は後部胴体低位置にあり垂尾頂部は空いています。後方から水平尾翼の高さだけで素早く区別できます。"),
            [("垂尾頂端與水平尾翼交叉成 T 字。", "The fin and tailplane intersect as a T.", "垂尾頂部と水平尾翼がT字に交差します。"), ("根部前方緊鄰兩具引擎短艙。", "Two engine nacelles sit immediately ahead of the fin root.", "垂尾根元前方に2基のナセルがあります。"), ("尾錐細長並延伸至引擎後方。", "A slender tailcone extends aft of the engines.", "細長いテールコーンがエンジン後方へ伸びます。")],
        ),
        "hstab": identify(
            ("717 水平尾翼安裝在垂直尾翼頂端，翼面後掠且略帶下反角；高置可避開尾置引擎的排氣流，也是最醒目的外觀特徵之一。", "The 717's swept tailplane sits atop the fin and shows slight anhedral. Its high position keeps it clear of rear-engine exhaust and is one of the aircraft's strongest visual cues.", "717の後退水平尾翼は垂尾頂部にあり、わずかな下反角を持ちます。尾部エンジン排気を避ける高位置は最も明確な特徴の一つです。"),
            ("A220 的水平尾翼位於機身尾端兩側，與傳統客機相同；若只看到尾部剪影，T 尾與低尾的差異已足以判斷。", "The A220 tailplane sits conventionally on either side of the aft fuselage. In a silhouette, T-tail versus low tail is sufficient to distinguish them.", "A220の水平尾翼は通常どおり後部胴体両側にあり、シルエットではT字尾翼と低位置尾翼の差だけで識別できます。"),
            [("整片尾翼位於垂尾最高處。", "The entire tailplane occupies the top of the fin.", "水平尾翼全体が垂尾最上部にあります。"), ("左右翼面向外後掠並略向下。", "Both panels sweep aft and angle slightly downward.", "左右翼面は後退しわずかに下向きです。"), ("位置遠高於客艙窗與引擎中心線。", "It sits far above the cabin windows and engine centreline.", "客室窓やエンジン中心線よりはるかに高い位置です。")],
        ),
        "gear": identify(
            ("717 前起落架為雙輪，左右主起落架也各為單軸雙輪；收起後主輪收入翼根／機身下方的輪艙。", "The 717 has twin nose wheels and a single-axle twin-wheel main unit on each side, retracting into bays around the wing root and lower fuselage.", "717は前脚2輪、左右主脚も各単軸2輪で、主輪は翼根／胴体下部の脚庫へ格納されます。"),
            ("A220-100 的輪數配置同樣是前二、左右主腳各二，因此輪數不能判型；應改看 A220 的翼下引擎、較寬翼展與不同艙門／支柱。", "The A220-100 has the same two-wheel nose and two-wheel-per-side main arrangement, so wheel count is not diagnostic. Use underwing engines, broader span and different doors/struts.", "A220-100も前脚2輪・左右主脚各2輪で輪数は判別不能です。翼下エンジン、広い翼幅、異なる扉・脚柱を確認します。"),
            [("每側主腳只有一軸兩輪。", "Each main unit has one axle and two tyres.", "各主脚は1軸2輪です。"), ("主腳位於機身中段、主翼根附近。", "The main gear sits near the wing root at mid-fuselage.", "主脚は胴体中央の翼根付近にあります。"), ("判型需同時確認高 T 尾與尾置引擎。", "Confirm the high T-tail and rear engines at the same time.", "高いT字尾翼と尾部エンジンも同時に確認します。")],
        ),
    },
    "cs100": {
        "overview": identify(
            ("Airbus A220-100（原 Bombardier CS100）是 100–135 座級新世代單走道客機，全長約 35.0 m、翼展約 35.1 m；翼下雙發、上彎翼尖與低置水平尾翼構成現代化輪廓。", "The Airbus A220-100, originally the Bombardier CS100, is a new-generation 100-135-seat single-aisle jet about 35.0 m long with a 35.1 m span, combining underwing twins, upturned tips and a low tailplane.", "Airbus A220-100（旧Bombardier CS100）は100～135席級の新世代単通路機で、全長約35.0 m、翼幅約35.1 m、翼下双発、上向き翼端、低位置水平尾翼を備えます。"),
            ("A220 於 2018 年納入 Airbus 產品線，但構型源自 Bombardier 全新設計；它不是縮小版 A320。與 717 相比，布局差異遠大於尺寸差異。", "The A220 joined the Airbus portfolio in 2018 but remains a clean-sheet Bombardier-origin design rather than a shrunken A320. Against the 717, configuration differs far more than overall size.", "A220は2018年にAirbus製品群へ入りましたが、Bombardier起源の新規設計でA320の縮小版ではありません。717とは寸法以上に構成が異なります。"),
            [("兩具大型引擎吊掛於主翼下方。", "Two large engines hang beneath the wing.", "2基の大型エンジンが主翼下にあります。"), ("翼尖明顯向上彎曲。", "The wingtips curve conspicuously upward.", "翼端が明確に上方へ曲がります。"), ("水平尾翼低置，沒有 717 的 T 尾。", "The tailplane is low-mounted with no 717-style T-tail.", "水平尾翼は低位置で717式T字尾翼ではありません。")],
        ),
        "cockpit": identify(
            ("A220 駕駛艙採側桿、五具大型 Collins Pro Line Fusion 橫向顯示器與中央雙推力桿；正副駕駛前方沒有駕駛盤。", "The A220 flight deck uses sidesticks, five large landscape Collins Pro Line Fusion displays and twin thrust levers, with no yokes ahead of the pilots.", "A220の操縦席はサイドスティック、5面大型横長Collins Pro Line Fusion表示器、2本の推力レバーを採用し、操縦輪はありません。"),
            ("雖然使用側桿，A220 的座艙並非 A320 家族同款：螢幕數量、尺寸、中央台與控制面板布局都不同。", "Despite its sidesticks, the A220 does not share the A320-family flight deck; screen count, proportions, pedestal and control panels all differ.", "サイドスティックを使いますがA320系と同じ操縦席ではなく、画面数・比率・中央台・操作盤が異なります。"),
            [("五具大型橫向螢幕形成連續玻璃面板。", "Five wide displays form a continuous glass panel.", "5面の大型横長画面が連続したグラスパネルを作ります。"), ("側桿位於兩名駕駛外側。", "Sidesticks sit outboard of both pilots.", "サイドスティックは両操縦席外側にあります。"), ("中央台有兩支推力桿與系統控制器。", "Twin thrust levers and system controllers occupy the pedestal.", "中央台に2本の推力レバーとシステム操作部があります。")],
        ),
        "windshield": identify(
            ("A220 的駕駛艙窗具有寬大的正面風擋、厚黑窗框與圓角外側窗；整組窗帶沿長而尖的機鼻平順向側面收束。", "The A220 has broad front windscreens, dark substantial frames and rounded outer panes. The complete belt tapers smoothly around a long pointed nose.", "A220の窓は広い前面風防、太い暗色枠、丸角の外側窓を持ち、長く尖った機首に沿って滑らかに側面へ絞られます。"),
            ("717 的窗框更細碎、折角更銳利，機鼻也更短圓；正面看 A220 主風擋像一組寬大的深色面罩。", "The 717 glazing is more segmented and angular over a shorter rounder nose. Head-on, the A220 front panes read as one broad dark mask.", "717はより細分化され角張り、機首も短く丸いです。正面のA220窓は広い暗色マスクのように見えます。"),
            [("兩片主風擋寬且上緣略帶弧度。", "The two main panes are broad with subtly curved upper edges.", "2枚の主風防は幅広く上縁に緩い曲線があります。"), ("外側窗較圓，窗框連續包向側面。", "Rounded outer panes and frames flow continuously around the side.", "丸い外側窓と枠が側面へ連続します。"), ("窗下機鼻較長並向前下方收尖。", "The nose below stretches forward and tapers downward.", "窓下の機首は長く前下方へ細くなります。")],
        ),
        "fuselage": identify(
            ("A220-100 機身最大直徑約 3.5 m、客艙寬約 3.28 m，典型為 2-3 座位；大型橢圓客艙窗、較寬機身與長尖機鼻帶來不同於 717 的比例。", "The A220-100 fuselage is about 3.5 m in maximum diameter with a 3.28 m cabin and typical 2-3 seating. Large oval windows, a broader body and long pointed nose distinguish it from the 717.", "A220-100の最大胴体径は約3.5 m、客室幅約3.28 mで通常2-3配列です。大型楕円窓、太い胴体、長く尖った機首が717と異なります。"),
            ("A220-100 比 A220-300 短 3.7 m；辨識 -100 時可看主翼前後較短的窗列與較緊湊艙門間距。", "The A220-100 is 3.7 m shorter than the A220-300. Its shorter window rows ahead of and behind the wing and tighter door spacing identify the variant.", "A220-100はA220-300より3.7 m短く、主翼前後の短い窓列と詰まった扉間隔で判別できます。"),
            [("橢圓客艙窗比 717 窗片更大。", "Oval cabin windows are larger than the 717's.", "楕円客室窓は717より大型です。"), ("長機鼻從駕駛艙窗向前平順收尖。", "A long nose tapers smoothly ahead of the cockpit glazing.", "長い機首が操縦席窓から前方へ滑らかに細くなります。"), ("後機身沒有尾置引擎遮擋窗列。", "No rear-mounted engines interrupt the aft fuselage.", "尾部エンジンがなく後部胴体が遮られません。")],
        ),
        "engine": identify(
            ("A220 家族只使用 Pratt & Whitney PW1500G 齒輪傳動渦扇，短艙直徑大、風扇葉片寬，兩具引擎由吊架安裝於主翼下。", "The A220 family exclusively uses Pratt & Whitney PW1500G geared turbofans. Their large-diameter nacelles and broad fan blades hang beneath the wings on pylons.", "A220ファミリーはPratt & Whitney PW1500Gギヤードターボファン専用で、大径ナセルと幅広ファンを主翼下パイロンに搭載します。"),
            ("BR715 與 PW1500G 都是高旁通比引擎，但位置完全不同：717 在尾部，A220 在翼下；這比辨認風扇葉片更可靠。", "Both BR715 and PW1500G are high-bypass engines, but placement is entirely different: aft fuselage on the 717 and underwing on the A220, a more reliable cue than blade details.", "BR715とPW1500Gはいずれも高バイパスですが、717は尾部、A220は翼下で、ファン形状より確実な識別点です。"),
            [("大型風扇進氣口位於主翼前緣下方。", "Large fan inlets sit below and ahead of the wing leading edge.", "大型ファン吸気口は主翼前縁下方にあります。"), ("每側一具引擎，由短吊架連接主翼。", "One engine per side hangs from a short pylon.", "左右各1基が短いパイロンで主翼に接続します。"), ("後機身保持乾淨，沒有引擎短艙。", "The aft fuselage remains clean without nacelles.", "後部胴体にはナセルがありません。")],
        ),
        "wingtip": identify(
            ("A220 翼尖由外翼平順向上彎成融合式小翼，外形細長、後掠並略向外傾；從客艙窗看十分明顯。", "The A220 outer wing blends smoothly upward into a slender swept winglet that leans slightly outward and is conspicuous from the cabin.", "A220の外翼は滑らかに上方へ曲がる細長い後退ウイングレットとなり、やや外傾して客室窓から明瞭に見えます。"),
            ("717 只有低矮平直翼尖；當機身或尾翼被遮住時，有無上彎小翼仍可快速分辨。", "The 717 has only a low plain tip. When fuselage or tail is hidden, the presence or absence of the upturned winglet still separates them.", "717は低い通常翼端のみで、胴体や尾翼が隠れても上向きウイングレットの有無で判別できます。"),
            [("小翼與外翼之間沒有銳利直角。", "There is no sharp right-angle break between wing and winglet.", "主翼とウイングレット間に鋭い直角はありません。"), ("翼尖高於主翼上表面並向後收尖。", "The tip rises above the wing and tapers aft.", "翼端は主翼上面より高く後方へ細くなります。"), ("航空公司塗裝常延伸到小翼表面。", "Airline colours often continue onto the winglet.", "航空会社塗装がウイングレットまで続くことがあります。")],
        ),
        "wing": identify(
            ("A220-100 主翼翼展約 35.1 m，展弦比高且具明顯上反角；大型 PW1500G、襟翼整流罩與融合式翼尖共同形成寬大的平面輪廓。", "The A220-100 wing spans about 35.1 m with high aspect ratio and visible dihedral. Large PW1500Gs, flap-track fairings and blended tips create a broad planform.", "A220-100の主翼幅は約35.1 mで高アスペクト比と明確な上反角を持ち、大型PW1500G、フラップトラックフェアリング、融合翼端が広い平面形を作ります。"),
            ("翼展略大於機長是 A220-100 的重要比例；717 則是狹翼、機長遠大於翼展。", "A span slightly greater than length is an important A220-100 proportion; the 717 has a narrow wing and is much longer than its span.", "翼幅が全長をわずかに上回るのがA220-100の重要比率で、717は狭い翼で全長が翼幅を大きく上回ります。"),
            [("主翼下方各吊掛一具大型引擎。", "One large engine hangs beneath each wing.", "各主翼下に大型エンジン1基があります。"), ("外翼細長並平順接入上彎小翼。", "The slender outer wing flows into an upturned winglet.", "細長い外翼が上向きウイングレットへ滑らかにつながります。"), ("翼面具多片擾流板與大型單縫襟翼。", "Multiple spoilers and large single-slotted flaps occupy the wing.", "複数スポイラーと大型単隙間フラップがあります。")],
        ),
        "vstab": identify(
            ("A220 垂直尾翼高大後掠，根部以長背鰭平順接入後機身；頂端沒有水平尾翼，輪廓清楚獨立。", "The A220 has a tall swept fin with a long dorsal root blending into the aft fuselage. Its tip is unobstructed because the tailplane is mounted low.", "A220の垂直尾翼は高く後退し、長い背びれ根元が後部胴体へ滑らかにつながります。水平尾翼が低位置のため頂部は独立しています。"),
            ("717 的垂尾頂部被水平尾翼橫穿，且根部兩側有引擎；A220 的乾淨單垂尾從任何後方角度都更傳統。", "The 717 fin is crossed by its tailplane and flanked by engines at the root. The A220's clean standalone fin looks conventional from every rear angle.", "717は垂尾頂部を水平尾翼が横切り根元両側にエンジンがありますが、A220は後方から通常の独立垂尾に見えます。"),
            [("垂尾頂端略方，沒有 T 尾橫翼。", "The slightly squared fin tip carries no T-tail surface.", "やや角形の垂尾頂部にT字尾翼はありません。"), ("前緣背鰭向前延伸，與機身平順融合。", "A forward dorsal fillet blends smoothly into the fuselage.", "前縁背びれが前方へ伸び胴体へ滑らかにつながります。"), ("低置水平尾翼從尾錐兩側伸出。", "Low-mounted tailplanes extend from the tailcone sides.", "低位置水平尾翼が尾部両側から伸びます。")],
        ),
        "hstab": identify(
            ("A220 水平尾翼低置於後機身兩側，後掠並向外收尖；尾錐上方只剩獨立垂尾，構成傳統尾翼布局。", "The A220's swept tapered tailplanes mount low on either side of the aft fuselage, leaving a standalone fin above in a conventional empennage.", "A220の後退・先細水平尾翼は後部胴体両側の低位置にあり、その上に独立垂尾が立つ通常尾翼配置です。"),
            ("與 717 高置 T 尾相比，高度差異非常大；即使照片只拍到尾部，也不需要依靠塗裝或航空公司判斷。", "The height difference from the 717's T-tail is enormous. Even a tail-only photograph can be identified without relying on livery or operator.", "717の高いT字尾翼とは高さが大きく異なり、尾部だけの写真でも塗装や航空会社に頼らず判別できます。"),
            [("水平尾翼根部位於機身尾錐中段。", "The tailplane root sits midway up the tailcone.", "水平尾翼根元はテールコーン中段にあります。"), ("左右翼面後掠並逐漸收尖。", "Both surfaces sweep aft and taper outward.", "左右翼面は後退し外側へ細くなります。"), ("位置低於垂尾高度一半。", "It sits well below half the fin height.", "垂尾高さの半分より十分低い位置です。")],
        ),
        "gear": identify(
            ("A220-100 前起落架為雙輪，左右主腳各為單軸雙輪；主腳由機腹向外可見厚實支柱、拖曳連桿與分段艙門。", "The A220-100 has twin nose wheels and a single-axle twin-wheel main unit on each side. Its main gear exposes a substantial strut, trailing links and segmented bay doors.", "A220-100は前脚2輪、左右主脚各単軸2輪で、主脚には太い脚柱、トレーリングリンク、分割脚扉が見えます。"),
            ("總輪數與 717 相同，兩者都不能靠『六輪』判型；A220 的主腳附近可同時看見翼下引擎與更寬的主翼。", "Total wheel count matches the 717, so 'six wheels' identifies neither. Around the A220 gear, underwing engines and a broader wing remain visible.", "総輪数は717と同じで「6輪」だけでは判別できません。A220主脚付近では翼下エンジンと広い主翼も確認できます。"),
            [("左右主腳各一軸兩輪。", "Each main gear has one axle and two tyres.", "左右主脚は各1軸2輪です。"), ("支柱與輪艙門外形不同於 717。", "Strut and bay-door geometry differ from the 717's.", "脚柱と脚扉形状は717と異なります。"), ("判型時優先看翼下 PW1500G。", "Prioritise the underwing PW1500Gs when identifying it.", "識別では翼下PW1500Gを優先確認します。")],
        ),
    },
})


CONTENT.update({
    "b737": {
        "overview": identify(
            ("737-700 是短機身 737NG，全長約 33.63 m；低矮窄機身、較尖機鼻、底部扁平的 CFM56-7B 與收起後外露的主輪，是比機身長短更可靠的外型線索。", "The 737-700 is the short-bodied 737NG, about 33.63 m long. Its low narrow body, pointed nose, flat-bottomed CFM56-7Bs and exposed retracted main wheels are stronger cues than length alone.", "737-700は全長約33.63 mの短胴737NGです。低く細い胴体、尖り気味の機首、下面が平たいCFM56-7B、格納後も露出する主輪が、全長より確実な特徴です。"),
            ("A319 全長約 33.84 m，只比 737-700 長約 0.21 m；兩者幾乎等長，遠距辨識應改看引擎短艙、機鼻與離地高度。", "At roughly 33.84 m, the A319 is only about 0.21 m longer. The pair is effectively equal in length, so use nacelles, nose and ground stance.", "A319は約33.84 mで差は約0.21 mしかありません。全長ではなくナセル、機首、地上姿勢で判別します。"),
            [("機身低、窄，機鼻較有折角。", "Low narrow fuselage with a more angular nose.", "低く細い胴体と角張った機首です。"), ("CFM56-7B 進氣口底部明顯扁平。", "CFM56-7B inlets have a flattened lower lip.", "CFM56-7B吸気口下面が平たい形です。"), ("主輪收起後胎面仍從機腹外露。", "Main-wheel faces remain exposed after retraction.", "格納後も主輪面が機腹に露出します。")],
        ),
        "cockpit": identify(
            ("737NG 駕駛艙保留傳統駕駛盤、中央操縱柱、六具主要顯示器與大量實體控制器；中央台兩側的大型黑白配平輪很醒目。", "The 737NG flight deck retains yokes, control columns, six main displays and many physical controls; large black-and-white trim wheels flank the centre pedestal.", "737NG操縦席は操縦輪、コラム、6面主要表示器、多数の物理操作部を持ち、中央台両側の白黒トリムホイールが目立ちます。"),
            ("A319 使用側桿並在飛行員正前方保留桌板；是否有駕駛盤是兩者最直接的座艙差異。", "The A319 uses sidesticks and leaves tray tables ahead of the pilots. Yokes versus no yokes is the clearest cockpit distinction.", "A319はサイドスティックと正面テーブルを使います。操縦輪の有無が最も直接的な差です。"),
            [("正副駕駛前方各有駕駛盤。", "A yoke sits ahead of each pilot.", "両操縦席正面に操縦輪があります。"), ("典型 737NG 有六具主要顯示器。", "A typical 737NG has six main displays.", "標準737NGは6面主要表示器です。"), ("中央台可見大型手動配平輪。", "Large manual trim wheels sit beside the pedestal.", "中央台脇に大型手動トリムホイールがあります。")],
        ),
        "windshield": identify(
            ("737-700 的正面風擋較扁、中央接縫近直立，外側窗以銳利折角轉向側面；配合較尖機鼻形成典型 Boeing 737 窗帶。", "The 737-700 has shallow front panes with a near-vertical centre seam and sharply angled outer panes wrapping around a pointed nose.", "737-700は浅い前面窓、ほぼ垂直の中央継ぎ目、鋭く側面へ折れる外側窓を持ち、尖った機首と737特有の窓帯を作ります。"),
            ("不要只數窗片；正面窗高寬比、外側窗折角及窗帶與機鼻的銜接方式，比片數更有辨識力。", "Do not count panes alone. Front-pane proportions, outer-pane corners and the way the belt meets the nose are more useful.", "窓枚数だけでなく、前面窓比率、外側窓の角、機首とのつながりを見ます。"),
            [("兩片主風擋較寬扁。", "The two main panes look broad and shallow.", "2枚の主風防は幅広く浅く見えます。"), ("外側窗框折角明顯。", "Outer frames have pronounced angular breaks.", "外側窓枠の折れ角が明瞭です。"), ("窗下機鼻較尖而低。", "The nose below is relatively pointed and low.", "窓下の機首は低く尖り気味です。")],
        ),
        "fuselage": identify(
            ("737-700 機身外寬約 3.76 m，典型每側有前後主艙門與一個機翼上方逃生窗；短窗列和單一翼上出口可與較長的 737-800 區分。", "The 737-700 fuselage is about 3.76 m wide and typically has forward/aft main doors plus one overwing exit per side. Its short window rows and single overwing exit distinguish it from a 737-800.", "737-700の胴体幅は約3.76 mで、通常は各側に前後ドアと翼上非常口1か所があります。短い窓列と単一翼上出口が737-800との違いです。"),
            ("A319 也通常只有一個翼上逃生窗，因此出口數不能單獨分辨；737 較窄、較低且機鼻窗框更有折角。", "The A319 also normally has one overwing exit per side, so exit count alone is insufficient; the 737 is narrower, lower and more angular at the nose.", "A319も通常翼上出口1か所のため数だけでは不十分です。737は細く低く、機首窓がより角張ります。"),
            [("每側前後各一扇主艙門。", "One main door sits at each end on either side.", "各側前後に主ドア1枚ずつです。"), ("典型配置每側一個翼上逃生窗。", "A typical layout has one overwing exit per side.", "標準配置は各側翼上出口1か所です。"), ("機身比 A319 約窄 19 cm。", "The fuselage is about 19 cm narrower than the A319's.", "胴体はA319より約19 cm細いです。")],
        ),
        "engine": identify(
            ("737-700 固定使用兩具 CFM56-7B。因 737 離地低，附件移到兩側，使進氣口與短艙底部呈明顯扁平的非圓形輪廓。", "The 737-700 exclusively uses two CFM56-7Bs. Low clearance forced accessories to the sides, giving the inlet and nacelle a visibly flattened underside.", "737-700はCFM56-7Bを2基使用します。低い地上高に合わせ補機を側面配置し、吸気口・ナセル下面が明確に平たくなっています。"),
            ("A319ceo 的 CFM56-5B 或 V2500 短艙底部更接近圓形；即使兩者都寫 CFM56，-7B 與 -5B 的安裝外形仍不同。", "A319ceo CFM56-5B or V2500 nacelles are rounder underneath. Both may say CFM56, but -7B and -5B installations look different.", "A319ceoのCFM56-5B／V2500は下面がより円形です。同じCFM56でも-7Bと-5Bの装着外形は異なります。"),
            [("進氣口下緣壓扁。", "The inlet lower lip is flattened.", "吸気口下縁が平たい形です。"), ("短艙緊貼低置主翼下方。", "The nacelle sits tightly beneath the low wing.", "ナセルは低い主翼直下に密着します。"), ("此子型只使用 CFM56-7B。", "This variant uses only the CFM56-7B.", "この型はCFM56-7B専用です。")],
        ),
        "wingtip": identify(
            ("737-700 可完全沒有小翼，也可裝高大的融合式小翼或 Split Scimitar；構型取決於出廠與後續改裝狀態。", "A 737-700 may have plain tips, tall blended winglets or Split Scimitar devices depending on production and retrofit status.", "737-700は通常翼端、背の高いブレンデッド型、スプリット・シミター型があり、製造・改修状態で変わります。"),
            ("A319 也有翼尖擋板與 Sharklet 兩種主要外觀，所以高小翼本身不是 Boeing／Airbus 的充分證據。", "The A319 likewise appears with tip fences or Sharklets, so a tall winglet alone is not proof of Boeing or Airbus.", "A319にも翼端フェンスとシャークレットがあり、高い小翼だけではBoeing／Airbusを確定できません。"),
            [("融合式小翼由翼面平順向上彎。", "A blended winglet curves smoothly upward.", "ブレンデッド型は翼面から滑らかに上方へ曲がります。"), ("Split Scimitar 另有向下小翼片。", "Split Scimitar adds a lower blade.", "スプリット・シミター型は下向き翼片も持ちます。"), ("需搭配扁平短艙與外露主輪判型。", "Confirm with flat nacelles and exposed main wheels.", "平たいナセルと露出主輪で照合します。")],
        ),
        "wing": identify(
            ("737NG 主翼後掠約 25°，翼根離地低，襟翼滑軌整流罩突出；客艙視角可同時看到扁平 CFM56-7B 與選裝小翼。", "The 737NG wing is swept about 25 degrees, sits low and carries prominent flap-track fairings; cabin views also reveal flat CFM56-7Bs and optional winglets.", "737NG主翼は約25度後退し低位置で、フラップトラックフェアリングが目立ちます。客室から平たいCFM56-7Bと小翼も見えます。"),
            ("737-700 與 A319 翼展在裝小翼時都約 35.8 m；翼展幾乎相同，不能當作現場判型依據。", "With winglets, both span about 35.8 m. Their nearly identical span is not a practical identification cue.", "小翼装備時は両機とも翼幅約35.8 mで、翼幅は現場識別に使えません。"),
            [("低置主翼與機腹距離較小。", "The low wing sits close to the belly.", "低置主翼は機腹に近い位置です。"), ("後緣有多段襟翼與擾流板。", "Multi-section flaps and spoilers line the trailing edge.", "後縁に多段フラップとスポイラーがあります。"), ("扁平引擎短艙是客艙視角的強線索。", "Flat nacelles are a strong cabin-view cue.", "平たいナセルが客室視点の強い手掛かりです。")],
        ),
        "vstab": identify(
            ("737-700 垂直尾翼前緣下方有長背鰭，方向舵後緣較直，頂端向後收尖；尾翼比例在短機身上顯得較高。", "The 737-700 fin has a long dorsal fillet, a relatively straight rudder trailing edge and an aft-tapered tip; it appears tall on the short fuselage.", "737-700垂直尾翼は長い背びれ、比較的直線的な方向舵後縁、後方へ細る上端を持ち、短胴では高く見えます。"),
            ("A319 的垂尾根部與後機身過渡較寬；尾翼塗裝只能辨識營運者，不能代替結構比較。", "The A319 fin root blends more broadly into the aft body. Livery identifies the operator, not the structure.", "A319の垂尾根元は後部胴体へより幅広くつながります。塗装は会社識別用で機体構造判定には使えません。"),
            [("前緣背鰭向前延伸。", "A dorsal fillet extends forward.", "前縁背びれが前方へ伸びます。"), ("方向舵後緣近直線。", "The rudder trailing edge is nearly straight.", "方向舵後縁はほぼ直線です。"), ("短機身讓垂尾視覺比例偏高。", "The short body makes the fin look proportionally tall.", "短胴のため垂尾が相対的に高く見えます。")],
        ),
        "hstab": identify(
            ("737-700 水平尾翼低置於尾錐兩側，後掠並向外收尖；由下方可同時看到尾翼與 737 特有的外露主輪。", "The 737-700 has low-mounted swept tapered tailplanes. An underside view can show the tail together with the 737's exposed main wheels.", "737-700水平尾翼は尾部両側の低位置にあり後退・先細です。下面から尾翼と737特有の露出主輪を同時に確認できます。"),
            ("737-700 與 A319 都是傳統低置水平尾翼，單看此部位很難定型，應視為輔助線索。", "Both use conventional low tailplanes, so this part alone is weak and should remain a supporting cue.", "両機とも通常の低位置水平尾翼で、この部位単独では弱い補助手掛かりです。"),
            [("尾翼低置且後掠。", "The tailplane is low-mounted and swept.", "水平尾翼は低位置・後退形です。"), ("翼根與尾錐平順接合。", "The root blends smoothly into the tailcone.", "翼根が尾部へ滑らかにつながります。"), ("應搭配引擎與收輪方式判讀。", "Use it with nacelle and gear-retraction cues.", "ナセルと脚格納方式も合わせて見ます。")],
        ),
        "gear": identify(
            ("737-700 前腳雙輪，左右主腳各單軸雙輪；主腳收起時沒有完整外側艙門，輪胎胎面仍可從機腹看見。", "The 737-700 has twin nose wheels and a two-wheel main unit per side. With no full outer doors, tyre faces remain visible when retracted.", "737-700は前脚2輪、左右主脚各単軸2輪で、完全な外扉がなく格納後もタイヤ面が見えます。"),
            ("A319 的輪數完全相同，但主輪收入有艙門遮蔽；輪數不能分辨，收輪外觀才可以。", "The A319 has the same wheel count, but doors cover its retracted mains. Wheel count does not distinguish them; retraction appearance does.", "A319も輪数は同じですが格納主輪は扉で覆われます。輪数ではなく格納外観を見ます。"),
            [("前腳與每側主腳皆為雙輪。", "Nose and each main unit use twin wheels.", "前脚と左右主脚は各2輪です。"), ("收起主輪胎面從機腹外露。", "Retracted main tyre faces remain exposed.", "格納主輪面が機腹に露出します。"), ("機身離地高度低於 A319。", "The fuselage sits lower than the A319's.", "胴体地上高はA319より低いです。")],
        ),
    },
    "a319": {
        "overview": identify(
            ("A319 是短機身 A320 家族成員，全長約 33.84 m；較寬且離地較高的機身、圓鈍機鼻、近圓形引擎短艙與有艙門遮蔽的主輪構成主要外型。", "The A319 is the short-bodied A320-family member, about 33.84 m long. Its wider higher body, rounded nose, rounder nacelles and covered retracted mains define the profile.", "A319は全長約33.84 mの短胴A320ファミリー機です。太く高い胴体、丸い機首、円形に近いナセル、扉で覆われる格納主輪が特徴です。"),
            ("它與 737-700 幾乎等長、裝 Sharklet 時翼展也幾乎相同；辨識不能依賴尺寸，必須回到機鼻、引擎與起落架。", "It is nearly identical to the 737-700 in length and, with Sharklets, span. Size is therefore weak; use nose, engines and landing gear.", "737-700と全長がほぼ同じで、Sharklet装備時の翼幅も同等です。寸法でなく機首、エンジン、脚を見ます。"),
            [("機身寬且離地較高。", "The fuselage is wider and sits higher.", "胴体が太く地上高も高めです。"), ("機鼻圓鈍，窗帶輪廓較平順。", "The nose is rounder with a smoother window belt.", "機首は丸く窓帯も滑らかです。"), ("短艙底部接近圓形，主輪格納後被遮蔽。", "Nacelles are round underneath and retracted mains are covered.", "ナセル下面は円形に近く格納主輪は覆われます。")],
        ),
        "cockpit": identify(
            ("A319 與 A320 家族共用側桿式玻璃座艙：飛行員前方沒有駕駛盤，而是桌板；中央兩具 ECAM 顯示引擎與系統狀態。", "The A319 shares the A320-family sidestick glass cockpit: no yokes ahead of the pilots, tray tables instead, and two central ECAM system displays.", "A319はA320ファミリー共通のサイドスティック式グラスコックピットで、正面に操縦輪がなくテーブルと中央2面ECAMがあります。"),
            ("A318、A319、A320、A321 的座艙高度共通，僅靠內裝通常無法判斷機身子型；但可立即排除有駕駛盤的 737。", "A318/A319/A320/A321 cockpits are highly common, so the exact subtype is hard to tell inside; the absence of yokes immediately separates a 737.", "A318／A319／A320／A321の操縦席は共通性が高く子型判別は困難ですが、操縦輪がないため737とはすぐ区別できます。"),
            [("側桿位於兩名駕駛外側。", "Sidesticks sit outboard of both pilots.", "サイドスティックは両席外側です。"), ("飛行員正前方設有桌板。", "Tray tables occupy the space ahead of the pilots.", "両席正面にテーブルがあります。"), ("中央 ECAM 上下排列。", "Central ECAM displays are stacked vertically.", "中央ECAMは上下配置です。")],
        ),
        "windshield": identify(
            ("A319 的主風擋較高，外側窗沿圓鈍機鼻向後收尖，整組窗帶的上下線條比 737 平順；正面看有典型 Airbus 六片式面貌。", "The A319 has taller front panes and outer panes tapering smoothly around a rounded nose, forming the classic six-pane Airbus face.", "A319は高い前面窓と、丸い機首に沿って滑らかに後方へ細る外側窓を持つ典型的Airbus六枚窓です。"),
            ("737-700 的主窗較扁、外側折角更銳利；正面與側面照片一起看，比單一角度可靠。", "The 737-700's main panes are shallower and outer corners sharper. Compare front and side views together.", "737-700は主窓が浅く外側角が鋭いです。正面・側面写真を併用します。"),
            [("正面主風擋較高。", "The main front panes appear taller.", "正面主風防が高く見えます。"), ("外側窗向後平順收尖。", "Outer panes taper smoothly aft.", "外側窓が後方へ滑らかに細くなります。"), ("圓鼻讓整組窗帶顯得較寬。", "The rounded nose makes the belt look broader.", "丸い機首で窓帯が幅広く見えます。")],
        ),
        "fuselage": identify(
            ("A319 機身外寬約 3.95 m，典型每側有前後主艙門及一個機翼上方逃生窗；比 A320 短的翼前、翼後窗列是辨識子型的重點。", "The A319 fuselage is about 3.95 m wide and typically has forward/aft main doors plus one overwing exit per side. Short window runs ahead of and behind the wing separate it from an A320.", "A319の胴体幅は約3.95 mで、通常各側に前後ドアと翼上出口1か所があります。翼前後の短い窓列がA320との識別点です。"),
            ("737-700 也有相近的門／出口數，因此應再看 A319 較寬機身、圓鼻與圓形短艙。", "The 737-700 has a similar door/exit count, so confirm the A319's wider body, round nose and round nacelles.", "737-700も似た扉数なので、A319の太い胴体、丸い機首、円形ナセルで確認します。"),
            [("每側前後各一扇主艙門。", "One main door sits at each end per side.", "各側前後に主ドア1枚ずつです。"), ("典型配置每側一個翼上逃生窗。", "A typical layout has one overwing exit per side.", "標準配置は各側翼上出口1か所です。"), ("機身比 737-700 約寬 19 cm。", "The body is about 19 cm wider than the 737-700's.", "胴体は737-700より約19 cm太いです。")],
        ),
        "engine": identify(
            ("A319ceo 可選 CFM56-5B 或 IAE V2500，兩者進氣口底部都比 737 的 CFM56-7B 更接近圓形，且因機身姿態較高而有較大離地間隙。", "The A319ceo uses CFM56-5B or IAE V2500 engines. Both are rounder underneath than the 737's CFM56-7B and have more ground clearance.", "A319ceoはCFM56-5BまたはV2500を使用し、737のCFM56-7Bより下面が円形で地上間隔も大きいです。"),
            ("A319neo 改用 LEAP-1A 或 PW1100G，風扇更大；本頁實機照片與辨識重點以常見 A319ceo 為主。", "The A319neo uses larger LEAP-1A or PW1100G engines. This reference and its cues focus on the common A319ceo.", "A319neoは大型LEAP-1A／PW1100Gを使用します。本写真と識別点は一般的なA319ceo中心です。"),
            [("短艙下緣接近圓形。", "The nacelle lower lip is close to circular.", "ナセル下縁は円形に近いです。"), ("離地間隙大於 737-700。", "Ground clearance exceeds the 737-700's.", "地上間隔は737-700より大きいです。"), ("ceo 有 CFM56-5B 與 V2500 兩種外觀。", "The ceo appears with CFM56-5B or V2500 nacelles.", "ceoにはCFM56-5BとV2500の2種があります。")],
        ),
        "wingtip": identify(
            ("早期 A319 常見上下各伸出一片的小型翼尖擋板；較晚期或改裝機可見高大的 Sharklet，外觀會隨年代改變。", "Early A319s commonly use small upper-and-lower tip fences, while later or retrofitted aircraft may carry tall Sharklets.", "初期A319は上下の小型翼端フェンス、後期・改修機は背の高いSharkletを装備します。"),
            ("上下翼尖擋板是很強的 A320 家族線索；若看到 Sharklet，則需用圓形短艙、圓鼻與主輪艙門排除 737。", "Upper/lower fences are a strong A320-family cue. With Sharklets, use round nacelles, round nose and covered mains to exclude a 737.", "上下フェンスは強いA320系の特徴です。Sharklet装備では円形ナセル、丸い機首、覆われる主輪で737を除外します。"),
            [("經典擋板同時向上、向下伸出。", "Classic fences project both above and below the tip.", "従来フェンスは翼端上下へ伸びます。"), ("Sharklet 高大且向外後掠。", "A Sharklet is tall and swept outward.", "Sharkletは高く外後方へ伸びます。"), ("構型會隨出廠與改裝狀態改變。", "Configuration varies by production and retrofit status.", "構成は製造・改修状態で変わります。")],
        ),
        "wing": identify(
            ("A319 與 A320 共用基本低翼，後掠約 25°；翼根位置較 737 高，外翼末端可接翼尖擋板或 Sharklet。", "The A319 shares the basic A320 low wing, swept about 25 degrees. Its wing sits higher than the 737's and ends in fences or Sharklets.", "A319はA320共通の約25度後退低翼で、737より高い位置にあり、翼端フェンスまたはSharkletを備えます。"),
            ("兩型翼展十分接近；從客艙看，A319 的圓形短艙與翼尖擋板通常比翼面形狀更有辨識力。", "The spans are very close. From the cabin, round nacelles and tip devices are more useful than planform.", "両機の翼幅は近く、客室からは翼形より円形ナセルと翼端装置が有効です。"),
            [("翼根離地較高。", "The wing root sits higher above the ground.", "翼根地上高が高めです。"), ("後緣有大型襟翼與擾流板。", "Large flaps and spoilers line the trailing edge.", "後縁に大型フラップとスポイラーがあります。"), ("翼尖裝置是客艙視角的重要線索。", "The tip device is a useful cabin-view cue.", "翼端装置が客室視点の重要な手掛かりです。")],
        ),
        "vstab": identify(
            ("A319 垂直尾翼高大後掠，根部以寬背鰭平順接入後機身；在短機身上也呈現偏高的視覺比例。", "The A319 has a tall swept fin with a broad dorsal root blending into the aft fuselage; it also looks proportionally tall on the short body.", "A319垂直尾翼は高く後退し、幅広い背びれ根元が後部胴体へつながり、短胴上で高く見えます。"),
            ("尾翼輪廓與 737 有差異但不如引擎、機鼻與起落架明顯；應作輔助而非單一判據。", "Fin shape differs from the 737 but less clearly than engines, nose and gear, so it is supporting rather than decisive.", "737との差はありますがエンジン・機首・脚ほど明確でなく、補助判定に使います。"),
            [("前緣後掠、頂端較方。", "The leading edge is swept and the tip relatively squared.", "前縁は後退し上端は比較的角形です。"), ("根部整流區寬而平順。", "The root fairing is broad and smooth.", "根元フェアリングは幅広く滑らかです。"), ("短機身讓尾翼顯得較高。", "The short body makes the fin appear tall.", "短胴で尾翼が高く見えます。")],
        ),
        "hstab": identify(
            ("A319 水平尾翼低置、後掠並向翼尖收窄，根部與尾錐整流罩平順融合；與 A320 家族共用基本輪廓。", "The A319 has low-mounted swept tapered tailplanes smoothly faired into the tailcone, sharing the basic A320-family form.", "A319水平尾翼は低位置で後退・先細、尾部へ滑らかに接続するA320ファミリー共通形状です。"),
            ("737-700 也使用相似的低置尾翼，因此應同時查看垂尾根部、引擎短艙與主輪收納方式。", "The 737-700 has a similar low tailplane, so also inspect fin root, nacelles and main-gear stowage.", "737-700も似た低位置尾翼なので、垂尾根元、ナセル、主輪格納も確認します。"),
            [("水平尾翼低置於尾錐兩側。", "Tailplanes mount low on either side of the tailcone.", "水平尾翼は尾部両側の低位置です。"), ("後掠並向外逐漸收窄。", "They sweep aft and taper outward.", "後退し外側へ細くなります。"), ("單看此部位不足以定型。", "This part alone is insufficient for identification.", "この部位だけでは機種を確定できません。")],
        ),
        "gear": identify(
            ("A319 前腳雙輪、左右主腳各單軸雙輪；主腳向內收入翼身整流區，艙門會遮蔽輪胎，不像 737 收輪後仍露出胎面。", "The A319 has twin nose wheels and a two-wheel main unit per side. The mains retract inward behind doors, unlike the 737's exposed tyre faces.", "A319は前脚2輪、左右主脚各単軸2輪で、内側へ格納され扉に覆われ、737のようにタイヤ面が露出しません。"),
            ("兩者總輪數都為六輪，輪數完全無法區分；最可靠的是 A319 較長腳柱、較高離地姿態與完整艙門。", "Both total six wheels, so wheel count is useless. The A319's taller struts, higher stance and full doors are stronger cues.", "両機とも合計6輪で輪数は使えません。A319の長い脚柱、高い姿勢、完全な脚扉を見ます。"),
            [("前腳與每側主腳皆為雙輪。", "Nose and each main unit use twin wheels.", "前脚と左右主脚は各2輪です。"), ("收起主輪由艙門遮蔽。", "Doors cover the retracted main wheels.", "格納主輪は扉で覆われます。"), ("離地高度高於 737-700。", "Ground clearance is greater than the 737-700's.", "地上高は737-700より高いです。")],
        ),
    },
})


CONTENT.update({
    "crj900": {
        "overview": identify(
            ("CRJ900 是細長的區域噴射機，全長約 36.4 m、翼展 24.85 m；兩具 CF34 裝在後機身，水平尾翼位於垂尾頂端。", "The CRJ900 is a slender regional jet about 36.4 m long with a 24.85 m span. Two aft-fuselage CF34s sit below a high T-tail.", "CRJ900は全長約36.4 m、翼幅24.85 mの細長いリージョナル機で、後部胴体のCF34双発と高いT字尾翼が特徴です。"),
            ("E190 幾乎同樣長，卻有更寬的機身與更大翼展；先看引擎位置和尾翼高度，比估算尺寸可靠。", "The E190 is almost the same length but wider and broader-winged. Engine location and tailplane height are more reliable than apparent size.", "E190はほぼ同じ長さですが胴体と翼幅が大きく、見かけの寸法よりエンジン位置と水平尾翼高さが確実です。"),
            [("後機身左右各一具引擎。", "One engine mounts on each side of the aft fuselage.", "後部胴体左右にエンジンが1基ずつあります。"), ("水平尾翼形成清楚的 T 字。", "The tailplane forms a clear T-tail.", "水平尾翼は明確なT字を形成します。"), ("機身細、翼展短，外形像被拉長。", "A narrow body and short span create a stretched look.", "細い胴体と短い翼幅で引き伸ばされた外観です。")],
        ),
        "cockpit": identify(
            ("CRJ900 駕駛艙使用傳統駕駛盤與 Collins Pro Line 4 系列玻璃座艙，六具顯示器分列在兩名飛行員與中央區域。", "The CRJ900 flight deck uses conventional yokes and a Collins Pro Line 4 glass cockpit with six displays across the pilot and centre panels.", "CRJ900は従来型操縦輪とCollins Pro Line 4グラスコックピットを採用し、操縦席と中央部に6画面を配置します。"),
            ("E190 同樣使用駕駛盤，不能只靠『有沒有駕駛盤』分辨；CRJ 面板較緊湊，中央顯示器比例也不同。", "The E190 also uses yokes, so yoke presence alone does not identify it. The CRJ panel is tighter, with a different centre-display arrangement.", "E190も操縦輪式のため、それだけでは区別できません。CRJはパネルが狭く中央表示配置も異なります。"),
            [("兩席前方都有駕駛盤與操縱柱。", "Both pilots have yokes and control columns.", "両席に操縦輪とコラムがあります。"), ("典型布局為六具電子顯示器。", "The typical layout uses six electronic displays.", "標準配置は6面電子表示器です。"), ("窄機身讓座艙橫向空間較緊湊。", "The narrow fuselage makes the flight deck visibly compact.", "細い胴体のため操縦席幅はコンパクトです。")],
        ),
        "windshield": identify(
            ("CRJ900 正面風擋較直立而窄，中央兩片近矩形；外側窗以明顯折角接入細長機鼻，正面看窗帶較緊湊。", "CRJ900 windscreens are upright and narrow, with near-rectangular centre panes and sharply angled outer panes wrapping a slim nose.", "CRJ900の風防は直立気味で細く、中央窓は矩形に近く、外側窓が鋭い角度で細い機首へ回り込みます。"),
            ("E190 的主風擋更寬，外側窗與較圓的機鼻融合；兩型都應同時查看正面和側面，避免受拍攝角度誤導。", "The E190 has broader main panes blended into a rounder nose. Use front and side views together because perspective can mislead.", "E190は主窓が広く丸い機首へ滑らかにつながります。撮影角度の影響を避けるため正面と側面を併用します。"),
            [("中央窗片高而較窄。", "Centre panes look tall and narrow.", "中央窓は高く細く見えます。"), ("外側窗折角清楚。", "Outer panes form a distinct angular break.", "外側窓の折れ角が明瞭です。"), ("窗帶相對整個機鼻顯得小。", "The glazing looks small relative to the nose.", "窓帯は機首に対して小さく見えます。")],
        ),
        "fuselage": identify(
            ("CRJ900 外寬約 2.69 m，客艙為 2+2 座位；長而窄的窗列、低矮艙門與後機身引擎整流區形成典型 CRJ 比例。", "The CRJ900 fuselage is about 2.69 m wide with 2+2 seating. Its long narrow window row, compact doors and aft-engine fairings define CRJ proportions.", "CRJ900の胴体幅は約2.69 mで2+2席です。長く細い窓列、小型ドア、後部エンジン整流部がCRJらしい比率を作ります。"),
            ("E190 機身約寬 3.01 m，雖然同為 2+2，艙門與舷窗看起來更大，機鼻到主翼的體積也更飽滿。", "The E190 is about 3.01 m wide. Though also 2+2, its doors, windows and forward body look visibly larger and fuller.", "E190は幅約3.01 mで同じ2+2ですが、ドアと窓が大きく機首から主翼までの胴体もふっくら見えます。"),
            [("細長機身是最直接的比例線索。", "The pencil-thin body is the clearest proportion cue.", "鉛筆のような細長い胴体が最も明確です。"), ("客艙窗尺寸較小且排列密集。", "Cabin windows are small and closely spaced.", "客室窓は小さく密に並びます。"), ("後段機身被兩具引擎夾住。", "The aft fuselage is flanked by two engines.", "後部胴体は2基のエンジンに挟まれます。")],
        ),
        "engine": identify(
            ("CRJ900 使用兩具 GE CF34-8C5，高旁通比短艙直接固定在後機身兩側；主翼下方完全沒有引擎吊架。", "The CRJ900 uses two GE CF34-8C5 turbofans attached directly to the aft fuselage, leaving the wing undersides free of engine pylons.", "CRJ900はGE CF34-8C5を後部胴体両側へ直接搭載し、主翼下にエンジンパイロンがありません。"),
            ("E190 的 CF34-10E 更大且吊在主翼下；兩者雖同屬 CF34 家族，引擎安裝位置才是最強辨識點。", "The E190's larger CF34-10Es hang beneath the wings. Although both use CF34-family engines, installation location is decisive.", "E190の大型CF34-10Eは主翼下にあり、同じCF34系でも搭載位置が決定的な識別点です。"),
            [("短艙緊貼後機身。", "Nacelles hug the aft fuselage.", "ナセルは後部胴体に密着します。"), ("進氣口位於主翼後方。", "Intakes sit behind the wing.", "吸気口は主翼後方です。"), ("翼下輪廓保持乾淨。", "The wing underside remains free of engines.", "主翼下面にエンジンがありません。")],
        ),
        "wingtip": identify(
            ("CRJ900 主翼末端有小型直立翼尖小翼，翼展短且小翼比例醒目；從正面可看見兩片小翼像細小刀片向上伸出。", "The CRJ900 ends its short-span wing in small upright winglets that look like thin blades from the front.", "CRJ900は短い主翼端に小型直立ウイングレットを持ち、正面では細い刃のように見えます。"),
            ("E190 也有上彎翼尖裝置，因此『有小翼』本身不能分辨；應搭配翼展和引擎位置。", "The E190 also has upturned tips, so winglets alone do not identify either aircraft; combine them with span and engine location.", "E190にも上向き翼端装置があるため、小翼だけでなく翼幅とエンジン位置を併用します。"),
            [("小翼窄而接近直立。", "The winglet is narrow and nearly vertical.", "小翼は細くほぼ直立です。"), ("相對短翼展，小翼顯得較突出。", "It stands out against the short span.", "短い翼幅に対して小翼が目立ちます。"), ("不是判型的單一證據。", "It is not a standalone identification cue.", "単独の識別根拠にはなりません。")],
        ),
        "wing": identify(
            ("CRJ900 主翼翼展 24.85 m，後掠且面積緊湊，引擎不在翼下；機翼中央位置較後，強化細長機身的視覺比例。", "The CRJ900 has a compact swept 24.85 m wing with no underwing engines. Its relatively aft position emphasizes the long narrow fuselage.", "CRJ900の主翼は翼幅24.85 mのコンパクトな後退翼で翼下エンジンがなく、後寄りの位置が細長い胴体を強調します。"),
            ("E190 翼展達 28.72 m，約多 3.9 m，且翼下吊有引擎；從下方或遠距離看差異很明顯。", "The E190 spans 28.72 m—about 3.9 m more—and carries underwing engines, making the difference clear from below or at distance.", "E190の翼幅は28.72 mで約3.9 m広く、翼下エンジンもあるため下面や遠距離で差が明瞭です。"),
            [("主翼下沒有引擎吊架。", "No engine pylons hang beneath the wing.", "主翼下にエンジンパイロンがありません。"), ("翼展明顯短於機長。", "Span is much shorter than fuselage length.", "翼幅は全長より大幅に短いです。"), ("後緣可見襟翼與小型整流罩。", "Flaps and compact fairings line the trailing edge.", "後縁にフラップと小型整流部があります。")],
        ),
        "vstab": identify(
            ("CRJ900 垂直尾翼高而後掠，頂端直接承載水平尾翼；根部前方兩側就是引擎短艙，形成集中而複雜的尾部輪廓。", "The CRJ900's tall swept fin carries the tailplane at its tip, while engine nacelles flank the root, creating a concentrated T-tail silhouette.", "CRJ900の高い後退垂尾は頂部に水平尾翼を載せ、根元両側にナセルがある集中的なT字尾部です。"),
            ("E190 垂尾頂端沒有水平翼面，低置尾翼從後機身兩側伸出；尾翼布局可在一秒內分開兩型。", "The E190 fin tip is clear, with tailplanes extending low from the aft fuselage. Tail layout separates the pair immediately.", "E190は垂尾頂部が空き、水平尾翼は後部胴体低位置から伸びるため即座に区別できます。"),
            [("垂尾頂端與水平尾翼交叉。", "The tailplane intersects the fin tip.", "垂尾頂部で水平尾翼と交差します。"), ("垂尾根部鄰近雙發短艙。", "Twin nacelles flank the fin root.", "垂尾根元の両側にナセルがあります。"), ("尾部整體高度高但翼展窄。", "The empennage is tall but narrow in span.", "尾部は高い一方で幅は狭いです。")],
        ),
        "hstab": identify(
            ("CRJ900 水平尾翼位於垂直尾翼頂端，是完整的 T 型尾翼；高置設計讓尾翼遠離主翼和後置引擎尾流。", "The CRJ900 tailplane sits atop the fin as a full T-tail, keeping it high above the wing and aft-engine flow field.", "CRJ900の水平尾翼は垂尾頂部の完全なT字尾翼で、主翼や後置エンジン流れから高く離れます。"),
            ("E190 的水平尾翼低置在尾錐兩側；即使只看到後半機身，水平尾翼高度通常已足以分辨。", "The E190 tailplane mounts low beside the tailcone. Even a partial rear view usually reveals enough height difference to identify it.", "E190の水平尾翼は尾部両側の低位置にあり、後半部だけでも高さで識別できます。"),
            [("位於整架飛機最高處。", "It sits at the aircraft's highest point.", "機体の最上部にあります。"), ("由正面形成鮮明 T 字。", "It forms a strong T shape head-on.", "正面で明確なT字になります。"), ("位置比 E190 高出整個後機身。", "It sits a full aft-fuselage height above the E190's.", "E190より後部胴体一つ分ほど高い位置です。")],
        ),
        "gear": identify(
            ("CRJ900 為前三點式起落架，前腳雙輪、左右主腳各雙輪，共六輪；短腳柱配合窄機身，落地時姿態低而纖細。", "The CRJ900 has twin nose wheels and a twin-wheel main unit per side—six wheels total. Short struts support its low, slender stance.", "CRJ900は前脚2輪、左右主脚各2輪の計6輪で、短い脚柱が低く細い姿勢を支えます。"),
            ("E190 輪數完全相同，但腳距更寬、機身離地較高，且主腳位於翼下引擎附近；輪數不能作為判型依據。", "The E190 has the same wheel count but a wider track, taller stance and mains near the underwing engines. Wheel count is not diagnostic.", "E190も同じ6輪ですが、輪距が広く地上高が高く、主脚は翼下エンジン近くにあります。輪数では区別できません。"),
            [("前腳與每側主腳皆為雙輪。", "Nose and each main unit use twin wheels.", "前脚と左右主脚は各2輪です。"), ("主腳間距較窄。", "The main-gear track is relatively narrow.", "主脚輪距は比較的狭いです。"), ("機身離地姿態較低。", "The fuselage sits relatively low.", "胴体の地上高は比較的低いです。")],
        ),
    },
    "e190": {
        "overview": identify(
            ("E190 是約百座級 E-Jet，全長 36.24 m、翼展 28.72 m；較寬機身、翼下雙發與低置水平尾翼構成接近縮小型幹線客機的比例。", "The E190 is a roughly 100-seat E-Jet, 36.24 m long with a 28.72 m span. Its wider body, underwing twinjets and low tailplane resemble a compact mainline airliner.", "E190は約100席、全長36.24 m、翼幅28.72 mで、太い胴体、翼下双発、低位置尾翼が小型幹線機のような比率を作ります。"),
            ("CRJ900 幾乎同長，但翼展少約 3.9 m，且引擎與水平尾翼都集中在尾部；不要靠機長猜測。", "The CRJ900 is nearly the same length but spans about 3.9 m less and concentrates engines and tailplane at the rear. Length alone misleads.", "CRJ900はほぼ同じ長さでも翼幅が約3.9 m狭く、エンジンと水平尾翼が尾部へ集中します。全長だけでは誤認します。"),
            [("兩具引擎吊在主翼下。", "Two engines hang beneath the wings.", "2基のエンジンは主翼下です。"), ("水平尾翼位於後機身低處。", "The tailplane sits low on the aft fuselage.", "水平尾翼は後部胴体の低位置です。"), ("機身比 CRJ900 寬而飽滿。", "The body is wider and fuller than the CRJ900's.", "胴体はCRJ900より太くふっくらしています。")],
        ),
        "cockpit": identify(
            ("E190 使用 Honeywell Primus Epic 玻璃座艙，兩席都有傳統駕駛盤，五具大型彩色顯示器橫向排列，面板比 CRJ900 更寬。", "The E190 uses a Honeywell Primus Epic glass cockpit with conventional yokes and five large colour displays across a broader panel.", "E190はHoneywell Primus Epicグラスコックピットで、操縦輪と幅広いパネル上の大型カラー5画面を備えます。"),
            ("兩型都有駕駛盤；E190 的五螢幕布局、較寬中央面板與更寬座艙才是內部辨識重點。", "Both types have yokes. The E190's five-display layout, broader centre panel and wider cockpit are the useful interior cues.", "両機とも操縦輪式で、E190の5画面配置、広い中央パネル、広い操縦席が識別点です。"),
            [("兩席前方各有駕駛盤。", "A yoke sits ahead of each pilot.", "両席正面に操縦輪があります。"), ("五具大型顯示器橫向排列。", "Five large displays span the panel.", "大型5画面が横方向に並びます。"), ("座艙寬度明顯大於 CRJ。", "The cockpit is visibly wider than the CRJ's.", "操縦席幅はCRJより明らかに広いです。")],
        ),
        "windshield": identify(
            ("E190 主風擋較寬，中央接縫下方配合圓鈍機鼻形成柔和 V 形；外側窗向後收尖，整組窗帶比 CRJ900 更寬。", "The E190 has broad main windscreens forming a soft V over a rounded nose, with outer panes tapering aft into a wider glazing band.", "E190は丸い機首上に柔らかなV字を作る広い主風防と、後方へ細る外側窓を持ち、窓帯はCRJ900より幅広いです。"),
            ("CRJ900 的中央窗更窄、折角更明顯；辨識時把窗帶寬度與機鼻圓鈍程度一起看。", "The CRJ900's centre panes are narrower and more angular. Compare glazing width together with nose fullness.", "CRJ900は中央窓が細く角張ります。窓帯幅と機首の丸みを合わせて見ます。"),
            [("主風擋寬而稍向外傾。", "Main panes are broad and slightly splayed.", "主風防は広く外側へわずかに開きます。"), ("外側窗沿機身側面收尖。", "Outer panes taper along the fuselage side.", "外側窓は胴体側面へ細くなります。"), ("圓鼻讓窗帶顯得較低而寬。", "The round nose makes the glazing look low and wide.", "丸い機首で窓帯が低く広く見えます。")],
        ),
        "fuselage": identify(
            ("E190 外寬約 3.01 m，客艙採 2+2 座位且沒有中間座；較大的舷窗、全尺寸前後艙門和飽滿翼身整流罩接近幹線客機尺度。", "The E190 is about 3.01 m wide with 2+2 seating and no middle seat. Larger windows, full-size end doors and a broad wing-body fairing give mainline-aircraft proportions.", "E190の胴体幅は約3.01 m、2+2席で中央席がありません。大きな窓、前後ドア、幅広い翼胴フェアリングが幹線機らしい比率です。"),
            ("CRJ900 雖然同樣是 2+2，機身約窄 32 cm；從正面或艙門尺度比較，差異比側面長度更清楚。", "Although both seat 2+2, the CRJ900 is about 32 cm narrower. Front views and door scale reveal the difference better than side length.", "同じ2+2でもCRJ900は約32 cm細く、側面の長さより正面やドア寸法で差が分かります。"),
            [("機身截面較圓且寬。", "The fuselage section is rounder and wider.", "胴体断面はより丸く幅広いです。"), ("前後均有大型客艙門。", "Large passenger doors sit fore and aft.", "前後に大型客室ドアがあります。"), ("翼身整流罩寬而平順。", "The wing-body fairing is broad and smooth.", "翼胴フェアリングは幅広く滑らかです。")],
        ),
        "engine": identify(
            ("E190 使用兩具 GE CF34-10E，短艙以吊架固定在低置主翼下方；進氣口尺寸大於 CRJ900 的 CF34-8C5。", "The E190 uses two GE CF34-10E turbofans suspended below the low wing, with larger intakes than the CRJ900's CF34-8C5s.", "E190はGE CF34-10Eを低翼下へ吊り下げ、吸気口はCRJ900のCF34-8C5より大きいです。"),
            ("兩型名稱都出現 CF34，但短艙位置完全不同；看到翼下雙發就應優先考慮 E190，而非 CRJ900。", "Both engine names include CF34, but installation is completely different. Underwing twinjets strongly favour the E190 over the CRJ900.", "両方CF34系でも搭載位置は全く異なり、翼下双発ならCRJ900よりE190を優先します。"),
            [("每側主翼下吊掛一具引擎。", "One engine hangs beneath each wing.", "左右主翼下に1基ずつあります。"), ("短艙進氣口接近圓形。", "The nacelle intake is nearly circular.", "ナセル吸気口はほぼ円形です。"), ("後機身兩側沒有引擎。", "No engines flank the aft fuselage.", "後部胴体側面にエンジンはありません。")],
        ),
        "wingtip": identify(
            ("原型 E190 主翼末端有向上延伸的融合式翼尖小翼，外形比 CRJ900 小翼更寬、後掠更明顯。", "The original E190 wing ends in an upturned blended winglet, broader and more swept than the CRJ900's narrow tip device.", "初代E190は上向きブレンデッド・ウイングレットを持ち、CRJ900の細い小翼より幅広く後退しています。"),
            ("E190-E2 改為重新設計的無傳統小翼翼尖；本頁照片與內容描述第一代 E190，不應套用到 E190-E2。", "The E190-E2 uses a redesigned wing without this traditional winglet. This page describes the first-generation E190.", "E190-E2は従来型小翼のない新主翼で、本頁は初代E190を対象とします。"),
            [("小翼向上且略向後彎。", "The winglet rises and sweeps slightly aft.", "小翼は上方かつやや後方へ伸びます。"), ("底部與翼尖平順融合。", "Its base blends smoothly into the tip.", "基部は翼端へ滑らかにつながります。"), ("需確認不是 E190-E2。", "Confirm that the aircraft is not an E190-E2.", "E190-E2でないことを確認します。")],
        ),
        "wing": identify(
            ("E190 主翼翼展 28.72 m，後掠且翼下承載兩具引擎；大型襟翼、擾流板與明顯襟翼滑軌整流罩可從客艙清楚觀察。", "The E190's 28.72 m swept wing carries two engines and features large flaps, spoilers and visible flap-track fairings.", "E190の翼幅28.72 mの後退翼は2基のエンジンを搭載し、大型フラップ、スポイラー、フラップトラック整流部が見えます。"),
            ("CRJ900 翼展較短且翼下完全乾淨；由下方看，E190 的引擎吊架和更寬翼面是直接差異。", "The CRJ900 has a shorter, engine-free wing underside. From below, the E190's pylons and broader wing are unmistakable.", "CRJ900は翼幅が短く翼下が空いており、下面ではE190のパイロンと広い翼面が明確です。"),
            [("翼下可見引擎與吊架。", "Engines and pylons are visible beneath the wing.", "主翼下にエンジンとパイロンがあります。"), ("翼展約比 CRJ900 多 3.9 m。", "Span exceeds the CRJ900's by about 3.9 m.", "翼幅はCRJ900より約3.9 m広いです。"), ("後緣有明顯襟翼滑軌整流罩。", "Prominent flap-track fairings line the trailing edge.", "後縁に目立つフラップトラック整流部があります。")],
        ),
        "vstab": identify(
            ("E190 垂直尾翼高而後掠，根部以寬背鰭平順接入後機身；頂端沒有水平尾翼，輪廓保持單一三角形。", "The E190 has a tall swept fin with a broad dorsal blend into the aft fuselage. Its tip is clear of the tailplane, preserving a simple triangular outline.", "E190の垂尾は高く後退し幅広い背びれで後部胴体へつながり、頂部に水平尾翼がない単純な三角形です。"),
            ("CRJ900 的垂尾頂端被水平尾翼橫穿，根部又鄰近兩具引擎；只看垂尾輪廓就能快速排除。", "The CRJ900 fin is crossed by a tailplane at the top and flanked by engines at the root, making separation immediate.", "CRJ900は頂部を水平尾翼が横切り根元にエンジンがあるため、垂尾だけでもすぐ区別できます。"),
            [("垂尾頂端沒有橫向翼面。", "No horizontal surface crosses the fin tip.", "垂尾頂部に水平面がありません。"), ("根部背鰭寬而平順。", "The dorsal root is broad and smooth.", "根元背びれは幅広く滑らかです。"), ("後機身側面沒有引擎短艙。", "No nacelles flank the aft fuselage.", "後部胴体側面にナセルがありません。")],
        ),
        "hstab": identify(
            ("E190 水平尾翼低置在後機身兩側，後掠並向外收尖；其高度約與主翼同屬機身中下部，而非架在垂尾頂端。", "The E190's swept tapered tailplanes mount low on either side of the aft fuselage rather than atop the fin.", "E190の後退・先細水平尾翼は後部胴体両側の低位置にあり、垂尾頂部ではありません。"),
            ("CRJ900 使用 T 尾；由正面、側面或後方，只要看到水平尾翼高度就能完成最可靠的判型。", "The CRJ900 uses a T-tail. From front, side or rear, tailplane height is the most reliable distinction.", "CRJ900はT字尾翼で、正面・側面・後方いずれも水平尾翼高さが最も確実です。"),
            [("水平尾翼從尾錐兩側伸出。", "Tailplanes project from the sides of the tailcone.", "水平尾翼は尾部両側から伸びます。"), ("位置遠低於垂尾頂端。", "They sit well below the fin tip.", "垂尾頂部より大幅に低い位置です。"), ("低置尾翼與翼下引擎應一起確認。", "Confirm the low tail with underwing engines.", "低位置尾翼と翼下エンジンを合わせて確認します。")],
        ),
        "gear": identify(
            ("E190 前腳雙輪、左右主腳各雙輪，共六輪；較長腳柱與較寬輪距讓機身和翼下引擎保持足夠離地間隙。", "The E190 has twin nose wheels and twin wheels on each main unit—six total. Taller struts and a wider track provide clearance for the body and underwing engines.", "E190は前脚2輪、左右主脚各2輪の計6輪で、長い脚柱と広い輪距が胴体と翼下エンジンの地上間隔を確保します。"),
            ("CRJ900 也是六輪，但主腳更靠近窄機身、姿態更低；比較輪距與引擎位置，不要比較輪數。", "The CRJ900 also has six wheels, but its mains sit closer to the narrow body and lower stance. Compare track and engines, not wheel count.", "CRJ900も6輪ですが主脚は細い胴体に近く姿勢も低いため、輪数でなく輪距とエンジン位置を見ます。"),
            [("前腳與每側主腳皆為雙輪。", "Nose and each main unit use twin wheels.", "前脚と左右主脚は各2輪です。"), ("主腳輪距較寬。", "The main-gear track is relatively wide.", "主脚輪距は比較的広いです。"), ("機身與翼下引擎離地較高。", "The fuselage and engines sit higher above ground.", "胴体と翼下エンジンの地上高が高めです。")],
        ),
    },
})


SOURCES.update({
    "crj700": {
        "overview": "https://commons.wikimedia.org/wiki/File:D-ACPF.JPG",
        "cockpit": "https://commons.wikimedia.org/wiki/File:Bombardier-crj-900-cockpit-by-RalfR.jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:N154GJ_(6961124918)_(cropped).jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:D-ACPF.JPG",
        "fuselage": "https://commons.wikimedia.org/wiki/File:D-ACPF.JPG",
        "engine": "https://commons.wikimedia.org/wiki/File:D-ACPF.JPG",
        "wingtip": "https://commons.wikimedia.org/wiki/File:American_Eagle_CRJ-700_at_Eugene_Airport.jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:Lufthansa_D-ACPH.JPG",
        "vstab": "https://commons.wikimedia.org/wiki/File:D-ACPF.JPG",
        "hstab": "https://commons.wikimedia.org/wiki/File:LH_CRJ-700_D-ACPO_EDDT.jpg",
        "gear": "https://commons.wikimedia.org/wiki/File:N154GJ_(6961124918)_(cropped).jpg",
    },
    "e170": {
        "overview": "https://commons.wikimedia.org/wiki/File:Finnair_Embraer_170_OH-LEK_at_HEL_17AUG2014.JPG",
        "cockpit": "https://commons.wikimedia.org/wiki/File:Cockpit_of_LOT_Embraer_ERJ-175LR_(SP-LIN).jpg",
        "window_front": "https://commons.wikimedia.org/wiki/File:Peoples_Viennaline_ERJ-170_OE-LMK_LSZR_01.jpg",
        "window_side": "https://commons.wikimedia.org/wiki/File:Finnair_Embraer_170_OH-LEK_at_HEL_17AUG2014.JPG",
        "fuselage": "https://commons.wikimedia.org/wiki/File:Finnair_Embraer_170_OH-LEK_at_HEL_17AUG2014.JPG",
        "engine": "https://commons.wikimedia.org/wiki/File:Finnair_Embraer_170_OH-LEK_at_HEL_17AUG2014.JPG",
        "wingtip": "https://commons.wikimedia.org/wiki/File:Peoples_Viennaline_ERJ-170_OE-LMK_LSZR_01.jpg",
        "wing": "https://commons.wikimedia.org/wiki/File:Peoples_Viennaline_ERJ-170_OE-LMK_LSZR_01.jpg",
        "vstab": "https://commons.wikimedia.org/wiki/File:Finnair_Embraer_170_OH-LEK_at_HEL_17AUG2014.JPG",
        "hstab": "https://commons.wikimedia.org/wiki/File:Finnair_Embraer_170_OH-LEK_at_HEL_17AUG2014.JPG",
        "gear": "https://commons.wikimedia.org/wiki/File:Peoples_Viennaline_ERJ-170_OE-LMK_LSZR_01.jpg",
    },
})

CONTENT.update({
    "crj700": {
        "overview": identify(
            ("CRJ700 全長 32.51 m、翼展 23.24 m；細長低矮的機身、尾部雙發與 T 型尾翼形成主要輪廓，翼下沒有引擎。", "At 32.51 m long with a 23.24 m span, the CRJ700 combines a slender low-slung body, rear engines and a T-tail; its wings carry no engines.", "CRJ700は全長32.51 m、翼幅23.24 m。細長く低い胴体、後部双発、T字尾翼が特徴で、翼下にエンジンはありません。"),
            ("比 E170 約長 2.6 m，翼展卻少約 2.8 m。與 CRJ900 比較則機身更短，不能只用相同的機鼻或尾翼判定子型。", "It is about 2.6 m longer than the E170 but about 2.8 m narrower in span. It is shorter than the CRJ900: the shared nose and tail alone cannot identify the variant.", "E170より約2.6 m長い一方、翼幅は約2.8 m短くなります。CRJ900より短胴で、共通の機首・尾翼だけでは型式を判定できません。"),
            [("尾部兩側各一具引擎。", "One engine on each side of the rear body.", "後部胴体の左右にエンジン各1基。"), ("水平尾翼位於垂尾頂端。", "Tailplanes sit atop the fin.", "水平尾翼は垂尾頂部。"), ("細長機身搭配較短翼展。", "Slender body with a relatively short span.", "細長い胴体と比較的短い翼幅。")],
        ),
        "cockpit": identify(
            ("CRJ700 採傳統駕駛盤與六具主要電子顯示器，左右飛行資訊及中央系統顯示形成對稱布局。附圖為 CRJ900 實照，僅示範 CRJ700／900 共通的基本座艙配置。", "The CRJ700 uses conventional yokes and six main electronic displays, arranged symmetrically around central system displays. The photograph is a CRJ900, illustrating the shared basic CRJ700/900 layout only.", "CRJ700は操縦輪と主要表示器6面を備え、中央のシステム表示を挟む対称配置です。写真はCRJ900で、CRJ700／900共通の基本配置のみを示します。"),
            ("E170 也有駕駛盤，但使用五具大型顯示器；判別時看面板布局，不能把『有駕駛盤』直接當成 CRJ。", "The E170 also has yokes but uses five large displays. Identify the panel layout rather than assuming every yoke-equipped cockpit is a CRJ.", "E170も操縦輪を持ちますが大型画面は5面。操縦輪の有無でなくパネル配置を比較します。"),
            [("六具主要顯示器。", "Six main displays.", "主要表示器6面。"), ("左右各有傳統駕駛盤。", "Conventional yoke at each seat.", "両席に従来型操縦輪。"), ("家族參考圖不代表所有選裝設備相同。", "Family reference does not imply identical optional equipment.", "共通参考写真でも選択装備は機体ごとに異なります。")],
        ),
        "windshield": identify(
            ("CRJ700 外窗沿狹窄機鼻環繞，正面有明顯中央窗柱，側窗呈稜角分明的梯形；窗帶下方的機鼻向前收成較尖輪廓。", "CRJ700 glazing wraps around a narrow nose, with a prominent centre post and angular trapezoidal side panes. Below the windows the nose tapers to a relatively pointed profile.", "CRJ700の窓は細い機首を囲み、中央窓柱と角張った台形の側窓が目立ちます。窓の下の機首は比較的鋭く絞られます。"),
            ("CRJ700／900 的窗型十分接近，外窗主要用來區分家族；要分辨兩者仍須看機身長度與出口配置。", "CRJ700 and CRJ900 window shapes are very similar. Glazing identifies the family; body length and exit layout help separate the variants.", "CRJ700／900の窓形状は非常に近く、窓は系列の識別用です。型式は胴体長と出口配置も見ます。"),
            [("正面中央窗柱明顯。", "Distinct centre windshield post.", "明確な中央窓柱。"), ("側窗稜角清楚、機鼻狹長。", "Angular side glazing on a narrow nose.", "角張った側窓と細い機首。"), ("用正面與側面兩個角度交叉確認。", "Cross-check front and side views.", "正面と側面の両方で確認。")],
        ),
        "fuselage": identify(
            ("CRJ700 保留窄機身 2+2 客艙，前方乘客門接近地面，舷窗沿細長機身排列；照片可見翼上逃生出口與後段引擎之間的間距。", "The CRJ700 retains a narrow 2+2 cabin, a low front passenger door and a long row of windows. The photo shows the spacing between the overwing exit and aft engine.", "CRJ700は細い2+2客室、地面に近い前方乗降扉、細長く並ぶ窓を持ちます。写真で翼上非常口と後部エンジンの間隔を確認できます。"),
            ("E170 同樣每排四座，但機身更寬且較短。CRJ700 的門檻高度與細長比例，比塗裝或航空公司名稱更有判型價值。", "The E170 also seats four abreast but has a wider, shorter body. Door-sill height and slenderness are more useful than livery or airline branding.", "E170も横4席ですが胴体は太く短く、塗装より扉の高さと細長さが識別に役立ちます。"),
            [("窄機身四座並列客艙。", "Narrow four-abreast cabin.", "細い横4席の客室。"), ("前乘客門門檻較低。", "Low front passenger-door sill.", "低い前方乗降扉。"), ("出口與後置引擎位置一起觀察。", "Read exits together with the rear engines.", "出口と後部エンジンの位置を合わせて観察。")],
        ),
        "engine": identify(
            ("CRJ700 的兩具 GE CF34-8C 系列引擎安裝在後機身兩側，圓形進氣口與短吊架清楚可見，主翼下方保持乾淨。", "Two GE CF34-8C-series engines flank the CRJ700's rear fuselage. Circular inlets and short mounting pylons are visible, leaving the wing undersides clear.", "CRJ700のGE CF34-8C系2基は後部胴体両側にあり、円形吸気口と短いパイロンが見え、翼下は空いています。"),
            ("早期使用 CF34-8C1，後續有 CF34-8C5B1；不能只憑短艙照片確認細部引擎型號。E170 則是翼下 CF34-8E。", "Early aircraft used CF34-8C1s, followed by CF34-8C5B1s. A nacelle photo alone cannot establish the exact engine subvariant. The E170 uses underwing CF34-8Es.", "初期はCF34-8C1、後にCF34-8C5B1を採用。ナセル写真だけで細部型式は断定できません。E170は翼下CF34-8Eです。"),
            [("進氣口在後段客艙兩側。", "Inlets flank the aft cabin.", "後部客室両側に吸気口。"), ("短吊架連接機身。", "Short pylons connect to the fuselage.", "短いパイロンで胴体に接続。"), ("翼下沒有引擎短艙。", "No underwing nacelles.", "翼下ナセルなし。")],
        ),
        "wingtip": identify(
            ("CRJ700 翼端有細窄、向上伸起的小翼，主翼與小翼之間的轉折清楚；由正面可見兩端像小型直立鰭。", "The CRJ700 has narrow upturned winglets with a distinct transition from wing to tip. Head-on, each tip resembles a small upright fin.", "CRJ700の翼端は細い上向き小翼で、主翼との折れ曲がりが明確です。正面では小さな立ち上がりに見えます。"),
            ("E170 也有上彎小翼，因此小翼不是獨有特徵；搭配尾置引擎和 T 尾才是可靠組合。", "The E170 also has upturned winglets, so this is not unique. Combine the tip with rear engines and a T-tail.", "E170も上向き小翼を持つため、小翼だけでなく後部エンジンとT字尾翼を組み合わせます。"),
            [("細窄向上的小翼。", "Narrow upward winglet.", "細い上向き小翼。"), ("翼端轉折清楚。", "Clear wing-to-winglet transition.", "翼端の折れ曲がりが明確。"), ("不是上下各一片的翼尖擋板。", "Not an upper/lower wingtip fence.", "上下に分かれた翼端フェンスではありません。")],
        ),
        "wing": identify(
            ("CRJ700 採低置後掠翼，翼展約 23.24 m；主翼下沒有引擎吊架，從下方可清楚觀察翼根、襟翼及收起的主輪。", "The CRJ700 has a low swept wing spanning about 23.24 m. With no engine pylons beneath it, the wing root, flaps and retracted main wheels are easy to distinguish from below.", "CRJ700は翼幅約23.24 mの低翼後退翼です。翼下パイロンがなく、下面から翼根、フラップ、格納主輪を確認できます。"),
            ("相近座級的 E170 翼展較大且翼下有引擎。CRJ700 的窄長機身與較短主翼組合，可從斜下方辨認。", "The similarly sized E170 has a greater span and underwing engines. The CRJ700's narrow body and shorter wing are useful from a low oblique angle.", "同程度の座席数のE170は翼幅が広く翼下エンジンを備えます。斜め下からはCRJ700の細長い胴体と短めの翼を見ます。"),
            [("低置後掠主翼。", "Low-mounted swept wing.", "低翼・後退翼。"), ("無翼下引擎吊架。", "No underwing engine pylons.", "翼下エンジンパイロンなし。"), ("翼展小於 E170。", "Shorter span than the E170.", "E170より短い翼幅。")],
        ),
        "vstab": identify(
            ("CRJ700 垂尾高而後掠，頂部承載水平尾翼，底部前方則有兩具後置引擎，形成明確的 T 字形尾部結構。", "The CRJ700's swept fin carries the tailplane at its top, with the rear engines just ahead of its base: a clear T-tail arrangement.", "CRJ700の後退垂尾は頂部に水平尾翼、根元前方に後部エンジンを持つ明確なT字構成です。"),
            ("E170 垂尾頂端沒有橫向翼面；即使航空公司塗裝相似，只看水平尾翼接在哪裡也能快速區分。", "The E170 has no horizontal surface atop its fin. Tailplane attachment remains useful even with similar airline liveries.", "E170は垂尾頂部に水平面がなく、似た塗装でも水平尾翼の取付位置で区別できます。"),
            [("頂端承載水平尾翼。", "Tailplane mounted at the fin tip.", "垂尾頂部に水平尾翼。"), ("後掠前緣。", "Swept leading edge.", "後退した前縁。"), ("根部鄰近兩具引擎。", "Two engines near the fin root.", "根元近くにエンジン2基。")],
        ),
        "hstab": identify(
            ("CRJ700 水平尾翼架在垂尾頂端，由後方能看到橫向翼面與高垂尾組成 T 字，遠高於主翼和引擎。", "The CRJ700 tailplane sits atop the fin. Seen from behind, it forms a T well above the wing and engines.", "CRJ700の水平尾翼は垂尾頂部にあり、後方から主翼・エンジンより高いT字形が見えます。"),
            ("與 E170 低置水平尾翼相比，安裝高度是比尾翼塗裝更可靠的差異；CRJ900 同樣採 T 尾，仍須配合機身長度。", "Mounting height is more reliable than tail paint when comparing with the E170's low tailplane. The CRJ900 also has a T-tail, so check body length too.", "E170の低位置水平尾翼との比較では塗装より取付高さが確実です。CRJ900もT字尾翼なので胴体長も確認します。"),
            [("水平翼面位於機體尾端最高處。", "Horizontal surface at the top of the tail.", "尾部最高位置の水平面。"), ("後視呈 T 字。", "T-shaped rear view.", "後方からT字。"), ("明顯高於引擎中心線。", "Clearly above the engine centreline.", "エンジン中心線より明確に高い位置。")],
        ),
        "gear": identify(
            ("CRJ700 前起落架雙輪，左右主腳各雙輪，總共六輪；前視可見主輪在細窄機身兩側，尾部引擎在更高的位置。", "The CRJ700 has twin nose wheels and twin wheels on each main leg, six in total. Head-on, the mains flank the slim fuselage below the rear engines.", "CRJ700は前脚2輪、左右主脚各2輪で計6輪。正面では細い胴体両側に主輪、その上方に後部エンジンが見えます。"),
            ("E170 也是六輪，不能以輪數判型；應一起看引擎在主翼上方後段或吊掛在主翼下方。", "The E170 also has six wheels. Use engine installation—high at the rear or beneath the wings—rather than wheel count.", "E170も6輪なので輪数では区別できません。後方高位置か翼下か、エンジン配置を合わせて確認します。"),
            [("前腳雙輪。", "Twin-wheel nose leg.", "前脚は2輪。"), ("左右主腳各雙輪。", "Twin wheels on each main leg.", "左右主脚各2輪。"), ("輪數與 E170 相同。", "Same wheel count as the E170.", "E170と同じ輪数。")],
        ),
    },
    "e170": {
        "overview": identify(
            ("E170 是第一代 E-Jet 家族短機身機型，全長 29.90 m、翼展 26.00 m；翼下雙發、較寬圓潤的機身與低置水平尾翼構成主要輪廓。", "The E170 is a short-bodied first-generation E-Jet, 29.90 m long with a 26.00 m span. Underwing twins, a wider rounded body and low tailplanes define its silhouette.", "E170は初代E-Jetの短胴型で全長29.90 m、翼幅26.00 m。翼下双発、太く丸い胴体、低位置水平尾翼が特徴です。"),
            ("比 CRJ700 短但翼展更大；不要把同家族較長的 E175 或 E190 照片當成 E170。", "It is shorter than the CRJ700 but wider in span. Do not mistake the longer E175 or E190 for the E170.", "CRJ700より短い一方で翼幅は広く、同系列の長胴E175・E190との混同に注意します。"),
            [("兩具引擎位於翼下。", "Two engines beneath the wings.", "翼下にエンジン2基。"), ("短而較寬的機身。", "Shorter, wider body.", "短く太めの胴体。"), ("水平尾翼低置。", "Low-mounted tailplanes.", "水平尾翼は低位置。")],
        ),
        "cockpit": identify(
            ("E170 使用 Honeywell Primus Epic 玻璃座艙，五具大型顯示器與兩側駕駛盤是主要特徵。附圖為 E175 實照，用於示範第一代 E170／175 共通基本布局。", "The E170 uses a Honeywell Primus Epic glass cockpit with five large displays and yokes at both seats. The E175 photograph illustrates the shared basic first-generation E170/175 layout.", "E170はHoneywell Primus Epic、主要大型画面5面、両席操縦輪が特徴です。写真はE175で、初代E170／175共通の基本配置を示します。"),
            ("不是 Airbus 式側桿座艙；與 CRJ700 相比，螢幕數目及中央顯示布局更有辨識價值。", "It is not an Airbus-style sidestick cockpit. Display count and centre-panel layout distinguish it from the CRJ700.", "Airbus式サイドスティックではありません。CRJ700との差は画面数と中央配置を見ます。"),
            [("五具大型主要顯示器。", "Five large main displays.", "主要大型画面5面。"), ("左右仍有駕駛盤。", "Yokes at both pilot seats.", "両席に操縦輪。"), ("附圖為家族共通配置參考。", "Photo is a shared-family layout reference.", "写真は系列共通配置の参考。")],
        ),
        "windshield": identify(
            ("E170 正面窗由中央窗柱分開，側面窗較短，配合寬圓機鼻與平順下收的鼻部輪廓；正面和側面照片可對照窗框角度。", "The E170 has a centre-divided windshield and short side panes above a broad rounded nose that tapers smoothly downward. Compare frame angles in front and side photos.", "E170は中央で分かれた前窓と短い側窓を持ち、その下に太く丸く下へ絞られる機首があります。正面・側面で窓枠角度を比較します。"),
            ("E170、E175、E190 的家族窗型相近，窗型只能先確定 E-Jet 家族，不能單靠這裡判斷機身長短。", "E170, E175 and E190 share similar family glazing. Windows can indicate an E-Jet but cannot establish its body-length variant alone.", "E170・E175・E190の窓は類似し、E-Jet系列の判定には役立ちますが胴体長型式は断定できません。"),
            [("寬圓鼻部搭配多片窗框。", "Multi-pane glazing above a broad rounded nose.", "太く丸い機首上の複数窓。"), ("側面窗較短。", "Short side panes.", "短めの側窓。"), ("需配合翼下引擎與機身長度。", "Cross-check underwing engines and body length.", "翼下エンジンと胴体長も確認。")],
        ),
        "fuselage": identify(
            ("E170 的 2+2 客艙採較寬機身，前後艙門之間的窗列較短，尾段沒有引擎短艙遮蔽；前後艙門和翼根的位置可用來觀察短機身比例。", "The E170's wider 2+2 body has a short window run between front and rear doors and no aft nacelles hiding the tail area. Door and wing-root positions help reveal the short-body proportions.", "E170は幅広い2+2胴体で前後ドア間の窓列が短く、後部ナセルもありません。ドアと翼根位置で短胴比率を見ます。"),
            ("每排同樣四座不代表外形一樣；CRJ700 更細長、前門離地更低，兩者外觀上的寬高比例不同。", "Four seats abreast does not imply the same shape. The CRJ700 is more slender with a lower front door, giving different width and height proportions.", "同じ横4席でも外形は異なり、CRJ700はより細長く前方扉が低いため幅・高さの比率が違います。"),
            [("較寬、較短的客艙段。", "Wider, shorter cabin section.", "太く短い客室部分。"), ("前後艙門位置清楚。", "Clearly separated front and rear doors.", "明確な前後ドア配置。"), ("尾部兩側沒有引擎。", "No engines beside the tail.", "尾部両側にエンジンなし。")],
        ),
        "engine": identify(
            ("E170 使用 GE CF34-8E 系列渦扇，兩具短艙由吊架懸掛在主翼下方；進氣口近圓形，側面可見短艙與機翼的明顯間隙。", "GE CF34-8E-series turbofans hang beneath the E170's wings on pylons. The inlets are nearly circular and a clear nacelle-to-wing gap is visible from the side.", "E170はGE CF34-8E系ターボファンを主翼下パイロンに搭載。吸気口はほぼ円形で、側面からナセルと翼の間隔が見えます。"),
            ("同屬 CF34 並不表示與 CRJ700 外形相同；最明顯的差異是翼下吊掛而非後機身安裝。", "Sharing the CF34 name does not mean the same appearance as a CRJ700: underwing rather than rear-fuselage installation is decisive.", "同じCF34でもCRJ700と外観は異なり、後部胴体でなく翼下搭載であることが決定的です。"),
            [("主翼下每側一具。", "One beneath each wing.", "左右翼下に各1基。"), ("可見吊架與短艙間隙。", "Visible pylon and wing clearance.", "パイロンと翼との間隔が見える。"), ("不是 E190 的 CF34-10E。", "Not the E190's CF34-10E.", "E190のCF34-10Eとは異なります。")],
        ),
        "wingtip": identify(
            ("E170 的翼尖向上彎起，與主翼平順銜接；正面照片可看出小翼的傾斜與後掠，不是完全垂直的端板。", "The E170 wingtip curves upward with a smooth transition from the wing. Front views show its cant and sweep rather than a purely vertical end plate.", "E170の翼端は滑らかにつながって上向きに曲がり、正面で傾きと後退が分かる、単なる垂直板ではない形です。"),
            ("本頁為 E170 原型翼尖；較晚 E175 的加大型翼尖不可直接套用。CRJ700 也有小翼，要搭配引擎位置確認。", "This is the original E170 tip, not the later enlarged E175 wingtip. The CRJ700 also has winglets, so check engine location too.", "本頁はE170本来の翼端で、後期E175の大型翼端とは異なります。CRJ700も小翼を持つためエンジン位置も確認します。"),
            [("向上彎曲的翼尖。", "Upturned tip.", "上向きに曲がる翼端。"), ("主翼與小翼銜接平順。", "Smooth wing-to-winglet blend.", "滑らかな主翼との接続。"), ("需區分 E175 後期翼尖。", "Distinguish later E175 tips.", "後期E175の翼端と区別。")],
        ),
        "wing": identify(
            ("E170 翼展 26.00 m，低置後掠主翼下承載引擎，後緣有襟翼及滑軌整流罩；正面照片可同時比較主翼、引擎和小翼的位置。", "The E170's 26.00 m low swept wing carries the engines and has trailing-edge flaps and track fairings. A front view shows the relationship between wing, nacelles and tips.", "E170の翼幅26.00 mの低翼後退翼はエンジンを搭載し、後縁にフラップとトラック整流部があります。正面で主翼・ナセル・小翼の位置を比較できます。"),
            ("比 CRJ700 的翼展多約 2.8 m，但機身反而較短；這種短機身配寬翼展的比例有助於辨識 E170。", "Its span is about 2.8 m greater than the CRJ700's despite a shorter body. This short-body/wide-span proportion helps identify an E170.", "CRJ700より胴体が短いのに翼幅は約2.8 m広く、この短胴・広翼の比率がE170の手掛かりです。"),
            [("低置主翼承載兩具引擎。", "Low wing carrying two engines.", "エンジン2基を搭載する低翼。"), ("翼展 26.00 m。", "26.00 m span.", "翼幅26.00 m。"), ("後緣整流罩可見。", "Visible trailing-edge fairings.", "後縁整流部が見える。")],
        ),
        "vstab": identify(
            ("E170 垂尾是高而後掠的單一翼面，根部以背鰭平順連接後機身；垂尾頂端沒有水平尾翼，與 CRJ700 的 T 尾相反。", "The E170 fin is a tall swept surface with a dorsal blend into the aft body. No tailplane crosses its tip, unlike the CRJ700 T-tail.", "E170垂尾は高い後退面で根元背びれが胴体へ滑らかにつながり、CRJ700と違い頂部に水平尾翼がありません。"),
            ("不要依航空公司尾翼圖案判型；確認垂尾頂端是否有橫向翼面，通常比塗裝更可靠。", "Do not identify the aircraft by its tail logo. Whether a horizontal surface crosses the fin tip is more reliable.", "尾翼ロゴでなく垂尾頂部を横切る水平面の有無を見る方が確実です。"),
            [("頂端保持單一垂直翼面。", "Uninterrupted fin tip.", "頂部は単一の垂直面。"), ("根部背鰭平順延伸。", "Smooth dorsal-root extension.", "滑らかな根元背びれ。"), ("不承載 T 型水平尾翼。", "Does not carry a T-tailplane.", "T字水平尾翼を支えません。")],
        ),
        "hstab": identify(
            ("E170 水平尾翼從後機身兩側低位伸出，後掠且向外收尖；從側面可看到翼根遠低於垂尾頂端。", "The E170's swept tapered tailplanes extend from low on each side of the aft fuselage. Their roots sit well below the fin tip.", "E170の後退・先細水平尾翼は後部胴体両側の低位置から伸び、根元は垂尾頂端より大幅に低くなります。"),
            ("這是與 CRJ700 最容易從遠處辨識的差異之一；同時看翼下雙發，可以排除同樣短機身的 T 尾客機。", "This is one of the clearest distant distinctions from the CRJ700. Check the underwing engines too to exclude short-bodied T-tail jets.", "遠方からCRJ700と区別しやすい特徴の一つです。翼下双発も合わせて短胴T字尾翼機を除外します。"),
            [("根部接在後機身側面。", "Roots attach to the aft body sides.", "根元は後部胴体側面。"), ("遠低於垂尾頂端。", "Well below the fin tip.", "垂尾頂部より低い。"), ("後掠、向翼尖收窄。", "Swept and tapered.", "後退・先細の形状。")],
        ),
        "gear": identify(
            ("E170 前腳雙輪、左右主腳各雙輪，共六輪；主腳位於翼根附近，照片可觀察輪距以及翼下引擎的離地間隙。", "The E170 uses twin nose wheels and twin wheels on each main leg, six total. The mains sit near the wing roots; the photo shows their track and underwing engine clearance.", "E170は前脚2輪、左右主脚各2輪の計6輪。主脚は翼根付近にあり、写真で輪距と翼下エンジンの地上間隔を確認できます。"),
            ("CRJ700 也是六輪，輪數不是兩型差別；從前方看主輪上方是否有翼下引擎，能更快完成判型。", "The CRJ700 also has six wheels. From the front, underwing engines above the main-wheel area are a better discriminator than wheel count.", "CRJ700も6輪。正面から主輪付近上方に翼下エンジンがあるかを見る方が、輪数より有効です。"),
            [("前腳與兩側主腳均雙輪。", "Twin wheels on nose and both mains.", "前脚・左右主脚とも2輪。"), ("主輪位於翼根附近。", "Mains near the wing roots.", "主輪は翼根付近。"), ("觀察翼下短艙離地空間。", "Observe underwing nacelle clearance.", "翼下ナセルの地上間隔を観察。")],
        ),
    },
})

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
    if model in ("crj700", "e170"):
        family = "CRJ700/900" if model == "crj700" else "E170/175"
        actual = "CRJ900" if model == "crj700" else "E175"
        parts["cockpit"]["images"][0]["caption"] = tr(
            f"{family} 家族共通座艙布局參考（{actual} 實照）",
            f"{family} shared cockpit-layout reference ({actual} photograph)",
            f"{family}共通操縦席配置の参考（{actual}実機写真）",
        )
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
