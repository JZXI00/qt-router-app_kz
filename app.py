import sys
from PyQt5 import QtWidgets, uic
from datetime import datetime
from PyQt5.QtGui import *
import subprocess
import pyautogui
import time
import random

IP_POOL = ["192.168.1.1", "192.168.1.2", "192.168.1.3", "192.168.1.4"]
PORT_POOL = [80, 443, 22, 23, 3389]
ATTACK_VECTORS = ["SQL инъекция", "DDoS шабуыл", "Брутофорс шабуылы", "Зиянды код (Cross-site)", "Зиянды бағдарлама инъекциясы"]

app = QtWidgets.QApplication(sys.argv)
ui_file = "mainwindow.ui"
ui = uic.loadUi(ui_file)

# Конфигурациның көшірмесін файлға сақтаған кездегі жазылатын ақпарат
config_1 = """
# Router Configuration

# Global Settings
hostname Router
domain-name example.com

# Interfaces
interface GigabitEthernet0/0
  ip address 192.168.0.1 255.255.255.0
  no shutdown

interface GigabitEthernet0/1
  ip address 10.0.0.1 255.255.255.0
  no shutdown

# Routing
ip routing

# Static Routes
ip route 0.0.0.0 0.0.0.0 <next_hop_ip_address>

# DHCP Configuration
service dhcp
ip dhcp pool LAN
  network 192.168.1.0 255.255.255.0
  default-router 192.168.0.1
  dns-server 8.8.8.8
  lease 7200

# Security
enable secret <enable_password>
enable password <enable_password>
username admin privilege 15 secret <admin_password>

# Access Control Lists (ACLs)
access-list 1 permit any

# NAT Configuration
ip nat inside source list 1 interface GigabitEthernet0/0 overload

# Logging
logging buffered 4096
logging console

# SSH Configuration
crypto key generate rsa
ip ssh version 2
line vty 0 4
  transport input ssh

# Management
snmp-server community public RO

"""

# Командная строка-да командаларды орындайтын функция
def execute_commands_in_console(commands):
	time.sleep(2)

	for command in commands:
		pyautogui.typewrite(command + '\n')
		time.sleep(1)

# Басты беттегі "Тексеру" түймесін басқан кездегі орындалатын функция
def check_click():
	subprocess.Popen(['start', 'cmd'], shell=True)

	# Роутермен байланыс болмағандықтан барлық өрістерді белгісіз деп қояды
	commands = [
		'ipconfig',
		'ping ' + ui.hostname_2.text(),
	]
	execute_commands_in_console(commands)

	ui.status.setText("Байланыс жоқ")
	ui.dhcp_active.setText("Жоқ")
	ui.dns_active.setText("Жоқ")
	ui.ntp_active.setText("Жоқ")

	ui.status.setStyleSheet("color: red;")
	ui.dhcp_active.setStyleSheet("color: red;")
	ui.dns_active.setStyleSheet("color: red;")
	ui.ntp_active.setStyleSheet("color: red;")
	time.sleep(2)
	pyautogui.hotkey('alt', 'f4')

# Желінің баптаулары бетіндегі "Қосып өшіру" түймесін басқан кездегі орындалатын функция
def reboot():
	subprocess.Popen(['start', 'cmd'], shell=True)
	# Роутермен байланыс болмағандықтан қосылу сәтсіз деген хабарлама шығарады
	commands = [
		'ipconfig',
		'telnet ' + ui.hostname_2.text(),
	]
	execute_commands_in_console(commands)

	time.sleep(2)
	pyautogui.hotkey('alt', 'f4')
	QtWidgets.QMessageBox.information(ui, "Сәтсіз", "Роутерға қосылу сәтсіз!")

# Басты беттегі "Қосылу" түймесін басқан кездегі орындалатын функция
def connect_click():
	ui.plainTextEdit.setPlainText(ui.plainTextEdit.toPlainText() + "\nБайланыс сәтсіз")

