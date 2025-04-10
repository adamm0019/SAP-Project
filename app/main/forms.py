from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
import bleach

class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[
        DataRequired(),
        Length(min=1, max=500, message="Message must be between 1 and 500 characters")
    ])
    submit = SubmitField('Post')

    def validate_message(self, message):
        if len(message.data) > 500:
            raise ValidationError('Message must be less than 500 characters.')

        stripped = bleach.clean(message.data, tags=[], strip=True)
        if not stripped.strip():
            raise ValidationError('Message cannot be empty.')

class SearchForm(FlaskForm):
    search_term = StringField('Search', validators=[
        DataRequired(),
        Length(min=2, max=100, message="Search term must be between 2 and 100 characters")
    ])
    submit = SubmitField('Search')

    def validate_search_term(self, search_term):
        if len(search_term.data) < 2:
            raise ValidationError('Search term must be at least 2 characters long.')

        if len(search_term.data) > 100:
            raise ValidationError('Search term must be less than 100 characters long.')

        stripped = bleach.clean(search_term.data, tags=[], strip=True)
        if not stripped.strip():
            raise ValidationError('Search term cannot be empty.')