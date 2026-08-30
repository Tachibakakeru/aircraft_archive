$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot

function Get-CommonsImageInfo($fileTitles, $width, $includeMetadata = $false) {
  $byTitle = @{}
  foreach ($title in @($fileTitles | Sort-Object -Unique)) {
    $escaped = [uri]::EscapeDataString($title)
    $byTitle[$title] = @{ thumburl = "https://commons.wikimedia.org/wiki/Special:Redirect/file/${escaped}?width=$width" }
  }
  return $byTitle
}

$photos = [ordered]@{
  "b738/overview.jpg" = "Boeing 737-800 (TC-SNR) 01.jpg"
  "b738/cockpit.jpg" = "The Flight Deck of the Boeing 737-800. (2956276002).jpg"
  "b738/fuselage.jpg" = "Forward fuselage of Virgin Australia (VH-YFC) Boeing 737-81D at Sydney Airport.jpg"
  "b738/engine.jpg" = "CFM-56 Lauda 737.jpg"
  "b738/wingtip.jpg" = "Winglet of Boeing 737-800.jpg"
  "b738/wing.jpg" = "Boeing 737-800 American Airlines, clean and shiny wing + winglet (4898075792).jpg"
  "b738/vstab.jpg" = "LN-RCY Boeing 737-800 Tail Scheme (7510635508).jpg"
  "b738/hstab.jpg" = "Boeing 737-800 Tail from Below.jpg"
  "b738/gear.jpg" = "737-800 main gear bay (3858029769).jpg"
  "a320/overview.jpg" = "Jetstar Airbus A320 VH-XNJ Perth 2023 (01).jpg"
  "a320/cockpit.jpg" = "Airbus A320-214 Vueling EC-HHA cockpit (5508849819).jpg"
  "a320/fuselage.jpg" = "Aft door of A320.jpg"
  "a320/engine.jpg" = "Philippine Airlines A320 Engine.jpg"
  "a320/wingtip.jpg" = "F-WWIQ Airbus A320 sharklet ILA 2012 07.jpg"
  "a320/wing.jpg" = "The Sharklet on our newest Airbus A320 (8657081970).jpg"
  "a320/vstab.jpg" = "Vertical stabilizer of A-320.jpg"
  "a320/hstab.jpg" = "Airbus-Höhenruder.jpg"
  "a320/gear.jpg" = "A320neo Nose Landing Gear.jpg"
  "b773/overview.jpg" = "Boeing 777-300ER, Geneva Airport, Le Grand-Saconnex (BL7C0540).jpg"
  "b773/cockpit.jpg" = "Boeing 777-200ER cockpit.jpg"
  "b773/fuselage.jpg" = "B-KPL Boeing 777 Cathay Pacific In OneWorld Colours Nose (9320566483).jpg"
  "b773/engine.jpg" = "Engine of Jet Airways Boeing 777-300ER.jpg"
  "b773/wingtip.jpg" = "Emirates 77W wing view, July 2015.jpg"
  "b773/wing.jpg" = "Emirates 77W wing view, July 2015.jpg"
  "b773/vstab.jpg" = "View of EVA Air Boeing 777-300ER tail.jpg"
  "b773/hstab.jpg" = "Boeing 777's Tail (2573279746).jpg"
  "b773/gear.jpg" = "B777 Landinggear (51127441259).jpg"
  "a359/overview.jpg" = "Airbus A350-941 F-WWCF MSN002 ILA Berlin 2016 17.jpg"
  "a359/cockpit.jpg" = "Airbus A-350 XWB F-WWYB cockpit view.jpg"
  "a359/fuselage.jpg" = "Airbus A350-900 (40862885025).jpg"
  "a359/engine.jpg" = "Airbus A350-941 F-WWCF MSN002 ILA Berlin 2016 23.jpg"
  "a359/wingtip.jpg" = "Airbus A-350 XWB F-WWYB winglet.jpg"
  "a359/wing.jpg" = "Airbus A350-941 F-WWCF MSN002 blended winglet ILA Berlin 2016 05.jpg"
  "a359/vstab.jpg" = "Airbus A350-941 F-WWCF MSN002 ILA Berlin 2016 18.jpg"
  "a359/hstab.jpg" = "Airbus A350-941 F-WWCF MSN002 ILA Berlin 2016 20.jpg"
  "a359/gear.jpg" = "Airbus A350-941 F-WWCF MSN002 main landing gear ILA Berlin 2016 06.jpg"
  "b789/overview.jpg" = "Qantas Boeing 787 VH-ZNM Perth 2026 (01).jpg"
  "b789/cockpit.jpg" = "Boeing 787-8 N787BA cockpit.jpg"
  "b789/fuselage.jpg" = "VN-A819 Boeing 787-9 Bamboo Airways LHR 23.3.22.jpg"
  "b789/engine.jpg" = "Boeing 787 engine chevrons.jpg"
  "b789/wingtip.jpg" = "Wingtip device of Boeing 787 (1).jpg"
  "b789/wing.jpg" = "Boeing 787 Dreamliner wing view.jpg"
  "b789/vstab.jpg" = "Vertical tail of B787 (1).jpg"
  "b789/hstab.jpg" = "Horizontal stabilizer of B787 (1).jpg"
  "b789/gear.jpg" = "Air India Boeing 787 Dreamliner N1008S PAS 2013 06 main landing gear.jpg"
  "a333/overview.jpg" = "AirAsia X Airbus A330 9M-XXQ Perth 2024 (02).jpg"
  "a333/cockpit.jpg" = "Airbus A330-302 Iberia EC-LYF cockpit (10983484845).jpg"
  "a333/fuselage.jpg" = "Airbus A330-300 (Air Canada) 333.jpg"
  "a333/engine.jpg" = "Rolls-Royce Trent 700 viewed from boarding gangway.jpg"
  "a333/wingtip.jpg" = "Wingtip device on a China Eastern Airlines Airbus A330-343.jpg"
  "a333/wing.jpg" = "02-JUL-2022 - QR184 VIE-DOH (A330-300 - A7-AEO) (04).jpg"
  "a333/vstab.jpg" = "Airbus A330 tail Leitwerk.jpg"
  "a333/hstab.jpg" = "China Eastern Airbus A330-300 B-6095 lining up at Taipei Songshan April 2026 3.jpg"
  "a333/gear.jpg" = "Landing gear on a Malaysian Airlines Airbus A330-300.jpg"
  "b748/overview.jpg" = "Lufthansa Boeing 747-8i at San Francisco September 2023.jpg"
  "b748/cockpit.jpg" = "Boeing 747-8I flight deck Beltyukov.jpg"
  "b748/fuselage.jpg" = "Boeing 747-8 Baden-Württemberg.jpg"
  "b748/engine.jpg" = "General Electric GEnx on 747-8I prototype.jpg"
  "b748/wingtip.jpg" = "2015 10 01 LH Boeing 747 8 D ABYT@EDDF left wingtip.jpg"
  "b748/wing.jpg" = "2015 10 01 LH Boeing 747 8 D ABYT@EDDF left wing.jpg"
  "b748/vstab.jpg" = "Boeing 747-8 of Korean Air at Los Angeles International Airport.jpg"
  "b748/hstab.jpg" = "Boeing 747-8F N5017Q inflight.jpg"
  "b748/gear.jpg" = "Boeing 747-8I landing gear.jpg"
  "a380/overview.jpg" = "Emirates Airbus A380 A6-EOG Perth 2024 (01).jpg"
  "a380/cockpit.jpg" = "Airbus A380 cockpit.jpg"
  "a380/fuselage.jpg" = "Airbus A380 front side.jpg"
  "a380/engine.jpg" = "A380 Engines.jpg"
  "a380/wingtip.jpg" = "British Airways Airbus A380-841 F-WWSK PAS 2013 10 Wingtip device.jpg"
  "a380/wing.jpg" = "A380 Wing.jpg"
  "a380/vstab.jpg" = "A380 Tail.jpg"
  "a380/hstab.jpg" = "A380-tail.JPG"
  "a380/gear.jpg" = "British Airways Airbus A380-841 F-WWSK PAS 2013 08 main landing gear.jpg"
  "b752/overview.jpg" = "Icelandair Boeing 757 TF-ISR Milan Malpensa 2024 (01).jpg"
  "b752/cockpit.jpg" = "Boeing 757-200 flight deck.jpg"
  "b752/fuselage.jpg" = "American Airlines B757-200 forward fuselage view in hangar.jpg"
  "b752/engine.jpg" = "British Airways B757 Heathrow Airport jet engine intake.jpg"
  "b752/wingtip.jpg" = "Boeing 757 winglet (4269906229).jpg"
  "b752/wing.jpg" = "Onboard the Boeing 757 (3390330324).jpg"
  "b752/vstab.jpg" = "Boeing 757-200 - Icelandair (tail).jpg"
  "b752/hstab.jpg" = "Icelandair tail at Oslo.jpg"
  "b752/gear.jpg" = "Ba b757-200 g-bpei closeup arp.jpg"
  "a321/overview.jpg" = "Finnair Airbus A321 OH-LZF Oslo Gardermoen 2024 (01).jpg"
  "a321/cockpit.jpg" = "Airbus A321 cockpit - G-EUXG British Airways.jpg"
  "a321/fuselage.jpg" = "Airbus A321-211, N827Q - open doors.jpg"
  "a321/engine.jpg" = "Airbus A321-231, Middle East Airlines (MEA) JP6762964.jpg"
  "a321/wingtip.jpg" = "Wingtip device of Airbus A-321-200.JPG"
  "a321/wing.jpg" = "Airbus A321 wingtip fence.jpg"
  "a321/vstab.jpg" = "TC-JRN Airbus A321 Turkish Airlines Tail (8633650011).jpg"
  "a321/hstab.jpg" = "TransAsia Airways Airbus A321-231 B-22612 Departing from Taipei Songshan Airport 20151003f.jpg"
  "a321/gear.jpg" = "Port side main landing gear of Finnair Airbus A321 OH-LZA.jpg"
  "b763/overview.jpg" = "Hawaiian Airlines (N592HA) Boeing 767-300ER at Sydney Airport.jpg"
  "b763/cockpit.jpg" = "AeroMexico Boeing 767-300ER cockpit.jpg"
  "b763/fuselage.jpg" = "Boeing 767-300ER United Airlines N656UA.jpg"
  "b763/engine.jpg" = "Air Canada Boeing 767-300ER with CF6-80 engines.jpg"
  "b763/wingtip.jpg" = "ALL NIPPON BOEING 767-300 WINGLETS AT NARITA AIRPORT TOKYO JAPAN JUNE 2012 (7456802526).jpg"
  "b763/wing.jpg" = "Boeing 767-323ER spoilers on descent to POS, AAL 1167, 11-29-12.jpg"
  "b763/vstab.jpg" = "ET-ALO at ADD.jpg"
  "b763/hstab.jpg" = "Ba b767-300 g-bnwa planform arp.jpg"
  "b763/gear.jpg" = "American Airlines B767-300ER main landing gear.jpg"
  "a332/overview.jpg" = "Airbus A330-200 Hainan AL (CHH) F-WWYJ - MSN 1168 - Will be B-6520 (5413679264).jpg"
  "a332/cockpit.jpg" = "13-08-06-Cockpit-d-alpa-a330-200.jpg"
  "a332/fuselage.jpg" = "KLM Airbus A330-200 PH-AOI nose section (3186787311).jpg"
  "a332/engine.jpg" = "Pratt & Whitney PW4000 turbofan with open cowling.jpg"
  "a332/wingtip.jpg" = "翼尖小翼02.JPG"
  "a332/wing.jpg" = "Window and wing inflight.jpg"
  "a332/vstab.jpg" = "KLM Airbus A330-200 PH-AOC tail (6924834528).jpg"
  "a332/hstab.jpg" = "Cyprus airways a330-200 5b-dbs arp.jpg"
  "a332/gear.jpg" = "VH-SSA 'Outback' Airbus A330-223 Strategic Airlines (7107083943).jpg"
  "b744/overview.jpg" = "Air New Zealand 747-400 sideview.jpg"
  "b744/cockpit.jpg" = "Boeing 747-400 cockpit.jpg"
  "b744/fuselage.jpg" = "KLM Boeing 747-400 PH-BFI nose section (10205055606).jpg"
  "b744/engine.jpg" = "Rolls Royce Trent jet engine, Qantas 747-400 (5381505855).jpg"
  "b744/wingtip.jpg" = "Winglet and nav light arp.jpg"
  "b744/wing.jpg" = "Elal 747-400 wing.jpg"
  "b744/vstab.jpg" = "KLM Boeing 747-400 PH-BFT tail (6972557066).jpg"
  "b744/hstab.jpg" = "Ba b747-400 g-bnle arp.jpg"
  "b744/gear.jpg" = "Boeing 747 main landing gear.jpg"
  "a346/overview.jpg" = "Etihad Airways Airbus A340-600 SYD Gilbert-1.jpg"
  "a346/cockpit.jpg" = "A340-642 flight deck.jpg"
  "a346/fuselage.jpg" = "G-VSHY Airbus A340-642 (cn 383) Virgin Atlantic Airways. (6100631197).jpg"
  "a346/engine.jpg" = "Iberia A340-600 Rolls-Royce Trent 500 engines.jpg"
  "a346/wingtip.jpg" = "Airbus A340-600 Wing.JPG"
  "a346/wing.jpg" = "A340-600 clean-wing bottom plan-view.jpg"
  "a346/vstab.jpg" = "Airbus A340-600 Tail assembly (8459395384).jpg"
  "a346/hstab.jpg" = "G-VBUG Airbus A346 Virgin Atlantic Tail (13891670573).jpg"
  "a346/gear.jpg" = "Thai airways a340-600 hs-tna takeoff arp.jpg"
  "b717/overview.jpg" = "Boeing 717, N483HA, Hawaiian Airlines.jpg"
  "b717/cockpit.jpg" = "N938AT Boeing 717 flight deck.jpg"
  "b717/fuselage.jpg" = "N937AT Boeing 717 Air Tran Nose (7438725424).jpg"
  "b717/engine.jpg" = "Boeing 717 MD95, Hawaiian, left port tail and engine, at gate (4389633539) (3).jpg"
  "b717/wingtip.jpg" = "11-APR-2022 - HA284 LIH-HNL (B717-200 - N488HA) (02).jpg"
  "b717/wing.jpg" = "Boeing 717 (1).jpg"
  "b717/vstab.jpg" = "EC-MGT 717 Volotea tailfin VGO.jpg"
  "b717/hstab.jpg" = "Air Tran Boeing 717 aka MD-95 - note tail surrface anhedral - frame 1049 (4906658072) (2).jpg"
  "b717/gear.jpg" = "QantasLink B717-231 (VH-NXO) departing Perth Airport.jpg"
  "cs100/overview.jpg" = "ITA Airways A220-100 EI-HLE 2024-06-15 Munich Airport p02.jpg"
  "cs100/cockpit.jpg" = "Bombardier CS100 (23463394635).jpg"
  "cs100/fuselage.jpg" = "Swiss, HB-JBC, Bombardier CS100 (31383514146).jpg"
  "cs100/engine.jpg" = "Bombardier CS100 at Brussels Airport (25272589779).jpg"
  "cs100/wingtip.jpg" = "Cabin window view of Swissair aircraft wings (24482756908).jpg"
  "cs100/wing.jpg" = "ITA Airways, I-ADVA, Airbus A220-100 (54007495525) at Milan Linate.jpg"
  "cs100/vstab.jpg" = "Swiss, HB-JBI, Airbus A220-100 (49580114558).jpg"
  "cs100/hstab.jpg" = "Swiss International Airlines HB-JBH BOMBARDIER CS100 A220-100 (Ank Kumar, Infosys Limited) 05.jpg"
  "cs100/gear.jpg" = "Bombardier CS100 (23437223616).jpg"
  "b737/overview.jpg" = "Southwest Boeing 737-700 N947WN BWI MD1.jpg"
  "b737/cockpit.jpg" = "Cockpit-737-700-by-RalfR.jpg"
  "b737/wingtip.jpg" = "Boeing 737-700 Southwest winglet, and headquarters, Love Field (2717214038) (3).jpg"
  "b737/wing.jpg" = "Southwest Starboard Wing (33198022825).jpg"
  "b737/vstab.jpg" = "Boeing 737-700 PH-BGP of KLM Tail (12291134464).jpg"
  "b737/hstab.jpg" = "Boeing 737-700, Southwest, winglets, from below (6190651480).jpg"
  "a319/overview.jpg" = "Ba a319-100 g-euog arp.jpg"
  "a319/cockpit.jpg" = "Airbus-319-cockpit.jpg"
  "a319/wingtip.jpg" = "Airbus A319 wintip.jpg"
  "a319/wing.jpg" = "A319 Port Wing (40736437962).jpg"
  "b736/overview.jpg" = "Boeing 737-600 (6778274137).jpg"
  "b736/cockpit.jpg" = "Cockpit-737-700-by-RalfR.jpg"
  "a318/cockpit.jpg" = "Airbus A318 Cockpit (8605111142).jpg"
  "a318/gear.jpg" = "Airbus A318 Landing Gear (8604009277).jpg"
  "b772/cockpit.jpg" = "Boeing 777-200ER cockpit.jpg"
  "a343/cockpit.jpg" = "A340-300 cockpit (8459431964).jpg"
  "beluga/cockpit.jpg" = "Airbus A300 panel.jpg"
  "dreamlifter/cockpit.jpg" = "Boeing 747-400 cockpit.jpg"
  "crj900/cockpit.jpg" = "Bombardier-crj-900-cockpit-by-RalfR.jpg"
  "crj900/overview.jpg" = "Air Canada Express Bombardier CRJ-900 C-FJFZ BWI MD1.jpg"
  "e190/cockpit.jpg" = "Cabine do Embraer 190.jpg"
  "e190/engine.jpg" = "Embraer E190 engine in-flight.jpg"
  "e190/wingtip.jpg" = "Embraer E190 wingtip.jpg"
  "e190/wing.jpg" = "Embraer E190 wing.jpg"
}

