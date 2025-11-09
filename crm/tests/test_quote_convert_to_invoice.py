import pytest
from decimal import Decimal
from finacc.models.company import Company
from sales.models.party import Customer
from sales.models.item import UoM, Item
from sales.models.doc import SalesInvoice
from crm.models.contact import Contact
from crm.models.quotation import Quotation, QuotationLine
from crm.services.converters import confirm_quote_to_invoice

@pytest.mark.django_db
def test_quote_to_invoice():
    c = Company.objects.create(name="ACME")
    ct = Contact.objects.create(company=c, name="Foo")
    # minimal sales deps
    u = UoM.objects.create(code="pcs", name="Pieces")
    it = Item.objects.create(company=c, sku="PRD-1", name="Widget", type="product", uom=u, sales_price=1000)
    Customer.objects.create(company=c, name="Foo")

    q = Quotation.objects.create(company=c, contact=ct, number="Q-1", date="2025-11-09", currency="INR")
    QuotationLine.objects.create(quotation=q, item=it, qty=1, rate=Decimal("1000.00"))

    inv = confirm_quote_to_invoice(q)
    assert inv.id and q.is_confirmed