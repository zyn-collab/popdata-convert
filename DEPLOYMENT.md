# Deploying to Vercel

This guide will help you deploy the Citizen Complaint Analysis Tool to Vercel so others can use it online.

## Prerequisites

1. **GitHub Account**: You'll need a GitHub account
2. **Vercel Account**: Sign up at [vercel.com](https://vercel.com) (free)
3. **Git**: Make sure Git is installed on your computer

## Step 1: Prepare Your Code

1. **Remove unnecessary files** (optional):
   - Delete `run_app.bat` (not needed for Vercel)
   - Delete `sample_complaint_data.xlsx` and `sample_population_data.xlsx` (optional)

2. **Verify your files**:
   - `app.py` - Main Flask application
   - `templates/index.html` - Web interface
   - `requirements.txt` - Python dependencies
   - `vercel.json` - Vercel configuration

## Step 2: Create GitHub Repository

1. **Initialize Git repository**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Citizen Complaint Analysis Tool"
   ```

2. **Create GitHub repository**:
   - Go to [github.com](https://github.com)
   - Click "New repository"
   - Name it: `citizen-complaint-analysis`
   - Make it public (required for free Vercel)
   - Don't initialize with README (you already have files)

3. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/citizen-complaint-analysis.git
   git branch -M main
   git push -u origin main
   ```

## Step 3: Deploy to Vercel

1. **Go to Vercel**:
   - Visit [vercel.com](https://vercel.com)
   - Sign in with your GitHub account

2. **Import Project**:
   - Click "New Project"
   - Select your GitHub repository: `citizen-complaint-analysis`
   - Click "Import"

3. **Configure Deployment**:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (default)
   - **Build Command**: Leave empty (Vercel will auto-detect)
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt`

4. **Deploy**:
   - Click "Deploy"
   - Wait for deployment to complete (2-3 minutes)

## Step 4: Test Your Deployment

1. **Access your app**:
   - Vercel will provide a URL like: `https://your-app-name.vercel.app`
   - Click the URL to test your application

2. **Test file upload**:
   - Try uploading a small Excel file
   - Verify the analysis report downloads correctly

## Step 5: Custom Domain (Optional)

1. **Add custom domain**:
   - In Vercel dashboard, go to your project
   - Click "Settings" → "Domains"
   - Add your custom domain (if you have one)

## Important Notes

### File Size Limits
- **Vercel has limits**: 50MB for serverless functions
- **Large files**: For files > 10MB, consider using a different service or optimizing your data

### Environment Variables
- **Secret Key**: Vercel will use the default secret key
- **For production**: Set a proper secret key in Vercel dashboard:
  - Go to Settings → Environment Variables
  - Add: `SECRET_KEY` = `your-secure-random-string`

### Performance
- **Cold starts**: First request might be slower (2-3 seconds)
- **Subsequent requests**: Much faster
- **Timeout**: 10 seconds for free tier, 60 seconds for Pro

## Troubleshooting

### Common Issues:

1. **Build fails**:
   - Check `requirements.txt` has all dependencies
   - Ensure Python version compatibility

2. **File upload fails**:
   - Check file size (should be < 50MB)
   - Verify file format (.xlsx or .xls)

3. **Timeout errors**:
   - Large files might timeout on free tier
   - Consider upgrading to Pro for longer timeouts

### Getting Help:
- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **Flask on Vercel**: [vercel.com/docs/frameworks/flask](https://vercel.com/docs/frameworks/flask)

## Sharing Your App

Once deployed, you can share your app with:
- **Direct URL**: `https://your-app-name.vercel.app`
- **QR Code**: Generate QR codes for easy mobile access
- **Embed**: Embed in other websites if needed

## Cost

- **Free Tier**: Perfect for testing and small-scale use
- **Pro Tier**: $20/month for production use with higher limits
- **Enterprise**: Custom pricing for large organizations

Your app is now live and accessible to anyone with the URL! 🎉
