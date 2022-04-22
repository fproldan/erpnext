# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals

import re
import itertools
from functools import lru_cache
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


@lru_cache
def get_dolarsi_exchange_rate_xml() -> str:
	return requests.get("https://www.dolarsi.com/api/dolarSiInfo.xml").content.decode()


def get_currency_exchange_rate(from_currency: str, to_currency: str) -> float:
	exchange_rate_type = db.get_value(
		"Currency",
		{"currency_name": to_currency if from_currency == "ARS" else from_currency},
		"exchange_rate_type",
	)

	exchange_rate_info = re.search(
		rf"<(?P<casa>casa\d*)>(?P<info>[\S\s]*<nombre>{exchange_rate_type}</nombre>[\S\s]*)</(?P=casa)>",
		get_dolarsi_exchange_rate_xml(),
	).group("info")

	if from_currency == "ARS":
		exchange_rate_value = re.search(r"<venta>(?P<venta>.*)</venta>", exchange_rate_info).group("venta")
		return 1 / float(exchange_rate_value.replace(",", "."))

	exchange_rate_value = re.search(r"<compra>(?P<compra>.*)</compra>", exchange_rate_info).group("compra")
	return float(exchange_rate_value.replace(",", "."))


def set_currency_exchange_rates(*args, **kwargs):
	for currency_pair in tuple(
		itertools.product(
			("ARS",), get_all("Currency", {"exchange_rate_type": ("!=", "")}, pluck="name")
		)
	):
		for from_currency, to_currency in (currency_pair, currency_pair[::-1]):
			currency_exchange = new_doc("Currency Exchange")
			currency_exchange.from_currency = from_currency
			currency_exchange.to_currency = to_currency
			currency_exchange.exchange_rate = get_currency_exchange_rate(from_currency, to_currency)
			try:
				currency_exchange.insert()
			except DuplicateEntryError:
				pass
