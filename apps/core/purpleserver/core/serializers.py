from enum import Enum
from drf_yasg import openapi
from rest_framework.serializers import (
    CharField, FloatField,
    BooleanField, IntegerField, ListField,
    ChoiceField, DictField, URLField
)

from purplship.core.units import (
    Country, WeightUnit, DimensionUnit,
    PackagingUnit, PaymentType, Currency,
    CustomsContentType, Incoterm,
    LabelType
)
from purpleserver.providers.models import MODELS
from purpleserver.serializers import Serializer, allow_model_id
from purpleserver.core.validators import (
    AugmentedAddressSerializer,
    PresetSerializer,
    valid_time_format,
    valid_date_format,
)


class ShipmentStatus(Enum):
    created = 'created'
    purchased = 'purchased'
    cancelled = 'cancelled'
    shipped = 'shipped'
    transit = 'in-transit'
    delivered = 'delivered'


class TrackerStatus(Enum):
    pending = 'pending'
    in_transit = 'in-transit'
    incident = 'incident'
    delivered = 'delivered'


SHIPMENT_STATUS = [(c.value, c.value) for c in list(ShipmentStatus)]
TRACKER_STATUS = [(c.value, c.value) for c in list(TrackerStatus)]
CUSTOMS_CONTENT_TYPE = [(c.name, c.name) for c in list(CustomsContentType)]
INCOTERMS = [(c.name, c.name) for c in list(Incoterm)]
CARRIERS = [(k, k) for k in sorted(MODELS.keys())]
COUNTRIES = [(c.name, c.name) for c in list(Country)]
CURRENCIES = [(c.name, c.name) for c in list(Currency)]
WEIGHT_UNIT = [(c.name, c.name) for c in list(WeightUnit)]
DIMENSION_UNIT = [(c.name, c.name) for c in list(DimensionUnit)]
PACKAGING_UNIT = [(c.name, c.name) for c in list(PackagingUnit)]
PAYMENT_TYPES = [(c.name, c.name) for c in list(PaymentType)]
LABEL_TYPES = [(c.name, c.name) for c in list(LabelType)]


class StringListField(ListField):
    child = CharField()


class PlainDictField(DictField):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "additional_properties": True,
        }


class FlagField(BooleanField):
    pass


class FlagsSerializer(Serializer):
    def __init__(self, *args, **kwargs):
        data = kwargs.get('data', {})
        self.flags = [
            (label, label in data)
            for label, field in self.fields.items()
            if isinstance(field, FlagField)
        ]

        super().__init__(*args, **kwargs)

    def validate(self, data):
        validated = super().validate(data)
        for flag, specified in self.flags:
            if specified and validated[flag] is None:
                validated.update({flag: True})

        return validated


class EntitySerializer(Serializer):
    id = CharField(required=False, help_text="A unique identifier")


class CarrierSettings(Serializer):
    id = CharField(required=True, help_text="A unique address identifier")
    carrier_name = ChoiceField(choices=CARRIERS, required=True, help_text="Indicates a carrier (type)")
    carrier_id = CharField(required=True, help_text="Indicates a specific carrier configuration name.")
    test = BooleanField(required=True, help_text="""
    The test flag indicates whether to use a carrier configured for test.
    """)
    active = BooleanField(required=True, help_text="""
    The active flag indicates whether the carrier account is active or not.
    """)


class TestFilters(FlagsSerializer):
    test = FlagField(
        required=False, allow_null=True, default=False,
        help_text="The test flag indicates whether to use a carrier configured for test.")


class Message(Serializer):

    carrier_name = CharField(required=False, help_text="The targeted carrier")
    carrier_id = CharField(required=False, help_text="The targeted carrier name (unique identifier)")
    message = CharField(required=False, help_text="The error or warning message")
    code = CharField(required=False, help_text="The message code")
    details = DictField(required=False, help_text="any additional details")


