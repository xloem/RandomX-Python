upload: clean update-version ensure-git
	python3 setup.py sdist
	twine check dist/*
	twine upload dist/*

clean:
	python3 setup.py clean
	rm -rf dist build *.egg-info
    
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
