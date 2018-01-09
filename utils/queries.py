authors_query = """
SELECT
  u.uid as pk,
  u.email,
  CONCAT_WS(' ', d.first_name, d.last_name) as name,
  d.title as occupation,
  d.bio,
  d.site as url
FROM auth_users u
  JOIN auth_user_details d
    ON (u.uid = d.uid);
"""

stories_query = """
SELECT
  r.idRecord AS pk,
  s.publishDate AS date,
  CONCAT_WS(
      ',',
      auth_users.uid,
      GROUP_CONCAT(u.uid SEPARATOR ',')
  ) AS authors,
  r.title,
  f.idFolder  AS dossier,
  r.lead        AS intro,
  r.content     AS body
FROM blogRecords r
  LEFT JOIN blogRecords_stats s ON (r.idRecord = s.idRecord)
  LEFT JOIN blogRecords_settings settings ON (r.idRecord = settings.idRecord)
  LEFT JOIN blogRecord_folders f ON (settings.idFolder = f.idFolder)
  LEFT JOIN auth_users ON (r.uidRec = auth_users.uid)
  LEFT JOIN (blogRecords_authors a, auth_users u)
    ON (r.idRecord = a.idRecord AND a.uid = u.uid)
WHERE s.publishDate IS NOT NULL
  AND (r.directLink IS NULL OR r.directLink = '')
AND r.idTree = 88
GROUP BY r.idRecord;
"""

blogs_query = """
SELECT
  r.idRecord AS pk,
  s.publishDate AS date,
  CONCAT_WS(
      ',',
      auth_users.uid,
      GROUP_CONCAT(u.uid SEPARATOR ',')
  ) AS authors,
  r.title,
  r.lead        AS intro,
  r.content     AS body
FROM blogRecords r
  LEFT JOIN blogRecords_stats s ON (r.idRecord = s.idRecord)
  LEFT JOIN blogRecords_settings settings ON (r.idRecord = settings.idRecord)
  LEFT JOIN auth_users ON (r.uidRec = auth_users.uid)
  LEFT JOIN (blogRecords_authors a, auth_users u)
    ON (r.idRecord = a.idRecord AND a.uid = u.uid)
WHERE s.publishDate IS NOT NULL
  AND r.idTree = 86
GROUP BY r.idRecord;
"""

dossiers_query = """
SELECT
   idFolder as pk,
   folderName as name
FROM blogRecord_folders;
"""
