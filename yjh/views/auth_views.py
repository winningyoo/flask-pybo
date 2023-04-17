from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from yjh import db
from yjh.forms import UserCreateForm, UserLoginForm
from yjh.models import User
import functools  # 함수명을 annotation 할 수 있게 만들어 주는 tool

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit(): # 검증결과를 보여주는 함수 (통과되어야만 결과를 보여줌)
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data), # generate_password_hash : 암호화 시켜주는 함수
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.') # 사용자 브라우저에 직접 보이게 하는 함수 flash
    return render_template('auth/signup.html', form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data): # 입력한 암호화 암호화된 암호와 비교하는 함수
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            _next = request.args.get('next', '')
            if _next:
                return redirect(_next)
            else:
                return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

@bp.before_app_request # 요청하기 전에 (가장)먼저 실행하기 _ 가장 먼저 실행되는 annotation..?
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)
        # g : request를 요청 했을때만 살아있는 Flask 자체 변수
        #각 HTML > APP > Flask

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

def login_required(view): # 현재 페이지 (view)로 이동
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next)) # redirect = 바로이동 , auth가 login 을 가지고 있음.
        return view(*args, **kwargs)
    return wrapped_view