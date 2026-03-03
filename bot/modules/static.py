WelcomeText = \
"""\
Olá **%(first_name)s**, envie-me um arquivo para gerar links instantâneos.

**Comandos Disponíveis:**
/start - Iniciar o bot e ver esta mensagem.
/help - Mostrar ajuda e comandos.
/delete - Deletar todo o banco de dados (Apenas Dono).
/backup - Fazer backup manual do banco de dados (Apenas Dono).
/restore - Restaurar o banco de dados do canal (Apenas Dono).
/privacy - Ver a política de privacidade do bot.
/log - Obter o arquivo de log do bot (Apenas Dono).
"""

PrivacyText = \
"""
**Política de Privacidade**

**1. Armazenamento de Dados:** Os arquivos que você envia são salvos com segurança no canal privado do Telegram do bot.

**2. Links de Download:** Os links incluem um código secreto para evitar acesso não autorizado.

**3. Controle do Usuário:** Você pode revogar os links a qualquer momento usando o botão "Revoke".

**4. Moderação:** O proprietário do bot pode visualizar e excluir seus arquivos, se necessário.

**5. Código Aberto:** O bot é de [código aberto](https://github.com/TheCaduceus/FileStreamBot). Implante sua própria instância para máxima privacidade.

**6. Retenção:** Os arquivos são armazenados até que você revogue seus links.

__Ao usar este bot, você concorda com esta política.__
"""

FileLinksText = \
"""
**Link de Download:**
`%(dl_link)s`
"""

MediaLinksText = \
"""
**Link de Download:**
`%(dl_link)s`

**Link de Transmissão:**
`%(stream_link)s`

**Link Direto (VLC/Player):**
`%(direct_link)s`
"""

InvalidQueryText = \
"""
Dados da consulta incompatíveis.
"""

MessageNotExist = \
"""
Arquivo revogado ou inexistente.
"""

LinkRevokedText = \
"""
O link foi revogado. Pode levar algum tempo para que as alterações entrem em vigor.
"""

InvalidPayloadText = \
"""
Payload inválido.
"""

UserNotInAllowedList = \
"""
Você não tem permissão para usar este bot.
"""
