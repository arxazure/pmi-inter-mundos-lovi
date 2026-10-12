<?php
declare(strict_types=1);
require __DIR__.'/common.php';
if ($_SERVER['REQUEST_METHOD']!=='POST') {http_response_code(405);exit('Metodo nao permitido');}
if (!empty($_POST['website']??'')) {http_response_code(400);exit('Formulario recusado.');}
$origin=$_SERVER['HTTP_ORIGIN']??'';
if ($origin && rtrim($origin,'/')!==rtrim($config['base_url'],'/')) {http_response_code(403);exit('Origem invalida.');}
$name=trim((string)($_POST['nome']??''));
$email=strtolower(trim((string)($_POST['email']??'')));
$city=trim((string)($_POST['cidade']??''));
$state=strtoupper(trim((string)($_POST['estado']??'')));
$first=trim((string)($_POST['cpf_inicio']??''));
$last=trim((string)($_POST['cpf_fim']??''));
$consent=(string)($_POST['consentimento']??'');
$length=static fn(string $s):int=>function_exists('mb_strlen')?mb_strlen($s):strlen($s);
if ($length($name)<5||$length($name)>160||!str_contains($name,' ')||!filter_var($email,FILTER_VALIDATE_EMAIL)||strlen($email)>254||$length($city)<2||$length($city)>100||!in_array($state,explode(',','AC,AL,AP,AM,BA,CE,DF,ES,GO,MA,MT,MS,MG,PA,PB,PR,PE,PI,RJ,RN,RS,RO,RR,SC,SP,SE,TO'),true)||!preg_match('/^[0-9]{3}$/',$first)||!preg_match('/^[0-9]{3}$/',$last)||$consent!=='sim') {http_response_code(422);exit('Verifique os campos obrigatorios e o consentimento.');}
$ip=$_SERVER['REMOTE_ADDR']??'unknown';$ipDigest=blind('ip:'.$ip);
$limit=$pdo->prepare('SELECT COUNT(*) FROM pmi_signatures WHERE ip_digest=? AND created_at>DATE_SUB(UTC_TIMESTAMP(),INTERVAL 24 HOUR)');$limit->execute([$ipDigest]);
if((int)$limit->fetchColumn()>=5){http_response_code(429);exit('Limite temporario de solicitacoes atingido.');}
$token=bin2hex(random_bytes(32));$digest=hash('sha256',$token);
try{
 $st=$pdo->prepare('INSERT INTO pmi_signatures (email_digest,name_enc,email_enc,city_enc,state,cpf_prefix_enc,cpf_suffix_enc,token_digest,expires_at,ip_digest,consent_version) VALUES (?,?,?,?,?,?,?,?,DATE_ADD(UTC_TIMESTAMP(),INTERVAL 24 HOUR),?,?)');
 $st->execute([blind('email:'.$email),enc($name),enc($email),enc($city),$state,enc($first),enc($last),$digest,$ipDigest,$config['consent_version']]);
 $id=$pdo->lastInsertId();
}catch(PDOException $e){http_response_code(409);exit('Ja existe uma solicitacao para este e-mail. Contate o responsavel pela privacidade se precisar de ajuda.');}
$link=rtrim($config['base_url'],'/').'/api/confirmar.php?token='.urlencode($token);
$subject='Confirme sua assinatura do pedido de consulta popular PMI31';
$message="Foi solicitado o registro de apoio a um PEDIDO de consulta popular (nao apoio a um modelo de governo).\n\nAbra este link e pressione Confirmar para validar em ate 24 horas:\n".$link."\n\nSe voce nao solicitou, ignore a mensagem.\nContato para privacidade: ".$config['privacy_contact']."\n";
$headers=['From: '.$config['mail_from'],'Content-Type: text/plain; charset=UTF-8'];
if(!mail($email,$subject,$message,implode("\r\n",$headers))){$pdo->prepare('DELETE FROM pmi_signatures WHERE id=? AND verified_at IS NULL')->execute([$id]);http_response_code(503);exit('Nao foi possivel enviar o email de confirmacao. Tente mais tarde.');}
header('Content-Type: text/html; charset=utf-8');echo '<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Confira seu email</title><body><h1>Confira seu e-mail</h1><p>Enviamos um link para confirmar sua solicitacao. Ela ainda NAO e uma assinatura validada.</p><p><a href="../pedido-plebiscito-gpc.html">Voltar ao pedido</a></p></body></html>';
