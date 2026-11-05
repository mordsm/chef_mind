from app.coach import CoachCommand, JourneyState, apply_command


def test_roast_defaults_start_at_first_step_and_remain_editable():
    state = apply_command(None, CoachCommand(action='start_custom', dish_title='עוף בתנור', method='oven_roast'), 1000)
    assert state['current_step'] == 0
    assert [step['title'] for step in state['custom_steps']] == ['הכנה', 'תיבול', 'צלייה בתנור']
    assert not any(q['id'] == 'progress' for q in state['decision_questions'])
    assert state['intake_guidance']['defaults']['temperature'] == 200
    state = JourneyState.model_validate(state).model_dump()
    facts = {**state['intake_facts'], 'oven_temperature': 190, 'estimated_minutes': 35}
    state = apply_command(state, CoachCommand(action='intake', expected_revision=state['revision'], intake_facts=facts), 1001)
    assert '190°C' in state['custom_steps'][2]['instruction']
    assert '35' in state['custom_steps'][2]['instruction']
    assert state['current_step'] == 0


def test_chicken_context_does_not_expose_turkey_comparisons():
    state = apply_command(None, CoachCommand(action='start_custom', dish_title='עוף בגריל', method='grill_direct'), 1000)
    context = state['context']
    assert context['label'] == 'עוף'
    assert 'הודו' not in str(context['tips'])
    assert 'בחירת שיטה אינה מספקת' not in str(context['tips'])
    assert 'בבשר ועוף' not in state['intake_guidance']['guidance']
