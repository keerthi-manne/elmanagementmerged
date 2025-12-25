-- Database Migration Script
-- Add Interests column to Faculty table for auto-assignment
-- Add capacity constraints to Theme table

-- Add Interests field to Faculty table
ALTER TABLE Faculty ADD COLUMN IF NOT EXISTS Interests TEXT;

-- Add capacity constraints to Theme table
ALTER TABLE Theme ADD COLUMN IF NOT EXISTS MaxMentors INT DEFAULT 5;
ALTER TABLE Theme ADD COLUMN IF NOT EXISTS MaxJudges INT DEFAULT 5;

-- Optional: Add indexes for performance
CREATE INDEX IF NOT EXISTS idx_faculty_interests ON Faculty(UserID);
CREATE INDEX IF NOT EXISTS idx_facultytheme_theme ON FacultyTheme(ThemeID);