class AddressValidation(Serializer):
    success = BooleanField(help_text="True if the address is valid")
    meta = PlainDictField(required=False, allow_null=True, help_text="validation service details")


class AddressData(AugmentedAddressSerializer):

    postal_code = CharField(required=False, allow_blank=True, allow_null=True, help_text="""
    The address postal code

    **(required for shipment purchase)**
    """)
    city = CharField(required=False, allow_blank=True, allow_null=True, help_text="""
    The address city.

    **(required for shipment purchase)**
    """)
    federal_tax_id = CharField(required=False, allow_blank=True, allow_null=True, help_text="The party frederal tax id")
    state_tax_id = CharField(required=False, allow_blank=True, allow_null=True, help_text="The party state id")
    person_name = CharField(required=False, allow_blank=True, allow_null=True, help_text="""
    attention to

    **(required for shipment purchase)**
    """)
    company_name = CharField(required=False, allow_blank=True, allow_null=True, help_text="The company name if the party is a company")
    country_code = ChoiceField(required=True, choices=COUNTRIES, help_text="The address country code")
    email = CharField(required=False, allow_blank=True, allow_null=True, help_text="The party email")
    phone_number = CharField(required=False, allow_blank=True, allow_null=True, help_text="The party phone number.")

    state_code = CharField(required=False, allow_blank=True, allow_null=True, help_text="The address state code")
    suburb = CharField(required=False, allow_blank=True, allow_null=True, help_text="The address suburb if known")
    residential = BooleanField(
        allow_null=True, required=False, default=False,
        help_text="Indicate if the address is residential or commercial (enterprise)"
    )

    address_line1 = CharField(required=False, allow_blank=True, allow_null=True, help_text="""
    The address line with street number <br/>
    **(required for shipment purchase)**
    """)
    address_line2 = CharField(required=False, allow_blank=True, allow_null=True, help_text="The address line with suite number")
    validate_location = BooleanField(required=False, allow_null=True, default=False, help_text="Indicate if the address should be validated")


class Address(EntitySerializer, AddressData):
    validation = AddressValidation(required=False, allow_null=True, help_text="Specify address validation result")


class CommodityData(Serializer):

    weight = FloatField(required=True, help_text="The commodity's weight")
    weight_unit = ChoiceField(required=True, choices=WEIGHT_UNIT, help_text="The commodity's weight unit")
    description = CharField(required=False, allow_blank=True, allow_null=True, help_text="A description of the commodity")
    quantity = IntegerField(required=False, allow_null=True, help_text="The commodity's quantity (number or item)")
    sku = CharField(required=False, allow_blank=True, allow_null=True, help_text="The commodity's sku number")
    value_amount = FloatField(required=False, allow_null=True, help_text="The monetary value of the commodity")
    value_currency = CharField(required=False, allow_blank=True, allow_null=True, help_text="The currency of the commodity value amount")
    origin_country = CharField(required=False, allow_blank=True, allow_null=True, help_text="The origin or manufacture country")


class Commodity(EntitySerializer, CommodityData):
    pass


class ParcelData(PresetSerializer):

    weight = FloatField(required=True, help_text="The parcel's weight")
    width = FloatField(required=False, allow_null=True, help_text="The parcel's width")
    height = FloatField(required=False, allow_null=True, help_text="The parcel's height")
    length = FloatField(required=False, allow_null=True, help_text="The parcel's length")
    packaging_type = CharField(required=False, allow_blank=True, allow_null=True, help_text=f"""
    The parcel's packaging type.

    **Note that the packaging is optional when using a package preset**

    values: <br/>- {'<br/>- '.join([f'**{pkg}**' for pkg, _ in PACKAGING_UNIT])}

    For specific carriers packaging type, please consult [the reference](#operation/references).
    """)
    package_preset = CharField(required=False, allow_blank=True, allow_null=True, help_text="""
    The parcel's package preset.

    For specific carriers package preset, please consult [the reference](#operation/references).
    """)
    description = CharField(required=False, allow_blank=True, allow_null=True, help_text="The parcel's description")
    content = CharField(required=False, allow_blank=True, allow_null=True, help_text="The parcel's content description")
    is_document = BooleanField(required=False, allow_null=True, default=False, help_text="Indicates if the parcel is composed of documents only")
    weight_unit = ChoiceField(required=True, choices=WEIGHT_UNIT, help_text="The parcel's weight unit")
    dimension_unit = ChoiceField(required=False, allow_blank=True, allow_null=True, choices=DIMENSION_UNIT, help_text="The parcel's dimension unit")


