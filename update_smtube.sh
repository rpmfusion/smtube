version=21.10.0
REPOS="f35 f34 f33 el8 el7"

if [ -z "$1" ]
then
      stage=0
else
      stage=$1
fi

if test $stage -le 0
then
echo STAGE 0
git checkout master && git pull || exit 2

if [[ -z $2 ]]; then
MSG="Update smtube to $version"
else
MSG=$2
fi
if [[ -z $3 ]]; then
rpmdev-bumpspec -n $version -c "$MSG" smtube.spec
else
rpmdev-bumpspec -c "$MSG" smtube.spec
fi

spectool -g smtube.spec
rfpkg scratch-build --srpm --nowait
fi
if test $stage -le 1
then
echo STAGE 1
echo Press enter to upload sources and commit; read dummy;
rfpkg new-sources ./smtube-$version.tar.bz2
rfpkg ci -c && git show
echo Press enter to push and build in rawhide; read dummy;
rfpkg push && rfpkg build --nowait
fi

if test $stage -le 2
then
for repo in $REPOS ; do
echo Press enter to build on branch $repo; read dummy;
git checkout $repo && git merge master && git push && rfpkg build --nowait; git checkout master
done
fi