$byTitle = Get-CommonsImageInfo $photos.Values 960 $true

foreach ($entry in $photos.GetEnumerator()) {
  $dest = Join-Path $root ("assets/reference/" + $entry.Key)
  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dest) | Out-Null
  $info = $byTitle[$entry.Value]
  if (-not $info) { throw "Wikimedia Commons file not found: $($entry.Value)" }
  if (-not (Test-Path $dest)) {
    for ($attempt = 1; $attempt -le 4; $attempt++) {
      try {
        Invoke-WebRequest -Uri $info.thumburl -OutFile $dest -UserAgent "SKY-ARCHIVE/1.0 (reference photo downloader)"
        break
      } catch {
        if ($attempt -eq 4) { throw }
        Start-Sleep -Seconds (10 * $attempt)
      }
    }
    Start-Sleep -Seconds 6
  }
  if ((Get-Item $dest).Length -lt 10000) { throw "Downloaded file is unexpectedly small: $dest" }
}

$windowPhotos = @(
  @{ Dest="b738/window-front.jpg"; Title="Front view of boeing 737-800 of Ryanair at Orio al Serio International Airport, 2006.jpg"; Crop=@(.27,.23,.46) },
  @{ Dest="b738/window-side.jpg"; Title="Cockpit window of Qantas Boeing 737 (VH-VYE) taxiing prior to takeoff at SYD.jpg"; Crop=@(.26,.18,.68) },
  @{ Dest="a320/window-front.jpg"; Title="Finnair Airbus A320 OH-LXB Budapest 2006 (03).jpg"; Crop=@(.42,.38,.38) },
  @{ Dest="a320/window-side.jpg"; Title='Airbus A320-200 Airbus Industries (AIB) "House colors" F-WWBA - MSN 001 (10276181983).jpg'; Crop=@(.02,.25,.42) },
  @{ Dest="b773/window-front.jpg"; Title="Cockpit windows of an AA B773.jpg"; Crop=@(.03,.12,.92) },
  @{ Dest="b773/window-side.jpg"; Title="Boeing 777 nose from starboard side (2719420855) (2).jpg"; Crop=@(.50,.05,.42) },
  @{ Dest="a359/window-front.jpg"; Title="Airbus A350-941 F-WWCF MSN002 ILA Berlin 2016 17.jpg"; Crop=@(.50,.17,.30) },
  @{ Dest="a359/window-side.jpg"; Title="Airbus A350 cockpit windows (14274972354).jpg"; Crop=@(.03,.12,.92) }
  @{ Dest="b789/window-front.jpg"; Title="Front view of ANA Boeing 787-8 JA834A at Taipei Songshan Airport 20150101.jpg"; Crop=@(.39,.43,.22) }
  @{ Dest="b789/window-side.jpg"; Title="Cockpit windows of a Boeing 787 (3).jpg"; Crop=@(.08,.15,.84) }
  @{ Dest="a333/window-front.jpg"; Title="Airbus A330 Front View.jpg"; Crop=@(.28,.10,.44) }
  @{ Dest="a333/window-side.jpg"; Title="Airbus A330-343X, China Eastern Airlines JP7548435.jpg"; Crop=@(.48,.04,.46) }
  @{ Dest="b748/window-front.jpg"; Title="Lufthansa Boeing 747-8 20180513 3722.jpg"; Crop=@(.36,.18,.30) }
  @{ Dest="b748/window-side.jpg"; Title="Boeing 747 cockpit window from outside.jpg"; Crop=@(.02,.08,.94) }
  @{ Dest="a380/window-front.jpg"; Title="A380-front.JPG"; Crop=@(.29,.03,.42) }
  @{ Dest="a380/window-side.jpg"; Title="Airbus A380 front side.jpg"; Crop=@(.02,.08,.50) }
  @{ Dest="b752/window-front.jpg"; Title="Face to Face with Delta (N616DL) (8331933080).jpg"; Crop=@(.30,.15,.40) }
  @{ Dest="b752/window-side.jpg"; Title="The front end of a 757 (2710024227).jpg"; Crop=@(.03,.08,.62) }
  @{ Dest="a321/window-front.jpg"; Title="Delta A321 at Airbus Mobile.jpg"; Crop=@(.02,.10,.78) }
  @{ Dest="a321/window-side.jpg"; Title="Finnair Airbus A321 OH-LZF Oslo Gardermoen 2024 (02).jpg"; Crop=@(.47,.07,.46) }
  @{ Dest="b763/window-front.jpg"; Title="Boeing 767-300ER (Japan Airlines) 02.jpg"; Crop=@(.35,.42,.30) }
  @{ Dest="b763/window-side.jpg"; Title="Hawaiian Airlines (N592HA) Boeing 767-300ER at Sydney Airport.jpg"; Crop=@(.01,.29,.32) }
  @{ Dest="a332/window-front.jpg"; Title="Face to face (F-OONE) (14771492742).jpg"; Crop=@(.28,.12,.44) }
  @{ Dest="a332/window-side.jpg"; Title="KLM Airbus A330-200 PH-AOI nose section (3186787311).jpg"; Crop=@(.58,.17,.40) }
  @{ Dest="b744/window-front.jpg"; Title="Boeing 747 Jumbo front cockpit windows.jpg"; Crop=@(.00,.20,1.00) }
  @{ Dest="b744/window-side.jpg"; Title="KLM Boeing 747-400 PH-BFI nose section (10205055606).jpg"; Crop=@(.54,.08,.44) }
  @{ Dest="a346/window-front.jpg"; Title="A340-600 (13024845015).jpg"; Crop=@(.34,.34,.32) }
  @{ Dest="a346/window-side.jpg"; Title="G-VSHY Airbus A340-642 (cn 383) Virgin Atlantic Airways. (6100631197).jpg"; Crop=@(.02,.05,.42) }
  @{ Dest="b717/window-front.jpg"; Title="Boeing 717 MD95, Hawaiian, Honolulu, nose-on (4389641139) (3).jpg"; Crop=@(.05,.31,.90) }
  @{ Dest="b717/window-side.jpg"; Title="N937AT Boeing 717 Air Tran Nose (7438725424).jpg"; Crop=@(.55,.22,.42) }
  @{ Dest="cs100/window-front.jpg"; Title="Bombardier CS100 (23463413085).jpg"; Crop=@(.25,.24,.50) }
  @{ Dest="cs100/window-side.jpg"; Title="Swiss, HB-JBC, Bombardier CS100 (31383514146).jpg"; Crop=@(.00,.30,.38) }
  @{ Dest="b737/window-front.jpg"; Title="B-5265 Boeing 737-79P China Eastern Airlines Lining Up for Take Off - Head On (8613160786).jpg"; Crop=@(.34,.37,.32) }
  @{ Dest="b737/window-side.jpg"; Title="KLM Boeing 737-700 PH-BGF cockpit closeup (3517238451).jpg"; Crop=@(.48,.12,.48) }
  @{ Dest="b737/fuselage.jpg"; Title="Southwest Boeing 737-700 N947WN BWI MD1.jpg"; Crop=@(.18,.28,.65) }
  @{ Dest="b737/engine.jpg"; Title="Virgin Blue Boeing 737-700 SYD Spijkers.jpg"; Crop=@(.25,.38,.40) }
  @{ Dest="b737/gear.jpg"; Title="VH-VBY 'Virginia Blue' Boeing 737-7FE Virgin Blue (9046044503).jpg"; Crop=@(.28,.56,.43) }
  @{ Dest="a319/window-front.jpg"; Title="G-EZGM easyJet Airbus A319-111 - cn 4778 head-on taxiing.JPG"; Crop=@(.36,.48,.28) }
  @{ Dest="a319/window-side.jpg"; Title="Ba a319-100 g-euog arp.jpg"; Crop=@(.02,.30,.35) }
  @{ Dest="a319/fuselage.jpg"; Title="Hamburg Airport easyJet Airbus A319-111 G-EZAO (DSC08652).jpg"; Crop=@(.08,.27,.84) }
  @{ Dest="a319/engine.jpg"; Title="Hamburg Airport easyJet Airbus A319-111 G-EZAO (DSC08652).jpg"; Crop=@(.27,.42,.35) }
  @{ Dest="a319/vstab.jpg"; Title="Germanwings Airbus A319-112 D-AKNP STR 2016 01.jpg"; Crop=@(.65,.18,.32) }
  @{ Dest="a319/hstab.jpg"; Title="Adria Airways Airbus A319 (S5-AAR) @CDG, 2015-06-25.jpg"; Crop=@(.63,.22,.34) }
  @{ Dest="a319/gear.jpg"; Title="QantasLink Airbus A319 VH-8NP Perth 2025 (02).jpg"; Crop=@(.30,.52,.45) }
  @{ Dest="b736/window-front.jpg"; Title="SAS Boeing 737-600 parked at Kiruna Airport (DSCF0852).jpg"; Crop=@(.38,.35,.24) }
  @{ Dest="b736/window-side.jpg"; Title="Boeing 737-600 (6778274137).jpg"; Crop=@(.03,.42,.27) }
  @{ Dest="b736/fuselage.jpg"; Title="Boeing 737-600 (6778274137).jpg"; Crop=@(.09,.39,.73) }
  @{ Dest="b736/engine.jpg"; Title="Boeing 737-600 (6778274137).jpg"; Crop=@(.33,.53,.27) }
  @{ Dest="b736/wingtip.jpg"; Title="SAS Boeing 737-600 parked at Kiruna Airport (DSCF0852).jpg"; Crop=@(.10,.36,.28) }
  @{ Dest="b736/wing.jpg"; Title="SAS Boeing 737-600 parked at Kiruna Airport (DSCF0852).jpg"; Crop=@(.13,.33,.38) }
  @{ Dest="b736/vstab.jpg"; Title="Boeing 737-600 (6778274137).jpg"; Crop=@(.58,.18,.27) }
  @{ Dest="b736/hstab.jpg"; Title="Boeing 737-600 (6778274137).jpg"; Crop=@(.64,.35,.31) }
  @{ Dest="b736/gear.jpg"; Title="Boeing 737-600 (6778274137).jpg"; Crop=@(.33,.57,.34) }
  @{ Dest="a318/overview.jpg"; Title="Airbus A318-111 (F-GUGJ) 01.jpg"; Crop=@(.17,.33,.68) }
  @{ Dest="a318/window-front.jpg"; Title="Airbus A318 aterrizando pista 20L en SDU (8781193831).jpg"; Crop=@(.40,.39,.20) }
  @{ Dest="a318/window-side.jpg"; Title="Airbus A318-111 (F-GUGJ) 01.jpg"; Crop=@(.65,.45,.20) }
  @{ Dest="a318/fuselage.jpg"; Title="Airbus A318-122 (8360157259).jpg"; Crop=@(.05,.29,.84) }
  @{ Dest="a318/engine.jpg"; Title="Airbus A318-122 (8360157259).jpg"; Crop=@(.23,.45,.31) }
  @{ Dest="a318/vstab.jpg"; Title="Airbus A318-122 (8360157259).jpg"; Crop=@(.68,.20,.28) }
  @{ Dest="a318/hstab.jpg"; Title="Airbus A318-122 (8360157259).jpg"; Crop=@(.74,.43,.24) }
  @{ Dest="a318/wingtip.jpg"; Title="Airbus A318-122 (8360157259).jpg"; Crop=@(.47,.23,.31) }
  @{ Dest="a318/wing.jpg"; Title="Airbus A318-122 (8360157259).jpg"; Crop=@(.35,.25,.43) }
  @{ Dest="b772/overview.jpg"; Title="United Boeing 777-200 N77019 MD1.jpg"; Crop=@(.08,.27,.84) }
  @{ Dest="b772/window-front.jpg"; Title="Boeing 777-200 (Japan Airlines) JA704J (3220615977).jpg"; Crop=@(.34,.24,.32) }
  @{ Dest="b772/window-side.jpg"; Title="United Boeing 777-200 N77019 MD1.jpg"; Crop=@(.70,.37,.24) }
  @{ Dest="b772/fuselage.jpg"; Title="United Boeing 777-200 N77019 MD1.jpg"; Crop=@(.12,.34,.78) }
  @{ Dest="b772/engine.jpg"; Title="United Boeing 777-200 N77019 MD1.jpg"; Crop=@(.48,.47,.27) }
  @{ Dest="b772/wingtip.jpg"; Title="United Airlines - N772UA - Boeing 777-200 - San Francisco International Airport-0406.jpg"; Crop=@(.56,.54,.22) }
  @{ Dest="b772/wing.jpg"; Title="United Airlines - N772UA - Boeing 777-200 - San Francisco International Airport-0406.jpg"; Crop=@(.32,.27,.52) }
  @{ Dest="b772/vstab.jpg"; Title="United Boeing 777-200 N77019 MD1.jpg"; Crop=@(.06,.25,.24) }
  @{ Dest="b772/hstab.jpg"; Title="United Boeing 777-200 N77019 MD1.jpg"; Crop=@(.10,.37,.30) }
  @{ Dest="b772/gear.jpg"; Title="Boeing 777-200 center, aft, fuselage, wing root fairing, main gear and doors, etc. (2719420955) (3).jpg"; Crop=@(.02,.44,.50) }
  @{ Dest="a343/overview.jpg"; Title="South African Airways Airbus A340-313 ZS-SXE MUC 2015 06.jpg"; Crop=@(.05,.30,.90) }
  @{ Dest="a343/window-front.jpg"; Title="South African Airways Airbus A340-313 ZS-SXE MUC 2015 02.jpg"; Crop=@(.20,.38,.22) }
  @{ Dest="a343/window-side.jpg"; Title="Airbus A340-313X, Virgin Atlantic Airways JP359341.jpg"; Crop=@(.00,.18,.48) }
  @{ Dest="a343/fuselage.jpg"; Title="South African Airways Airbus A340-313 ZS-SXE MUC 2015 06.jpg"; Crop=@(.08,.34,.82) }
  @{ Dest="a343/engine.jpg"; Title="South African Airways Airbus A340-313 ZS-SXE MUC 2015 06.jpg"; Crop=@(.36,.46,.38) }
  @{ Dest="a343/wingtip.jpg"; Title="BLADE, ILA 2018, Schönefeld (1X7A5551).jpg"; Crop=@(.31,.15,.48) }
  @{ Dest="a343/wing.jpg"; Title="BLADE, ILA 2018, Schönefeld (1X7A5551).jpg"; Crop=@(.05,.15,.80) }
  @{ Dest="a343/vstab.jpg"; Title="South African Airways Airbus A340-313 ZS-SXE MUC 2015 06.jpg"; Crop=@(.05,.25,.25) }
  @{ Dest="a343/hstab.jpg"; Title="South African Airways Airbus A340-313 ZS-SXE MUC 2015 06.jpg"; Crop=@(.08,.38,.30) }
  @{ Dest="a343/gear.jpg"; Title="South African Airways Airbus A340-313 ZS-SXE MUC 2015 02.jpg"; Crop=@(.35,.51,.35) }
  @{ Dest="beluga/overview.jpg"; Title="Airbus Beluga Airbus A300B4-608ST F-GSTA (28858044414).jpg"; Crop=@(.04,.27,.92) }
  @{ Dest="beluga/window-front.jpg"; Title="Airbus A300-600ST Beluga F-GSTB 44675.jpg"; Crop=@(.35,.61,.30); Force=$true }
  @{ Dest="beluga/window-side.jpg"; Title="Airbus A300-600ST Beluga F-GSTA.jpg"; Crop=@(.18,.43,.20); Force=$true }
  @{ Dest="beluga/fuselage.jpg"; Title="Airbus Beluga A300-600ST open.jpeg"; Crop=@(.02,.18,.96) }
  @{ Dest="beluga/engine.jpg"; Title="Airbus A300-600ST Beluga F-GSTA.jpg"; Crop=@(.31,.49,.34) }
  @{ Dest="beluga/wingtip.jpg"; Title="Airbus A300-600ST Beluga 1 (1).jpg"; Crop=@(.00,.29,.38) }
  @{ Dest="beluga/wing.jpg"; Title="Airbus A300-600ST Beluga 1 (1).jpg"; Crop=@(.05,.29,.66) }
  @{ Dest="beluga/vstab.jpg"; Title="Airbus A300-600ST Beluga 1 (1).jpg"; Crop=@(.58,.13,.38) }
  @{ Dest="beluga/hstab.jpg"; Title="Airbus A300-600ST Beluga 1 (1).jpg"; Crop=@(.51,.31,.46) }
  @{ Dest="beluga/gear.jpg"; Title="Airbus A300-600ST Beluga F-GSTB 44675.jpg"; Crop=@(.27,.51,.46) }
  @{ Dest="dreamlifter/overview.jpg"; Title="Boeing Dreamlifter Landing.jpg"; Crop=@(.08,.35,.84) }
  @{ Dest="dreamlifter/window-front.jpg"; Title="Boeing Dreamlifter Landing.jpg"; Crop=@(.70,.52,.22); Force=$true }
  @{ Dest="dreamlifter/window-side.jpg"; Title="Boeing 747-400LCF Dreamlifter.jpg"; Crop=@(.67,.29,.27) }
  @{ Dest="dreamlifter/fuselage.jpg"; Title="747 400LCF DREAM LIFTER.jpg"; Crop=@(.10,.17,.80); Force=$true }
  @{ Dest="dreamlifter/engine.jpg"; Title="Boeing Dreamlifter Landing.jpg"; Crop=@(.39,.49,.34) }
  @{ Dest="dreamlifter/wingtip.jpg"; Title="Boeing 747-400LCF Dreamlifter.jpg"; Crop=@(.00,.48,.35); Force=$true }
  @{ Dest="dreamlifter/wing.jpg"; Title="Boeing Dreamlifter Landing.jpg"; Crop=@(.16,.36,.55) }
  @{ Dest="dreamlifter/vstab.jpg"; Title="Boeing 747-409(LCF) Dreamlifter, N249BA - PAE (21348697683).jpg"; Crop=@(.40,.02,.20); Force=$true }
  @{ Dest="dreamlifter/hstab.jpg"; Title="Boeing 747-409(LCF) Dreamlifter, N249BA - PAE (21348697683).jpg"; Crop=@(.20,.35,.60); Force=$true }
  @{ Dest="dreamlifter/gear.jpg"; Title="Boeing Dreamlifter Landing.jpg"; Crop=@(.39,.56,.40) }
  @{ Dest="crj900/window-front.jpg"; Title="THE CRJ-900 head on (2436749543).jpg"; Crop=@(.35,.42,.30) }
  @{ Dest="crj900/window-side.jpg"; Title="Air Canada Express Bombardier CRJ-900 C-FJFZ BWI MD1.jpg"; Crop=@(.02,.25,.27) }
  @{ Dest="crj900/fuselage.jpg"; Title="Air Canada Express Bombardier CRJ-900 C-FJFZ BWI MD1.jpg"; Crop=@(.06,.03,.76) }
  @{ Dest="crj900/engine.jpg"; Title="Air Canada Express Bombardier CRJ-900 C-FJFZ BWI MD1.jpg"; Crop=@(.63,.38,.25) }
  @{ Dest="crj900/wingtip.jpg"; Title="Air Canada Express Bombardier CRJ-900 C-FJFZ BWI MD1.jpg"; Crop=@(.38,.12,.34) }
  @{ Dest="crj900/wing.jpg"; Title="Lufthansa Regional Bombardier CRJ-900LR D-ACKK MUC 2015 01.jpg"; Crop=@(.37,.30,.39) }
  @{ Dest="crj900/vstab.jpg"; Title="Air Canada Express Bombardier CRJ-900 C-FJFZ BWI MD1.jpg"; Crop=@(.72,.20,.25) }
  @{ Dest="crj900/hstab.jpg"; Title="On nice looking tail (2813033694).jpg"; Crop=@(.08,.05,.84) }
  @{ Dest="crj900/gear.jpg"; Title="Lufthansa Regional Bombardier CRJ-900LR D-ACKK MUC 2015 01.jpg"; Crop=@(.22,.47,.44) }
  @{ Dest="e190/overview.jpg"; Title="Finnair Embraer 190 OH-LKP at HEL 05JUN2015.JPG"; Crop=@(.08,.19,.84) }
  @{ Dest="e190/window-front.jpg"; Title="PH-EZX KLM Cityhopper Embraer ERJ-190STD (ERJ-190-100) - cn 19000545 taxiing front view 13july2013 pic1.JPG"; Crop=@(.30,.40,.40) }
  @{ Dest="e190/window-side.jpg"; Title="Finnair Embraer 190 OH-LKP at HEL 05JUN2015.JPG"; Crop=@(.03,.39,.30) }
  @{ Dest="e190/fuselage.jpg"; Title="Finnair Embraer 190 OH-LKP at HEL 05JUN2015.JPG"; Crop=@(.08,.25,.80) }
  @{ Dest="e190/vstab.jpg"; Title="LV-CDY Embraer 190 Austral Tail (8164021706).jpg"; Crop=@(.05,.05,.90) }
  @{ Dest="e190/hstab.jpg"; Title="LV-CDY Embraer 190 Austral Tail (8164021706).jpg"; Crop=@(.02,.30,.96) }
  @{ Dest="e190/gear.jpg"; Title="PH-EZX KLM Cityhopper Embraer ERJ-190STD (ERJ-190-100) - cn 19000545 taxiing front view 13july2013 pic1.JPG"; Crop=@(.20,.54,.60) }
)

