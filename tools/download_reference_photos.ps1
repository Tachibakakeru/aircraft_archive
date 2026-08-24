$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
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
}

$titles = ($photos.Values | Sort-Object -Unique | ForEach-Object { "File:$_" }) -join "|"
$api = "https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url%7Cextmetadata&iiurlwidth=960&titles=$([uri]::EscapeDataString($titles))"
$pages = (Invoke-RestMethod -Uri $api -UserAgent "SKY-ARCHIVE/1.0 (reference photo downloader)").query.pages.psobject.Properties.Value
$byTitle = @{}
foreach ($page in $pages) {
  if (-not $page.imageinfo) { throw "Wikimedia Commons file not found: $($page.title)" }
  $byTitle[$page.title.Substring(5)] = $page.imageinfo[0]
}

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
)

$windowTitles = ($windowPhotos | ForEach-Object { "File:$($_.Title)" } | Sort-Object -Unique) -join "|"
$windowApi = "https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url&iiurlwidth=1600&titles=$([uri]::EscapeDataString($windowTitles))"
$windowPages = (Invoke-RestMethod -Uri $windowApi -UserAgent "SKY-ARCHIVE/1.0 (reference photo downloader)").query.pages.psobject.Properties.Value
$windowByTitle = @{}
foreach ($page in $windowPages) { $windowByTitle[$page.title.Substring(5)] = $page.imageinfo[0] }

Add-Type -AssemblyName System.Drawing
foreach ($photo in $windowPhotos) {
  $dest = Join-Path $root ("assets/reference/" + $photo.Dest)
  if (Test-Path $dest) { continue }
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
