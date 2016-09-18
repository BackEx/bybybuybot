from models.awa import Offer

for offer in Offer.objects:
    print offer.get_id(),