from dbconnections import get_db_connection

def listAuthors():
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('SELECT id,full_name as fullname, IFNULL(birthyear,"") as birthyear,IFNULL(deathyear,"") as deathyear, comment from author order by id desc;'.format(str()))
    db_authors=cur.fetchall()
    conn.close()
    authors=[]
    for author in db_authors:
        authors.append(author)
    return authors

def listAuthorsAuto():
    conn = get_db_connection()
    cur=conn.cursor(dictionary=False)
    cur.execute('select full_name as author from author;')
    authors_db=cur.fetchall()
    conn.close()
    authors=[]
    for author in authors_db:
        authors.append(author[0])
    return authors

def loadAuthor(edit_id):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute(f'SELECT id,full_name as fullname, IFNULL(birthyear,"") as birthyear,IFNULL(deathyear,"") as deathyear, comment from author a where a.id={edit_id};')
    author=cur.fetchone()
    conn.close()
    return(author)

def saveAuthor(fullName,birthyear='',deathyear='',comment='', id=0):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    if id == 0:
        cur.execute(f'insert into author(full_name,birthyear,deathyear,comment) VALUES ("{fullName}", "{birthyear}", "{deathyear}", "{comment}");')
    else:
        cur.execute(f'update author set full_name = "{fullName}",birthyear = "{birthyear}",deathyear = "{deathyear}",comment = "{comment}" where id = "{id}";')
    a_id = cur.lastrowid
    conn.commit()
    conn.close()
    return(a_id)

def deleteAuthor(delete_ids):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    for id in delete_ids:
        cur.execute(f'delete from author where id={id}')
        cur.execute(f'delete ignore from associate_source_author where author_id={id}')
    conn.commit()
    conn.close()

def idFromFullNamesList(fullNames):
    conn = get_db_connection()
    cur=conn.cursor()
    ids=[]
    for fullName in fullNames:
        commitFlag=False
        cur.execute(f'select id from author where full_name="{fullName}";')
        id=cur.fetchone()
        if not id:
            cur.execute(f'insert into author(full_name) values("{fullName}");')
            id=cur.lastrowid
            commitFlag=True
        else:
            id=id[0]
        ids.append(id)
        if commitFlag:
            conn.commit()
    conn.close()
    return ids

def authorsStringFromNoteId(snippetId):
    conn=get_db_connection()
    cur=conn.cursor()
    cur.execute(f'with atable as (with a as(select asa.source_id, GROUP_CONCAT(a.full_name separator ", ") as authors from associate_source_author asa join author a on a.id=asa.author_id group by asa.source_id) select a.authors, s.title as title, s.id as source_id from source s left join a on a.source_id =s.id ) select atable.authors from associate_source_note asn left join atable on atable.source_id=asn.source_id where asn.note_id={snippetId};')
    authors=cur.fetchone()
    return(authors[0])