param()

$brokerBase = "http://localhost:7801"
$agentName  = "automation"
$outputDir  = "$PSScriptRoot\output\specs"
$pagesDir   = "$PSScriptRoot\output\pages"

if (-not (Test-Path $outputDir)) { New-Item -ItemType Directory -Force $outputDir | Out-Null }
if (-not (Test-Path $pagesDir))  { New-Item -ItemType Directory -Force $pagesDir  | Out-Null }

function Send-ToOrchestrator($payload) {
    $body = $payload | ConvertTo-Json -Depth 20
    Invoke-RestMethod -Uri "$brokerBase/send" -Method Post `
        -ContentType "application/json" -Body $body | Out-Null
}

function Get-SelectorForPlatform($platform, $id) {
    switch ($platform) {
        "web"     { return "`$('*[data-test=""$id""]')" }
        default   { return "`$('~test-$id')" }
    }
}

function New-PageObject($module, $platform, $selectors) {
    $className = "$($module)Page"
    $getters = $selectors | ForEach-Object {
        $sel = Get-SelectorForPlatform $platform $_
        "  get $($_)() { return $sel; }"
    }
    $openBody = if ($platform -eq "web") { "await browser.url('/');" } else { "// App launched via Appium capabilities" }
    @"
// pages/$($module.ToLower()).page.ts

class $className {
$($getters -join "`n")

  async open() {
    $openBody
  }
}

export default new $className();
"@
}

function New-SpecFile($module, $cases, $platform) {
    $pageName   = "$($module)Page"
    $pageImport = "$($module.ToLower()).page"
    $its = foreach ($tc in $cases) {
        $id   = $tc.id
        $name = $tc.name
        $body = $tc.steps | ForEach-Object { "    // $_" }
        @"
  it('$id`: $name', async () => {
$($body -join "`n")
    // TODO: add assertions
  });
"@
    }
    @"
// output/specs/$($module.ToLower()).spec.ts

import $pageName from '../pages/$pageImport';

describe('$module', () => {

  beforeEach(async () => {
    await $pageName.open();
  });

$($its -join "`n`n")
});
"@
}

function Process-AutomationRequest($msg) {
    $cases    = $msg.payload.cases
    $platform = if ($msg.payload.platform) { $msg.payload.platform } else { "android" }

    Write-Host "[automation] Processing $($cases.Count) cases for platform: $platform"

    # Group by module
    $grouped = $cases | Group-Object { $_.module }

    $generatedFiles = @()

    foreach ($group in $grouped) {
        $module   = $group.Name
        $modCases = $group.Group

        # Generate spec file
        $specContent = New-SpecFile $module $modCases $platform
        $specPath    = "$outputDir\$($module.ToLower()).spec.ts"
        Set-Content -Path $specPath -Value $specContent -Encoding UTF8

        $generatedFiles += "output/specs/$($module.ToLower()).spec.ts"
        Write-Host "[automation] Written: $specPath"
    }

    $summary = "$($generatedFiles.Count) spec files generated, $($cases.Count) test cases automated"
    Write-Host "[automation] $summary"

    Send-ToOrchestrator @{
        from    = "automation"
        to      = "orchestrator"
        type    = "automation_ready"
        payload = @{
            files   = $generatedFiles
            summary = $summary
        }
    }
    Write-Host "[automation] Sent automation_ready to orchestrator"
}

function Process-RevisionRequest($msg) {
    Write-Host "[automation] Revision request received: $($msg.payload.change)"
    # Re-process with updated cases if provided, or apply targeted change
    if ($msg.payload.cases) {
        Process-AutomationRequest $msg
    } else {
        Write-Host "[automation] No cases in revision payload — skipping"
    }
}

# SSE listener loop
Write-Host "[automation] Starting SSE listener on $brokerBase/stream/$agentName"

while ($true) {
    try {
        $req = [System.Net.WebRequest]::Create("$brokerBase/stream/$agentName")
        $req.Accept  = "text/event-stream"
        $req.Timeout = [System.Threading.Timeout]::Infinite

        $resp   = $req.GetResponse()
        $stream = $resp.GetResponseStream()
        $reader = [System.IO.StreamReader]::new($stream)

        Write-Host "[automation] SSE connected"

        $dataBuffer = ""

        while (-not $reader.EndOfStream) {
            $line = $reader.ReadLine()

            if ($line -match '^data:\s*(.+)$') {
                $dataBuffer = $Matches[1]
                try {
                    $msg = $dataBuffer | ConvertFrom-Json
                    switch ($msg.type) {
                        "automation_request" { Process-AutomationRequest $msg }
                        "revision_request"   { Process-RevisionRequest   $msg }
                        default              { Write-Host "[automation] Ignored message type: $($msg.type)" }
                    }
                } catch {
                    Write-Host "[automation] Failed to parse message: $_"
                }
                $dataBuffer = ""
            }
        }

        $reader.Close()
        $resp.Close()
        Write-Host "[automation] Stream ended — reconnecting in 3s"
    } catch {
        Write-Host "[automation] Stream error: $_ — reconnecting in 3s"
    }
    Start-Sleep -Seconds 3
}
