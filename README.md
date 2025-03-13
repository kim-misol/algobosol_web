# algobosol

주식/코인 투자 포트폴리오

## 로컬 실행

터미널에서 아래 명령어 실행
```shell
streamlit run app.py
```
브라우저가 자동으로 열리며 데모 페이지를 확인할 수 있습니다.

## 개발 환경 구성

공격적으로 버전을 업그레이드 하기 때문에 [pyenv](https://github.com/pyenv/pyenv)를
사용하여 python 설치하는 것을 권장하며 `pip`가 아닌 [poetry](https://python-poetry.org/docs/)를 사용함.

```shell
pip install --user poetry
make install  # 개발시 `make install-dev`를 사용
```

## Tech Stack


- [pandas](https://github.com/pandas-dev/pandas): data manipulation libray
- [streamlit](https://github.com/streamlit/streamlit)
개발용:

- [poetry](https://python-poetry.org/docs/): dependency manager