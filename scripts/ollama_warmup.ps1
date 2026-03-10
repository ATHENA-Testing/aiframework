param(
  [string] $Model      = 'llama2:latest',
  [string] $OllamaHost = 'http://127.0.0.1:11434',
  [int] $TimeoutSec    = 600
)

$body = @{
  model   = $Model
  prompt  = 'warmup'
  stream  = $false
  options = @{ num_predict = 16 }
} | ConvertTo-Json

Invoke-RestMethod `
  -Method POST `
  -Uri ($OllamaHost + '/api/generate') `
  -ContentType 'application/json' `
  -Body $body `
  -TimeoutSec $TimeoutSec `
  -Proxy $null `
| Out-Null