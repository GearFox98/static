# Static ⚡
### 1.0.1 - CLI and Media Support
> Implementing CLI arguments in static, now you can run static utility from the command line without modifying the script. There was added the folder 'media' for storing media files, such as pictures.
> - Script 'static.py' renamed to 'static' and added execution permissions. Now it is not mandatory to execute calling Python
> - Script 'main.py' renamed to 'static-init' and added execution permissions.
> - Setted a CLI argument in 'static-init' for copying the 'skel' dir into the path provided.
> - Added clean function to 'stutils.py' for removing dirs and folders at the same time.
> - Added media function to format the result in a variable included in a page file.
> - Added copy_data function to copy media files into 'dist' folder.
> - Added 'media' folder in the check function in 'static' script.

### 1.0.0 - Init
> Initiating the project:
> - Implemented directory structure and document fusion.
> - Defined 'routes.py' this stores variables with path of the structure and the site itself.
> - Defined 'stutils.py' for aid functions.
> - Defined 'static.py' for main functions, such as check directory structure and build the site.