class Parcel(EntitySerializer, ParcelData):
    pass


class Payment(Serializer):

    paid_by = ChoiceField(required=False, choices=PAYMENT_TYPES, default=PAYMENT_TYPES[0][0], help_text="The payor type")
    currency = ChoiceField(required=False, choices=CURRENCIES, help_text="The payment amount currency")
    account_number = CharField(required=False, allow_blank=True, allow_null=True, help_text="The payor account number")


class Duty(Serializer):

    paid_by = ChoiceField(required=False, choices=PAYMENT_TYPES, allow_blank=True, allow_null=True, help_text="The duty payer")
    currency = ChoiceField(required=False, choices=CURRENCIES, allow_blank=True, allow_null=True, help_text="The declared value currency")
    declared_value = FloatField(required=False, allow_null=True, help_text="The package declared value")
    account_number = CharField(required=False, allow_blank=True, allow_null=True, help_text="The duty payment account number")
    bill_to = Address(required=False, allow_null=True, help_text="The duty billing address")


@allow_model_id([
    ('commodities', 'purpleserver.manager.models.Commodity'),
])
class CustomsData(Serializer):

    aes = CharField(required=False, allow_blank=True, allow_null=True)
    eel_pfc = CharField(required=False, allow_blank=True, allow_null=True)
    content_type = ChoiceField(required=False, choices=CUSTOMS_CONTENT_TYPE, allow_blank=True, allow_null=True)
    content_description = CharField(required=False, allow_blank=True, allow_null=True)
    incoterm = ChoiceField(required=False, allow_null=True, choices=INCOTERMS, help_text="The customs 'term of trade' also known as 'incoterm'")
    commodities = Commodity(many=True, required=False, allow_null=True, help_text="The parcel content items")
    duty = Duty(required=False, allow_null=True, help_text="""
    The payment details.<br/>
    Note that this is required for a Dutiable parcel shipped internationally.
    """)
    invoice = CharField(required=False, allow_null=True, allow_blank=True, help_text="The invoice reference number")
    invoice_date = CharField(required=False, allow_null=True, allow_blank=True, validators=[valid_date_format], help_text="The invoice date")
    commercial_invoice = BooleanField(required=False, allow_null=True, help_text="Indicates if the shipment is commercial")
    certify = BooleanField(required=False, allow_null=True, help_text="Indicate that signer certified confirmed all")
    signer = CharField(required=False, allow_blank=True, allow_null=True)
    certificate_number = CharField(required=False, allow_blank=True, allow_null=True)
    options = PlainDictField(required=False, allow_null=True)


class Customs(EntitySerializer, CustomsData):
    pass


class COD(Serializer):

    amount = FloatField(required=True, help_text="The amount to collect on delivery")


class Notification(Serializer):

    email = CharField(required=False, allow_blank=True, allow_null=True, help_text="""
    The alternative notification email.

    Note that by default the recipient email will be used.
    """)
    locale = CharField(required=False, allow_blank=True, allow_null=True, default='en')


class Insurance(Serializer):

    amount = FloatField(required=True, allow_null=True, help_text="The insurance coverage amount.")


class Charge(Serializer):

    name = CharField(required=False, allow_blank=True, allow_null=True, help_text="The charge description")
    amount = FloatField(required=False, allow_null=True, help_text="The charge monetary value")
    currency = CharField(required=False, allow_blank=True, allow_null=True, help_text="The charge amount currency")


