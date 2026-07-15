# launch.ps1

#ps2exe -InputFile "run.ps1" -OutputFile "launch.exe" -NoConsole -iconFile "src\assets\flet.ico"

$scriptPath = ".\src\main.py"
$pythonwPath = ".venv\Scripts\pythonw.exe"

if (Test-Path $pythonwPath) {
    & $pythonwPath $scriptPath
} else {
    Write-Error "找不到 pythonw.exe，请确保虚拟环境已激活。"
    Pause
}