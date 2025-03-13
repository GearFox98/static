# Static ⚡
### 1.0-4 - Development Server
> - Added a development server, it will be serving `dist` on _127.0.0.1:8001_ by default.
> It can be launched with the command `run` in the `static` utility. If there's nothing in `dist` the site will be generated.
> - Added a 404 - NotFound error page.
> - Added interactive console wile debugging/testing
> - Moved `stutils` file to `static_lib/stutils.py`

# Static ⚡
### 1.0-3 - Bootsrap offline
> Added a new parameter to get **Bootsrap** dist packages offline into `data` folder  
> It will replace the `link` line of Bootstrap in `html/header.html` file with the distribution acquired. Useful for offline development.

### 1.0-2 - Prettify
> Added a 'prettify' function in `stutils.py` script and called it on `static-init`.  
> Compile function on `static-init` now creates extra temporary files to prettify and removes them.
### 1.0-1 - CLI and Media Support
> Implementing CLI arguments in static, now you can run static utility from the command line without modifying the script. There was added the folder 'media' for storing media files, such as pictures.
> - Script 'static.py' renamed to 'static' and added execution permissions. Now it is not mandatory to execute calling Python
> - Script 'main.py' renamed to 'static-init' and added execution permissions.
> - Setted a CLI argument in 'static-init' for copying the 'skel' dir into the path provided.
> - Added clean function to 'stutils.py' for removing dirs and folders at the same time.
> - Added media function to format the result in a variable included in a page file.
> - Added copy_data function to copy media files into 'dist' folder.
> - Added 'media' folder in the check function in 'static' script.
> - Redesigned HTML templates

### 1.0-0 - Init
> Initiating the project:
> - Implemented directory structure and document fusion.
> - Defined 'routes.py' this stores variables with path of the structure and the site itself.
> - Defined 'stutils.py' for aid functions.
> - Defined 'static.py' for main functions, such as check directory structure and build the site.