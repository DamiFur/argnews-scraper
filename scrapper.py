import newspaper
import mongo
import time

diarios = {"LaNacion": "https://www.lanacion.com.ar/", "LID": "https://www.laizquierdadiario.com/", "Clarin": "https://www.clarin.com/", "PO": "https://www.prensaobrera.com", "P12": "https://www.pagina12.com.ar/"}

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
		for article in diario.articles:
			guardados = 0
			article.download()
			article.parse()
			if not mongo.check_if_exists({"text": article.text}, nombre):
				mongo.store(getAttributes(article), nombre)
				guardados += 1
		print("Guardados {} articulos de {}".format(guardados, nombre))

	memoize = True
	print("Me duermo por 2 horas")
	time.sleep(2 * 60 * 60)
