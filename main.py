from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import Label, SubmitField, StringField, SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from config import Config
import random

app = Flask(__name__)
app.config.from_object(Config)

class StartGameForm(FlaskForm):
    # message = Label(text='Вы готовы отправиться в путешествие?', field_id='start_submit')
    submit = SubmitField('Приступить к игре', id='start_submit')

rooms = {
    0: ('dungeon', 'Подземелье'),
    1: ('hall', 'Коридор'),
    2: ('armoury', 'Оружейная'),
    3: ('bedroom', 'Спальня'),
    4: ('hall2', 'Холл'),
    5: ('kitchen', 'Кухня'),
    7: ('balcony', 'Балкон')
}

@app.route('/', methods=['get', 'post'])
def index():
    form = StartGameForm()
    if form.validate_on_submit():
        room_id = 0
        return redirect(url_for("gameplay", room=rooms[room_id][0]))
    return render_template('index.html', form=form)

class GameplayForm(FlaskForm):
    way = SelectField('Выберите сторону света, в которую желаете отправиться', coerce=int,
                      choices=[
                          (-1, 'Запад'),
                          (1, 'Восток'),
                          (-3, 'Юг'),
                          (3, 'Север')
                      ], render_kw={'class': 'form-control'})
    number_steps = IntegerField('Сколько шагов хотите сделать?', validators=[DataRequired(), NumberRange(min=1, max=2)],
                                default=1,
                                render_kw={'class': 'form-control'})
    submit = SubmitField('В путь!', render_kw={'class': 'btn btn-primary'})

@app.route('/gameplay/<string:room>/', methods=['get', 'post'])
def gameplay(room):
    room_id = 0
    for k, v in rooms.items():
        if v[0] == room:
            room_id = k
            break
    form = GameplayForm()
    if form.validate_on_submit():
        room_id = room_id + (form.way.data * form.number_steps.data)
        if room_id in rooms:
            if room_id < 6:
                flash('Вы находитесь в комнате: {room}'.format(room=rooms[room_id][1]))
                return redirect(url_for("gameplay", room=rooms[room_id][0]))
            else:
                return redirect(url_for("finish"))
    flash('Вы находитесь в комнате: {room}'.format(room=rooms[room_id][1]))
    return render_template('gameplay.html', form=form)

class FinishForm(FlaskForm):
    rate = IntegerField('Поставьте оценку игре от 0 до 10', validators=[DataRequired(), NumberRange(min=0, max=10)],
                        render_kw={'class': 'form-control'})
    feedback = StringField('Напишите отзыв, если вам есть что сказать', render_kw={'class': 'form-control'})
    submit = SubmitField('Отправить оценку', render_kw={'class': 'btn btn-primary'})


@app.route('/finish/', methods=['get', 'post'])
def finish():
    form = FinishForm()
    flash('Уииии! Вы вышли на балкон. И можете раскрыть свои лёгкие на свежем воздухе и почувствовать себя победителем.')
    if form.validate_on_submit():
        print('игра оценена в {rate} баллов из 10'.format(rate=form.rate.data))
        print('Отзыв об игре: {feedback}'.format(feedback=form.feedback.data))
        flash('Спасибо за оценку!')
    return render_template('finish.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
