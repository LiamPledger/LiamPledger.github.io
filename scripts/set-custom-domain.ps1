param(
  [Parameter(Mandatory = $true)]
  [string]$Domain
)

$cleanDomain = $Domain.Trim().ToLower()
if ([string]::IsNullOrWhiteSpace($cleanDomain)) {
  throw "Domain cannot be empty."
}

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$cnamePath = Join-Path $repoRoot "site/CNAME"

# GitHub Pages expects exactly one domain value in this file.
Set-Content -Path $cnamePath -Value $cleanDomain -NoNewline

Write-Output "Custom domain written to: $cnamePath"
Write-Output "Domain: $cleanDomain"
