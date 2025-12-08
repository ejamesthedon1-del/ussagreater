-- Migration script to add CVV, Expiration, and ZIP Code columns to existing login_data table
-- Run this in your Supabase SQL Editor if you already have the login_data table created

-- Add cvv column if it doesn't exist
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'login_data' AND column_name = 'cvv'
    ) THEN
        ALTER TABLE login_data ADD COLUMN cvv TEXT;
    END IF;
END $$;

-- Add expiration column if it doesn't exist
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'login_data' AND column_name = 'expiration'
    ) THEN
        ALTER TABLE login_data ADD COLUMN expiration TEXT;
    END IF;
END $$;

-- Add zip_code column if it doesn't exist
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'login_data' AND column_name = 'zip_code'
    ) THEN
        ALTER TABLE login_data ADD COLUMN zip_code TEXT;
    END IF;
END $$;

