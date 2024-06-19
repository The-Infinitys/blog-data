import datetime
import os
import markdown
from sys import exit
article_temp_head = '''
<!DOCTYPE html>
<html lang="Ja">
  <head>
    <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" /><meta name="description" content="The Infinity's awesome blog article" />
    <meta name="description" content="The Infinity's awesome blog article" />
    <title>HERE TO THE TITLE</title>
    <link rel="stylesheet" href="../../Infinity-style/style.css" />
    <script defer src="../../Infinity-style/script.js"></script>
    <script defer src="/The-Infinitys-Infinity/script.js"></script>
    <link rel="stylesheet" href="/The-Infinitys-Infinity/style.css">
    <script defer src="/The-Infinitys-Infinity/script.js"></script>
    <link rel="stylesheet" href="/The-Infinitys-Infinity/style.css" />
  </head>
  <body>
    <div id="article-body">
      <div id="article-content">
'''
article_temp_foot = '''      </div>
    </div>
  </body>
</html>
'''
def listfolders(dir_path):
  result = [
      f for f in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, f))
  ]
  return result
def listfiles(dir_path):
  result = [
      f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))
  ]
  return result
now=datetime.datetime.now()
now=str(now.year)+"-"+str(now.month)
root_dir="./"+now
if not os.path.isdir(root_dir):
  print("No datas")
  exit()
for article_dir in listfolders(root_dir):
  path = root_dir+"/"+article_dir
  file_names = listfiles(path)
  index_path = None
  article_path=None
  for file_name in file_names:
    if file_name.startswith("index"):
      index_path=file_name
    elif file_name==("article.md"):
      article_path=file_name
  if article_path!=None:
    markdown_text = ""
    markdown_title = ""
    with open(root_dir+"/"+article_dir+"/"+article_path,mode="r") as f:
      markdown_text = f.read()
      f.close()
          
    def convertmarkdown(markdown_text):
      global markdown_title
      markdown_result=""
      code_mode=False
      for markdown_line in markdown_text.split("\n"):
          if markdown_line.startswith("#title: "):
            markdown_title=markdown_line[8:]
          elif markdown_line.startswith("```"):
            if code_mode:
              markdown_result+="</pre>\n"
            else:
              markdown_result+="<pre>\n"
            code_mode = not code_mode
          elif code_mode:
            markdown_result+="<code>"+markdown_line.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")+"</code>\n"
          else:
            markdown_result+=markdown_line+"\n"
      return markdown.markdown(markdown_result)
    html_text = convertmarkdown(markdown_text)
    html_result=""
    for html_line in html_text.split("\n"):
      html_result+=" "*8+html_line+"\n"
    if index_path==None:
      with open(root_dir+"/"+article_dir+"/index.html",mode="w") as f:
        f.write(article_temp_head.replace("HERE TO THE TITLE",markdown_title)+html_result+article_temp_foot)
        f.close()