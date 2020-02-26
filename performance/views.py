from django.shortcuts import render
import json
from django.http import HttpResponse
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
import time
import urllib.parse


def grade(x):
    if (x == 0):
        return ('E')
    elif (x < 40):
        return ('D')
    elif (x < 60):
        return ('C')
    elif (x < 80):
        return ('B')
    elif (x < 100):
        return ('A')
    elif(x==100):
        return ('A+')


def result(request):
    if request.method == 'POST':
        nm = request.POST.get('nm')
        if not re.match("^https://|http://", nm):
            nm = ('https://') + nm
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if (re.match(regex, nm) is not None):
            li = []
            catlen = []
            adtlen = []
            catttl = []
            adtttl = []
            catscr = []
            adtscr = []
            adtds = []
            adtg = []
            urll = []
            urlp = []
            adtdp = []
            json_file_path = nm.split('/')[2].split('.')[0]

                        #     #added
            keyyslow = ['Minimize HTTP Requests', 'Use a Content Delivery Network', 'Avoid empty src or href',
                        'Add an Expires or a Cache-Control Header', 'Gzip Components',
                        'Put StyleSheets at the Top', 'Put Scripts at the Bottom', 'Make JavaScript and CSS External',
                        'Reduce DNS Lookups', 'Avoid Redirects',
                        'Remove Duplicate Scripts', 'Configure ETags', 'Make AJAX Cacheable',
                        'Use GET for AJAX Requests', 'Reduce the Number of DOM Elements',
                        'No 404s', 'Reduce Cookie Size', 'Use Cookie-Free Domains for Components',
                        'Do Not Scale Images in HTML', 'Make favicon.ico Small and Cacheable']
            gra = []
            sz = []
            typ = []
            lnk = []
            tm = []
            simp = []
            simval = []
            si = []
            si.append(['component', 'size'])
            yli = []
            yliv = []
            ydes = []

            # os.system('phantomjs /home/admin/web/monitor.iserveradmin.com/public_html/phantomjs/bin/yslow-phantomjs-3.1.8/yslow.js --info all --format json {} > /home/admin/web/monitor.iserveradmin.com/public_html/static/yslow{}.json'.format(nm, json_file_path))
            # os.system('sed "1d" /home/admin/web/monitor.iserveradmin.com/public_html/static/yslow{}.json >  /home/admin/web/monitor.iserveradmin.com/public_html/static/yslowupdated{}.json'.format(json_file_path, json_file_path))
            # yslow_file_path = '/home/admin/web/monitor.iserveradmin.com/public_html/static/yslowupdated{}.json'.format(json_file_path)
            yslow_file_path = 'yslowreport.json'
            with open(yslow_file_path, encoding='utf8') as j:
                    cont = json.loads(j.read())
            count = 0
            for keys in cont['stats']:
                    simp.append(keys)
            for i in range(len(simp)):
                    simval.append(cont['stats'][simp[i]]['w'])
            for i in range(len(simp)-1):
                    si.append([simp[i], simval[i]])
            for keys in cont['comps']:
                    gra.append([])
                    for key in keys:
                     gra[count].append(key)
                    count = count+1
            for i in range(len(gra)):
                    typ.append(cont['comps'][i]['type'])
                    ln = (cont['comps'][i]['url'])
                    l = urllib.parse.unquote(ln)
                    lnk.append(l)
                    tm.append(cont['comps'][i]['resp'])
                    sz.append(cont['comps'][i]['size'])
            for keys in cont['g']:
                    yli.append(keys)
            for i in range(len(yli)):
                 try:
                    yliv.append((cont['g'][yli[i]])['score'])
                    ydes.append((cont['g'][yli[i]])['message'])
                 except:
                    yliv.append(0)
                    ydes.append('-')
            yzp = zip(keyyslow, yliv, ydes)
            # #finish
            url=nm
            # path = 'static/'+ json_file_path + '.png'
            # try:
            #  display = Display(visible=0, size=(1360, 800))
            #  display.start()
            #  driver = webdriver.Chrome( )
            #  driver.get(nm)
            #  time.sleep(10)
            #  driver.find_element_by_tag_name('body')
            #  time.sleep(0.5)
            #  driver.save_screenshot(path)
            #  driver.quit()
            #  display.stop()
            #  imgpath = 'http://monitor.iserveradmin.com/static/'+ json_file_path + '.png'
            # except:
            #  imgpath = 'https://support.vyond.com/hc/en-us/article_attachments/205203106/Screen_Shot_2016-07-11_at_3.18.59_PM.png'
            # os.system(
            #     'lighthouse --chrome-flags="--headless" --output json --output-path {} {}'.format('static/'+ json_file_path + '.json', nm))
            # read json file
            with open('iserveradmin.json', encoding='utf8') as j:
                contents = json.loads(j.read())
            # display images
            # try:
            #     for i in range(10):
            #        img = contents['audits']['screenshot-thumbnails']['details']['items'][i]['data']
            #        finalss = contents['audits']['final-screenshot']['details']['data']
            #        li.append(img)
            # except:
            #     finalss = 'https://support.vyond.com/hc/en-us/article_attachments/205203106/Screen_Shot_2016-07-11_at_3.18.59_PM.png'
            #     pass
            # show length of categories key in json file
            for keys in contents["categories"]:
                catlen.append(keys)
            # show categories key's title and score
            try:
             for i in catlen:
                 if contents["categories"][i]['score']is not None:
                  catscr.append(int(contents["categories"][i]['score'] * 100))
                 else:
                  catscr.append(0)
                 catttl.append(contents["categories"][i]['title'])
            except:
                pass
            # show length of audits key in json file
            for keys in contents["audits"]:
                adtlen.append(keys)
            # show audits key's title and score
            for i in adtlen:
                try:
                    adtscr.append(int(contents["audits"][i]['score'] * 100))
                except:
                    adtscr.append(0)
                adtttl.append(contents["audits"][i]['id'])
                adtds.append(contents["audits"][i]['description'])
                try:
                    val = contents["audits"][i]['displayValue']
                    adtdp.append(val)
                except:
                    adtdp.append('')
                for i in adtscr:
                    adtg.append(grade(i))
            # show length of url
            try:
                for keys in contents['audits']['uses-http2']['details']['items']:
                        urll.append(keys)
                for i in range(len(urll)):
                        urlp.append(contents['audits']['uses-http2']['details']['items'][i]['url'])
            except:

                pass
            print(si)
            zpa = zip(adtttl, adtscr, adtg, adtds, adtdp)
            zpc = zip(catttl, catscr)
            performance = int(contents["categories"]['performance']['score'] * 100)
            gper = grade(performance)
            accessibility = int(contents["categories"]["accessibility"]['score'] * 100)
            gacc = grade(accessibility)
            bp = int(contents["categories"]["best-practices"]['score'] * 100)
            gbp = grade(bp)
            seo = int(contents["categories"]["seo"]['score'] * 100)
            gseo = grade(seo)
            pwa = int(contents["categories"]["pwa"]['score'] * 100)
            gpwa = grade(pwa)
            date = contents["fetchTime"].split("T")[0]
            url = contents["finalUrl"].split('//')[1]
            url = url.split('/')[0]
            ga = (cont['o'])
            gb = (cont['g']['yno404']['score'])
            fmn = int(contents["audits"]['first-meaningful-paint']['score'] * 100)
            fcn = int(contents["audits"]['first-contentful-paint']['score'] * 100)
            return render(request, 'auditresult.html', {'li': li, 'date': date, 'url': url, 'per': performance, 'acc': accessibility,
                                                  'bp': bp, 'pwa': pwa, 'seo': seo, "acc": accessibility, 'adtttl': adtttl,
                                                  'adtscr': adtscr, 'urlp': urlp, 'gper': gper, 'gacc': gacc,
                                                  'gpwa': gpwa, 'gseo': gseo, 'gbp': gbp, #'finalss':finalss,
                                                 'catttl': catttl, 'catscr': catscr, 'zip': zpa, 'zipcat': zpc, 'yzp': yzp,
                                                 'yli': yli,'tm': tm, 'sz':sz, 'lnk':lnk, 'typ':typ, 'simp':si,
                                                  'ga':ga, 'gb':gb, 'gc':fmn, 'gd':fcn,})
        else:
            return HttpResponse("<html><body><h1>Invalid url</h1>")
    else:
        return render(request, 'search.html')


def monitor(request):
    return render(request, 'search.html')






