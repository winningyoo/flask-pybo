from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect

from yjh.models import Question


bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'

@bp.route('/')
def index():
    return redirect(url_for('question._list')) # 반드시 url을 써줘야함. 불러오는 함수는 question._list


# 블루 프린트로 기능 분리하기 전까지 코드
# @bp.route('/')
# def index():
#     question_list = Question.query.order_by(Question.create_date.desc())
#     return render_template('question/question_list.html', question_list=question_list)
#     #return 'Pybo index'
#
# @bp.route('/detail/<int:question_id>/')
# def detail(question_id):
#     question = Question.query.get_or_404(question_id)
#     return render_template('question/question_detail.html', question=question)



