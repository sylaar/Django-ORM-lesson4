from django.contrib import admin

from pokemon_entities.models import Pokemon
from pokemon_entities.models import PokemonEntity


admin.site.register(Pokemon)
admin.site.register(PokemonEntity)