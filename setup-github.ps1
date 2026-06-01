# Deployment script for Render - Run this after installing Git

Set-Location -Path "c:\Users\as\PYTHON"

Write-Host "🚀 Starting Render deployment setup..." -ForegroundColor Green

git init
Write-Host "✓ Git initialized" -ForegroundColor Green

git add .
Write-Host "✓ All files staged" -ForegroundColor Green

git commit -m "Deploy booking system to Render"
Write-Host "✓ Changes committed" -ForegroundColor Green

git branch -M main
Write-Host "✓ Branch renamed to main" -ForegroundColor Green

git remote add origin https://github.com/abhishebaghel/Trip-Booking-For.git
Write-Host "✓ Remote repository added" -ForegroundColor Green

Write-Host ""
Write-Host "⚠️  IMPORTANT: Before pushing, you need to:" -ForegroundColor Yellow
Write-Host "1. Create the repository on GitHub: https://github.com/new" -ForegroundColor Yellow
Write-Host "2. Repository name: Trip-Booking-For" -ForegroundColor Yellow
Write-Host "3. Make it PUBLIC so Render can access it" -ForegroundColor Yellow
Write-Host "4. Do NOT initialize with README (we already have files)" -ForegroundColor Yellow
Write-Host ""
Write-Host "After creating the GitHub repo, run this to push:" -ForegroundColor Cyan
Write-Host "git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "Then connect the repo to Render:" -ForegroundColor Cyan
Write-Host "1. Go to https://dashboard.render.com/" -ForegroundColor Cyan
Write-Host "2. Click 'New +' > 'Web Service'" -ForegroundColor Cyan
Write-Host "3. Connect your GitHub account" -ForegroundColor Cyan
Write-Host "4. Select your repository: abhishebaghel/Trip-Booking-For" -ForegroundColor Cyan
Write-Host "5. Choose name: bookingtripform" -ForegroundColor Cyan
Write-Host "6. Runtime: Python 3" -ForegroundColor Cyan
Write-Host "7. Build command: pip install -r requirements.txt" -ForegroundColor Cyan
Write-Host "8. Start command: python app.py" -ForegroundColor Cyan
