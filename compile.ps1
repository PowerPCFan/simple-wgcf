param (
    [System.Management.Automation.SwitchParameter] $Linux,
    [System.Management.Automation.SwitchParameter] $Windows,
    [System.Management.Automation.SwitchParameter] $Verbose
)

if ($Windows) {
    Write-Host -ForegroundColor DarkCyan "Compiling for Windows...`n"

    try {
        # Windows compile
        & .\venv\Scripts\Activate.ps1
        Push-Location "app"

        if ($Verbose) {
            pyinstaller --noconfirm --onefile --console --add-data "modules;modules/" --add-data "commands;commands/"  "main.py"
        } else {
            pyinstaller --noconfirm --onefile --console --add-data "modules;modules/" --add-data "commands;commands/"  "main.py" 2>&1 > $null
        }

        Pop-Location
    } catch {
        Write-Host -ForegroundColor Red "An error occurred during the Windows compilation: $_"
        exit 1
    } finally {
        if (Test-Path ".\app\main.spec") {
            Remove-Item -Path ".\app\main.spec" -Force
        }
    }
}

if ($Linux) {
    if ($Windows) {
        Write-Host "`n`n`n`n`n"  # for extra spacing between both
    }

    Write-Host -ForegroundColor DarkCyan "Compiling for Linux...`n"

    try {
        # Linux compile with WSL
        if ($Verbose) {
            wsl -d 'Ubuntu-24.04' -- bash -c "
                cd '~/Documents/GitHub/simple-wgcf';
                source linuxvenv/bin/activate;
                cd 'app';
                pyinstaller --noconfirm --onefile --console --add-data 'modules:modules/' --add-data 'commands:commands/'  'main.py'
            "
        } else {
            wsl -d 'Ubuntu-24.04' -- bash -c "
                cd '~/Documents/GitHub/simple-wgcf';
                source linuxvenv/bin/activate;
                cd 'app';
                pyinstaller --noconfirm --onefile --console --add-data 'modules:modules/' --add-data 'commands:commands/'  'main.py'
            " 2>&1 > $null
        }
    } catch {
        Write-Host -ForegroundColor Red "An error occurred during the Linux compilation: $_"
        exit 1
    } finally {
        if (Test-Path ".\app\main.spec") {
            Remove-Item -Path ".\app\main.spec" -Force
        }
    }
}

if (-not (Test-Path ".\dist")) {
    New-Item -ItemType Directory -Path ".\dist" -Force
}

if (Test-Path ".\app\build") {
    Remove-Item -Path ".\app\build" -Recurse -Force
}

if (Test-Path ".\app\dist") {
    foreach ($item in Get-ChildItem -Path ".\app\dist") {
        Move-Item -Path $item.FullName -Destination ".\dist" -Force
        if ($item.Name -eq "main.exe") {
            Rename-Item -Path ".\dist\main.exe" -NewName "simple-wgcf.exe" -Force
        } elseif ($item.Name -eq "main") {
            Rename-Item -Path ".\dist\main" -NewName "simple-wgcf" -Force
        }
    }

    Remove-Item -Path ".\app\dist" -Recurse -Force
}
