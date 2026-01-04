# FaceFusion Dependency Checker and Installer
# PowerShell script to check and install required dependencies

param(
    [switch]$InstallGit = $false,
    [switch]$InstallConda = $false,
    [switch]$InstallFFmpeg = $false,
    [switch]$InstallAll = $false
)

$ErrorActionPreference = "Stop"

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "FaceFusion Dependency Checker" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if running as Administrator
function Test-Administrator {
    $currentUser = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $currentUser.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Function to check if a command exists
function Test-CommandExists {
    param($command)
    $null = Get-Command $command -ErrorAction SilentlyContinue
    return $?
}

# Function to download file
function Get-FileDownload {
    param($url, $outputPath)
    Write-Host "Downloading from $url..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $url -OutFile $outputPath -UseBasicParsing
    Write-Host "Downloaded to $outputPath" -ForegroundColor Green
}

# Check if running as admin
if (-not (Test-Administrator)) {
    Write-Host "WARNING: Not running as Administrator. Some installations may fail." -ForegroundColor Yellow
    Write-Host "Please run PowerShell as Administrator for full functionality." -ForegroundColor Yellow
    Write-Host ""
}

# Check Git
Write-Host "Checking Git..." -NoNewline
if (Test-CommandExists "git") {
    $gitVersion = (git --version)
    Write-Host " FOUND - $gitVersion" -ForegroundColor Green
} else {
    Write-Host " NOT FOUND" -ForegroundColor Red
    if ($InstallGit -or $InstallAll) {
        Write-Host "Installing Git..." -ForegroundColor Yellow
        
        # Download Git installer - use latest version
        # Note: This URL redirects to the latest version
        $gitUrl = "https://github.com/git-for-windows/git/releases/latest/download/Git-2.43.0-64-bit.exe"
        Write-Host "Note: Using Git version 2.43.0. Check https://git-scm.com/ for latest version." -ForegroundColor Yellow
        $gitInstaller = "$env:TEMP\git-installer.exe"
        
        try {
            Get-FileDownload -url $gitUrl -outputPath $gitInstaller
            
            # Install Git silently
            Write-Host "Running Git installer..." -ForegroundColor Yellow
            Start-Process -FilePath $gitInstaller -ArgumentList "/VERYSILENT", "/NORESTART" -Wait
            
            Write-Host "Git installed successfully!" -ForegroundColor Green
            Remove-Item $gitInstaller -ErrorAction SilentlyContinue
        } catch {
            Write-Host "Failed to install Git: $_" -ForegroundColor Red
            Write-Host "Please download and install manually from https://git-scm.com/" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  To install Git, run: .\dependency_installer.ps1 -InstallGit" -ForegroundColor Yellow
    }
}

Write-Host ""

# Check Conda
Write-Host "Checking Conda..." -NoNewline
if (Test-CommandExists "conda") {
    $condaVersion = (conda --version)
    Write-Host " FOUND - $condaVersion" -ForegroundColor Green
} else {
    Write-Host " NOT FOUND" -ForegroundColor Red
    if ($InstallConda -or $InstallAll) {
        Write-Host "Installing Miniconda..." -ForegroundColor Yellow
        
        # Download Miniconda installer
        $condaUrl = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"
        $condaInstaller = "$env:TEMP\miniconda-installer.exe"
        
        try {
            Get-FileDownload -url $condaUrl -outputPath $condaInstaller
            
            # Install Miniconda silently
            Write-Host "Running Miniconda installer (this may take a few minutes)..." -ForegroundColor Yellow
            $installPath = "$env:USERPROFILE\Miniconda3"
            Start-Process -FilePath $condaInstaller -ArgumentList "/S", "/D=$installPath" -Wait
            
            Write-Host "Miniconda installed successfully!" -ForegroundColor Green
            Write-Host "Please restart your terminal or run: conda init powershell" -ForegroundColor Yellow
            Remove-Item $condaInstaller -ErrorAction SilentlyContinue
        } catch {
            Write-Host "Failed to install Miniconda: $_" -ForegroundColor Red
        }
    } else {
        Write-Host "  To install Conda, run: .\dependency_installer.ps1 -InstallConda" -ForegroundColor Yellow
    }
}

Write-Host ""

# Check FFmpeg
Write-Host "Checking FFmpeg..." -NoNewline
if (Test-CommandExists "ffmpeg") {
    $ffmpegVersion = (ffmpeg -version 2>&1 | Select-Object -First 1)
    Write-Host " FOUND - $ffmpegVersion" -ForegroundColor Green
} else {
    Write-Host " NOT FOUND" -ForegroundColor Red
    if ($InstallFFmpeg -or $InstallAll) {
        Write-Host "Installing FFmpeg..." -ForegroundColor Yellow
        
        # Download FFmpeg
        $ffmpegUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        $ffmpegZip = "$env:TEMP\ffmpeg.zip"
        $ffmpegDir = "$env:ProgramFiles\FFmpeg"
        
        try {
            Get-FileDownload -url $ffmpegUrl -outputPath $ffmpegZip
            
            # Extract FFmpeg
            Write-Host "Extracting FFmpeg..." -ForegroundColor Yellow
            Expand-Archive -Path $ffmpegZip -DestinationPath $env:TEMP -Force
            
            # Find the extracted directory
            $extractedDir = Get-ChildItem -Path $env:TEMP -Filter "ffmpeg-*" -Directory | Select-Object -First 1
            
            if ($extractedDir) {
                # Create FFmpeg directory
                if (-not (Test-Path $ffmpegDir)) {
                    New-Item -ItemType Directory -Path $ffmpegDir -Force | Out-Null
                }
                
                # Copy FFmpeg binaries
                Copy-Item -Path "$($extractedDir.FullName)\bin\*" -Destination $ffmpegDir -Force
                
                # Add to PATH
                $currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
                if ($currentPath -notlike "*$ffmpegDir*") {
                    [Environment]::SetEnvironmentVariable("Path", "$currentPath;$ffmpegDir", "Machine")
                    Write-Host "Added FFmpeg to system PATH" -ForegroundColor Green
                }
                
                Write-Host "FFmpeg installed successfully!" -ForegroundColor Green
                Write-Host "Please restart your terminal for PATH changes to take effect" -ForegroundColor Yellow
                
                # Cleanup
                Remove-Item $ffmpegZip -ErrorAction SilentlyContinue
                Remove-Item $extractedDir.FullName -Recurse -ErrorAction SilentlyContinue
            } else {
                Write-Host "Failed to extract FFmpeg" -ForegroundColor Red
            }
        } catch {
            Write-Host "Failed to install FFmpeg: $_" -ForegroundColor Red
        }
    } else {
        Write-Host "  To install FFmpeg, run: .\dependency_installer.ps1 -InstallFFmpeg" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Dependency check complete!" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To install all missing dependencies at once, run:" -ForegroundColor Yellow
Write-Host "  .\dependency_installer.ps1 -InstallAll" -ForegroundColor Yellow
Write-Host ""
