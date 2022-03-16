# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals

import itertools
from typing import Optional

import requests
from frappe import _, db, get_all, new_doc, throw
from frappe.exceptions import DuplicateEntryError
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
	exchange_rate_type = db.get_value(
		"Currency",
		{"currency_name": to_currency if from_currency == "ARS" else from_currency},
		"exchange_rate_type",
	)
	return next(
		(
			1 / float(data["casa"]["venta"].replace(",", "."))
			if from_currency == "ARS"
			else float(data["casa"]["compra"].replace(",", "."))
			for data in requests.get("https://www.dolarsi.com/api/api.php?type=valoresprincipales").json()
			if data["casa"]["nombre"] == exchange_rate_type
		),
		None,
	)


def set_currency_exchange_rates(*args, **kwargs):
	for currency_pair in tuple(
		itertools.product(
			("ARS",), get_all("Currency", {"exchange_rate_type": ("!=", "")}, pluck="name")
		)
	):
		for from_currency, to_currency in (currency_pair, currency_pair[::-1]):
			exchange_rate = get_currency_exchange_rate(from_currency, to_currency)
			if exchange_rate is None:
				continue
			currency_exchange = new_doc("Currency Exchange")
			currency_exchange.from_currency = from_currency
			currency_exchange.to_currency = to_currency
			currency_exchange.exchange_rate = exchange_rate
			try:
				currency_exchange.insert()
			except DuplicateEntryError:
				pass
