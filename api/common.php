<?php
declare(strict_types=1);
ini_set('display_errors','0');
header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: no-referrer');
header('Cache-Control: no-store');
if (!is_file(__DIR__.'/config.local.php')) {http_response_code(503); exit('Assinaturas ainda indisponiveis. Configure o servico primeiro.');}
$config=require __DIR__.'/config.local.php';
foreach (['dsn','user','password','encryption_key_b64','hmac_key','base_url','mail_from','privacy_contact','consent_version'] as $key) {
 if (!isset($config[$key]) || !$config[$key] || str_contains((string)$config[$key],'DOMINIO_VERIFICADO') || str_contains((string)$config[$key],'CHAVE_BASE64')) {http_response_code(503);exit('Configuracao pendente.');}
}
$key=base64_decode($config['encryption_key_b64'],true);
if (!$key || strlen($key)!==SODIUM_CRYPTO_SECRETBOX_KEYBYTES || strlen($config['hmac_key'])<32 || !str_starts_with($config['base_url'],'https://')) {http_response_code(503);exit('Configuracao insegura.');}
try {$pdo=new PDO($config['dsn'],$config['user'],$config['password'],[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION,PDO::ATTR_EMULATE_PREPARES=>false]);}
catch(Throwable $e){http_response_code(503);exit('Servico temporariamente indisponivel.');}
function enc(string $str): string {global $key;$nonce=random_bytes(SODIUM_CRYPTO_SECRETBOX_NONCEBYTES);return base64_encode($nonce.sodium_crypto_secretbox($str,$nonce,$key));}
function blind(string $str):string{global $config;return hash_hmac('sha256',$str,$config['hmac_key']);}
function esc(string $v):string{return htmlspecialchars($v,ENT_QUOTES|ENT_SUBSTITUTE,'UTF-8');}
