from types import SimpleNamespace
from unittest.mock import Mock, patch
import json

from app.coach import CoachCommand, apply_command, JourneyState
from app.dish_recognition import recognize_dish


def test_one_local_request_and_no_retry():
    monitor=Mock();monitor.reserve.return_value=True
    settings=SimpleNamespace(dish_model_provider='local',dish_local_model='test-local',model_timeout_seconds=2)
    facts=dict(family='meat',protein='chicken',method='grill_direct',goal='brown',equipment='grill',main_ingredient='עוף')
    connection=Mock();connection.getresponse.return_value.status=200
    connection.getresponse.return_value.read.return_value=json.dumps({'message':{'content':json.dumps(facts)}}).encode()
    with patch('app.dish_recognition.HTTPConnection',return_value=connection):
        result=recognize_dish(settings,'עוף בגריל',[],monitor,'guest')
    assert result['facts']==facts
    assert connection.request.call_count==1
    connection.request.side_effect=TimeoutError()
    with patch('app.dish_recognition.HTTPConnection',return_value=connection):
        assert recognize_dish(settings,'עוף בגריל',[],monitor,'guest')['status']=='unavailable'
    assert connection.request.call_count==2


def test_grilled_chicken_does_not_offer_sauce_or_repeat_known_ingredient():
    state=apply_command(None,CoachCommand(action='start_custom',dish_title='עוף בגריל'),1000)
    assert state['method']=='גריל ישיר'
    assert state['intake_facts']['protein']=='chicken'
    assert state['intake_facts']['equipment']=='grill'
    assert 'sauce' not in state['intake_guidance']['goal_choices']
    assert not state['intake_guidance']['main_ingredient_needed']
    assert 'לגריל' in state['intake_guidance']['guidance'] or 'בגריל' in state['intake_guidance']['guidance']
    JourneyState.model_validate(state)


def test_recognition_is_persisted_and_explicit_method_wins():
    recognition={'status':'recognized','provider':'local','facts':dict(family='meat',protein='chicken',method='boil_simmer',goal='sauce',equipment='pot',main_ingredient='עוף')}
    state=apply_command(None,CoachCommand(action='start_custom',dish_title='עוף בגריל'),1000,recognition=recognition)
    assert state['dish_identity']['status']=='recognized'
    assert state['method']=='גריל ישיר'
    assert state['intake_facts']['goal']=='brown'


def test_all_actions_have_valid_structured_defaults():
    from datetime import datetime, UTC
    from app.action_log import configuration, validated_document, ReportInput
    config=configuration()
    assert len(config['actions'])==13
    for action in config['actions']:
        parameters={field['id']:field['default'] for field in action['fields']}
        if action['id']=='measure':
            parameters['temperature']=50
        document=validated_document(ReportInput(action_type=action['id'],config_version=config['version'],
            parameters=parameters,started_at=datetime.now(UTC)))
        assert bool(document['scheduled_end_at'])==action['auto_timer']