@allow_model_id([
    ('shipper', 'purpleserver.manager.models.Address'),
    ('recipient', 'purpleserver.manager.models.Address'),
    ('parcels', 'purpleserver.manager.models.Parcel')
])
class RateRequest(Serializer):
    shipper = AddressData(required=True, help_text="""
    The address of the party

    Origin address (ship from) for the **shipper**<br/>
    Destination address (ship to) for the **recipient**
    """)
    recipient = AddressData(required=True, help_text="""
    The address of the party

    Origin address (ship from) for the **shipper**<br/>
    Destination address (ship to) for the **recipient**
    """)
    parcels = ParcelData(many=True, required=True, help_text="The shipment's parcels")

    services = StringListField(required=False, allow_null=True, help_text="""
    The requested carrier service for the shipment.<br/>
    Please consult [the reference](#operation/references) for specific carriers services.

    Note that this is a list because on a Multi-carrier rate request you could specify a service per carrier.
    """)
    options = PlainDictField(required=False, allow_null=True, help_text=f"""
    The options available for the shipment.

    Please consult [the reference](#operation/references) for additional specific carriers options.
    """)
    reference = CharField(required=False, allow_blank=True, allow_null=True, help_text="The shipment reference")
    carrier_ids = StringListField(required=False, allow_null=True, help_text="""
    The list of configured carriers you wish to get rates from.
    """)


class TrackingRequest(Serializer):

    tracking_numbers = StringListField(required=True, help_text="a list of tracking numbers to fetch.")
    language_code = CharField(required=False, allow_blank=True, allow_null=True, default="en", help_text="The tracking details language code")
    level_of_details = CharField(required=False, allow_blank=True, allow_null=True, help_text="The level of event details.")

@allow_model_id([
    ('address', 'purpleserver.manager.models.Address'),
    ('parcels', 'purpleserver.manager.models.Parcel')
])
class PickupRequest(Serializer):

    pickup_date = CharField(required=True, validators=[valid_date_format], help_text="""
    The expected pickup date

    Date Format: `YYYY-MM-DD`
    """)
    address = AddressData(required=True, help_text="The pickup address")
    parcels = ParcelData(required=True, many=True, allow_null=True, help_text="The shipment parcels to pickup.")
    ready_time = CharField(required=True, validators=[valid_time_format], help_text="""
    The ready time for pickup.

    Time Format: `HH:MM`
    """)
    closing_time = CharField(required=True, validators=[valid_time_format], help_text="""
    The closing or late time of the pickup

    Time Format: `HH:MM`
    """)
    instruction = CharField(required=False, allow_blank=True, allow_null=True, help_text="""
    The pickup instruction.

    eg: Handle with care.
    """)
    package_location = CharField(required=False, allow_blank=True, allow_null=True, help_text="""
    The package(s) location.

    eg: Behind the entrance door.
    """)
    options = PlainDictField(required=False, allow_null=True, help_text="Advanced carrier specific pickup options")

@allow_model_id([
    ('address', 'purpleserver.manager.models.Address'),
    ('parcels', 'purpleserver.manager.models.Parcel')
])
class PickupUpdateRequest(Serializer):
    pickup_date = CharField(required=True, help_text="""
    The expected pickup date

    Date Format: `YYYY-MM-DD`
    """)
    address = Address(required=True, help_text="The pickup address")
    parcels = Parcel(required=True, many=True, allow_null=True, help_text="The shipment parcels to pickup.")
    confirmation_number = CharField(required=True, help_text="pickup identification number")
    ready_time = CharField(required=True, validators=[valid_time_format], help_text="""
    The ready time for pickup.

    Time Format: `HH:MM`
    """)
    closing_time = CharField(required=True, validators=[valid_time_format], help_text="""
    The closing or late time of the pickup

    Time Format: `HH:MM`
    """)
    instruction = CharField(required=False, allow_blank=True, allow_null=True, help_text="""
    The pickup instruction.

    eg: Handle with care.
    """)
    package_location = CharField(required=False, allow_blank=True, allow_null=True, help_text="""
    The package(s) location.

    eg: Behind the entrance door.
    """)
    options = PlainDictField(required=False, allow_null=True, help_text="Advanced carrier specific pickup options")


