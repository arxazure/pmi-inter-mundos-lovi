<?php
// COPIE para config.local.php SOMENTE no servidor. NUNCA envie esse arquivo ao GitHub.
// Use variaveis reais do MySQL da hospedagem e chaves aleatorias seguras.
return [
 'dsn' => 'mysql:host=localhost;dbname=NOME_BANCO;charset=utf8mb4',
 'user' => 'USUARIO_DB',
 'password' => 'SENHA_DB',
 // php -r "echo base64_encode(random_bytes(32)), PHP_EOL;"
 'encryption_key_b64' => 'CHAVE_BASE64_32_BYTES',
 'hmac_key' => 'SEGREDO_HMAC_LONGO_ALEATORIO',
 'base_url' => 'https://salmon-quail-451428.hostingersite.com',
 'mail_from' => 'contato@DOMINIO_VERIFICADO',
 'privacy_contact' => 'privacidade@DOMINIO_VERIFICADO',
 'consent_version' => 'peticao-gpc-v1'
];