import json
import pytest
from app.coach import CoachCommand, JourneyState, apply_command
from app.knowledge import DomainError
from app.recipe_import import RecipeImport, allowed_url, from_html, import_recipe


def test_recipe_json_ld_sections_preserve_original_steps_and_source():
    data={'@graph':[{'@type':['Recipe'],'name':'עוף בגריל','recipeIngredient':['500 גרם עוף'],
        'recipeInstructions':[{'@type':'HowToSection','itemListElement':[
            {'@type':'HowToStep','text':'צולים בגריל ומסובבים לפי ההשחמה.'},
            {'@type':'HowToStep','text':'בודקים את מרכז הנתח במדחום.'}]}]}]}
    recipe=from_html('<script type="application/ld+json">'+json.dumps(data)+'</script>','https://www.mako.co.il/food/example')
    assert len(recipe.steps)==2
    assert recipe.steps[0].action_type=='grill'
    assert recipe.ingredients==['500 גרם עוף']
    state=apply_command(None,CoachCommand(action='start_custom',dish_title='עוף בגריל'),1000)
    state=apply_command(state,CoachCommand(action='attach_recipe',expected_revision=state['revision'],recipe_snapshot=recipe),1001)
    JourneyState.model_validate(state)
    assert state['custom_steps'][0]['instruction']==recipe.steps[0].text
    assert state['recipe_snapshot']['url']==recipe.url
    assert state['completed_step_ids']==[]
    assert state['intake_guidance']['recipe_status']=='imported'
    assert not state['intake_guidance']['recipe_requested']


def test_pasted_recipe_is_explicit_reference_not_inferred_parameters():
    recipe=import_recipe(RecipeImport(title='אפייה',text='אופים לפי המתכון.\nבודקים את התוצאה.'))
    assert recipe.acquisition=='pasted'
    assert recipe.steps[0].action_type=='bake'
    assert len(recipe.steps)==2
    assert recipe.ingredients==[]
    same=import_recipe(RecipeImport(title='אפייה',text='אופים לפי המתכון.\nבודקים את התוצאה.'))
    assert same.id==recipe.id and same.steps[0].id==recipe.steps[0].id


def test_replacing_fish_recipe_resets_old_details_and_keeps_patties_safety():
    state=apply_command(None,CoachCommand(action='start_custom',dish_title='נסיכת הנילוס'),1000)
    state['intake_facts'].update(cut='פילה בעובי 3 סמ',quantity='500 גרם',equipment='pot')
    state['measured_temperature']=63
    recipe=import_recipe(RecipeImport(title='קציצות נסיכת הנילוס',text='מערבבים דג טחון עם פטרוזיליה.\nיוצרים קציצות.'))
    state=apply_command(state,CoachCommand(action='attach_recipe',expected_revision=state['revision'],recipe_snapshot=recipe),1001)
    JourneyState.model_validate(state)
    assert state['dish_title']==recipe.title
    assert state['intake_facts']['cut']==''
    assert state['measured_temperature'] is None
    assert state['custom_steps'][0]['instruction']==recipe.steps[0].text
    protocol=state['station_protocol']
    assert '70–80' not in protocol['blocks'][1]['text']
    assert protocol['current_action']['kind']=='safety'
    assert 'קציצות' in protocol['current_action']['text']


def test_instruction_in_howto_step_name_when_text_is_null():
    data={'@type':'Recipe','name':'אפייה','recipeInstructions':[{'@type':'HowToStep','name':'אופים בתנור.','text':None}]}
    recipe=from_html('<script type="application/ld+json">'+json.dumps(data)+'</script>','https://imaot.co.il/Book/Page/example')
    assert recipe.steps[0].text=='אופים בתנור.'


@pytest.mark.parametrize('url',['http://127.0.0.1:8800','https://127.0.0.1','https://evil.example','https://www.mako.co.il.evil.example','https://user@www.mako.co.il/','https://www.mako.co.il:8080/'])
def test_import_rejects_unapproved_destinations(url):
    with pytest.raises(DomainError):allowed_url(url)


def test_article_without_recipe_is_not_invented_into_a_recipe():
    with pytest.raises(DomainError):from_html('<p>Article only</p>','https://www.mako.co.il/example')
