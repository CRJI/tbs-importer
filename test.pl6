use v6;
use HTML::Entity :ALL;
use DBIish;

my $password = 'secret';

my $dbh = DBIish.connect('mysql', :host<127.0.0.1>, :port(3306),
                         :database<theblack_production>, :user<root>, :$password);

my $sth = $dbh.prepare(q/
  SELECT idRecord, title FROM blogRecords_view
  WHERE publishDate IS NOT NULL
/);

$sth.execute();

my @rows = $sth.allrows(:array-of-hash);
# say @rows.elems;

# @rows.map: *.say;
# for @rows {
#     decode("$_[0] $_[1]")
#     .subst('\'\'', '\'')
#     .say;
# }
for @rows {
    decode($_<idRecord> ~ " " ~ $_<title>)
    .subst('\'\'', '\'')
    .say;
}

$sth.finish;

$dbh.dispose;
