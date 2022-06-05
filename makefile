twine_upload: ensure-git update-version clean sdist bdist_wheel twine_check

help:
	@echo 'Target name is simply passed to setup.py . make build, make install, make bdist_wheel ...'

%:
	python3 setup.py "$@"

update-version:
	-git submodule update --init --recursive
	pushd RandomX &&\
        git fetch origin &&\
        describe=$$(git describe --tags origin/master) &&\
        tag=$${describe%%-*} &&\
        version=$${tag#v} &&\
        git checkout "$$tag" &&\
        popd &&\
        echo "$$version" | tee version
	git add RandomX version

ensure-git:
	#cd test; pytest .. --rootdir=.
	git update-index --refresh 
	git diff-index --quiet HEAD --
	git status
	u="$$(git ls-files --others --exclude-standard)" && test -z "$$u"
	git push

twine_check:
	pip3 install keyring==21.0.0 setuptools-twine
