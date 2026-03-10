param(
  [string[]] $Urls = @(
    'http://127.0.0.1:11434/api/tags',
    'http://localhost:11434/api/tags'
  ),
  [int] $Retries = 10,
  [int] $TimeoutSec = 15
)

$ErrorActionPreference = 'Stop'
$ok = $false

for ($i = 0; $i -lt $Retries; $i++) {
  foreach ($u in $Urls) {
    try {
      Invoke-WebRequest -Uri $u -UseBasicParsing -TimeoutSec $TimeoutSec -Proxy $null | Out-Null
      $ok = $true
      break
    } catch {
      Start-Sleep -Seconds 3
    }
  }
  if ($ok) { break }
}

if (-not $ok) { exit 1 }
