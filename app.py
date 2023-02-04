from flask import Flask, render_template, redirect, url_for, flash

from config import Config
from forms import FinishForm, GameplayForm, StartGameForm

app = Flask(__name__)
app.config.from_object(Config)

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
    flash(
        'Вчерашний поход к барону явно удался. Сейчас вы в Подземелье и ваше самочувствие оставляет желать лучшего. ' +
        'Глоток свежего воздуха — вот, что вам сейчас нужно. А это значит, что нужно найти балкон.')
    return render_template('index.html', form=form)


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
                # flash('Вы находитесь в комнате: {room}'.format(room=rooms[room_id][1]))
                return redirect(url_for("gameplay", room=rooms[room_id][0]))
            else:
                return redirect(url_for("finish"))
        else:
            flash('Туда пути нет. Поменяйте направление или количество шагов.')
            return render_template('gameplay.html', form=form, room=room)
    flash('Вы находитесь в комнате: {room}'.format(room=rooms[room_id][1]))
    return render_template('gameplay.html', form=form)


@app.route('/finish/', methods=['get', 'post'])
def finish():
    form = FinishForm()
    flash(
        'Уииии! Вы вышли на балкон. И можете раскрыть свои лёгкие на свежем воздухе и почувствовать себя победителем.')
    if form.validate_on_submit():
        print('игра оценена в {rate} баллов из 10'.format(rate=form.rate.data))
        print('Отзыв об игре: {feedback}'.format(feedback=form.feedback.data))
        flash('Спасибо за оценку!')
    return render_template('finish.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
