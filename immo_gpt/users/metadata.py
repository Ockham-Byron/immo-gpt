from dataclasses import dataclass
from django.utils.translation import gettext as _

@dataclass
class ProductMetadata(object):
    """
    Metadata for a Stripe product.
    """
    stripe_id: str
    name: str
    description: str = ''
    is_default: bool = False


Monthly = ProductMetadata(
    stripe_id='prod_PNzYkUaAltgZST',
    name=_('Monthly'),
    description=_("Elevate your real estate game with our Monthly Subscription! Enjoy unlimited access to PropertyPad's AI-driven features for a seamless and productive monthly journey."),
    is_default=True,
)

Yearly = ProductMetadata(
    stripe_id='prod_PNzaOFUTUeHBP3',
    name=_('Yearly'),
    description=_('Commit to success with our Annual Subscription! Dive deep into the world of polished property descriptions and reports for an entire year, ensuring you stay ahead in the competitive real estate landscape.'),
    is_default=False,
)

LifeTime = ProductMetadata(
    stripe_id='prod_PNzbHimPnHwsKE',
    name=_('LifeTime'),
    description=_("Embrace a lifetime of excellence with our Lifetime Subscription! Gain perpetual access to PropertyPad's cutting-edge AI, securing your place at the forefront of real estate innovation forever."),
    is_default=False,
)