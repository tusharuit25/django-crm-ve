import pytest
from finacc.models.company import Company
from crm.models.lead import Lead
from crm.services.converters import convert_lead

@pytest.mark.django_db
def test_lead_convert_creates_contact_opportunity():
    c = Company.objects.create(name="ACME")
    l = Lead.objects.create(company=c, name="Foo")
    contact, opp = convert_lead(c, l)
    assert contact.id and opp.id and l.is_converted