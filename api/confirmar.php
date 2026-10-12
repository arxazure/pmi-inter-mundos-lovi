<?php
declare(strict_types=1);
require __DIR__.'/common.php';
$token=(string)($_SERVER['REQUEST_METHOD']==='POST'?($_POST['token']??''):($_GET['token']??''));
if(!preg_match('/^[a-f0-9]{64}$/D',$token)){http_response_code(400);exit('Link invalido.');}
$d=hash('sha256',$token);
$stmt=$pdo->prepare('SELECT id FROM pmi_signatures WHERE token_digest=? AND verified_at IS NULL AND expires_at>UTC_TIMESTAMP()');
$stmt->execute([$d]);$id=$stmt->fetchColumn();
if(!$id){http_response_code(410);exit('Link expirado ou utilizado.');}
if($_SERVER['REQUEST_METHOD']==='POST'){
 $s=$pdo->prepare('UPDATE pmi_signatures SET verified_at=UTC_TIMESTAMP(),token_digest=NULL WHERE id=? AND token_digest=? AND verified_at IS NULL');
 $s->execute([$id,$d]);
 if($s->rowCount()===1){echo '<!doctype html><html lang="pt-BR"><meta charset="utf-8"><h1>Solicitacao de assinatura confirmada</h1><p>Seu apoio ao pedido de consulta foi registrado. Isto nao significa voto na proposta GPC nem assinatura gov.br.</p></html>';exit;}
 http_response_code(409);exit('Confirmacao indisponivel.');
}
header('Content-Type: text/html; charset=utf-8');
echo '<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Confirmar solicitacao</title><body><h1>Confirmar apoio ao pedido de consulta</h1><p>Isso nao representa concordancia com a implantacao de nenhum modelo nem validacao pelo gov.br.</p><form method="post"><input type="hidden" name="token" value="'.esc($token).'"><button type="submit">Confirmar meu apoio ao pedido</button></form></body></html>';
