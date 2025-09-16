@echo off
echo ========================================
echo Citizen Complaint Analysis Tool
echo Vercel Deployment Helper
echo ========================================
echo.

echo This script will help you deploy your app to Vercel
echo.

echo Step 1: Initialize Git repository
git init
echo.

echo Step 2: Add all files to Git
git add .
echo.

echo Step 3: Create initial commit
git commit -m "Initial commit: Citizen Complaint Analysis Tool for Vercel"
echo.

echo ========================================
echo NEXT STEPS:
echo ========================================
echo.
echo 1. Go to https://github.com and create a new repository
echo 2. Copy the repository URL (e.g., https://github.com/username/repo-name.git)
echo 3. Run these commands:
echo    git remote add origin YOUR_REPOSITORY_URL
echo    git branch -M main
echo    git push -u origin main
echo.
echo 4. Go to https://vercel.com and import your GitHub repository
echo 5. Follow the deployment guide in DEPLOYMENT.md
echo.
echo ========================================
echo.
pause
