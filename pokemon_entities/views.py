import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils.timezone import localtime

from pokemon_entities.models import Pokemon
from pokemon_entities.models import PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
        pokemons_json = json.load(database)['pokemons']

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemon_entities = PokemonEntity.objects.all()
    for pokemon_entity in pokemon_entities:
        if pokemon_entity.appeared_at <= localtime() and pokemon_entity.disappeared_at > localtime():
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(pokemon_entity.pokemon.image.url),
            )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.pk,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    current_time = localtime()

    pokemon_entities = PokemonEntity.objects.filter(
        pokemon=pokemon,
        appeared_at__lte=current_time,
        disappeared_at__gt=current_time,
    )

    for pokemon_entity in pokemon_entities:
        image_url = request.build_absolute_uri(pokemon.image.url)
        add_pokemon(folium_map, pokemon_entity.lat, pokemon_entity.lon, image_url)
    
    pokemon_info = {
        'pokemon_id': pokemon.pk,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'img_url': request.build_absolute_uri(pokemon.image.url),
    }

    if pokemon.previous_evolution:
        pokemon_info['previous_evolution'] = {
            'pokemon_id': pokemon.previous_evolution.pk,
            'title_ru': pokemon.previous_evolution.title,
            'img_url': request.build_absolute_uri(pokemon.previous_evolution.image.url)
        }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_info
    })
