#static-blog-generator

Yet another [static site generator](https://www.google.com/search?q=static+site+generator). 
I created it to power my own site, <http://rmgi.blog>. Later, I decided to release it to the public.

With this blog software, you can create blog entries, add tags to an entry or browse entries by tag, add comments to an entry,
 and search entries by keyword.

##Features
* Minimalistic design
* Just about 400 lines of code 
* Automatically generates sitemap and RSS feed
* Uses Markdown for post formatting
* Powered by Jinja2 template engine
* Code highlighting (requires [Pygments](http://pygments.org/))
* Comments hosted by [Widgetpack](https://widgetpack.com/)
* Client-side search powered by [fuse.js](https://fusejs.io/) 
* Social network share buttons
* Google Analytics integration (optional)

##Downsides
Though it is a fully functional software, it has it flaws.

* Every time you run the script, it rebuilds all the existing entries. 
In case you have hundreds of entries, the build process may be slow, or even run out of RAM and crash.
* Even if you haven't modified your drafts, the last modified date is changed every time the site is assembled. 
This also affects sitemap's "lastmod" attribute and may make search engines angry.
* Unused html files are not deleted, you have to do it by hand. This is done to prevent destructive behaviour.
* Though code is simple, it is not extendable.
* No automatic deployment/upload.
* No tests.

I hope to fix all of the above in the future.

##Usage
1. Clone or download the repository.
2. Install requirements `pip install -r requirements.txt`.
3. Run `python src/blog.py copysettings` or manually copy `src/settings.py.example` to `src/settings.py`.
4. Set `PUBLIC_DIR` and `DRAFTS_DIR` in the `src/settings.py`, although it should be good to go.
5. Run `python src/blog.py copystatic` or manually copy the contents of `staticfiles` folder
 to your `PUBLIC_DIR`.
6. Create some posts in `DRAFTS_DIR` folder.
7. Run `python blog.py build` to assemble the site.
8. Upload your `PUBLIC_DIR` folder to your server.

Every time your write a new post, repeat steps 6 to 8.

If you want to have code highlighting, install Pygments `pip install pygments`

##Credits
* HTML based on [HTML5 boilerplate](https://github.com/h5bp/html5-boilerplate) by H5BP
* Uses [window-centering script](http://www.xtf.dk/2011/08/center-new-popup-window-even-on.html) by xThomasFrost
* Uses [XML Sitemap Stylesheet](https://github.com/pedroborges/xml-sitemap-stylesheet) by pedroborg.es

If you think my code infringes your copyright, please contact me.

##License
Do whatever you want with the code, but it would be nice if you link back to this repo.