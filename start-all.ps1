$root = Split-Path -Parent $MyInvocation.MyCommand.Path

# Start broker
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root'; bun broker.ts" -WindowStyle Normal

Start-Sleep -Seconds 2

# Start all 4 agents
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\orchestrator'; claude" -WindowStyle Normal
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\agents\test-plan'; claude" -WindowStyle Normal
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\agents\test-cases'; claude" -WindowStyle Normal
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\agents\automation'; claude" -WindowStyle Normal

Write-Host "All 5 windows opened (broker + 4 agents). Go to Orchestrator window to start."
