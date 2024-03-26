from flask import render_template,request,redirect,url_for,flash  
import json 
import re
from . import filter_bp
from .. import tagmanagement as tm
from .. import notemanagement as nm

from flask_login import login_required, current_user


@filter_bp.route('/explore', methods=('GET', 'POST'))
@login_required
def filtersnippetslist():
    tags2=tm.tagsForUserIdSortable(current_user.id)
    tags=tm.tagsForUserIdWithCount(current_user.id)
    if request.method == 'POST':
        if request.form['action'] =='filter':
            note_ids_str = request.form['noteIds']
            note_ids = json.loads(note_ids_str)
            snippets=nm.listNotesEpoch(note_ids)
            snippets=json.dumps(snippets)
        elif re.search("Edit*",request.form['action']):
            return render_template('write.html')
        if request.form['action'] == 'Add':
            content = request.form['content']
            source_string = request.form['sources-auto']
            snippet_id=request.form['snippet-id']
            source_url=request.form['source-url']
            tagString=request.form['tags-auto'].strip()
            tag_list=tagString.split(',')
            tag_list = [item.strip() for item in tag_list]
            authorsString=request.form['authors-auto'].strip()
            author_list=authorsString.split(',')
            author_list = [item.strip() for item in author_list]
            if not content:
                flash('Content is required!')
                return redirect(url_for('home_bp.index'))
            if authorsString and not source_string:
                flash('Author entry requires Source Title or URL')
                return redirect(url_for('home_bp.index'))
            nm.alterSnippet(content,source_string,tag_list,source_url,author_list,snippet_id,current_user.id)
    else:
        snippets=[]
    return render_template('explore.html', items=snippets, tags=tags, tags2=tags2)

@filter_bp.route('/<user_username>/tag=<tag>', methods=('GET', 'POST'))
@login_required
def tag_sorted(user_username,tag):
    tags2=tm.tagsForUserIdSortable(current_user.id)
    tags=tm.tagsForUserIdWithCount(current_user.id)
    snippets=nm.listNotesForUserIdTag(current_user.id, tag)
    if request.method == 'POST':
        if request.form['action'] =='filter':
            note_ids_str = request.form['noteIds']
            note_ids = json.loads(note_ids_str)
            snippets=nm.listNotes(note_ids)
        elif re.search("Edit*",request.form['action']):
            return render_template('write.html')
    for dictionary in snippets:
        dictionary['exploreTag']=f'/{user_username}/tag={tag}'
    return render_template('exploreTag.html', items=snippets, tag=tag, tags=tags, tags2=tags2)