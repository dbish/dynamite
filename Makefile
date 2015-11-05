PREFIX=dynamite-deployable
DEPLOYABLE=${PREFIX}-$(shell date +%Y%m%d.%H%M%S)

all:
	exit 0

zip:
	mkdir ${DEPLOYABLE}
	pip install -t ${DEPLOYABLE} -r requirements-lambda.txt
	cp config.py ${DEPLOYABLE}
	cp -R dynamite/ ${DEPLOYABLE}
	zip -rm ${DEPLOYABLE}.zip ${DEPLOYABLE}

clean:
	-rm -rf ${PREFIX}*
	-find . -name '*pyc' | xargs rm -f
