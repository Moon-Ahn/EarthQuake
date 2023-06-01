import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox)
import subprocess
from threading import Thread


class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login Form')
        self.resize(400, 100)

        layout = QGridLayout()


        label_ip = QLabel('<font size="4"> User IP </font>')
        self.lineEdit_ip = QLineEdit()
        self.lineEdit_ip.setPlaceholderText('Please enter your ip')
        layout.addWidget(label_ip, 1, 0)
        layout.addWidget(self.lineEdit_ip, 1, 1)

        label_name = QLabel('<font size="4"> UserName </font>')
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText('Please enter your username')
        layout.addWidget(label_name, 2, 0)
        layout.addWidget(self.lineEdit_username, 2, 1)

        label_password = QLabel('<font size="4"> Password </font>')
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.lineEdit_password.setPlaceholderText('Please enter your password')
        layout.addWidget(label_password, 3, 0)
        layout.addWidget(self.lineEdit_password, 3, 1)

        button_login = QPushButton('Login')
        button_login.clicked.connect(self.check_password)
        layout.addWidget(button_login, 4, 0, 1, 2)
        layout.setRowMinimumHeight(4, 40)

        self.setLayout(layout)

    def check_password(self):
        msg = QMessageBox()

        #if self.lineEdit_username.text() == 'Usernmae' and self.lineEdit_password.text() == '000':
        msg.setText('Login')
        msg.exec_()
        app.quit()
        execute_python ="python Earth2.py "+self.lineEdit_ip.text()+" "+self.lineEdit_username.text()+" "+self.lineEdit_password.text()
        execute_C ="CallFwCgi.exe "+self.lineEdit_ip.text()+" "+self.lineEdit_username.text()+" "+self.lineEdit_password.text()
        #print(execute_C)
        #print(execute_python)
        subprocess.Popen(execute_C, shell = True)
        subprocess.Popen(execute_python, shell = True)
        #os.system("Earth_UI_ChangeValue.exe 192.168.0.250 root root")
        #else:
            # msg.setText('Incorrect Password')
            # msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = LoginForm()
    form.show()

    sys.exit(app.exec_())