import random as r
from datetime import datetime

fechaHoy = datetime.today()

notasDict = []
recuperar = []
'''
ESTRUCTURA DE notasDict

notasDict = [(folio, fecha que ingresa usuario, cliente, total a pagar, {folio: [(servicio, costo)]})]
'''
folios = []
adquiridosFinal ={}