# Желіні сканерлеу бетіндегі "Іске қосу" түймесін басқан кездегі орындалатын функция 
# Өтірік желіні сканерлеу жасайды, ақпаратты IP_POOL, PORT_POOL, ATTACK_VECTORS айнымалыларын кездейсоқ түрде алады
def nmap():
	for i in range(10):
		current_time = datetime.now()
		formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

		ip_address = random.choice(IP_POOL)
		port = random.choice(PORT_POOL)
		attack_vector = random.choice(ATTACK_VECTORS)
		severity = random.randint(1, 5)
		delay = random.uniform(0.5, 2)
		time.sleep(delay)

		log = f"[{formatted_time}] - {attack_vector} - [{ip_address}:{port}] - Әсері {severity}"

		ui.textEdit.append(log)

# MAC фильтрлеу бетіндегі "+" (Рұқсат етілген кестеге жаңа адрес қосу) түймесін басқан кездегі орындалатын функция 
def add_mac_1():
	mac = ui.dvc_mac1.text()
	name = ui.dvc_name1.text()

	if mac.strip() and name.strip():
		row_text = '[' + name + '] - ' + mac

		current_row = ui.table1.rowCount()
		ui.table1.insertRow(current_row)

		item = QtWidgets.QTableWidgetItem(row_text)

		ui.table1.setItem(current_row, 1, item)

		ui.dvc_mac1.clear()
		ui.dvc_name1.clear()

# MAC фильтрлеу бетіндегі "+" (Бұғатталған құрылғылардың кестесіне жаңа адрес қосу) түймесін басқан кездегі орындалатын функция 
def add_mac_2():
	mac = ui.dvc_mac2.text()
	name = ui.dvc_name2.text()

	if mac.strip() and name.strip():
		row_text = '[' + name + '] - ' + mac

		current_row = ui.table2.rowCount()
		ui.table2.insertRow(current_row)

		item = QtWidgets.QTableWidgetItem(row_text)

		ui.table2.setItem(current_row, 1, item)

		ui.dvc_mac2.clear()
		ui.dvc_name2.clear()

# Желінің баптаулары бетіндегі конфигурацияны "Сақтау" түймесін басқан кездегі орындалатын функция 
def save_config_to_file():
	# Файлдың атын өрістен алады
	if not ui.backup_name_2.text():
		QtWidgets.QMessageBox.information(ui, "Сәтсіз", "Конфигурация атауын толтырыңыз!")
	else:
		with open(ui.backup_name_2.text(), 'w') as file:
			file.write(config_1)
		QtWidgets.QMessageBox.information(ui, "Сәтті", "Конфигурация сәтті сақталды!")

# Желінің баптаулары бетіндегі конфигурацияның атын өшіреді
def erase():
	ui.backup_name_2.setText('')

# Желінің баптаулары бетіндегі өтірік құпиясөзді ауыстыру функциясы
def change_pass():
	if not ui.new_pass.text() and not ui.old_pass.text() and not ui.rep_new_pass.text() :
		QtWidgets.QMessageBox.information(ui, "Сәтсіз", "Ақпаратты енгізіңіз!")
	else:
		QtWidgets.QMessageBox.information(ui, "Сәтсіз", "Роутерға қосылу сәтсіз!")


current_datetime = datetime.now()

current_date_str = current_datetime.strftime("%d-%m-%Y")
current_time_str = current_datetime.strftime("%H:%M:%S")

ui.date.setText(current_date_str)
ui.time_2.setText(current_time_str)
ui.check_btn.clicked.connect(check_click)
ui.connect_btn.clicked.connect(connect_click)
ui.backup_button_2.clicked.connect(save_config_to_file)
ui.pushButton_8.clicked.connect(erase)
ui.add_mac1.clicked.connect(add_mac_1)
ui.add_mac2.clicked.connect(add_mac_2)
ui.pushButton_5.clicked.connect(nmap)
ui.reboot_button_2.clicked.connect(reboot)
ui.change_pass_button.clicked.connect(change_pass)
ui.show()

sys.exit(app.exec_())
