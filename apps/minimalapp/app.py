# flask 클래스를 import한다
from flask import Flask, render_template, url_for, request, redirect, flash, make_response, session
from email_validator import validate_email, EmailNotValidError
import logging
from flask_debugtoolbar import DebugToolbarExtension

# flask 클래스를 인스턴스화한다
app = Flask(__name__)
# SECRET_KEY를 추가한다
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBs"
# 로그 레벨을 설정한다
app.logger.setLevel(logging.DEBUG)
# 리다이렉트를 중단하지 않도록 한다
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# DebugToolbarExtension에 애플리케이션을 설정한다
toolbar = DebugToolbarExtension(app)

# URL과 실행할 함수를 매핑한다
@app.route("/")
def index():
    return "Hello, Flaskbook"

@app.route("/hello/<name>", methods=["GET", "POST"], endpoint="hello-endpoint")
def hello(name):
    # Python 3.6부터 도입된 f-string으로 문자열을 정의
    return f"Hello, {name}!"

@app.route("/name/<name>")
def show_name(name):
    # 변수를 템플릿 엔진에게 건넨다
    return render_template("index.html", name=name)

@app.route("/contact")
def contact():
    # 응답 객체를 취득한다
    response = make_response(render_template("contact.html"))
    # 쿠키를 설정한다
    response.set_cookie("flaskbook key", "flaskbook value")
    # 세션을 설정한다
    session["username"] = "AK"
    # 응답 오브젝트를 반환한다
    return response

    #return render_template("contact.html")

@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        # form 속성을 사용해서 폼의 값을 취득한다
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        # 입력 체크
        is_valid = True

        if not username:
            flash("사용자명은 필수입니다")
            is_valid = False
        
        if not email:
            flash("메일 주소는 필수입니다")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("메일 주소의 형식으로 입력해주세요")
            is_valid = False

        if not description:
            flash("문의 내용은 필수입니다")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))

        # 이메일을 보낸다(나중에 구현할 부분)

        # contact 엔드포인트로 리다렉트한다
        flash("문의해 주셔서 감사합니다")
        return redirect(url_for("contact_complete"))
    
    return render_template("contact_complete.html")

with app.test_request_context():
    # /
    print(url_for("index"))
    # /hello/world
    print(url_for("hello-endpoint", name="world"))
    # /name/AK?page=1
    print(url_for("show_name", name="AK", page="1"))

with app.test_request_context("/users?updated=true"):
    # true가 출력된다
    print(request.args.get("updated"))