class PickupDetails(Serializer):

    id = CharField(required=False, help_text="A unique pickup identifier")
    carrier_name = CharField(required=True, help_text="The pickup carrier")
    carrier_id = CharField(required=True, help_text="The pickup carrier configured name")
    confirmation_number = CharField(required=True, help_text="The pickup confirmation identifier")
    pickup_date = CharField(required=False, allow_null=True, help_text="The pickup date")
    pickup_charge = Charge(required=False, allow_null=True, help_text="The pickup cost details")
    ready_time = CharField(required=False, allow_null=True, help_text="The pickup expected ready time")
    closing_time = CharField(required=False, allow_null=True, help_text="The pickup expected closing or late time")


class Pickup(PickupDetails, PickupRequest):
    address = Address(required=True, help_text="The pickup address")
    parcels = Parcel(required=True, many=True, allow_null=True, help_text="The shipment parcels to pickup.")
    test_mode = BooleanField(required=True, help_text="Specified whether it was created with a carrier in test mode")

@allow_model_id([
    ('address', 'purpleserver.manager.models.Address'),
])
class PickupCancelRequest(Serializer):
    confirmation_number = CharField(required=True, help_text="The pickup confirmation identifier")
    address = AddressData(required=False, help_text="The pickup address")
    pickup_date = CharField(required=False, allow_null=True, validators=[valid_date_format], help_text="""
    The pickup date

    Date Format: `YYYY-MM-DD`
    """)
    reason = CharField(required=False, help_text="The reason of the pickup cancellation")


class TrackingEvent(Serializer):

    date = CharField(required=False, help_text="The tracking event's date")
    description = CharField(required=False, help_text="The tracking event's description")
    location = CharField(required=False, help_text="The tracking event's location")
    code = CharField(required=False, allow_blank=True, allow_null=True, help_text="The tracking event's code")
    time = CharField(required=False, allow_blank=True, allow_null=True, help_text="The tracking event's time")


class Rate(EntitySerializer):

    carrier_name = CharField(required=True, help_text="The rate's carrier")
    carrier_id = CharField(required=True, help_text="The targeted carrier's name (unique identifier)")
    currency = CharField(required=True, help_text="The rate monetary values currency code")
    service = CharField(required=False, allow_blank=True, allow_null=True, help_text="The carrier's rate (quote) service")
    discount = FloatField(required=False, allow_null=True, help_text="The monetary amount of the discount on the rate")
    base_charge = FloatField(default=0.0, help_text="""
    The rate's monetary amount of the base charge.<br/>
    This is the net amount of the rate before additional charges
    """)
    total_charge = FloatField(default=0.0, help_text="""
    The rate's monetary amount of the total charge.<br/>
    This is the gross amount of the rate after adding the additional charges
    """)
    duties_and_taxes = FloatField(required=False, allow_null=True, help_text="The monetary amount of the duties and taxes if applied")
    transit_days = IntegerField(required=False, allow_null=True, help_text="The estimated delivery transit days")
    extra_charges = Charge(many=True, required=False, default=[], help_text="list of the rate's additional charges")
    meta = PlainDictField(required=False, allow_null=True, help_text="provider specific metadata")

    carrier_ref = CharField(required=False, allow_blank=True, allow_null=True, help_text="The system carrier configuration id")
    test_mode = BooleanField(required=True, help_text="Specified whether it was created with a carrier in test mode")


