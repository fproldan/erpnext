# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals

from typing import Optional

import requests
from frappe import _, new_doc, throw
from frappe.model.document import Document
from frappe.utils import cint, formatdate, get_datetime_str, nowdate


class CurrencyExchange(Document):
	def autoname(self):
		purpose = ""
		if not self.date:
			self.date = nowdate()

		# If both selling and buying enabled
		purpose = "Selling-Buying"
		if cint(self.for_buying)==0 and cint(self.for_selling)==1:
			purpose = "Selling"
		if cint(self.for_buying)==1 and cint(self.for_selling)==0:
			purpose = "Buying"

		self.name = '{0}-{1}-{2}{3}'.format(formatdate(get_datetime_str(self.date), "yyyy-MM-dd"),
			self.from_currency, self.to_currency, ("-" + purpose) if purpose else "")

	def validate(self):
		self.validate_value("exchange_rate", ">", 0)

		if self.from_currency == self.to_currency:
			throw(_("From Currency and To Currency cannot be same"))

		if not cint(self.for_buying) and not cint(self.for_selling):
			throw(_("Currency Exchange must be applicable for Buying or for Selling."))


def get_currency_exchange_rate(from_currency: str, to_currency: str) -> Optional[float]:
	if from_currency == "ARS" and to_currency == "USD":
		for data in requests.get("https://www.dolarsi.com/api/api.php?type=valoresprincipales").json():
			if data["casa"]["nombre"] == "Dolar Oficial":
				return float(data["casa"]["venta"].replace(",", "."))
	if from_currency == "USD" and to_currency == "ARS":
		for data in requests.get("https://www.dolarsi.com/api/api.php?type=valoresprincipales").json():
			if data["casa"]["nombre"] == "Dolar Oficial":
				return 1 / float(data["casa"]["compra"].replace(",", "."))
	return None


def set_currency_exchange_rates(*args, **kwargs):
	for from_currency, to_currency in (
		("ARS", "USD"),
		("USD", "ARS"),
	):
		currency_exchange = new_doc("Currency Exchange")
		currency_exchange.from_currency = from_currency
		currency_exchange.to_currency = to_currency
		currency_exchange.exchange_rate = get_currency_exchange_rate(from_currency, to_currency)
		currency_exchange.insert()
