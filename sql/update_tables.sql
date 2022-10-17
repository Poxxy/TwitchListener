-- Update side tables 

INSERT INTO "channels" (channel)
SELECT DISTINCT channel
FROM  "content"
ON CONFLICT DO NOTHING;

INSERT INTO "users" (username)
SELECT DISTINCT username
FROM  "content"
ON CONFLICT DO NOTHING;