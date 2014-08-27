#set up mysql server to run as logged in user
unset TMPDIR
mysql_install_db --verbose --user=`whoami` \\
--basedir="$(brew --prefix mysql)" \\
--datadir=/usr/local/var/mysql --tmpdir=/tmp