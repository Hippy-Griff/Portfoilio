import html2text
from bs4 import BeautifulSoup
import requests
import os

# Initial variables
board_suffix=1.25
# Replace placeholder with the current directory.
parent_dir="[placeholder]"
# Replace placeholder with the name of the new folder.
new_dir='[placeholder]'

path_root=os.path.join(parent_dir,new_dir)
junk=[':','|',';','!','\n']

def thread_links(url):
    # This function extracts all thread links in a board page. There are a crap-ton.
    topic='topic='
    msg='msg'
    navPages='navPages'
    html=requests.get(url)
    soup=BeautifulSoup(html.text,'html.parser')
    raw_links=(soup.find_all("a"))
    link_list=[str(x) for x in raw_links]
    link_list=[link for link in link_list if topic in link and msg not in link and navPages not in link]
    thread_list=[]
    for item in link_list:
        item=item.replace('href="',"pika").replace('">', "pika")
        item=item.split("pika")
        thread_list.append(item[1])
    return thread_list

def extract_posts(url):
    # This function extracts the thread title, writers and post content and writes them all to text files.
    # Yeah, it's a proper bugger of a function, I know. Don't judge me for liking my functions being big.
        
        counter=0
        orig_suffix=0
        junk=[':','|',';','!','\n']
        html=requests.get(url)
        soup=BeautifulSoup(html.text,'html.parser')
        raw_title=soup.find("header","category_header")
        title=str(raw_title)
        title=html2text.html2text(title)
        title=title.split("Topic:")
        title=title[1]
        title=title.split("(Read")
        file_title=title[0]
        file_title=file_title.strip()
        file_title=''.join(x for x in file_title if x.isalnum() or x.isspace())
        for crap in junk:
            file_title=file_title.replace(crap,'')
        title=title[0]+" \n"+ " \n"


        a_list=soup.find_all("a","linklevel1 name")
        name_list=[]
        for a in a_list:
            if a.get_text() not in name_list:
                name_list.append(a.get_text())


        for name in name_list:
            name=name.replace('\n','').replace('\t','')

        post_list=soup.find_all("section","messageContent")
        dir_list=os.listdir()
        
#         If the file doesn't exist, we make it.
        if file_title+'.txt' not in dir_list:
            sample_post=post_list[0]
            f = open(f'{file_title}.txt','w+', encoding="utf-8")
            f.write(title)
            f.write('Written by:')
            for name in name_list:
                f.write(name+'\n'+'\n')
            for post in post_list:
                f.write(html2text.html2text(str(post))+'\n'+(60*'_')+(3*'\n'))
            
            f.close()
            test_str=post_list[0]
            
#            Otherwise, we move through the thread, adjusting the url suffix as needed until the end.
            while True:
                counter+=25
                url=url.replace(('.'+str(orig_suffix)),('.'+str(counter)))
                orig_suffix+=25
                html=requests.get(url)
                soup=BeautifulSoup(html.text,'html.parser')
                post_list=soup.find_all("section","messageContent")
                if post_list[0]!=test_str and counter<250:
                    f = open(f"{file_title}.txt", "a", encoding="utf-8")
                    for post in post_list:
                        f.write(html2text.html2text(str(post))+'\n'+(60*'_')+(3*'\n'))
                    f.close()
                    test_str=post_list[0]
                else:
                    break

# Here we go...cocking hell, I'm scared to run this script...
os.mkdir(path_root)
os.chdir(path_root)
for board in range(2,30):
    try:
        # First, we iterate through each forum board based on the address suffix, starting at 1.0.
        # Adjust the range if more boards are added or removed, or to do specific sections, because to hell with scraping the giant OOC thread.
        url=(f'https://(placeholder).com/forum/index.php?board={board_suffix}')
        html=requests.get(url)
        soup=BeautifulSoup(html.text,'html.parser')
        p_list=soup.find("ul","pagelinks floatleft")
        pages=p_list.get_text()
        max_page=int(max([page for page in pages if page.isdigit()]))
        max_suffix=str(int(board_suffix))+'.'+str(((max_page+1)*50)-25)
        temp_suffix=str(board_suffix)

        # Now we get the board name, make the new directory and move to it...bloody terrified...
        thread_list=[]
        raw_board_title=soup.find('h2')
        board_title=raw_board_title.get_text()
        for crap in junk:
            board_title=board_title.replace(crap,' ')
        board_title=board_title.strip()
        board_title=''.join(x for x in board_title if x.isalnum() or x.isspace())
        path_board=(os.path.join(path_root,board_title))
        os.mkdir(path_board)
        os.chdir(path_board)

        # Now we get a list of threads per board, appending them page by page.
        counter=25
        while temp_suffix!=max_suffix and len(thread_list)<(max_page*50):
            temp_url=(f'https://(placeholder)/forum/index.php?board={temp_suffix}')
            thread_list+=thread_links(temp_url)
            counter+=50
            temp_suffix=str(int(board_suffix))+'.'+str(counter)

        # Now we create our yummy text files, using the suffix in the function.

        for thread in thread_list:
            extract_posts(thread)

        board_suffix+=1
        os.chdir(path_root)
        
    except:
        board_suffix+=1
        continue

print("Victory!")