class TrackingDetails(Serializer):

    carrier_name = CharField(required=True, help_text="The tracking carrier")
    carrier_id = CharField(required=True, help_text="The tracking carrier configured identifier")
    tracking_number = CharField(required=True, help_text="The shipment tracking number")
    events = TrackingEvent(many=True, required=False, allow_null=True, help_text="The tracking details events")
    delivered = BooleanField(required=False, help_text="Specified whether the related shipment was delivered")
    test_mode = BooleanField(required=True, help_text="Specified whether the object was created with a carrier in test mode")
    status = ChoiceField(
        required=False, default=SHIPMENT_STATUS[0][0], choices=SHIPMENT_STATUS, help_text="The current tracking status")


class TrackingStatus(EntitySerializer, TrackingDetails):
    pass


@allow_model_id([
    ('shipper', 'purpleserver.manager.models.Address'),
    ('recipient', 'purpleserver.manager.models.Address'),
    ('parcels', 'purpleserver.manager.models.Parcel'),
    ('customs', 'purpleserver.manager.models.Customs')
])
class ShippingData(Serializer):
    shipper = AddressData(required=True, help_text="""
    The address of the party

    Origin address (ship from) for the **shipper**<br/>
    Destination address (ship to) for the **recipient**
    """)
    recipient = AddressData(required=True, help_text="""
    The address of the party

    Origin address (ship from) for the **shipper**<br/>
    Destination address (ship to) for the **recipient**
    """)
    parcels = ParcelData(many=True, required=True, help_text="The shipment's parcels")
    options = PlainDictField(required=False, allow_null=True, help_text="""
    The options available for the shipment.<br/>
    Please consult [the reference](#operation/references) for additional specific carriers options.
    """)
    payment = Payment(required=False, allow_null=True, help_text="The payment details")
    customs = CustomsData(required=False, allow_null=True, help_text="""
    The customs details.<br/>
    Note that this is required for the shipment of an international Dutiable parcel.
    """)
    reference = CharField(required=False, allow_blank=True, allow_null=True, help_text="The shipment reference")
    label_type = ChoiceField(required=False, choices=LABEL_TYPES, default=LabelType.PDF.name, help_text="The shipment label file type.")


class ShippingRequest(ShippingData):
    selected_rate_id = CharField(required=True, help_text="The shipment selected rate.")
    rates = Rate(many=True, help_text="The list for shipment rates fetched previously")
    payment = Payment(required=True, help_text="The payment details")


class ShipmentData(ShippingData):
    services = StringListField(required=False, allow_null=True, default=[], help_text="""
    The requested carrier service for the shipment.

    Please consult [the reference](#operation/references) for specific carriers services.<br/>
    Note that this is a list because on a Multi-carrier rate request you could specify a service per carrier.
    """)
    carrier_ids = StringListField(required=False, allow_null=True, default=[], help_text="""
    The list of configured carriers you wish to get rates from.

    *Note that the request will be sent to all carriers in nothing is specified*
    """)


