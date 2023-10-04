
from flask import Flask, render_template, request, flash, redirect, url_for
import re
import sourcemanagement as sm
from dbconnections import get_db_connection
import notemanagement as nm
import tagmanagement as tm
import sourcemanagement as sm
import authormanagement as am


app = Flask(__name__)
app.config['SECRET_KEY'] = 'HGrsAtU^Bt7cV8D5'

@app.route('/', methods=('GET', 'POST'))
def index():
    sourceString=""
    sourceUrl=""
    tagString=""
    contentString=""
    authorsString=""
    snippetId=False
    if request.method == 'POST':
        if request.form['action'] == 'Add':
            content = request.form['content']
            sourceString = request.form['sources-auto']
            snippetId=request.form['snippet-id']
            source_url=request.form['source-url']
            tagString=request.form['tags-auto'].strip()
            tagList=tagString.split(',')
            tagList = [item.strip() for item in tagList]
            authorsString=request.form['authors-auto'].strip()
            authorList=authorsString.split(',')
            authorList = [item.strip() for item in authorList]
            if not content:
                flash('Content is required!')
                return redirect(url_for('index'))
            if authorsString and not (sourceString or sourceUrl):
                flash('Author entry requires Source Title or URL')
                return redirect(url_for('index'))
            nm.alterSnippet(content,sourceString,tagList,source_url,authorList,snippetId)
        elif request.form['action'] == 'Delete':
            nm.deleteSnippet(request.form.getlist('delete-checks'))
        elif re.search("Edit*",request.form['action']):
            id=re.findall(r'\d+',request.form['action'])
            existingSnippet=nm.editSnippet(id)
            contentString=existingSnippet['content']
            sourceString=existingSnippet['sources']
            if sourceString is None:
                sourceString=''
            sourceUrl=existingSnippet['url']
            if sourceUrl is None:
                sourceUrl=''
            tagString=existingSnippet['tags']
            snippetId=existingSnippet['id']
            authorsString=am.authorsStringFromNoteId(snippetId)
    snippets=nm.listNotes()
    tags=tm.listTags()
    sources = sm.listSourceTitles()
    authors = am.listAuthorsAuto()
    return render_template('index.html', items=snippets, tags=tags, authors=authors,sources=sources,previous_authors=authorsString, previous_source=sourceString, previous_url=sourceUrl,previous_tags=tagString, previous_content=contentString, previous_id=snippetId)

@app.route('/filtersnippetslist/', methods=('GET', 'POST'))
def filtersnippetslist():
    tags=tm.listTags()
    snippets=nm.listNotes()
    if request.method == 'POST':
        if request.form['action'] =='filter':
            tagValues = request.form.getlist('tag-checks')
            filter = request.form['filter_logic']
            snippets=nm.listTaggedNotes(tagValues,filter)
        if request.form['action'] == 'Add':
            content = request.form['content']
            sourceString = request.form['sources-auto']
            snippetId=request.form['snippet-id']
            source_url=request.form['source-url']
            tagString=request.form['tags-auto'].strip()
            tagList=tagString.split(',')
            tagList = [item.strip() for item in tagList]
            authorsString=request.form['authors-auto'].strip()
            authorList=authorsString.split(',')
            authorList = [item.strip() for item in authorList]
            if not content:
                flash('Content is required!')
                return redirect(url_for('index'))
            if authorsString and not (sourceString or sourceUrl):
                flash('Author entry requires Source Title or URL')
                return redirect(url_for('index'))
            nm.alterSnippet(content,sourceString,tagList,source_url,authorList,snippetId)        
        if re.search("Edit*",request.form['action']):
            id=re.findall(r'\d+',request.form['action'])
            existingSnippet=nm.editSnippet(id)
            contentString=existingSnippet['content']
            sourceString=existingSnippet['sources']
            if sourceString is None:
                sourceString=''
            sourceUrl=existingSnippet['url']
            if sourceUrl is None:
                sourceUrl=''
            tagString=existingSnippet['tags']
            snippetId=existingSnippet['id']
            authorsString=am.authorsStringFromNoteId(snippetId)
            snippets=nm.listNotes()
            tags=tm.listTags()
            sources = sm.listSourceTitles()
            authors = am.listAuthorsAuto()
            return render_template('index.html', items=snippets, tags=tags, authors=authors,sources=sources,previous_authors=authorsString, previous_source=sourceString, previous_url=sourceUrl,previous_tags=tagString, previous_content=contentString, previous_id=snippetId)
    else:
        snippets=nm.listNotes()
    return render_template('filtersnippetslist.html', items=snippets, tags=tags)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/source/', methods=('GET', 'POST'))
