$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $dir
claude --dangerously-skip-permissions
