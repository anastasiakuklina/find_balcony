from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField, StringField
from wtforms.validators import DataRequired, NumberRange


class StartGameForm(FlaskForm):
    # message = Label(text='Вы готовы отправиться в путешествие?', field_id='start_submit')
    submit = SubmitField('Приступить к игре', id='start_submit')


class FinishForm(FlaskForm):
    rate = IntegerField('Поставьте оценку игре от 0 до 10', validators=[DataRequired(), NumberRange(min=0, max=10)],
                        render_kw={'class': 'form-control'})
    feedback = StringField(
        'Напишите отзыв, если вам есть что сказать. (На самом деле, отзыв не сохранится. Оценка тоже)',
        render_kw={'class': 'form-control'})
    submit = SubmitField('Отправить оценку', render_kw={'class': 'btn btn-primary'})


class GameplayForm(FlaskForm):
    way = SelectField('Выберите сторону света, в которую желаете отправиться', coerce=int,
                      choices=[(3, 'Север'), (1, 'Восток'), (-3, 'Юг'), (-1, 'Запад')],
                      render_kw={'class': 'form-control'})
    number_steps = IntegerField('Сколько шагов хотите сделать? ( Не больше двух )',
                                validators=[DataRequired(), NumberRange(min=1, max=2)], default=1,
                                render_kw={'class': 'form-control'})
    submit = SubmitField('В путь!', render_kw={'class': 'btn btn-primary'})
