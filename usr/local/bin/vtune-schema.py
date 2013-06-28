#!/usr/bin/python

import sqlite3
import sys

# A simple way of bugging out with an error message:
def bail(msg, code=1):
    sys.stderr.write(msg + ". Exiting.\n")
    sys.exit(code)

def log(msg):
    sys.stderr.write(msg + ".\n")

if len(sys.argv) < 2:
    bail("Must specify a VTune result directory")

# VTune result:
vtr = sys.argv[1];

# SQLite3 database file name:
dbf = vtr + '/sqlite-db/dicer.db'

arc=[]
schemata={}
liveTables={}
deadTables={}
hasRefs={}
hasRows={}

omitTables=()
#'dd_region_type', 'dd_frame_type', 'dd_domain', 'dd_context_value', '_subtree_helpers', 'dd_collection')

try:
    dbh = sqlite3.connect( dbf )
    log("Opened: %s" % dbh)
    sth = dbh.cursor()

    log("Fetching table/view list")
    sth.execute("SELECT name FROM sqlite_master WHERE type='table' OR type='view'")
    tables = [row[0] for row in sth.fetchall()]

    log("Fetching foreign key data from Intel auxiliary table")
    sth.execute('SELECT path,ref FROM _schema_refs')

    # Make sure that tables mentioned in _schema_refs (a
    # developer-created table to document the foreign keys) actually
    # exist in this database:
    for row in sth.fetchall():
        path,dst = row
        (src,col)=path.split('.')
        if src in tables and dst in tables:
            arc.append( (src,col,dst) )
        else:
            if src not in tables:
                log("Source table '%s' in foreign key '%s.%s'->'%s' does not exist" % (src, src,col,dst))
            if src not in tables:
                log("Target table '%s' in foreign key '%s.%s'->'%s' does not exist" % (dst, src,col,dst))

    ntables=0
    nonzero=0
    for t in tables:
        ntables += 1
        log("Fetching schema for table '%s'..." % t)
        if '_schema_' not in t and 'sqlite_' not in t:
            # See how many rows are in table 't':
            sth.execute("SELECT COUNT(*) FROM %s" % t)
            nrows,=sth.fetchall()[0]
            if nrows == 0:
                log("Table '%s' is empty" % t)

            # Get the schema for table 't':
            sth.execute("PRAGMA TABLE_INFO(%s)" % t)
            schema=[row[1] for row in sth.fetchall()]

            # We already have this from arcs (above) but that was
            # added after this. We should probably refactor the rest
            # of this to get rid of the extraneous database calls.

            # Get the foreign key attributes of table 't':
            sth.execute("SELECT path FROM _schema_refs WHERE path LIKE '%s.%%'" % t)
            paths=sth.fetchall()
            if len(paths) <= 0:
                log("Table '%s' has no foreign key attributes" % t)
                forkeys=[]
            else:
                forkys=[row[0].split('.')[1] for row in paths]

            # Get the number of foreign key references *TO* table 't':
            sth.execute("SELECT COUNT(*) FROM _schema_refs WHERE ref='%s'" % t)
            nrefs,=sth.fetchall()[0]
            if nrefs==0:
                log("Table '%s' is not the target of any foreign key." % t)

            schemata[t]=(schema, forkys, nrefs, nrows)

except sqlite3.Error, e:
    log("Error %s\n" % e.args[0])
finally:
    if dbh:
        dbh.close()

print("""digraph structs {
        splines = true;
        overlap = false;
        ratio = 0.75;
        nodesep = 0.75;
        node [shape=record];
""")

# Print out the nodes:
for name,(schema, forkeys, nrefs, nrows) in schemata.iteritems():
    # If the table is empty, we omit it:
    if nrows!=0 and name not in omitTables:
        cols = [col for col in schema if col!='__explicit_rowid__'];
        if len(cols)!=len(schema):
            star='*'
        else:
            star=''

        attrpair=[]
        for col in cols:
#            print(col, forkeys)
            if col in forkeys:
                attrpair.append( (col, col[0].upper()) )
            else:
                attrpair.append( (col, col) )

        colspec=['<%s> %s' % colpair for colpair in attrpair]
        print('\t%s [label="<rowid> %s%s(%s)|'%(name,name,star,nrows) + '|'.join(colspec) + '"];') 

# Print out the arcs:
for src,attr,dst in arc:
    if src not in schemata:
        log( "Arc source table '%s' does not exist." % src )
    if dst not in schemata:
        log( "Arc destination table '%s' does not exist." % src )

    # If the source or destination tables are empty, or if we've
    # explicitly excluded the table for some reason, we omit the arc:
    if schemata[src][3]==0 or schemata[dst][3]==0 or src in omitTables or dst in omitTables:
        pass
    else:
        print( '\t%s:%s -> %s:rowid [label="%s"];' % (src,attr,dst,attr) )

print("}")

