while ($true) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:7801/stream/automation" -Method GET -TimeoutSec 60 -UseBasicParsing
        $lines = $response.Content -split "`n"
        foreach ($line in $lines) {
            if ($line -match "^data: (.+)$") {
                $json = $Matches[1]
                Add-Content -Path "C:\Users\Administrator\Desktop\mset-ai-pipeline\agents\automation\sse_messages.log" -Value "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | $json"
            }
        }
    } catch {
        Start-Sleep -Seconds 2
    }
}
