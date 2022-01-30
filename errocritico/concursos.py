import os
from flask import (
Blueprint, request
)
from bs4 import BeautifulSoup as BS
import requests
import hashlib
import smtplib, ssl


bp = Blueprint('concursos', __name__)


@bp.route('/concursos', methods=('GET', 'POST'))
def concursos():
	if request.method == 'GET':
		source = ('https://www.pciconcursos.com.br/cargos/ambiente')

		site = requests.post(source).content

		soup = BS(site, 'html.parser')

		lista = str(soup.find_all(class_="noticia_desc"))

		hash1 = hashlib.md5(lista.encode('utf-8'))

		hasher = hashlib.md5()

		with open ('concursos.txt', 'rb') as f:
			buf = f.read()
			hasher.update(buf)


		if hash1.hexdigest() != hasher.hexdigest():
			f = open("concursos.txt", "w")
			f.write(lista)
			f.close()


			port = 587  # For starttls
			smtp_server = "smtp.gmail.com"
			sender_email = "video181881@gmail.com"
			receiver_email = "lucas-camargo@outlook.com"
			password = "pwgsehtzfmyftwdu"
			message = """\
Subject: CONCURSO NOVO


Tem concurso novo pra ver hoje."""

			context = ssl.create_default_context()
			with smtplib.SMTP(smtp_server, port) as server:
			    server.ehlo()  # Can be omitted
			    server.starttls(context=context)
			    server.ehlo()  # Can be omitted
			    server.login(sender_email, password)
			    server.sendmail(sender_email, receiver_email, message)
		else:
			port = 587  # For starttls
			smtp_server = "smtp.gmail.com"
			sender_email = "video181881@gmail.com"
			receiver_email = "lucas-camargo@outlook.com"
			password = "pwgsehtzfmyftwdu"
			message = """\
Subject: Sem concurso


Nao tem concurso novo pra ver hoje."""

			context = ssl.create_default_context()
			with smtplib.SMTP(smtp_server, port) as server:
			    server.ehlo()  # Can be omitted
			    server.starttls(context=context)
			    server.ehlo()  # Can be omitted
			    server.login(sender_email, password)
			    server.sendmail(sender_email, receiver_email, message)
	return("Sucesso")