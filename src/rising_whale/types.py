from dataclasses import dataclass

from dataclasses_avroschema import AvroModel


@dataclass
class Purchase(AvroModel):
    purchase_id: str
    venue_id: str
    items: int
    price: float
