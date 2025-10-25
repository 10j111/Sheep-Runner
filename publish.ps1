<#
publish.ps1
PowerShell helper to initialize git, create a GitHub repo (via gh CLI) and publish a release

Usage: run this script from the project folder (sheep-runner) in PowerShell.

Notes:
- This script automates local git init / add / commit and (if available) uses GitHub CLI (`gh`) to
  create a public repository and upload the `dist\SheepRunner.zip` as a Release asset.
- You must run this locally. Do NOT share credentials here. If `gh` is not installed or not
  authenticated, the script will print manual commands to run.
#>
param(
    [string]$Owner = '',
    [string]$Repo = 'sheep-runner',
    [string]$Version = 'v1.0.0'
)

function Abort([string]$msg){ Write-Host $msg -ForegroundColor Red; exit 1 }

Write-Host "Publish helper — running in: $(Get-Location)" -ForegroundColor Cyan

# check git
if (-not (Get-Command git -ErrorAction SilentlyContinue)){
    Abort "Git is not installed or not in PATH. Please install Git for Windows first: https://git-scm.com/download/win"
}

# ensure dist zip exists
$distZip = Join-Path -Path (Get-Location) -ChildPath "dist\SheepRunner.zip"
if (-not (Test-Path $distZip)){
    Write-Host "Warning: dist\SheepRunner.zip not found. Ensure you built the executable with PyInstaller and zipped it into dist\SheepRunner.zip." -ForegroundColor Yellow
    $proceed = Read-Host "Continue anyway? (y/N)"
    if ($proceed -ne 'y') { Abort "Aborted by user." }
}

# init git if needed
if (-not (Test-Path .git)){
    Write-Host "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit - Sheep Runner"
} else {
    Write-Host "Existing git repo found. Staging and committing changes..."
    git add .
    git commit -m "Update project" -q 2>$null
}

# If gh is installed, try to use it to create the repo and release
if (Get-Command gh -ErrorAction SilentlyContinue){
    Write-Host "GitHub CLI detected. Checking authentication..."
    $auth = gh auth status 2>&1
    if ($LASTEXITCODE -ne 0){
        Write-Host "You are not authenticated with gh. Run: gh auth login" -ForegroundColor Yellow
        Write-Host "Falling back to manual remote setup."
    } else {
        if ([string]::IsNullOrEmpty($Owner)){
            $Owner = gh api user --jq .login
        }
        Write-Host "Creating GitHub repo $Owner/$Repo (public) ..."
        gh repo create "$Owner/$Repo" --public --source=. --remote=origin --push --confirm
        if ($LASTEXITCODE -ne 0){ Abort "gh repo create failed." }

        # create release and upload ZIP if present
        if (Test-Path $distZip){
            Write-Host "Creating release $Version and uploading $distZip ..."
            gh release create $Version $distZip -t "Sheep Runner $Version" -n "Standalone Windows build"
            if ($LASTEXITCODE -ne 0){ Write-Host "Warning: gh release create failed." -ForegroundColor Yellow }
        } else {
            Write-Host "No dist zip found to upload as release asset. You can upload via GitHub Releases web UI later." -ForegroundColor Yellow
        }

        Write-Host "Done. Repository created at: https://github.com/$Owner/$Repo" -ForegroundColor Green
        exit 0
    }
}

# Fallback: Ask user to create a repo on GitHub and push
Write-Host "Please create an empty PUBLIC repository on GitHub (no README) named: $Repo" -ForegroundColor Yellow
Write-Host "Then run these commands (replace <your-username>):" -ForegroundColor Cyan
Write-Host "git branch -M main"
Write-Host "git remote add origin https://github.com/<your-username>/$Repo.git"
Write-Host "git push -u origin main"

Write-Host "After the repo is created, upload dist\SheepRunner.zip in GitHub Releases (or use gh release create)." -ForegroundColor Cyan
