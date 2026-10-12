CREATE TABLE IF NOT EXISTS pmi_signatures (
 id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
 email_digest CHAR(64) NOT NULL UNIQUE,
 name_enc TEXT NOT NULL,
 email_enc TEXT NOT NULL,
 city_enc TEXT NOT NULL,
 state CHAR(2) NOT NULL,
 cpf_prefix_enc TEXT NOT NULL,
 cpf_suffix_enc TEXT NOT NULL,
 token_digest CHAR(64) DEFAULT NULL,
 verified_at DATETIME DEFAULT NULL,
 created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 expires_at DATETIME NOT NULL,
 ip_digest CHAR(64) NOT NULL,
 consent_version VARCHAR(30) NOT NULL,
 INDEX idx_token(token_digest),
 INDEX idx_ip_date(ip_digest,created_at),
 INDEX idx_expiry(expires_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;