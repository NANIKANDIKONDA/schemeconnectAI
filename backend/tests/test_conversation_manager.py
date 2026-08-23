from backend.api.routes.chat import get_all_schemes
from backend.conversation.conversation_manager import ConversationManager


def test_conversation_manager_profile_extraction():

    schemes = get_all_schemes()

    manager = ConversationManager(schemes)

    message = (
        "I am a 20 year old farmer from Andhra Pradesh. "
        "I own 2 acres of land and my annual income is 150000. "
        "What government schemes can I apply for?"
    )

    response = manager.process_message(message)

    print("\n" + "=" * 70)
    print("CONVERSATION MANAGER RESPONSE")
    print("=" * 70)

    print(response)

    print("\n" + "=" * 70)
    print("SESSION PROFILE")
    print("=" * 70)

    print(manager.session_profile)

    assert manager.session_profile.get("age") == 20
    assert manager.session_profile.get("state") == "Andhra Pradesh"
    assert manager.session_profile.get("occupation") == "Farmer"
    assert manager.session_profile.get("land_acres") == 2.0
    assert manager.session_profile.get("annual_income") == 150000.0