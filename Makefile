lint:
	pylint --rcfile=.pylintrc ./telegram/ --init-hook='sys.path.extend(["./telegram/"])'
build:
	docker build -t spentless-telegram .
