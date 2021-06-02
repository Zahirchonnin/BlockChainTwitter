from brownie import TwitterOnBlockChain, accounts
from scripts.appIntreface.main import Ui_Form
from datetime import datetime
from PyQt5 import QtWidgets
from time import time
import os


class APP(QtWidgets.QWidget):
    def __init__(self, contract):
        self.contract = contract
        super().__init__()
        self.inintalizeUI()
    
    def inintalizeUI(self):
        self.message = QtWidgets.QMessageBox()

        self.main = Ui_Form()
        self.main.setupUi()
        self.main.browse.clicked.connect(self.Browse)

        self.main.submit_up.clicked.connect(self.singUp)
        self.main.submit_in.clicked.connect(self.logIn)
        self.main.send.clicked.connect(self.newTweet)
        self.main.close.clicked.connect(self.close)
        self.main.minimize.clicked.connect(
            lambda: self.main.showMinimized()
        )
        self.main.show()
    
    def Browse(self):
        filepath = QtWidgets.QFileDialog.getOpenFileName(self, "Select account", "",
        "account Files (*.acc )")
        accountFile = filepath[0]
        self.main.account.setText(accountFile)
        with open(accountFile, 'rb') as f:
            prev_key = f.read()
        
        self.account = accounts.add(prev_key)
    
    def singUp(self):
        prev_key = b'0x' + os.urandom(15).hex().encode()
        name = self.main.name.text()
        self.account = accounts.add(prev_key)
        accountFile = 'scripts/Accounts/' + name + '-' + self.account.address + '.acc'
        with open(accountFile, 'wb') as f:
            f.write(prev_key)
        
        try: 
            self.contract.SingUp(name, {'from': self.account})
            self.message.information(
            self, 'Wellcom', 'You successfully' + 
            ' singed up. your account at scripts/Accounts', self.message.Ok, self.message.Ok
            )
        
        except :
            self.message.information(
                self, 'Faild', 'This account' +
                ' already exists', self.message.Ok, self.message.Ok
                )
            

    def logIn(self):
        try: 
            self.contract.logIn({'from': self.account})
            name = self.contract.getName({'from': self.account}).return_value
            self.message.information(
                self, 'Wellcome', f'Wellcome {name}.',
                self.message.Ok, self.message.Ok
                )
            self.main.frame.hide()
            self.main.send.setEnabled(True)
            self.main.tweetCont.setEnabled(True)

        except :
            self.message.information(
            self, 'Faild', 'This account' + ' not singed in.', 
            self.message.Ok, self.message.Ok
            )
        

    def newTweet(self):
        tweetCont = self.main.tweetCont.toPlainText()
        if len(tweetCont) > 280:
            return self.message.information(self, 'Faild',
                'Your tweet is longer then 280 character',
                self.message.Ok, self.message.Ok)
        try:
            tx = self.contract.newTweet(tweetCont, time(), {'from': self.account})
            if tx.status:
                name = self.contract.getName({'from': self.account}).return_value
                date = datetime.now().strftime("%d/%m/%y %H:%M")

                self.main.addTweet(name, date, tweetCont)
        
        except :
            self.message.information(self, 'Faild', 'You are' + 
            ' not singed in.', self.message.Ok, self.message.Ok)
        

    
    def close(self):
        answer = self.message.question(self, 'Quit!', 
        'Are you sure you want to exit?', self.message.Yes | self.message.No,
        self.message.No)
        if answer == self.message.Yes:
            exit()


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    contract = TwitterOnBlockChain.deploy({'from': accounts[0]})
    window = APP(contract)
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()