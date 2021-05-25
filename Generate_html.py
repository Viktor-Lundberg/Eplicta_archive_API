from lxml import etree as ET

def background(iterationvalue):
    colours = {0: 'white', 1:'lightblue'}
    return colours.get(iterationvalue % 2)


document = open('arkiverad_kanal.xml', encoding='utf-8')
tree = ET.parse(document)
iteration = 0

posts = tree.findall('/post')
sortingdict = {}
html_document = open('insta.html', 'w', encoding="utf8")
html_document.write('<!DOCTYPE html>\n<meta charset="UTF-8">\n<html>\n<head>')
html_document.write('<style>html {background-color: lightgray;}\n.container {margin-left:35%;}\n.post{background-color: white; width: 500px;height: auto;border: none;padding: 5px 10px;font-family: arial;resize: none;outline: none; border-bottom: 2px solid #0077CC;margin-bottom: 15px; word-wrap:break-word;}\n')
html_document.write('.comment {background-color:lightskyblue; width: 300px; font-size: x-small; border-radius: 25px; padding-left: 15px; padding-bottom: 2px; padding-top:}\n')
html_document.write('</style>\n</head>\n<body>\n<div class=container>')



for post in posts:
    datum = post.find('metadata/publishDate')
    sortingdict.update({datum.text: post})

for k,v in sorted(sortingdict.items(),reverse=True):
    html_document.write(f'<div class="post">\n')
    publish_date = v.find('metadata/publishDate')
    post_title = v.find('metadata/title')
    post_message = v.find('metadata/postMessage')
    share_title = v.find('resources/share/title')
    share_description = v.find('resources/share/description')
    resources = v.findall('resources/file')
    comments = v.findall('comments/comment')
    likes = v.find('metadata/likeCount')
    shares = v.find('metadata/shareCount')

    if resources is not None:
        for resorce in resources:
            print(resorce.attrib['name'])
            link = resorce.attrib['name']
            if link.endswith('.mp4'):
                html_document.write(f'<video width="500px" controls><source src="{link}" type="video/mp4"></video>\n')
            else:
                html_document.write(f'<img style="max-width:500px;" src={link} alt="picture">\n')

    dateslice = publish_date.text.split('T')
    dateyear = dateslice[0]
    datetime = dateslice[1].split('.')[0]
    print(datetime)
    html_document.write(f'<h5>{dateyear} {datetime}</h5>\n')
    iteration += 1
    if post_message is not None:
        #html_document.write(f'<h2>{post_title.text}</h2>')
        html_document.write(f'<p>{post_message.text}</p>')
    if share_description is not None:
        html_document.write(f'<h4>{share_title.text}</h4>')
        html_document.write(f'<p>{share_description.text}</p>')

    if (shares is not None) and (likes is not None):
        html_document.write(f'<p style="font-size: 75%;">Likes: {likes.text} Delningar: {shares.text} </p>')

    if comments is not None:
        for comment in comments:
            comment_message = comment.find('message')
            comment_author = comment.find('author')
            comment_create_time = comment.find('createTime')
            comment_dateslice = publish_date.text.split('T')
            comment_dateyear = comment_dateslice[0]
            comment_datetime = comment_dateslice[1].split('.')[0]

            html_document.write(f'<div class="comment">\n<h5>{comment_dateyear} {comment_datetime}</h5>\n<p><b>{comment_author.text}</b> - {comment_message.text}</p>\n</div>')


    html_document.write('\n</div>')

html_document.write('</div></body><html>')