def source():
    exisitingTitle=''
    exisitingYear=''      
    exisitingUrl=''
    exisitingFullname=''
    exisitingType=''
    sourceTypesDict=sm.dictSourceTypes()
    id=''
    if request.method == 'POST':
        if request.form['action'] == 'Add':
            if request.form['source_type'] == "None" or request.form['source_type']=='':
                flash('Sources require a type selected')
                return redirect(url_for('source'))
            else:
                 sourceTypeId = [d.get('id') for d in sourceTypesDict if d.get('entry')==request.form['source_type']][0]
            if not request.form['title'] or sourceTypeId == None:
                flash('A title and source type is required!')
                return redirect(url_for('source'))
            authorString=request.form['authors-auto'].strip()
            authorList=authorString.split(',')
            while("" in authorList):
                authorList.remove("")
            sm.alterSource(authorList,request.form['title'],request.form['year'],sourceTypeId,request.form['url'],request.form['source_id'])
        elif re.search("Edit*",request.form['action']):
            id=re.findall(r'\d+',request.form['action'])[0]
            existingSource=sm.loadSource(id)
            exisitingTitle=existingSource['title']
            exisitingYear=existingSource['year']
            exisitingUrl=existingSource['url']
            exisitingFullname=existingSource['author']
            exisitingType=existingSource['type']
        elif request.form['action'] == 'Delete':
            sm.deleteSource(request.form.getlist('delete-checks'))
    sourcesList=sm.listSources()
    authors = am.listAuthorsAuto()
    return render_template('source.html', sources=sourcesList, sourceTypes=sourceTypesDict, title=exisitingTitle, year=exisitingYear, url=exisitingUrl, type=exisitingType, previous_authors=exisitingFullname, previous_id=id, authors=authors )

@app.route('/author/', methods=('GET', 'POST'))
def author():
    exisitingBirthyear=''
    exisitingDeathyear=''
    exisitingComment=''
    exisitingFullname=''
    id=0
    if request.method == 'POST':
        if request.form['action']=='Add':
            authorFullname = str(request.form['author_fullname'])
            comment = str(request.form['author_comment'])
            birthyear = str(request.form['author_birthyear'])
            deathyear = str(request.form['author_deathyear'])
            id=int(request.form['author_id'])
            if not authorFullname:
                flash('Name required!')
                return redirect(url_for('author'))
            ## search existing authors to confirm no double entry
            am.saveAuthor(authorFullname,birthyear,deathyear,comment,id)
        elif re.search("Edit*",request.form['action']):
            id=re.findall(r'\d+',request.form['action'])[0]
            existingAuthor=am.loadAuthor(id)
            exisitingBirthyear=existingAuthor['birthyear']
            exisitingDeathyear=existingAuthor['deathyear']
            exisitingComment=existingAuthor['comment']
            exisitingFullname=existingAuthor['fullname']
        elif request.form['action'] == 'Delete':
            am.deleteAuthor(request.form.getlist('delete-checks'))
    authorList=am.listAuthors()
    return render_template('author.html', authors=authorList, author_birthyear=exisitingBirthyear, author_deathyear=exisitingDeathyear, author_comment=exisitingComment, author_fullname=exisitingFullname, author_id=id)

@app.route('/tag/', methods=('GET', 'POST'))
def tag():
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True) 
    if request.method == 'POST':
        if request.form['action']=='Add':
            tag = request.form['tag']
            if not tag:
                flash('Tag is required!')
                return redirect(url_for('tag'))
            cur.execute(f'insert into notetag(tag,entry_datetime, update_datetime) VALUES ("{tag}", now(), now())')
        if request.form['action']=='Delete':
            tm.deleteTags(request.form.getlist('delete-checks'))
        conn.commit()
        conn.close()
    tags=tm.listTagsFull()
    return render_template('tag.html', items=tags)

