import newspaper
import mongo
import time
from datetime import datetime

diarios = {"LaNacion": "https://www.lanacion.com.ar/", "LID": "https://www.laizquierdadiario.com/", "Clarin": "https://www.clarin.com/", "PO": "https://www.prensaobrera.com", "P12": "https://www.pagina12.com.ar/", "Ambito": "https://www.ambito.com", "Cronista": "https://www.cronista.com", "Cronica": "https://www.cronica.com.ar", "Infobae": "https://www.infobae.com", "Tiempo": "https://www.tiempoar.com.ar"}

def getAttributes(article):
	return {
	        "url": article.url,
	        "title": article.title,
	        "text": article.text,
	        "authors": article.authors,
	        "publish_date": article.publish_date,
	        # "imgs": article.imgs
	        }

while True:
	memoize = False
	for nombre in diarios:
		print("Descargando noticias de {}".format(nombre))
		diario = newspaper.build(diarios[nombre], memoize_articles=memoize)

		print("Obtuvimos {} articulos nuevos".format(len(diario.articles)))

		mongo.setup(nombre)
		guardados = 0
		for article in diario.articles:
			try:
				article.download()
				article.parse()
				print(dir(article))
				if not mongo.check_if_exists({"text": article.text}, nombre):
					print("lala")
					attributes = getAttributes(article)
					if attributes.publish_date == None or attributes.publish_date == "":
						attributes.publish_date = datetime.now()
					print("HERE")
					mongo.store(attributes, nombre)
					guardados += 1
			except Exception as e:
				print(e)
				continue
		print("Guardados {} articulos de {}".format(guardados, nombre))

	memoize = True
	print("Me duermo por 2 horas")
	time.sleep(2 * 60 * 60)
