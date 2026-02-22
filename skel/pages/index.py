var = "Congrats, it works!"

def render(context):
    return f'''
    <div class="container py-5">
        <h1 class="m-0">{var}</h1>
        <div class="text-muted m-1">
            <p><strong>{context['AUTHOR']}</strong> welcomes you to Static⚡!</p>
            <p>Now it's time to build new stuff!</p>
            <p>Go change the code in pages. Keep it simple and stable!</p>
        </div>
        <div class="dgrid gap-2">
            <a class="btn btn-warning" href={context['DOC']} target="_blank" rel="noopener">Documentation</a>
            <a class="btn btn-secondary" href="about.html">About page</a>
        </div>
    </div>
    '''
