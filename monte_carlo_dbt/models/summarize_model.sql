-- summarize_model.sql
SELECT
    id,
    title,
    description,
    LENGTH(description) AS description_length
FROM raw_data
WHERE description IS NOT NULL
