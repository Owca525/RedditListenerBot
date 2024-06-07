import concurrent.futures
import http.client
import socket
import re

class https:
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/jxl,image/webp,*/*;q=0.8",
        "Cookie": "loid=00000000006fqb9uoh.2.1589114664963.Z0FBQUFBQmstTjc2WVlXdGRpNjctQnJaWWhvb1F6d3V3Y05FMG1qM29XeUVqNnVySXNQWFJZZEg1N29hUEVLY1lCWDMwbFhJTFR4SVd6UFpiZjJHSHl6RXJKNjhwNGRPZWJ1OWg2em1CV1M5UFZzUUR6Rk0xZmtpYWdXczJtcy1nS0lZdTFBRGtpSjg; csv=2; edgebucket=VaIdTmiyMaji9Ij4CC; USER=eyJwcmVmcyI6eyJ0b3BDb250ZW50RGlzbWlzc2FsVGltZSI6MCwiZ2xvYmFsVGhlbWUiOiJSRURESVQiLCJuaWdodG1vZGUiOnRydWUsImNvbGxhcHNlZFRyYXlTZWN0aW9ucyI6eyJmYXZvcml0ZXMiOmZhbHNlLCJtdWx0aXMiOmZhbHNlLCJtb2RlcmF0aW5nIjpmYWxzZSwic3Vic2NyaXB0aW9ucyI6ZmFsc2UsInByb2ZpbGVzIjpmYWxzZX0sInRvcENvbnRlbnRUaW1lc0Rpc21pc3NlZCI6MH19; eu_cookie={%22opted%22:true%2C%22nonessential%22:false}; reddit_session=504427775633%2C2023-09-06T20%3A20%3A10%2Cccaaa79c03b13578b259b63b5b2eb1b94edce569; pc=1v; csrf_token=a4978681b41a51b1038f3e0fea89f5ad; generated_session_tracker=bcdeqbohkacdkccarm.1.1686347701000.WN6kDwKGndtKifT2gnQX87OLmKTDAESsIIu3jCM-cd0DwMvM7XskSlgt7fnSNA9q24mA1wszvXjRAsPVpH4SMA; session=8337fd15263be7c2f1915dc607809ac8fa2b2bf4gAWVSQAAAAAAAABKXCq9ZUdB2RXzRd5zFn2UjAdfY3NyZnRflIwoZDliOWYwYjBlYjhmYzU1NGFhMjQyMzVmYjVjZjRkNmM1MTk3MzU0MZRzh5Qu; session_tracker=mnajjagpnlergidojp.0.1706895975008.Z0FBQUFBQmx2U3BuMlN0RHhDMkY5YXBNVXBRaEo4b3NkZDBuaUViOHJHM1E0b2JYSFAyU0t3Zmp1eTlwX1V4WXdaXzZlaUQ3NnVERDROSy1rc2Z3cDBkUHAtZ2FhcXhwaHVfYzdJQjNXNkNraS1sdllfOW05bjJRa3E1SG1IVkFxQllDbWlxVnBBRG0; token_v2=eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpzS3dsMnlsV0VtMjVmcXhwTU40cWY4MXE2OWFFdWFyMnpLMUdhVGxjdWNZIiwidHlwIjoiSldUIn0.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNzA2OTgxNjQ2Ljk3NDEwOCwiaWF0IjoxNzA2ODk1MjQ2Ljk3NDEwOCwianRpIjoiS2F5cXRCc21tcnRCbk9yR2QyYVlVUmp6WGRXalRnIiwiY2lkIjoiOXRMb0Ywc29wNVJKZ0EiLCJsaWQiOiJ0Ml82ZnFiOXVvaCIsImFpZCI6InQyXzZmcWI5dW9oIiwibGNhIjoxNTg5MTE0NjY0OTYzLCJzY3AiOiJlSnhra2RHT3REQUloZC1sMXo3Ql95cF9OaHRzY1lhc0xRYW9rM243RFZvY2s3MDdjTDRpSFA4bktJcUZMRTJ1QktHa0tXRUZXdE9VTmlMdjU4eTlPWkVGU3lGVFI4NDN5d29rYVVwUFVtTjVweWxSd1daa0xsZmFzVUtEQjZZcFZTNloyMEtQUzV2UTNJMUZ6MDZNcWx4V0h0VFlvM0pwYkdNSzJ4UGp6Y1pxUXlxdXk2bE1ZRmtvbjhXTGZ2eUctdFktZjdiZmhIWXdyS2dLRF9UT3VGeHdZX0hERkhiX25wcjBiRjJ3cUwzWGc5US0xLU4yN2JObW9kbTVfVnpQdnphU2NUbUc1aWZZdjd0LUNSMTQ1SG1aVVFjd1lnMF95ckFqNl9Ddk9vREtCUVdNSlloUEk1QXJsMl9fSmRpdVRmOGF0eWQtLUdiRVRXXzRyUm1vNXhMRW9VX2o2emNBQVBfX1hEX2U0dyIsInJjaWQiOiJIbWcyN002UGQzR1Q0MkNnY01FMG4wRnhpTjc0Q2VGbEQxZkZPSC1FVUc0IiwiZmxvIjoyfQ.NCZx8kEd9G-4NOayk24t2j7kXuxphKR4mmdbmEONtfXKrfEQSCkUg0FcrizdiB0vRGhOIx89-2-aLmgDwTlLxcJfN4NyytqQIPOkccVdseHISO9Bxh3uz_8I_9RGP19-Uul1cL95iL4mSVxsHon5te9Si1yjogabmQidVjHcIJl5B-vaNewHOPmYodnvUuWGY6V3y17gpOQWq7tTKfb14D0btbFd6XTB9iTDlJtvmfvrYIGe4lDn5LVEySyLpFG-DEWzecdgFvrAxLNad6e44IHZT0VUTaeYKn4Zwbq8VIbiSLNt-fxj_RBjPG6PGOsIeCbWuJUyJvmdYyg5dNcCEw",
    }

    def __init__(self, header = {}, timeout = 30, decode = "utf-8", reconnect = 3) -> None:
        self.timeout = timeout
        self.header = self.head
        if header != {}:
            self.header = header

        self.decode = "utf-8"
        if decode != "":
            self.decode = decode

        self.status = None
        self.text = None

        self.reconnect = int(reconnect)

        self.headerConnection = ""

    async def get(self,url):
        socket.setdefaulttimeout(self.timeout)
        try:
            connection = http.client.HTTPSConnection(http.client.urlsplit(url).netloc)
            connection.request("GET", http.client.urlsplit(url).path,headers=self.header)
            response = connection.getresponse()

            self.status = response.status

            if self.status == 200:
                self.headerConnection = response.headers
                self.text = response.read().decode(self.decode)
            if self.status == 403:
                print(f"\033[91mForbidden 403: {url}\033[0m")

        except socket.timeout:
            self.status = 408
            self.text = None
        except UnicodeDecodeError:
            self.text = None

        except Exception as e:
            print(f"Error: {e} Retrying: {self.reconnect}")
            self.reconnect -= 1
        finally:
            connection.close()

class post_grabber:
    html_content = str
    return_list = []

    def __init__(self) -> None:
        self.media_prieview_patern = r'<div class="media-preview-content">.*?</div>'
        self.gallery_thumbnail_patern = r'<a class="may-blank gallery-item-thumbnail-link".*?href="(.*?)".*?>'
        self.url_find_pattern = r'<a[^>]*class="[^"]*title[^"]*may-blank[^"]*outbound[^"]*"[^>]*href="([^"]+)"[^>]*>'
        self.reddit_content_url_patern = r'https://i\.redd\.it/[^"]+'
        self.html_content = str
    
    def re_find(self, patern):
        return re.findall(patern, post_grabber.html_content, re.DOTALL)

    async def find_content(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            run = executor.map(post_grabber().re_find, [self.media_prieview_patern, self.url_find_pattern])
        return list(run)

    async def grabber(url: str, subreddit: str) -> list:
        connect = https()
        findID = re.findall(r'(?:https?:\/\/)?(?:www\.|old\.|i\.|new\.)?(?:reddit\.com|redd\.it)\/(?:r\/[^\s\/$.?#]+\/)?gallery\/',url)
        if findID != []:
            url = f"https://old.reddit.com/r/{subreddit}/comments/" + re.findall(r'(?:https?:\/\/)?(?:www\.|old\.|i\.|new\.)?(?:reddit\.com|redd\.it)\/(?:r\/[^\s\/$.?#]+\/comments\/|gallery\/)?([^\s\/$.?#]+)', url)[0]

        await connect.get(url=url.replace("www.reddit.com","old.reddit.com").replace("i.reddit.com","old.reddit.com").replace("new.reddit.com","old.reddit.com"))

        if connect.status == 404:
            return []

        if connect.headerConnection["location"] != None:
            connect.get(url=str(connect.headerConnection["location"]))

        if connect.text != None and connect.status == 200:
            post_grabber.html_content = connect.text
            content = await post_grabber().find_content()

            title = re.findall(r'<a\s+class="title[^"]*"\s+.*?>(.*?)<\/a>',connect.text)

            if content[1] != [] and re.findall(r'(?:https?:\/\/)?(?:www\.|old\.|i\.|new\.)?(?:reddit\.com|redd\.it)\/(?:r\/[^\s\/$.?#]+\/)?gallery\/',content[1][0]) == []:
                return [content[1], title[0]]

            if content[0] != []:
                for item in content[0]:
                    post_grabber.html_content = item
                    post_grabber.return_list.append(post_grabber().re_find(post_grabber().gallery_thumbnail_patern)[0].replace("amp;",""))
                return [post_grabber.return_list, title[0]]
            
            if content[1] != []:
                post_grabber.return_list.append(content[1][0])
            return [post_grabber.return_list, title[0]]
        return []

class subreddit_grabber:
    def __init__(self) -> None:
        pass

    async def grabber(url: str):
        connect = https()
        posts = []
        try:
            await connect.get(url=url.replace("www.reddit.com","old.reddit.com").replace("i.reddit.com","old.reddit.com").replace("new.reddit.com","old.reddit.com"))
        except TypeError:
            return

        if connect.status == 200:
            try:
                posts_tmp = re.findall(r'<a\s+[^>]*\bclass="[^"]*thumbnail[^"]*"\s+[^>]*\bhref="([^"]+)"[^>]*>',connect.text)
                posts_name_tmp = re.findall(r'<a class="title.*?>(.*?)</a>', connect.text)
                posts_url_tmp = re.findall(r'data-permalink="([^"]+)"', connect.text)

                for i,item in enumerate(posts_tmp):
                    if i > len(posts_tmp)-1:
                        break
                    if re.findall(r'(?:https?:\/\/)?(?:www\.|old\.|i\.|new\.)?(?:reddit\.com|redd\.it)\/(?:r\/[^\s\/$.?#]+\/comments\/)?(?:gallery\/)?([^\s\/$.?#]+)',item) != []:
                        posts.append((item, "https://old.reddit.com" + posts_url_tmp[i], posts_name_tmp[i]))
                
                return posts
            except IndexError:
                print("Post grabber error")
                return []