class ShipmentContent(Serializer):

    # Process result properties

    status = ChoiceField(
        required=False, default=ShipmentStatus.created.value, choices=SHIPMENT_STATUS, help_text="The current Shipment status")

    carrier_name = CharField(required=False, allow_blank=True, allow_null=True, help_text="The shipment carrier")
    carrier_id = CharField(required=False, allow_blank=True, allow_null=True, help_text="The shipment carrier configured identifier")
    label = CharField(required=False, allow_blank=True, allow_null=True, help_text="The shipment label in base64 string")
    tracking_number = CharField(required=False, allow_blank=True, allow_null=True, help_text="The shipment tracking number")
    shipment_identifier = CharField(required=False, allow_blank=True, allow_null=True, help_text="The shipment carrier system identifier")
    selected_rate = Rate(required=False, allow_null=True, help_text="The shipment selected rate")

    selected_rate_id = CharField(required=False, allow_blank=True, allow_null=True, help_text="The shipment selected rate.")
    rates = Rate(many=True, required=False, default=[], help_text="The list for shipment rates fetched previously")
    tracking_url = URLField(required=False, allow_blank=True, allow_null=True, help_text="The shipment tracking url")
    service = CharField(required=False, allow_blank=True, allow_null=True, help_text="The selected service")

    # Request properties

    shipper = Address(required=True, help_text="""
    The address of the party

    Origin address (ship from) for the **shipper**<br/>
    Destination address (ship to) for the **recipient**
    """)
    recipient = Address(required=True, help_text="""
    The address of the party

    Origin address (ship from) for the **shipper**<br/>
    Destination address (ship to) for the **recipient**
    """)
    parcels = Parcel(many=True, required=True, help_text="The shipment's parcels")

    services = StringListField(required=False, allow_null=True, default=[], help_text="""
    The carriers services requested for the shipment.

    Please consult [the reference](#operation/references) for specific carriers services.<br/>
    Note that this is a list because on a Multi-carrier rate request you could specify a service per carrier.
    """)
    options = PlainDictField(required=False, allow_null=True, help_text="""
    The options available for the shipment.<br/>
    Please consult [the reference](#operation/references) for additional specific carriers options.
    """)

    payment = Payment(required=False, allow_null=True, help_text="The payment details")
    customs = Customs(required=False, allow_null=True, help_text="""
    The customs details.<br/>
    Note that this is required for the shipment of an international Dutiable parcel.
    """)
    reference = CharField(required=False, allow_blank=True, allow_null=True, help_text="The shipment reference")
    label_type = ChoiceField(required=False, choices=LABEL_TYPES, allow_blank=True, allow_null=True, help_text="The shipment label file type.")
    carrier_ids = StringListField(required=False, allow_null=True, default=[], help_text="""
    The list of configured carriers you wish to get rates from.

    *Note that the request will be sent to all carriers in nothing is specified*
    """)
    tracker_id = CharField(required=False, allow_blank=True, allow_null=True, help_text="The attached tracker id")
    created_at = CharField(required=True, help_text="""
    The shipment creation datetime

    Date Format: `YYYY-MM-DD HH:MM:SS.mmmmmmz`
    """)
    test_mode = BooleanField(required=True, help_text="Specified whether it was created with a carrier in test mode")
    meta = PlainDictField(required=False, allow_null=True, help_text="provider specific metadata")
    messages = Message(required=False, many=True, default=[], help_text="The list of note or warning messages")


class Shipment(EntitySerializer, ShipmentContent):
    pass


class ShipmentCancelRequest(Serializer):
    shipment_identifier = CharField(required=True, help_text="The shipment identifier returned during creation")
    service = CharField(required=False, allow_blank=True, allow_null=True, help_text="The selected shipment service")
    options = PlainDictField(required=False, allow_null=True, help_text="Advanced carrier specific cancellation options")


class Operation(Serializer):
    operation = CharField(required=True, help_text="Operation performed")
    success = BooleanField(required=True, help_text="Specify whether the operation was successful")


class OperationConfirmation(Operation):
    carrier_name = CharField(required=True, help_text="The operation carrier")
    carrier_id = CharField(required=True, help_text="The targeted carrier's name (unique identifier)")


class OperationResponse(Serializer):
    messages = Message(required=False, many=True, help_text="The list of note or warning messages")
    confirmation = OperationConfirmation(required=False, help_text="The operation details")


class PickupResponse(Serializer):
    messages = Message(required=False, many=True, help_text="The list of note or warning messages")
    pickup = Pickup(required=False, help_text="The scheduled pickup's summary")


class RateResponse(Serializer):
    messages = Message(required=False, many=True, help_text="The list of note or warning messages")
    rates = Rate(many=True, help_text="The list of returned rates")


class TrackingResponse(Serializer):
    messages = Message(required=False, many=True, help_text="The list of note or warning messages")
    tracking = TrackingStatus(required=False, help_text="The tracking details retrieved")


class ErrorResponse(Serializer):
    messages = Message(many=True, required=False, help_text="The list of error messages")
