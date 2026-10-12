# PBU31 — implantação segura do cadastro de manifestações de apoio

**Status:** código preparado; NÃO ativado até configurar banco MySQL, email de domínio validado, segurança e documentação LGPD. Não chamar de assinatura gov.br, assinatura ICP-Brasil nem votação oficial.

1. Configurar no Hostinger Web Hosting Business um banco MySQL exclusivo PBU31, usuário com privilégios restritos e senha forte.
2. Executar `api/schema.sql` no banco isolado.
3. Criar no servidor `api/config.local.php` a partir de `config.example.php`; usar chaves aleatórias, endereço HTTPS definitivo, remetente de email efetivamente autorizado; nunca versionar esse arquivo.
4. Verificar extensões PHP `pdo_mysql` e `sodium`. Ajustar SMTP/remetente no servidor; o protótipo usa `mail()` somente se o envio estiver configurado.
5. Verificar suporte PHP da hospedagem e garantir que `api/.htaccess` seja respeitado. Bloquear acesso web ao config e schema; preferir guardar config fora da raiz pública quando o hPanel permitir.
6. Publicar um aviso de privacidade específico com controlador, finalidade, base legal adequada a opiniões políticas, prazo de retenção, contato do titular, acesso/revogação/exclusão, transferências, medida de segurança e processo de incidentes. Obter revisão jurídica antes de ativar.
7. Implementar ferramenta administrativa com autenticação forte, relatórios auditáveis, pedidos de exclusão, processamento de e-mails duplicados, expurgo automático de pendências, consentimento versionado e verificação antifraude proporcional. Não exportar dados brutos ao público.
8. Testar HTTPS, geração de tokens, expiração, confirmação, taxa de solicitações, falha de e-mail e exclusão dos dados, antes de divulgar o formulário.

**Limitações atuais:** usa criptografia dos dados pessoais em repouso (Sodium), índice HMAC do e-mail e fragmentos de CPF. E-mail verificado NÃO verifica identidade; não há proteção completa contra bots nem ferramenta de administração e direitos dos titulares. O fluxo de envio não está ativo até a configuração. Não adicionar via GitHub o arquivo config.local.php nem segredos.
