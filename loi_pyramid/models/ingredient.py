# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String
)

from .meta import Base


class Ingredient(Base):
    __tablename__ = 'ingredients'
    material = Column(String, primary_key=True)
    name = Column(String)
    category = Column(String)
    tier = Column(Integer)
    melee_stats = Column(String)
    half_melee_stats = Column(String)
    armor_stats = Column(String)
    half_armor_stats = Column(String)

    @property
    def public_payload(self):
        return {
            'material': self.material,
            'name': self.name,
            'category': self.category,
            'tier': self.tier,
            'melee_stats': self.melee_stats,
            'half_melee_stats': self.half_melee_stats,
            'armor_stats': self.armor_stats,
            'half_armor_stats': self.half_armor_stats
        }
