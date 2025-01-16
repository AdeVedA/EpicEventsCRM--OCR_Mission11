from sqlalchemy.orm import Session

from controllers.utils_ctrl import with_session


def test_with_session_decorator(mocker):
    """teste le decorateur de session"""

    @with_session
    def test_function(session=None):
        return session

    session = test_function()
    assert isinstance(session, Session)

    mock_session = mocker.Mock()
    session = test_function(session=mock_session)
    assert session == mock_session
