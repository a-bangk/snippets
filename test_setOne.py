
from app import authormanagement as am
from app.source import management as sm
from app import notemanagement as nm
from app import tagmanagement as tm
from app import helperfunctions as hf

def test_databaseConnection():
    print("Testing database connection")
    database=hf.get_db_connection().database
    print(database)
    assert database != None

def test_amIdFromFullNameList():
    assert am.idFromFullNamesList(["Milton Friedman","Finn Kjems","Gary Enzo","Karl Marx"]) == [71,72,73,74]

def test_smIdFromTitle():
    result=sm.idFromTitle("BabyWise")
    assert result == 61

def test_sourceFunctions():
    sm.alterSource("Bob Smith", "Test Title 1", '2000',3,'http://www.google.com','')
    sId=sm.idFromTitleAndUrl("Test Title 1","http://www.google.com")
    sm.alterSource("Bob Smith", "Test Title 2", '2002',3,'http://www.google.com',sId)
    sm.deleteSource([sId])

def test_usingQuotes():
    sId=sm.idFromTitleAndUrl('"','"')
    sm.deleteSource([sId])

def test_alterSnippet_SourceTitle():
    content="Test Content 667504ggyj"
    nm.alterSnippet(content,"New title 3",'','',[''],'False')        
    sIds=nm.idsFromContent(content)
    latestId=sIds[0][0]
    sValues=nm.editSnippet(latestId)
    nm.deleteSnippet([latestId])
    sm.deleteSource([sm.idFromTitle("New title 3")])
    assert sValues["content"]==content
    assert sValues["sources"]=="New title 3"
    assert sValues["id"]==latestId

def test_alterSnippet_Tag():
    content="Test Content adding Tags"
    tagString="test tag,    testtag    ,  @dae ,   "
    tagList=hf.commaStringToList(tagString)
    nm.alterSnippet(content,'',tagList,'',[''],'False')        
    sIds=nm.idsFromContent(content)
    latestId=sIds[0][0]
    sValues=nm.editSnippet(latestId)
    nm.deleteSnippet([latestId])
    tm.deleteTagsById(tm.idFromTagsList(tagList))
    assert sValues["content"]==content
    assert sValues["tags"]=="@dae, test tag, testtag"
    assert sValues["id"]==latestId

def test_alterSnippet_All():
    startCount=len(nm.listNotes())
    content="Test Content adding All"
    title='Source with Authors'
    url="www.AWESOME-TEST.org     "
    tagString="test tag,    testtag    ,  @dae ,   "
    authorsString="Author 1,     Author person 3, M.D manpanfan,    "
    tagList=hf.commaStringToList(tagString)
    authorsList=hf.commaStringToList(authorsString)
    nm.alterSnippet(content,title,tagList,url,authorsList,'False')        
    sIds=nm.idsFromContent(content)
    latestId=sIds[0][0]
    allSnippets=nm.listNotes()
    assert startCount<len(allSnippets)
    sValues=allSnippets[000]
    authorsInDb=am.authorsStringFromNoteId(latestId)
    nm.deleteSnippet([latestId])
    tm.deleteTagsById(tm.idFromTagsList(tagList))
    authorIds=am.idFromFullNamesList(authorsList)
    am.deleteAuthors(authorIds)
    sourceId=sm.idFromTitleAndUrl(title,url)
    sm.deleteSource([sourceId])
    assert sValues["content"]=='<p>'+content+'</p>'
    assert sValues["tags"]=='@dae; test tag; testtag'
    assert sValues["id"]==latestId
    assert sValues["sources"]==title
    assert authorsInDb=="Author 1, Author person 3, M.D manpanfan"

def test_authorManagement():
    assert 1==1

def test_tagManagement():
    tags=tm.listTagsFull()
    print (tags)