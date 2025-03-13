from static_lib.stutils import media

var = "It works!"

def get():
    return f'''
    <div class="container py-5">
        <h1>{var}</h1>
        <div class="text-muted">
            <p>Now it's time to build new stuff!</p>
            <p>Go change the code in pages. Keep it simple and stable!</p>
        </div>
        <div class="dgrid gap-2">
            <a class="btn btn-warning" href="https://gearfox98.github.com/static/wiki" target="_blank" rel="noopener">Documentation</a>
            <a class="btn btn-secondary" href="about.html">About page</a>
        </div>
    </div>
    '''
