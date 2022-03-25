# -*- coding: utf-8 -*-

# Módulos importados
from os.path import realpath
from subprocess import run

# Módulos do PyQt5
from PyQt5.QtCore import QUrl, qDebug
from PyQt5.QtMultimedia import QMediaContent

# Modulos integrados (src)
from jsonTools import set_json
from utils import setIcon, setSound
from version import __pagename__


########################################################################################################################


# Função para exibição de notificação.
def notifyMessage(self):
    if self.soma > 1:
        ms = self.message1
    else:
        ms = self.message2
    com = 'notify-send --app-name="' + __pagename__ + '" --expire-time=' + str(set_json('TimeMessage')) + \
          ' --icon="' + realpath(setIcon('notify')) + '" "' + str(self.soma) + ' ' + ms + '"'
    run(com, shell=True)


# Essa função pode variar conforme o webapp.
def verifyNotify(self, res):
    self.soma = 0
    for tag in res.xpath('//div[@class="bqXJH"]'):
        self.soma += int(tag.text)
    for tag in res.xpath(
            '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/a/div/div/div/div[2]/div/div/div/div'):
        self.soma += int(tag.text)
    if self.soma != self.notify and self.soma != 0:
        self.notify = self.soma  # Necessário para mapear alterações no número de notificações

        if self.isHidden() or int(self.windowState()) == 1 or int(self.windowState()) == 3:
            try:
                # As opções de notificação não funcionarão de primeira com o parâmetro '--system-login'
                if set_json('NotifySound') and not self.sysLogin:
                    self.notify_sound.setMedia(QMediaContent(QUrl.fromLocalFile(setSound(set_json('SoundTheme')))))
                    self.notify_sound.play()
                if set_json('NotifyMessage') and not self.sysLogin:
                    notifyMessage(self)
            except Exception as err:
                qDebug('\033[31m[DEBUG]\033[33m: ' + str(err) + '.\033[m')

            self.sysLogin = False  # Redefinição após a primeira verificação