$windowByTitle = Get-CommonsImageInfo ($windowPhotos | ForEach-Object Title) 1600

Add-Type -AssemblyName System.Drawing
foreach ($photo in $windowPhotos) {
  $dest = Join-Path $root ("assets/reference/" + $photo.Dest)
  if ((Test-Path $dest) -and -not $photo.Force) { continue }
  $info = $windowByTitle[$photo.Title]
  if (-not $info) { throw "Wikimedia Commons file not found: $($photo.Title)" }
  $raw = [System.IO.Path]::GetTempFileName()
  try {
    for ($attempt = 1; $attempt -le 4; $attempt++) {
      try { Invoke-WebRequest -Uri $info.thumburl -OutFile $raw -UserAgent "SKY-ARCHIVE/1.0 (reference photo downloader)"; break }
      catch { if ($attempt -eq 4) { throw }; Start-Sleep -Seconds (10 * $attempt) }
    }
    $image = [System.Drawing.Image]::FromFile($raw)
    $width = [int]($image.Width * $photo.Crop[2])
    $height = [int]($width * 9 / 16)
    $x = [int]($image.Width * $photo.Crop[0])
    $y = [int]($image.Height * $photo.Crop[1])
    $bitmap = [System.Drawing.Bitmap]::new(960, 540)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.DrawImage($image, [System.Drawing.Rectangle]::new(0, 0, 960, 540), [System.Drawing.Rectangle]::new($x, $y, $width, $height), [System.Drawing.GraphicsUnit]::Pixel)
    $graphics.Dispose(); $image.Dispose()
    $bitmap.Save($dest, [System.Drawing.Imaging.ImageFormat]::Jpeg); $bitmap.Dispose()
  } finally { Remove-Item -LiteralPath $raw -Force -ErrorAction SilentlyContinue }
  Start-Sleep -Seconds 6
}

Write-Host "Downloaded and checked $($photos.Count + $windowPhotos.Count) reference photos."
